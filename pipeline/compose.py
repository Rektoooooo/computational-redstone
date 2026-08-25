#!/usr/bin/env python3
"""
Join two extracted components into one working build.

    python3 pipeline/compose.py            # build it
    python3 pipeline/compose.py --verify   # build it and sweep it in the simulator

M1 of `docs/roadmap.md`. Chains two 8-bit adders into a device computing `(A + B) + C`.
Both halves are already confirmed working in game on their own, so anything that goes
wrong here is the wiring - which is the point.

## Why a join needs more than a wire

Extracted ports are HUMAN interfaces. Every build takes input from levers and reports
output on lamps, and neither can be wired to anything: a lever is hand-operated and a
lamp is a dead end. Both ends need converting, and the conversions are not symmetric.

**Source.** The block driving each sum lamp does track its bit, but only ever WEAKLY,
at levels as low as 1. Dust cannot pick that up - a weakly powered block will not start
a new dust run - so the tap has to be a repeater, which reads block power regardless of
strength and re-emits a clean 15. That also normalises the ragged 1-to-4 levels the
adder happens to leave there.

**Sink.** Each input lever is a wall lever mounted on its own indicator lamp; throwing
it strongly powers that lamp, which feeds interior dust at 15. A repeater aimed into the
same lamp reproduces exactly that.

## Colour

Structural blocks are wool, never stone, and each bus line gets its own colour, ordered
LSB to MSB as a spectrum. That is how a wire is traced in a build with eight parallel
lines: a mis-routed bit is visible at a glance instead of needing to be counted out in
F3. The source builds follow the same convention.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "worlds"))

from litemapy import Region, BlockState, Schematic
from sim.grid import Grid

ADDER = "worlds/primitives/addition/3-ticks-8-bit-cca-by-don.litematic"

# One colour per bus line, LSB -> MSB, running as a spectrum so the bit order can be
# read off the build itself.
BUS_COLOURS = ["white", "light_blue", "cyan", "lime",
               "yellow", "orange", "red", "magenta"]

AIR = BlockState("minecraft:air")
DUST = BlockState("minecraft:redstone_wire", power="0",
                  east="side", west="side", north="none", south="none")


def wool(colour):
    return BlockState(f"minecraft:{colour}_wool")


def repeater(facing, delay=1):
    """`facing` points at the INPUT; output leaves the opposite side."""
    return BlockState("minecraft:repeater", facing=facing, delay=str(delay),
                      locked="false", powered="false")


class Composition:
    """A region under construction, plus a record of anything that went wrong."""

    def __init__(self, w, h, l):
        self.region = Region(0, 0, 0, w, h, l)
        self.tile_entities = []
        self.collisions = []
        self.removed = []
        self.occupied = set()

    # -- placement --------------------------------------------------------

    def place(self, path, offset, label):
        """Copy a build's blocks into the region at `offset`, block entities and all."""
        ox, oy, oz = offset
        schem = Schematic.load(path)
        src = list(schem.regions.values())[0]
        n = 0
        for x in range(src.width):
            for y in range(src.height):
                for z in range(src.length):
                    bs = src[x, y, z]
                    if bs.id.replace("minecraft:", "") == "air":
                        continue
                    p = (x + ox, y + oy, z + oz)
                    if p in self.occupied:
                        self.collisions.append((p, f"{label} overlaps an earlier build"))
                        continue
                    self.region[p[0], p[1], p[2]] = bs
                    self.occupied.add(p)
                    n += 1
        # Shifted coordinates have to go back as NBT Int tags, not bare Python ints -
        # nbtlib writes by tag type and a plain int has none, so saving dies far from
        # here with an unhelpful AttributeError.
        from nbtlib.tag import Int
        for te in src.tile_entities:
            d = dict(te.to_nbt())
            d["x"] = Int(int(d["x"]) + ox)
            d["y"] = Int(int(d["y"]) + oy)
            d["z"] = Int(int(d["z"]) + oz)
            self.tile_entities.append(d)
        print(f"  placed {label:10} at {offset}  {n} blocks")
        return offset

    def put(self, pos, state, why, allow_replace=False):
        """Set one block, recording rather than hiding a clash."""
        x, y, z = pos
        if pos in self.occupied and not allow_replace:
            self.collisions.append((pos, why))
            return False
        self.region[x, y, z] = state
        self.occupied.add(pos)
        return True

    def clear(self, pos, why):
        """
        Remove a block, and the block entity that went with it.

        Dropping the block but keeping its entity would leave an orphan - a sign's text
        with no sign - which round-trips into the file and confuses anything reading it
        later. They have to go together.
        """
        x, y, z = pos
        self.region[x, y, z] = AIR
        self.occupied.discard(pos)
        before = len(self.tile_entities)
        self.tile_entities = [d for d in self.tile_entities
                              if (int(d["x"]), int(d["y"]), int(d["z"])) != pos]
        self.removed.append((pos, why, before != len(self.tile_entities)))

    def is_decoration(self, pos):
        """
        True if whatever is here can be removed without changing behaviour.

        Only signs qualify. They are labels, and a bus has to be allowed to pass through
        one - but it must NEVER be allowed to quietly delete circuitry, so everything
        else stays a collision.
        """
        try:
            bid = self.region[pos[0], pos[1], pos[2]].id.replace("minecraft:", "")
        except Exception:
            return False
        return "sign" in bid

    # -- port conversion --------------------------------------------------

    def tap_output(self, lamp_pos, facing):
        """
        Replace an output lamp with a repeater reading the block that drove it.

        `facing` names the direction of the DRIVER, since a repeater's facing points at
        its input. The signal then leaves from the opposite side.
        """
        self.put(lamp_pos, repeater(facing), "tap repeater", allow_replace=True)
        return lamp_pos

    def drive_input(self, lever_pos, facing):
        """
        Replace an input lever with a repeater aimed at the block the lever fed.

        `facing` names where the incoming signal arrives from.
        """
        self.put(lever_pos, repeater(facing), "drive repeater", allow_replace=True)
        return lever_pos

    # -- routing ----------------------------------------------------------

    def bus(self, x_from, x_to, y, z, colour):
        """
        A straight dust run east along x, on its own coloured wool.

        Straight lines only - M2 generalises this. Dust loses one per block, so a run
        longer than 15 needs a repeater; that is asserted rather than assumed.
        """
        length = x_to - x_from + 1
        if length > 15:
            self.collisions.append(((x_from, y, z), f"bus of {length} exceeds dust range"))
        for x in range(x_from, x_to + 1):
            if self.is_decoration((x, y, z)):
                self.clear((x, y, z), "bus passes through a sign")
            self.put((x, y - 1, z), wool(colour), "bus support")
            self.put((x, y, z), DUST, "bus dust")
        return length

    # -- output -----------------------------------------------------------

    def save(self, path, name, description):
        from litemapy.schematic import TileEntity
        from nbtlib.tag import Compound
        for d in self.tile_entities:
            self.region.tile_entities.append(TileEntity(Compound(d)))
        self.region.as_schematic(name=name, author="computational-redstone",
                                 description=description).save(path)
        return path


