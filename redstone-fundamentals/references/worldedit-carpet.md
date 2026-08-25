# WorldEdit and Carpet command reference

Both are Fabric mods. Install Fabric first.

## WorldEdit

Make a selection with `//wand` (gives a wooden axe): **left-click** sets corner 1,
**right-click** sets corner 2.

| Command | Effect |
|---|---|
| `//set <block>` | Fill the selection |
| `//set air` | Delete the selection |
| `//move <n>` | Move the selection n blocks in the direction you're looking |
| `//copy` | Copy, relative to where you are standing |
| `//paste` | Paste, positioned relative to where you are standing |
| `//stack <n>` | Repeat the selection n times in the direction you're looking |
| `//rotate <deg>` | Rotate the clipboard (90 / 180 / 270) |
| `//expand <n>` | Grow the selection |
| `//update` | Force block updates — needed after pasting redstone |

### The `-a` flag

`//paste -a` and `//move -a` **ignore air**. This matters constantly: selections are
always rectangular, so pasting a shaped component over existing redstone will
otherwise blank out everything around it.

Use `-a` by default when pasting a component into an existing build.

### Schematics

`//schem save <name>` and `//schem load <name>` persist builds to
`.minecraft/config/worldedit/schematics`. This is how you transfer builds between
worlds, share them, and how the CPU assembler delivers compiled programs.

### Reference point discipline

`//copy` records your position relative to the selection, and `//paste` reproduces
that offset. Always stand somewhere meaningful — a corner, or a specific bit line —
so the paste lands predictably. Getting this wrong is the most common WorldEdit
mistake; `//undo` exists for a reason.

## Carpet

| Command | Effect |
|---|---|
| `/tick rate <n>` | Game ticks per second (default 20, max 500) |
| `/tick freeze` | Pause the world; run again to resume |
| `/tick step <n>` | Advance n **game** ticks while frozen |
| `/carpet creativeNoClip true` | Fly through blocks, land on them when you stop |

`/tick step 2` = exactly one redstone tick. This is the primary debugging tool:
freeze, then step, and watch the circuit resolve one stage at a time.

`creativeNoClip` is essential for building inside tight circuits.

## RedstoneTools

A quality-of-life Fabric mod built by and for this community. Notably it was not
updated to 1.21 at the time the CPU series was recorded, which is part of why
1.18.2 remains the standard version.
