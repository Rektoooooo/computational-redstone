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

print(f"\n{len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    print("failed:", ", ".join(FAIL))
sys.exit(1 if FAIL else 0)
