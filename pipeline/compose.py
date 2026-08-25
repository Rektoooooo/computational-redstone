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


def direction(frm, to):
    """Compass name for a step from one (x, z) to an adjacent one."""
    dx, dz = to[0] - frm[0], to[1] - frm[1]
    if dx > 0:
        return "east"
    if dx < 0:
        return "west"
    return "south" if dz > 0 else "north"


def facing_from(prev, cur):
    """
    Which way a repeater at `cur` should face, having been reached from `prev`.

    A repeater's `facing` points at its INPUT, so it looks back the way the signal
    came. Getting this backwards points it into the wall and the line dies silently.
    """
    return direction(cur, prev)


def dust_shaped(prev, nxt, cur):
    """
    Dust carrying the connection shape this path implies.

    The game recomputes wire shape on placement anyway, but writing it correctly means
    the simulator sees the same wire the game will draw - so a prediction made here is
    a prediction about the real thing.
    """
    sides = {"north": "none", "south": "none", "east": "none", "west": "none"}
    for other in (prev, nxt):
        if other is not None:
            sides[direction(cur, other)] = "side"
    return BlockState("minecraft:redstone_wire", power="0", **sides)


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

    def tap_output(self, lamp_pos, facing, colour):
        """
        Replace an output lamp with a repeater reading the block that drove it.

        `facing` names the direction of the DRIVER, since a repeater's facing points at
        its input. The signal then leaves from the opposite side.

        A lamp needs no floor and a repeater does, so the swap has to bring a support
        block with it or the repeater pops off the moment the build is pasted.
        """
        self.put(lamp_pos, repeater(facing), "tap repeater", allow_replace=True)
        self.support(lamp_pos, colour)
        return lamp_pos

    def drive_input(self, lever_pos, facing, colour):
        """
        Replace an input lever with a repeater aimed at the block the lever fed.

        `facing` names where the incoming signal arrives from. These levers are WALL
        levers, hung off the side of a block, so like the lamp above they leave nothing
        underneath for the repeater to stand on.
        """
        self.put(lever_pos, repeater(facing), "drive repeater", allow_replace=True)
        self.support(lever_pos, colour)
        return lever_pos

    def support(self, pos, colour):
        """Put a floor under `pos` if there is not one already."""
        below = (pos[0], pos[1] - 1, pos[2])
        if below not in self.occupied:
            self.put(below, wool(colour), "support")

    # -- structural check -------------------------------------------------

    NEEDS_FLOOR = ("repeater", "comparator", "redstone_wire", "redstone_torch")

    def floating(self):
        """
        Everything that would fall or pop off the instant this is pasted.

        The simulator will not catch any of it. It models SIGNAL, not physics - a
        repeater hanging in mid-air solves perfectly and simply cannot exist. So a
        composed build has to be checked structurally as well as behaviourally, and
        this is that check.
        """
        out = []
        for x, y, z in sorted(self.occupied):
            bs = self.region[x, y, z]
            bid = bs.id.replace("minecraft:", "")
            needs = bid in self.NEEDS_FLOOR
            if bid == "lever" or "button" in bid:
                try:
                    needs = bs["face"] == "floor"      # wall and ceiling ones are fine
                except Exception:
                    needs = False
            if needs and (x, y - 1, z) not in self.occupied:
                out.append(((x, y, z), bid))
        return out

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

    # -- routing, the general case ----------------------------------------

    REDSTONE = ("redstone_wire", "repeater", "comparator", "redstone_torch",
                "redstone_wall_torch", "lever", "redstone_block")

    def keepout(self):
        """
        Cells a route must not enter, beyond the ones already filled.

        A dust line running alongside a machine's own wiring joins it, and the result
        is a build that looks right and computes nonsense. So every cell touching a
        redstone component is reserved - one block of clearance in every direction,
        including up and down, since dust reaches diagonally between levels too.
        """
        out = set()
        for x, y, z in list(self.occupied):
            bid = self.region[x, y, z].id.replace("minecraft:", "")
            if bid not in self.REDSTONE:
                continue
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        out.add((x + dx, y + dy, z + dz))
        return out

    def route_plane(self, y, start, goal, blocked):
        """
        Shortest path from `start` to `goal` across one horizontal plane.

        Breadth-first over (x, z) at fixed y. Each bit gets its own plane, which is what
        keeps this two-dimensional: the bits sit 2 apart in y and a support block over a
        live wire does not leak, so the lines cannot reach each other.

        Returns the cells from just after `start` up to and INCLUDING `goal`, or None if
        boxed in - which is a real answer and better than routing through something.
        """
        from collections import deque
        sx, sz = start
        gx, gz = goal
        seen = {(sx, sz): None}
        q = deque([(sx, sz)])
        while q:
            cur = q.popleft()
            if cur == (gx, gz):
                path = []
                while cur is not None:
                    path.append(cur)
                    cur = seen[cur]
                return list(reversed(path))[1:]
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nxt = (cur[0] + dx, cur[1] + dz)
                if nxt in seen:
                    continue
                if not (0 <= nxt[0] < self.region.width and 0 <= nxt[1] < self.region.length):
                    continue
                cell = (nxt[0], y, nxt[1])
                if nxt != (gx, gz) and cell in blocked:
                    continue
                # a sign can be routed through - it is a label, not circuitry - but
                # anything else in the way is a wall
                if nxt != (gx, gz) and cell in self.occupied and not self.is_decoration(cell):
                    continue
                seen[nxt] = cur
                q.append(nxt)
        return None

    def lay_route(self, path, y, colour, max_run=14, enter_from=None, exit_to=None):
        """
        Lay dust along `path`, with its floor, and a repeater before the signal dies.

        Dust loses one per block and starts at 15, so a run longer than 15 arrives as
        nothing. A repeater restores it - but only ever on a STRAIGHT stretch: put one
        on a corner and it faces the wrong way and silently breaks the line.

        `enter_from` and `exit_to` are the things at each END of the route - normally
        the tap and drive repeaters. They matter because a wire's stored shape has to
        mention them: give the first cell only its forward neighbour and it has a
        single connection, which draws as a straight line THROUGH rather than a turn
        into the repeater beside it. The game recomputes shape on update and recovers,
        but the pasted file looks wrong before anything nudges it, and the shape also
        decides which blocks the wire powers - so it should be right on disk.
        """
        placed, since_repeater = [], 0
        for i, (x, z) in enumerate(path):
            if self.is_decoration((x, y, z)):
                self.clear((x, y, z), "route passes through a sign")
            prev = path[i - 1] if i > 0 else enter_from
            nxt = path[i + 1] if i + 1 < len(path) else exit_to
            straight = (prev and nxt and
                        (prev[0] == x == nxt[0] or prev[1] == z == nxt[1]))
            since_repeater += 1

            if since_repeater >= max_run and straight:
                self.put((x, y, z), repeater(facing_from(prev, (x, z))), "route repeater")
                since_repeater = 0
            else:
                self.put((x, y, z), dust_shaped(prev, nxt, (x, z)), "route dust")
            self.support((x, y, z), colour)
            placed.append((x, y, z))
        return placed

    # -- output -----------------------------------------------------------

    def save(self, path, name, description):
        from litemapy.schematic import TileEntity
        from nbtlib.tag import Compound
        for d in self.tile_entities:
            self.region.tile_entities.append(TileEntity(Compound(d)))
        self.region.as_schematic(name=name, author="computational-redstone",
                                 description=description).save(path)
        return path


