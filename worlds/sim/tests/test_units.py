"""
Micro-circuits with known answers.

These are built by hand rather than extracted, so the expected result comes from the
documented rules and not from a saved world. If one of these fails, the model is wrong
in a way that would be very hard to find inside a 300-component build.

Run:  python -m sim.tests.test_units
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sim.grid import Grid, Cell
from sim.engine import Sim
from sim.power import solve
from sim import components as C

PASS, FAIL = [], []


def check(name, got, want):
    if got == want:
        PASS.append(name)
        print(f"  PASS  {name}")
    else:
        FAIL.append(name)
        print(f"  FAIL  {name}\n          got  {got}\n          want {want}")


def build(cells):
    g = Grid()
    for pos, (bid, props) in cells.items():
        g.cells[pos] = Cell(bid, props)
    xs = [p[0] for p in cells] or [0]
    ys = [p[1] for p in cells] or [0]
    zs = [p[2] for p in cells] or [0]
    g.w, g.h, g.l = max(xs) + 1, max(ys) + 1, max(zs) + 1
    return g


def dust_line(x0, x1, y=1, z=0):
    """A straight east-west dust run on the given row."""
    out = {}
    for x in range(x0, x1 + 1):
        out[(x, y, z)] = ("redstone_wire",
                          {"east": "side", "west": "side",
                           "north": "none", "south": "none", "power": "0"})
        out[(x, y - 1, z)] = ("purple_wool", {})
    return out


# 1. dust decays exactly 1 per block, dying after 15
cells = dust_line(1, 16)
cells[(0, 1, 0)] = ("lever", {"powered": "true", "face": "floor"})
cells[(0, 0, 0)] = ("purple_wool", {})
f = solve(build(cells), {})
check("dust decays 15 -> 0 over 15 blocks",
      [f.dust.get((x, 1, 0), 0) for x in (1, 2, 8, 15, 16)],
      [15, 14, 8, 1, 0])

# 2. a lit torch inverts: unpowered support -> lit
cells = {(0, 0, 0): ("purple_wool", {}),
         (0, 1, 0): ("redstone_torch", {"lit": "true"})}
g = build(cells)
f = solve(g, {})
check("torch on unpowered block stays lit",
      C.eval_torch(g, f, {}, (0, 1, 0), g.get((0, 1, 0))), True)

# 3. JAVA rule: a WEAKLY powered block still turns a torch off.
#    (Bedrock is the edition where weak power is ignored here.)
cells = {(0, 0, 0): ("purple_wool", {}),
         (0, 1, 0): ("redstone_torch", {"lit": "true"}),
         (1, 0, 0): ("redstone_wire", {"west": "side", "east": "side",
                                       "north": "none", "south": "none"}),
         (1, -1, 0): ("purple_wool", {}),
         (2, 0, 0): ("lever", {"powered": "true"}),
         (2, -1, 0): ("purple_wool", {})}
g = build(cells)
f = solve(g, {})
check("weak power (dust into block) turns torch OFF - Java rule",
      C.eval_torch(g, f, {}, (0, 1, 0), g.get((0, 1, 0))), False)

# 4. but a weakly powered block cannot power NEW dust
cells = {(5, 0, 0): ("purple_wool", {}),
         (4, 0, 0): ("redstone_wire", {"east": "side", "west": "side",
                                       "north": "none", "south": "none"}),
         (4, -1, 0): ("purple_wool", {}),
         (3, 0, 0): ("lever", {"powered": "true"}),
         (3, -1, 0): ("purple_wool", {}),
         (6, 0, 0): ("redstone_wire", {"east": "side", "west": "side",
                                       "north": "none", "south": "none"}),
         (6, -1, 0): ("purple_wool", {})}
f = solve(build(cells), {})
check("weakly powered block does NOT re-power dust on the far side",
      f.dust.get((6, 0, 0), 0), 0)

# 5. comparator arithmetic, both modes
def comparator(mode, rear, side):
    """
    rear/side injected directly, isolating the arithmetic from wiring.

    NOTE `facing` points at the INPUT for diodes, so a comparator facing north takes
    its REAR input from the north. These fixtures originally assumed facing was the
    output direction - the same mistake the solver had - so they agreed with the bug.
    """
    pos = (0, 1, 0)
    cells = {pos: ("comparator", {"facing": "north", "mode": mode, "powered": "false"}),
             (0, 0, 0): ("purple_wool", {})}
    g = build(cells)
    f = solve(g, {})
    # inject levels directly - isolates the arithmetic from wiring concerns
    orig = C.input_from
    def fake(grid, field, states, p, direction, sides_only=False):
        return {"north": rear, "west": side, "east": 0}.get(direction, 0)
    C.input_from = fake
    try:
        return C.eval_comparator(g, f, {}, pos, g.get(pos))
    finally:
        C.input_from = orig

check("comparator subtract 8 - 3 = 5", comparator("subtract", 8, 3), 5)
check("comparator subtract 3 - 8 floors at 0", comparator("subtract", 3, 8), 0)
check("comparator compare passes rear when side lower", comparator("compare", 8, 3), 8)
check("comparator compare passes when side EQUAL to rear", comparator("compare", 8, 8), 8)
check("comparator compare blocks when side higher", comparator("compare", 3, 8), 0)

# 6. repeater locking - only a diode into the side can do it
def locked_by(block_id):
    pos = (1, 1, 0)
    cells = {pos: ("repeater", {"facing": "north", "delay": "1",
                                "powered": "false", "locked": "false"}),
             (1, 0, 0): ("purple_wool", {})}
    if block_id == "repeater":
        # output leaves the side opposite `facing`, so facing=west outputs east
        cells[(0, 1, 0)] = ("repeater", {"facing": "west", "delay": "1",
                                         "powered": "true", "locked": "false"})
    elif block_id == "lever":
        cells[(0, 1, 0)] = ("lever", {"powered": "true"})
    elif block_id == "torch":
        cells[(0, 1, 0)] = ("redstone_torch", {"lit": "true"})
    cells[(0, 0, 0)] = ("purple_wool", {})
    g = build(cells)
    f = solve(g, {})
    return C.repeater_locked(g, f, {}, pos, g.get(pos))

check("repeater IS locked by a powered repeater into its side", locked_by("repeater"), True)
check("repeater is NOT locked by a lever", locked_by("lever"), False)
check("repeater is NOT locked by a torch", locked_by("torch"), False)

# 7. repeater restores signal to full strength
cells = dust_line(1, 10)
cells[(0, 1, 0)] = ("lever", {"powered": "true"})
cells[(0, 0, 0)] = ("purple_wool", {})
cells[(11, 1, 0)] = ("repeater", {"facing": "west", "delay": "1", "powered": "true",
                                  "locked": "false"})
cells[(11, 0, 0)] = ("purple_wool", {})
cells.update(dust_line(12, 14))
f = solve(build(cells), {})
check("repeater output restores dust to 15",
      f.dust.get((12, 1, 0), 0), 15)

# 8. point sources feeding a diode's REAR.
#    Written from the rule, not from the solver: a torch powers all six of its
#    neighbours except the block it is mounted on, and a diode's `facing` points at
#    its input. A torch sitting directly behind a repeater used to read as 0, which
#    left whole lamp screens stuck on.
def diode_fed_by(source):
    """Repeater at (1,1,0) reading east, with `source` placed at (2,1,0)."""
    pos = (1, 1, 0)
    cells = {pos: ("repeater", {"facing": "east", "delay": "1",
                                "powered": "false", "locked": "false"}),
             (1, 0, 0): ("purple_wool", {}),
             (3, 1, 0): ("purple_wool", {})}       # the wall torch's support
    if source == "wall_torch":
        # facing=west => mounted on the block to its EAST, pointing at the repeater
        cells[(2, 1, 0)] = ("redstone_wall_torch", {"facing": "west", "lit": "true"})
    elif source == "wall_torch_unlit":
        cells[(2, 1, 0)] = ("redstone_wall_torch", {"facing": "west", "lit": "false"})
    elif source == "lever":
        cells[(2, 1, 0)] = ("lever", {"powered": "true"})
        cells[(2, 0, 0)] = ("purple_wool", {})
    elif source == "button":
        cells[(2, 1, 0)] = ("stone_button", {"powered": "true"})
        cells[(2, 0, 0)] = ("purple_wool", {})
    g = build(cells)
    f = solve(g, {})
    return C.eval_repeater(g, f, {}, pos, g.get(pos))


check("lit torch behind a repeater powers it", diode_fed_by("wall_torch"), True)
check("unlit torch behind a repeater does not", diode_fed_by("wall_torch_unlit"), False)
check("lever behind a repeater powers it", diode_fed_by("lever"), True)
check("pressed button behind a repeater powers it", diode_fed_by("button"), True)

# 9. a torch never powers the block it is mounted on
cells = {(2, 1, 0): ("purple_wool", {}),
         (2, 2, 0): ("redstone_torch", {"lit": "true"})}
g = build(cells)
check("torch emits nothing toward its own support",
      C.source_signal(g, {}, (2, 2, 0), (2, 1, 0)), 0)
check("torch emits 15 to a neighbour that is not its support",
      C.source_signal(g, {}, (2, 2, 0), (3, 2, 0)), 15)

# 10. a comparator SIDE takes only dust, a redstone block or a diode pointing in.
#     The reason is worth stating correctly: side inputs are not restricted to diodes.
#     A side reads any signal SOURCE, but takes its DIRECT signal - and a torch emits
#     direct signal only upward, a lever only into its support, so neither reaches a
#     comparator sideways. Dust and redstone blocks are special-cased to their full
#     level, and a diode gives direct signal only out of its front.
pos = (1, 1, 0)
cells = {pos: ("comparator", {"facing": "north", "mode": "compare", "powered": "false"}),
         (1, 0, 0): ("purple_wool", {}),
         (0, 1, 0): ("redstone_torch", {"lit": "true"}),      # west = a SIDE
         (0, 0, 0): ("purple_wool", {}),
         (1, 1, -1): ("redstone_torch", {"lit": "true"}),     # north = the REAR
         (1, 0, -1): ("purple_wool", {})}
g = build(cells)
f = solve(g, {})
check("torch on a comparator SIDE reads 0 (diodes only)",
      C.input_from(g, f, {}, pos, "west", sides_only=True), 0)
check("torch on a comparator REAR reads 15",
      C.input_from(g, f, {}, pos, "north"), 15)

# 11. a lever mounted straight onto a lamp lights it
cells = {(0, 1, 0): ("redstone_lamp", {"lit": "true"}),
         (1, 1, 0): ("lever", {"powered": "true"}),
         (1, 0, 0): ("purple_wool", {})}
g = build(cells)
f = solve(g, {})
check("lever on a lamp lights it",
      C.eval_lamp(g, f, {}, (0, 1, 0), g.get((0, 1, 0))), True)
cells[(1, 1, 0)] = ("lever", {"powered": "false"})
g = build(cells)
f = solve(g, {})
check("lever off leaves the lamp dark",
      C.eval_lamp(g, f, {}, (0, 1, 0), g.get((0, 1, 0))), False)

# 12. dust changes level only when the block in the way allows it, and the two
#     directions demand OPPOSITE things of that block. Reading a source one level UP
#     needs the block between to be a conductor for the signal to climb; reading one
#     level DOWN needs it not to be. That asymmetry is why a glass tower behaves the
#     way it does, and it is the whole reason dust was 4:1 over-powered.

def reads_from_above(between, cap=None):
    """Source dust one level UP and one across; returns the reader's power."""
    cells = {(0, 0, 0): ("purple_wool", {}),          # reader's support
             (0, 1, 0): ("redstone_wire", {}),        # READER
             (1, 1, 0): (between, {}),                # the block in the way
             (1, 2, 0): ("redstone_wire", {}),        # source
             (2, 2, 0): ("lever", {"powered": "true", "face": "floor"}),
             (2, 1, 0): ("purple_wool", {})}
    if cap:
        cells[(0, 2, 0)] = (cap, {})
    return solve(build(cells), {}).dust.get((0, 1, 0), 0)