def compose_m1(out="pipeline/m1-two-adders.litematic"):
    """
    Two 8-bit adders chained: (A + B) + C.

    Adder #2 is offset so that bit i of its A input lands at the same y and z as bit i
    of adder #1's sum. That is what makes every bus line straight, and it is the whole
    reason this is M1 rather than M2.
    """
    a1 = (0, 1, 1)          # lifted so adder #2 can sit one lower without going negative
    a2 = (20, 0, 0)
    c = Composition(33, 23, 11)
    print("composing (A + B) + C")
    c.place(ADDER, a1, "adder #1")
    c.place(ADDER, a2, "adder #2")

    print("\n  bit  source tap        bus            sink drive")
    for i in range(8):
        y = 3 + 2 * i                     # same height at both ends, by construction
        z = 4
        src = (a1[0] + 10, y, z)          # adder #1 sum lamp for this bit
        dst = (a2[0] + 2, y, z)           # adder #2 A lever for this bit
        c.tap_output(src, "west")         # driver block lies to the west
        c.drive_input(dst, "west")        # bus arrives from the west
        n = c.bus(src[0] + 1, dst[0] - 1, y, z, BUS_COLOURS[i])
        print(f"  {i:3}  {str(src):16}  {n:2} × {BUS_COLOURS[i]:11}  {dst}")

    if c.removed:
        signs = sum(1 for _, _, had_entity in c.removed if had_entity)
        print(f"\n  removed {len(c.removed)} decorative blocks to make room "
              f"({signs} carried sign text - the bit labels the bus exits through)")
    if c.collisions:
        print(f"\n  {len(c.collisions)} COLLISIONS - the layout is wrong, not just untidy:")
        for pos, why in c.collisions[:12]:
            print(f"     {pos}  {why}")
    else:
        print("  no collisions")

    c.save(out, "m1-two-adders", "(A+B)+C - two 8-bit CCA adders chained")
    print(f"\n  wrote {out}")
    return out, a1, a2