def next_version(base):
    """
    The next unused `base-vN.litematic`.

    Every run writes a NEW file rather than replacing the last one. Overwriting loses
    the thing you most want when a build misbehaves in game: the previous version, to
    compare against and to fall back to. It cost us v1 of this build, which was pasted,
    broke, and then vanished under its own fix.
    """
    import glob
    import re
    existing = glob.glob(f"{base}-v*.litematic")
    versions = [int(m.group(1)) for f in existing
                if (m := re.search(r"-v(\d+)\.litematic$", f))]
    return f"{base}-v{max(versions, default=0) + 1}.litematic"


def compose_m1(out=None):
    """
    Two 8-bit adders chained: (A + B) + C.

    Adder #2 is offset so that bit i of its A input lands at the same y and z as bit i
    of adder #1's sum. That is what makes every bus line straight, and it is the whole
    reason this is M1 rather than M2.
    """
    out = out or next_version("pipeline/m1-two-adders")
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
        c.tap_output(src, "west", BUS_COLOURS[i])    # driver block lies to the west
        c.drive_input(dst, "west", BUS_COLOURS[i])   # bus arrives from the west
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

    # Structural check. The simulator cannot do this for us - it models signal, not
    # physics, so anything unsupported solves perfectly and then falls apart on paste.
    loose = c.floating()
    if loose:
        print(f"\n  {len(loose)} BLOCKS WITH NO FLOOR - these break the moment it is pasted:")
        for pos, bid in loose[:12]:
            print(f"     {pos}  {bid}")
    else:
        print("  nothing unsupported")

    c.save(out, "m1-two-adders", "(A+B)+C - two 8-bit CCA adders chained")
    print(f"\n  wrote {out}")
    return out, a1, a2


