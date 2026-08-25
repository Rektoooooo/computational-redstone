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
import json
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


GLASS = BlockState("minecraft:glass")


def steps():
    """
    Four lanes testing whether dust changes level, differing only in two things:
    whether the block it steps over is SOLID or GLASS, and whether the source is
    below or above.

    This is the sharpest test available, because the rule is asymmetric and the
    asymmetry was derived rather than read off. Reading a source one level DOWN needs
    the block between to be a non-conductor; reading one level UP needs it to BE a
    conductor. Glass is never a conductor, so power should climb ONTO a glass step but
    refuse to come back DOWN off one.

    Predicted: lanes 1-3 light their lamp, lane 4 does not. Only the last lane
    separates the model from the obvious guess that a step either works or does not.
    """
    lanes = [("solid", "below"), ("glass", "below"),
             ("solid", "above"), ("glass", "above")]
    spacing = 3
    reg = Region(0, 0, 0, 5, 3, len(lanes) * spacing - (spacing - 1))

    for i, (step_block, source) in enumerate(lanes):
        z = i * spacing
        stepper = GLASS if step_block == "glass" else FLOOR

        for x in range(5):
            reg[x, 0, z] = FLOOR
        reg[2, 1, z] = stepper          # the block under test
        reg[3, 1, z] = FLOOR            # support for the upper run
        reg[2, 2, z] = wire()
        reg[3, 2, z] = wire()

        if source == "below":
            # drive the LOW dust and watch power climb onto the step
            reg[0, 1, z] = REDSTONE_BLOCK
            reg[1, 1, z] = wire()
            reg[4, 1, z] = FLOOR
            reg[4, 2, z] = LAMP         # lit if the climb worked
        else:
            # drive the HIGH dust and watch whether power comes back down
            reg[4, 1, z] = FLOOR
            reg[4, 2, z] = REDSTONE_BLOCK
            reg[1, 1, z] = wire()       # the reader - the block that matters
            reg[0, 1, z] = LAMP         # lit only if the descent worked

    return reg, "steps", (
        "4 lanes: solid/glass step, source below/above. Lanes 1-3 should light "
        "their lamp; lane 4 (glass, source above) should stay dark."
    )


def _sign(reg, pos, lines):
    """A standing sign carrying real text, so the lane labels read in game."""
    from litemapy.schematic import TileEntity
    from nbtlib.tag import Compound, String, Int, Byte
    x, y, z = pos
    reg[x, y, z] = BlockState("minecraft:oak_sign", rotation="4", waterlogged="false")
    data = {"id": String("minecraft:sign"), "x": Int(x), "y": Int(y), "z": Int(z),
            "Color": String("black"), "GlowingText": Byte(0)}
    for i in range(4):
        text = lines[i] if i < len(lines) else ""
        data[f"Text{i+1}"] = String(json.dumps({"text": text}))
    reg.tile_entities.append(TileEntity(Compound(data)))


def _barrel(reg, pos, stacks):
    """A barrel holding `stacks` full stacks - 14 of them read as strength 8."""
    from litemapy.schematic import TileEntity
    from nbtlib.tag import Compound, String, Int, Byte, List
    x, y, z = pos
    reg[x, y, z] = BlockState("minecraft:barrel", facing="north", open="false")
    items = List[Compound]([
        Compound({"Slot": Byte(i), "id": String("minecraft:redstone"), "Count": Byte(64)})
        for i in range(stacks)
    ])
    reg.tile_entities.append(TileEntity(Compound({
        "id": String("minecraft:barrel"), "x": Int(x), "y": Int(y), "z": Int(z),
        "Items": items,
    })))


def comparator():
    """
    Does a comparator read a container THROUGH a solid block?

    It does, and that was worth ten points of comparator agreement (83.5 -> 93.4) when
    it went in. The rule: if the block directly behind is a full conductor and the
    reading so far is under 15, the comparator looks ONE STEP FURTHER for a container
    and takes that instead. Keeping a signal-strength barrel a block back, out of the
    wiring, is a normal thing to build.

    Three lanes, identical but for the block between barrel and comparator:

        1  nothing        - barrel straight into the comparator      -> 8
        2  stone          - reads through it                         -> 8
        3  glass          - glass is not a conductor, so nothing     -> 0

    Lane 3 is what separates the real rule from "a comparator can see two blocks
    back". Every barrel holds 14 stacks, which reads as strength 8.
    """
    lanes = [("1 DIRECT", None, "expect 8"),
             ("2 THRU STONE", FLOOR, "expect 8"),
             ("3 THRU GLASS", GLASS, "expect 0")]
    reg = Region(0, 0, 0, 8, 2, 7)

    for i, (name, between, note) in enumerate(lanes):
        z = i * 3
        for x in range(8):
            reg[x, 0, z] = FLOOR
        _sign(reg, (0, 1, z), [name, note])

        if between is None:
            _barrel(reg, (2, 1, z), 14)          # straight into the comparator
        else:
            _barrel(reg, (1, 1, z), 14)
            reg[2, 1, z] = between               # the block under test

        # facing points at the INPUT, so facing=west reads west and outputs east
        reg[3, 1, z] = BlockState("minecraft:comparator", facing="west",
                                  mode="compare", powered="false")
        for x in (4, 5, 6):
            reg[x, 1, z] = wire()
        reg[7, 1, z] = LAMP

    return reg, "comparator", (
        "3 lanes: barrel into a comparator directly, through stone, through glass. "
        "Expect 8, 8, 0 - the glass lane is the one that matters."
    )


BUILDERS = {"decay": decay, "steps": steps, "comparator": comparator}


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
