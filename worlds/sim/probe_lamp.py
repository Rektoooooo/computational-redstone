"""
Print a 2D slice around a lamp, showing saved vs computed.

    python -m sim.probe_lamp <build.litematic> <x> <y> <z> [--axis z|y|x]

The third of the three debugging techniques: seeing the structure around a wrong
cell explains far more than the cell itself does.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sim.grid import Grid, DIRS, UP, DOWN, LAMP, is_conductive, prop, step, truthy
from sim.engine import Sim
from sim import components as C

SHORT = {
    "redstone_wire": "wire", "redstone_lamp": "LAMP", "redstone_torch": "torU",
    "redstone_wall_torch": "torW", "repeater": "rept", "comparator": "comp",
    "lever": "levr", "redstone_block": "rblk", "air": ".",
}


def short(bid):
    if bid in SHORT:
        return SHORT[bid]
    if bid.endswith("_wool"):
        return bid[:-5][:4]
    if "glass" in bid:
        return "glas"
    if "sign" in bid:
        return "sign"
    return bid[:4]


def main():
    path = sys.argv[1]
    cx, cy, cz = (int(v) for v in sys.argv[2:5])
    axis = sys.argv[sys.argv.index("--axis") + 1] if "--axis" in sys.argv else "z"
    r = int(sys.argv[sys.argv.index("--r") + 1]) if "--r" in sys.argv else 3

    grid = Grid.from_file(path)
    sim = Sim(grid)
    sim.settle()
    f, states = sim.field, sim.states

    def cellinfo(p):
        c = grid.get(p)
        bid = c.id
        tag = short(bid)
        if bid == "redstone_wire":
            return f"{tag}{f.dust.get(p,0):>2}/{prop(c,'power','?'):>2}"
        if bid == LAMP:
            got = C.eval_lamp(grid, f, states, p, c)
            want = truthy(prop(c, "lit"))
            mark = "!" if got != want else " "
            return f"{tag}{'L' if got else 'd'}/{'L' if want else 'd'}{mark}"
        if bid in ("redstone_torch", "redstone_wall_torch"):
            return f"{tag} {'L' if states.get(p, True) else 'd'}  "
        if bid in ("repeater", "comparator"):
            return f"{tag}{prop(c,'facing','?')[:1]}{'P' if states.get(p) else '.'} "
        if bid == "air":
            return "  .   "
        if is_conductive(bid):
            bp = f.block_power(p)
            s = f.strong.get(p, 0)
            return f"{tag}{bp:>2}{'S' if s else 'w'} "
        return f"{tag}    "

    print(f"\n{path}  centre=({cx},{cy},{cz})  slice axis={axis}\n")
    if axis == "z":
        rows = range(cy + r, cy - r - 1, -1)
        cols = range(cx - r, cx + r + 1)
        print("      " + "".join(f"x={c:<5}" for c in cols))
        for y in rows:
            line = f"y={y:<3} " + "".join(cellinfo((x, y, cz)) + " " for x in cols)
            print(line)
    elif axis == "y":
        rows = range(cz + r, cz - r - 1, -1)
        cols = range(cx - r, cx + r + 1)
        print("      " + "".join(f"x={c:<5}" for c in cols))
        for z in rows:
            line = f"z={z:<3} " + "".join(cellinfo((x, cy, z)) + " " for x in cols)
            print(line)
    else:
        rows = range(cy + r, cy - r - 1, -1)
        cols = range(cz - r, cz + r + 1)
        print("      " + "".join(f"z={c:<5}" for c in cols))
        for y in rows:
            line = f"y={y:<3} " + "".join(cellinfo((cx, y, z)) + " " for z in cols)
            print(line)

    print("\nlegend: wire<computed>/<saved>   LAMP<got>/<want>  ! = mismatch")
    print("        block<power><S=strong,w=weak>   L=lit/on  d=dark/off\n")

    print("neighbours of centre:")
    for delta in list(DIRS.values()) + [UP, DOWN]:
        n = step((cx, cy, cz), delta)
        c = grid.get(n)
        if c.id == "air":
            continue
        extra = ""
        if is_conductive(c.id):
            extra = f"  strong={f.strong.get(n,0)} weak={f.weak.get(n,0)}"
        if c.id == "redstone_wire":
            extra = f"  power={f.dust.get(n,0)} activates={C.dust_activates(grid, n, (cx,cy,cz))}"
        print(f"  {delta} {n} {c.id}{extra}  props={c.props}")


if __name__ == "__main__":
    main()