def compose_m2(out=None):
    """
    One adder with its output brought round to the FRONT.

    As extracted, the machine is inside-out for whoever is using it: inputs on the west
    face, sum lamps on the east, so you set the numbers and then walk around 517 blocks
    to read the answer. This routes all eight bits round to the front, giving

        (Input A, z=4)   (Input B, z=7)   (Output, z=10)

    Unlike M1 there is no freedom to line the ports up by choosing an offset - the
    adder sits where it sits and the wire has to get past it. Each bit is routed inside
    its own horizontal plane, which is what keeps this a two-dimensional search: the
    bits are 2 apart in y and a support block over a live wire does not leak, so the
    eight lines cannot reach one another.
    """
    out = out or next_version("pipeline/m2-front-output")
    c = Composition(13, 22, 11)          # one deeper than the adder, for the front row
    print("routing the adder's output round to the front")
    c.place(ADDER, (0, 0, 0), "adder")

    # Work out the no-go zone BEFORE adding anything of our own, so the margin is drawn
    # around the machine's wiring rather than around our own wire as it grows.
    blocked = c.keepout()
    print(f"  {len(blocked)} cells reserved as clearance around the adder's wiring\n")

    print("  bit   y  route                                  cells")
    routed = []
    for i in range(8):
        y = 2 + 2 * i
        colour = BUS_COLOURS[i]
        tap = (10, y, 3)                 # the sum lamp becomes the tap
        drive = (3, y, 10)               # repeater that lights the new front lamp
        lamp = (2, y, 10)
        # Route to the cell EAST of the drive repeater rather than to the repeater
        # itself. A repeater takes its input from one specific side, so the direction
        # the wire arrives from is not a detail the router may choose freely - the
        # first attempt hardcoded "east", the router approached from the north, and
        # the signal reached the last cell and stopped dead there.
        arrival = (drive[0] + 1, drive[2])

        c.tap_output(tap, "west", colour)
        path = c.route_plane(y, (tap[0], tap[2]), arrival, blocked)
        if path is None:
            print(f"  {i:3} {y:3}  NO ROUTE FOUND")
            c.collisions.append((tap, "no route to the front"))
            continue
        cells = c.lay_route(path, y, colour,
                            enter_from=(tap[0], tap[2]), exit_to=(drive[0], drive[2]))
        routed += cells
        c.drive_input(drive, "east", colour)
        c.put(lamp, BlockState("minecraft:redstone_lamp", lit="false"), "front lamp",
              allow_replace=True)
        c.support(lamp, colour)
        print(f"  {i:3} {y:3}  {str(path[0])} -> {str(path[-1]):9} "
              f"{colour:11} {len(cells):3}")

    if c.removed:
        print(f"\n  removed {len(c.removed)} decorative blocks the routes pass through")
    print(f"  {len(c.collisions)} collisions" if c.collisions else "  no collisions")

    loose = c.floating()
    if loose:
        print(f"  {len(loose)} BLOCKS WITH NO FLOOR - would break on paste:")
        for pos, bid in loose[:8]:
            print(f"     {pos}  {bid}")
    else:
        print("  nothing unsupported")

    # Cross-talk is the failure this whole design is arranged to avoid, so assert it
    # rather than hope. A routed cell touching the machine's wiring joins it.
    touching = [p for p in routed if p in blocked]
    print(f"  {len(touching)} routed cells touching the adder's wiring"
          if touching else "  no routed cell touches the adder's wiring")

    c.save(out, "m2-front-output", "8-bit adder with its output routed to the front")
    print(f"\n  wrote {out}")
    return out


