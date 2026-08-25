#!/usr/bin/env python3
"""
Turn a schematic into /setblock commands, pasteable straight into chat.

    python3 verify/to_commands.py verify/decay.litematic [--skip-floor]

Litematica's paste needs creative mode, the right tool mode and a hotkey that varies
by install. Commands need none of that, and they have one real advantage for this
job: /setblock triggers block updates, so the redstone actually settles. A pasted
schematic often lands inert until something pokes it.

Coordinates are relative to the player, along world axes: ~1 is one block east
whichever way you happen to be facing.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "worlds"))

from sim.grid import Grid

# Placed last, because a lamp is what we want to observe settling.
LAST = ("redstone_lamp",)


def rel(v):
    return "~" if v == 0 else f"~{v}"


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "verify/decay.litematic"
    skip_floor = "--skip-floor" in sys.argv

    grid = Grid.from_file(path)
    cells = []
    for pos in sorted(grid.positions(), key=lambda p: (p[1], p[0], p[2])):
        cell = grid.get(pos)
        if skip_floor and pos[1] == 0:
            continue          # a superflat world already has a floor
        cells.append((pos, cell))

    # components after plain blocks, so wiring settles onto a finished floor
    cells.sort(key=lambda pc: (pc[1].id in LAST, pc[0][1], pc[0][0], pc[0][2]))

    print(f"\n# {os.path.basename(path)} - {len(cells)} blocks")
    print("# stand where you want the LEFT end, face east, then paste one at a time\n")

    # Dropping the schematic's own floor means everything above it comes down a level,
    # so the run lands at the player's feet instead of hovering one block up.
    y_off = 1 if skip_floor else 0
    for (x, y, z), cell in cells:
        print(f"/setblock {rel(x)} {rel(y - y_off)} {rel(z)} minecraft:{cell.id}")

    # Poking the source forces an update, in case anything landed inert.
    src = [p for p in grid.positions() if grid.get(p).id == "redstone_block"]
    if src:
        x, y, z = src[0]
        print("\n# then poke the source so everything re-evaluates:")
        print(f"/setblock {rel(x)} {rel(y - y_off)} {rel(z)} minecraft:air")
        print(f"/setblock {rel(x)} {rel(y - y_off)} {rel(z)} minecraft:redstone_block")
    print()


if __name__ == "__main__":
    main()