def reads_from_below(between):
    """Source dust one level DOWN and one across; returns the reader's power."""
    cells = {(0, 0, 0): ("purple_wool", {}),          # source's support
             (0, 1, 0): ("redstone_wire", {}),        # source
             (1, 1, 0): ("purple_wool", {}),          # reader's support
             (1, 2, 0): ("redstone_wire", {}),        # READER
             (-1, 1, 0): ("lever", {"powered": "true", "face": "floor"}),
             (-1, 0, 0): ("purple_wool", {})}
    if between:
        cells[(0, 2, 0)] = (between, {})              # the block in the way
    return solve(build(cells), {}).dust.get((1, 2, 0), 0)


check("dust climbs a diagonal step over a SOLID block",
      reads_from_above("purple_wool"), 14)
check("dust does NOT climb a diagonal step over GLASS",
      reads_from_above("glass"), 0)
check("a solid block capping the reader blocks the step",
      reads_from_above("purple_wool", cap="purple_wool"), 0)
check("dust drops a diagonal step when nothing is in the way",
      reads_from_below(None), 14)
check("dust does NOT drop a diagonal step through a SOLID block",
      reads_from_below("purple_wool"), 0)

print(f"\n{len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    print("failed:", ", ".join(FAIL))
sys.exit(1 if FAIL else 0)