def compose_m3(stagger=3, out=None):
    """
    The front-output adder again, but with the readout fanned out diagonally.

    M2's eight routes were all the same shape, so their delays matched for free. Here
    bit `i`'s lamp sits `stagger` blocks further along than bit `i-1`, so the routes are
    genuinely different lengths - and once a route passes 14 cells it needs another
    repeater, which is 2 more game ticks. That is STRUCTURAL skew: fixed by the wiring,
    the same for every input, and therefore paddable.

    Note that length alone does nothing. Dust carries within the tick, so a longer route
    is not a slower one - only the repeaters it forces are.
    """
    out = out or next_version("pipeline/m3-staggered")
    depth = 11 + stagger * 7
    c = Composition(13, 22, depth)
    print(f"front-output adder, readout staggered {stagger} blocks per bit")
    c.place(ADDER, (0, 0, 0), "adder")
    blocked = c.keepout()

    print("\n  bit   y   lamp z   route cells  repeaters on route")
    for i in range(8):
        y = 2 + 2 * i
        colour = BUS_COLOURS[i]
        z = 10 + stagger * i
        tap = (10, y, 3)
        drive = (3, y, z)
        arrival = (drive[0] + 1, drive[2])

        c.tap_output(tap, "west", colour)
        path = c.route_plane(y, (tap[0], tap[2]), arrival, blocked)
        if path is None:
            print(f"  {i:3} {y:3}   NO ROUTE")
            c.collisions.append((tap, "no route"))
            continue
        cells = c.lay_route(path, y, colour,
                            enter_from=(tap[0], tap[2]), exit_to=(drive[0], drive[2]))
        c.drive_input(drive, "east", colour)
        c.put((2, y, z), BlockState("minecraft:redstone_lamp", lit="false"),
              "front lamp", allow_replace=True)
        c.support((2, y, z), colour)
        reps = sum(1 for p in cells
                   if c.region[p[0], p[1], p[2]].id.endswith("repeater"))
        print(f"  {i:3} {y:3} {z:6} {len(cells):11} {reps:16}")

    print(f"\n  {len(c.collisions)} collisions" if c.collisions else "  no collisions")
    loose = c.floating()
    print(f"  {len(loose)} unsupported" if loose else "  nothing unsupported")
    c.save(out, "m3-staggered", "adder with a diagonal readout - structural skew")
    print(f"  wrote {out}")
    return out


