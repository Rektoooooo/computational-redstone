# World setup and tooling

## Creating the world

- **Game mode:** Creative
- **Cheats:** on
- **Difficulty:** Peaceful
- **Generate structures:** off
- **World type:** Superflat → Customize → Presets → **"Redstone Ready"** or **"The Void"**
  - The Void spawns a small platform on load, so you can place your first block.

### Game rules to turn off

| Category | Rules |
|---|---|
| Spawning | all of them |
| Drops | **doBlockDrops** — stops redstone popping off when you break a supporting block |
| World updates | **doDaylightCycle**, **doWeatherCycle** |

Those three categories are pure nuisance for redstone work.

## Version

The reference series are built in **Java 1.18.2**. That is the version the
computational redstone community standardised on, and the version the BatPU-2
computer and its schematics target. Building the CPU in a newer version risks
schematic and mod incompatibility. General circuits port fine to 1.19+.

**Java only.** Bedrock has no quasi-connectivity, different update ordering, and
a consume/produce tick split. Computational redstone designs will not port.

## Quality of life

**Middle-click** picks the block you are looking at — fast way to alternate
between two colours while building.

**Saved hotbars** (creative inventory, bottom section) — load an entire hotbar on
demand. A proven layout:

1. Basic redstone components (used most)
2. Common colours for colour-coding
3. Signal-strength barrels 1–7
4. Signal-strength barrels 8–15
5. Shulker boxes with letters and symbols for labelling

**Texture pack** — at minimum use one that prints the signal strength number on
the dust itself. Available from Vanilla Tweaks if you don't want a full pack.

## The performance ceiling

Vanilla runs at 20 game ticks per second. A full CPU executes roughly **one
instruction every 10 seconds** at that speed. Two escapes:

- **Carpet mod** — `/tick rate 500` is the maximum, a 25× speedup, giving about
  2.5 instructions per second.
- **MCHPRS** — a custom server that reimplements redstone for speed. `/rtps [X]`
  sets redstone ticks per second, `/rtps unlimited` for maximum. This is what
  showcase videos use.

**MCHPRS does not support droppers and hoppers.** This is why CPU-grade randomness
uses a linear feedback shift register rather than a dropper-based binary randomizer.
