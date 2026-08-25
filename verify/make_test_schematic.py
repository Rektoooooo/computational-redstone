#!/usr/bin/env python3
"""
Build small schematics whose behaviour the simulator predicts, for checking that
prediction against the real game.

    python3 verify/make_test_schematic.py decay

Everything the simulator knows has so far been checked against SAVED state - real
circuits, but frozen ones. The game is the authority, and nothing from this project
has ever been pasted back into it. These are deliberately tiny so that a disagreement
points at one rule rather than at a haystack.

Dust is written with `power=0` on purpose. If the values were baked in, the game would
simply show us what we put there; starting cold makes the numbers a real prediction.
"""
import os
import sys

from litemapy import Region, BlockState

FLOOR = BlockState("minecraft:stone")
REDSTONE_BLOCK = BlockState("minecraft:redstone_block")
LAMP = BlockState("minecraft:redstone_lamp", lit="false")


def wire(east="side", west="side", north="none", south="none"):
    """Dust, unpowered, with the connection shape the game would give it."""
    return BlockState("minecraft:redstone_wire", power="0",
                      east=east, west=west, north=north, south=south)


def decay(length=6):
    """
    Redstone block -> a run of dust -> lamp, in a straight line heading east.

    The point of interest is the dust levels. A redstone block hands 15 to the dust
    touching it and every further block of dust drops one, so with six the lamp is
    still reached comfortably. Reading the levels off F3 makes this a much sharper
    test than "the lamp is on".

    Note the last dust connects EAST into the lamp even though a lamp is not something
    dust connects to: a wire with nothing to its north or south straightens itself out
    into a line. Without that rule the lamp would stay dark.
    """
    width = 1 + length + 1
    reg = Region(0, 0, 0, width, 2, 1)

    for x in range(width):
        reg[x, 0, 0] = FLOOR

    reg[0, 1, 0] = REDSTONE_BLOCK
    for i in range(length):
        reg[1 + i, 1, 0] = wire()
    reg[width - 1, 1, 0] = LAMP

    return reg, "decay", (
        f"redstone block -> {length} dust -> lamp, running east. "
        "Expect 15 at the first dust, dropping 1 each block, and the lamp lit."
    )


BUILDERS = {"decay": decay}


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "decay"
    if which not in BUILDERS:
        sys.exit(f"unknown test '{which}'. Available: {', '.join(BUILDERS)}")

    reg, name, description = BUILDERS[which]()
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(out_dir, f"{name}.litematic")

    reg.as_schematic(name=name, author="computational-redstone",
                     description=description).save(out)

    print(f"wrote {out}")
    print(f"  {reg.width} x {reg.height} x {reg.length}  (x, y, z)")
    print(f"  {description}")


if __name__ == "__main__":
    main()