def align(path, ports, outputs, out=None, probe=(255, 0)):
    """
    Pad the fast lines until every bit arrives on the same tick.

    Only STRUCTURAL skew can be treated this way - the fixed kind, caused by one route
    carrying more repeaters than another. Data-dependent skew from a carry chain varies
    with the input and no fixed padding can flatten it; `settle_profile` is the tool for
    that, and the answer there is to wait for the worst case.

    Padding costs no blocks. A repeater's delay setting runs 1 to 4, which is 2 to 8
    game ticks, so turning up repeaters that are already on the line buys up to 6 ticks
    each. Only a skew bigger than the line can absorb would need new hardware.

    Each bit lives in its own y-plane, so "the repeaters belonging to bit i" is simply
    every repeater at that height - no bookkeeping needed.
    """
    from litemapy import Schematic

    out = out or next_version("pipeline/m3-aligned")
    arrivals = arrival_ticks(path, ports, (0, 0), probe, outputs)
    if len(arrivals) < len(outputs):
        print("  not every bit moved on the probe input - cannot measure them all")
        return None
    target = max(arrivals.values())

    schem = Schematic.load(path)
    region = list(schem.regions.values())[0]
    print(f"\n  aligning to the slowest line, {target} game ticks\n")
    print(f"  {'bit':>3} {'was':>4} {'needs':>6}  repeaters raised")

    for i, p in enumerate(outputs):
        need = target - arrivals[p]
        y = p[1]
        raised = []
        if need:
            for x in range(region.width):
                for z in range(region.length):
                    if need <= 0:
                        break
                    bs = region[x, y, z]
                    if not bs.id.endswith("repeater"):
                        continue
                    delay = int(bs["delay"])
                    room = (4 - delay) * 2          # each step up is 2 game ticks
                    if room <= 0:
                        continue
                    add = min(need, room)
                    region[x, y, z] = BlockState(
                        "minecraft:repeater", facing=bs["facing"],
                        delay=str(delay + add // 2), locked=bs["locked"],
                        powered=bs["powered"])
                    raised.append(f"({x},{z}) {delay}->{delay + add // 2}")
                    need -= add
        note = ", ".join(raised) if raised else ("-" if not need else "COULD NOT PAD")
        print(f"  {i:3} {arrivals[p]:4} {target - arrivals[p]:6}  {note}")

    schem.save(out)
    print(f"\n  wrote {out}")
    return out


def settle_profile(path, ports, outputs, values, max_ticks=200):
    """
    How long this build takes to settle, across many inputs.

    There are two different things called "skew" and they need different answers:

      STRUCTURAL   fixed, caused by the wiring - one route carrying more repeaters
                   than another. Constant across inputs, so it can be PADDED flat.
      DATA-DEPENDENT  varies with the input, caused by carry chains. A ripple-carry
                   adder settles in 8 ticks for most inputs and 22 when the carry has
                   to climb every stage. No fixed padding fixes that; the only correct
                   answer is to WAIT for the worst case before sampling.

    Returns (worst, histogram). The worst case is the number that matters - it is what
    a downstream register's clock period has to clear.
    """
    hist = {}
    worst, worst_at = 0, None
    for a, b in values:
        arr = arrival_ticks(path, ports, (0, 0), (a, b), outputs, max_ticks=max_ticks)
        t = max(arr.values()) if arr else 0
        hist[t] = hist.get(t, 0) + 1
        if t > worst:
            worst, worst_at = t, (a, b)
    return worst, worst_at, hist


def arrival_ticks(path, ports, before, after, outputs, max_ticks=400):
    """
    How many game ticks after an input change each output settles.

    Records the **last** change, not the first. A bit can flicker on its way to an
    answer - a carry arriving late can flip it back - and the first change would report
    a bit as arrived while it is still moving. Skew computed from that would be wrong
    in the one case it matters most.

    `before` and `after` are (A, B) pairs: settle on the first, switch to the second,
    then count. Outputs that never change simply do not appear, which is correct - a bit
    that stays put has no arrival time.
    """
    from sim.engine import Sim

    grid = Grid.from_file(path)
    sim = Sim(grid)
    for port, value in zip(ports, before):
        sim.set_port(port, value)
    sim.prime()
    sim.run_until_stable(max_ticks=max_ticks)

    base = sim.time
    for port, value in zip(ports, after):
        sim.set_port(port, value)

    last, prev = {}, sim.lamp_states()
    for _ in range(max_ticks):
        sim.tick()
        cur = sim.lamp_states()
        for p in outputs:
            if cur.get(p) != prev.get(p):
                last[p] = sim.time - base
        prev = cur
        if not len(sim.queue):
            break
    return last


def report_skew(label, arrivals, outputs):
    """Print per-bit arrival and the spread between fastest and slowest."""
    ticks = [arrivals.get(p) for p in outputs]
    known = [t for t in ticks if t is not None]
    spread = (max(known) - min(known)) if known else 0
    print(f"\n  {label}")
    print("     bit   " + "  ".join(f"{i:>3}" for i in range(len(outputs))))
    print("     tick  " + "  ".join(f"{t if t is not None else '-':>3}" for t in ticks))
    print(f"     skew: {spread} game ticks"
          f"{'  (aligned)' if spread == 0 else '  <-- bits do not arrive together'}")
    return spread


def verify_m2(path):
    """
    Sweep the front-output adder.

    The back lamps are gone - that was the point - so arithmetic is the reference: the
    front lamps must read (A + B) & 0xFF. A mis-routed line shows up as a bit that is
    always wrong; cross-talk shows up as bits that are wrong together.
    """
    from sim.engine import Sim

    grid = Grid.from_file(path)
    A = [(2, 3 + 2 * i, 4) for i in range(8)]
    B = [(2, 3 + 2 * i, 7) for i in range(8)]
    OUT = [(2, 2 + 2 * i, 10) for i in range(8)]

    def run(a, b):
        sim = Sim(grid)
        sim.set_port(A, a)
        sim.set_port(B, b)
        sim.prime()
        settled = sim.run_until_stable(max_ticks=600)
        lamps = sim.lamp_states()
        return sum(1 << i for i, p in enumerate(OUT) if lamps.get(p)), settled, sim.time

    cases = ([(v, 0) for v in range(256)]
             + [(a, b) for a in range(16) for b in range(16)]
             + [(255, 1), (128, 128), (37, 91), (255, 255), (170, 85)])
    bad, slowest, wrong_bits = [], 0, [0] * 8
    for a, b in cases:
        got, settled, t = run(a, b)
        slowest = max(slowest, t)
        want = (a + b) & 0xFF
        if got != want or not settled:
            bad.append((a, b, got, want))
            for i in range(8):
                if ((got >> i) & 1) != ((want >> i) & 1):
                    wrong_bits[i] += 1

    print(f"\n  front lamps vs (A + B): {len(cases)} cases, {len(bad)} wrong"
          f"   (slowest settle: {slowest} game ticks)")
    if bad:
        print(f"  wrong-bit counts by position (LSB first): {wrong_bits}")
        for a, b, got, want in bad[:6]:
            print(f"     {a}+{b}: got {got:08b} want {want:08b}")
    print(f"\n   {'PASS - safe to paste' if not bad else 'FAIL - do not paste'}\n")
    return not bad


def verify_m1(path):
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
    if "--m1" in sys.argv:
        written, _, _ = compose_m1()
        if "--verify" in sys.argv:
            verify_m1(written)
    else:
        written = compose_m2()
        if "--verify" in sys.argv:
            verify_m2(written)
