#!/usr/bin/env python3
"""
Print what the simulator expects a schematic to do, in a form that can be checked
against the game block by block.

    python3 verify/predict.py verify/decay.litematic

The prediction is written down BEFORE looking at the game on purpose. A model that is
consulted after the fact always seems to agree.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "worlds"))

from sim.grid import Grid, DUST, LAMP, LEVER, REPEATER, COMPARATOR, TORCHES, prop, truthy
from sim.engine import Sim
from sim import components as C


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "verify/decay.litematic"
    grid = Grid.from_file(path)
    sim = Sim(grid).prime()
    settled = sim.run_until_stable(max_ticks=200)

    print(f"\n{path}")
    print(f"  {grid.w} x {grid.h} x {grid.l}, {len(grid.cells)} blocks")
    print(f"  settles: {settled}   after {sim.time} game ticks\n")

    rows = []
    for pos in sorted(grid.positions()):
        cell = grid.get(pos)
        if cell.id == DUST:
            rows.append((pos, "dust", f"power {sim.field.dust.get(pos, 0)}"))
        elif cell.id == LAMP:
            lit = C.eval_lamp(grid, sim.field, sim.states, pos, cell)
            rows.append((pos, "lamp", "LIT" if lit else "dark"))
        elif cell.id in TORCHES:
            rows.append((pos, "torch", "lit" if sim.states.get(pos, True) else "out"))
        elif cell.id in (REPEATER, COMPARATOR):
            rows.append((pos, cell.id, f"out {sim.states.get(pos)}"))
        elif cell.id == LEVER:
            rows.append((pos, "lever", "on" if truthy(prop(cell, "powered")) else "off"))

    print(f"  {'position':<14} {'block':<11} predicted")
    print("  " + "-" * 44)
    for pos, kind, value in rows:
        print(f"  {str(pos):<14} {kind:<11} {value}")
    print()


if __name__ == "__main__":
    main()