def verify_m1(path="pipeline/m1-two-adders.litematic"):
    """
    Sweep the composed build in the simulator.

    The full cross product is 256^3, which is not runnable - but it is also not the
    right test. Correctness decomposes, and each part sweeps exhaustively:

    1. THE BUS, ALONE. Adder #2's A-input indicator lamps show what actually arrived.
       Comparing them bit-for-bit against the value adder #1 produced isolates the
       wiring from the arithmetic. A dropped, transposed or mistimed bit shows up here
       and nowhere else - and a transposition in particular would still give
       plausible-looking sums downstream, so checking values alone would miss it.
    2. END TO END. That the whole thing computes (A + B) + C.
    """
    from sim.engine import Sim

    grid = Grid.from_file(path)
    A = [(2, 4 + 2 * i, 5) for i in range(8)]       # adder #1, operand A
    B = [(2, 4 + 2 * i, 8) for i in range(8)]       # adder #1, operand B
    C = [(22, 3 + 2 * i, 7) for i in range(8)]      # adder #2, operand C
    ARRIVED = [(23, 3 + 2 * i, 4) for i in range(8)]   # what the bus delivered
    OUT = [(30, 2 + 2 * i, 3) for i in range(8)]       # final sum

    def run(a, b, c):
        sim = Sim(grid)
        sim.set_port(A, a)
        sim.set_port(B, b)
        sim.set_port(C, c)
        sim.prime()
        settled = sim.run_until_stable(max_ticks=600)
        lamps = sim.lamp_states()
        got = lambda ps: sum(1 << i for i, p in enumerate(ps) if lamps.get(p))
        return got(ARRIVED), got(OUT), settled, sim.time

    print("\n1. BUS FIDELITY - does adder #2 receive exactly what adder #1 sent?")
    bad = []
    for v in range(256):                                  # every possible sum value
        arrived, _, _, _ = run(v, 0, 0)
        if arrived != v:
            bad.append((v, 0, arrived))
    for a in range(16):                                   # and with real carry activity
        for b in range(16):
            arrived, _, _, _ = run(a, b, 0)
            if arrived != ((a + b) & 0xFF):
                bad.append((a, b, arrived))
    print(f"   512 cases, {len(bad)} wrong")
    for a, b, arrived in bad[:6]:
        print(f"     A={a} B={b}: expected {(a+b)&0xFF:08b} arrived {arrived:08b}")

    print("\n2. END TO END - (A + B) + C")
    bad2, slowest = [], 0
    cases = ([(a, b, 0) for a in range(16) for b in range(16)]
             + [(37, 91, c) for c in range(256)]
             + [(255, 1, 1), (128, 128, 0), (0, 0, 0), (255, 255, 255), (200, 100, 55)])
    for a, b, c in cases:
        _, out, settled, t = run(a, b, c)
        slowest = max(slowest, t)
        if out != ((a + b + c) & 0xFF) or not settled:
            bad2.append((a, b, c, out, (a + b + c) & 0xFF, settled))
    print(f"   {len(cases)} cases, {len(bad2)} wrong   (slowest settle: {slowest} game ticks)")
    for a, b, c, got, want, settled in bad2[:6]:
        print(f"     ({a}+{b})+{c}: got {got} want {want} settled={settled}")

    ok = not bad and not bad2
    print(f"\n   {'PASS - safe to paste' if ok else 'FAIL - do not paste'}\n")
    return ok


if __name__ == "__main__":
    compose_m1()
    if "--verify" in sys.argv:
        verify_m1()
