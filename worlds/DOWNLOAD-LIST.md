# mattbatwings world downloads — primitive source

Twenty freely-published world downloads, one per episode, mapped to the skill they
feed. These are the source for the **primitive library** (Phase 2 of
`BUILD-PIPELINE-RESEARCH.md`).

## How to get them

PlanetMinecraft sits behind Cloudflare bot protection, so scripted downloading does
not work — and shouldn't be worked around. Download them in your own browser instead.

Every project exposes a **direct download URL**:

```
https://www.planetminecraft.com/project/<slug>/download/worldmap/
```

Pasting that straight into the address bar starts the `.zip` immediately — no need to
find the button on the page.

`fetch.sh` in this folder opens each one in your default browser, a few seconds apart.
Run it, then let the downloads land.

Save the zips into this folder, then unzip. Each becomes a world directory containing
`region/*.mca`, which is what the extractor reads.

> **Version note:** these are Java **1.18.2** worlds, matching the skill library.
> `anvil-parser2` reads that range fine.

## The list

### Logical Redstone Reloaded

| Ep | Contents | Feeds | Slug |
|---|---|---|---|
| 3 | logic gates, XOR designs | `redstone-logic-gates` | `redstone-logic-gates-lrr-episode-3` |
| 4 | half/full adders, RCA, CCA variants | `redstone-arithmetic` | `redstone-binary-addition-lrr-episode-4` |
| 5 | subtractors, conditional inverters | `redstone-arithmetic` | `redstone-binary-subtraction` |
| 6 | decoders, encoders, mux, comparators, redcoder | `redstone-combinational` | `combinational-redstone-devices` |
| 7 | pulse gens, clocks, SR/D latches, T flip-flops | `redstone-sequential` | `pulses-clocks-latches-amp-flip-flops` |
| 8 | registers, counters, shift registers, memory | `redstone-sequential` | `sequential-redstone-devices-lrr-8` |
| 9 | pixel displays, matrix decoders, 7-segment | `redstone-displays` | `redstone-displays-lrr-9` |
| 10 | Lights Out, Connect 4 | (game patterns) | `game-design-lrr-10` |

### Let's Make a Redstone Computer

| Ep | Contents | Feeds | Slug |
|---|---|---|---|
| 2 | ALU designs (all three) | `redstone-cpu` | `redstone-alus-from-let-s-make-a-computer` |
| 3 | register file, dual read | `redstone-cpu` | `redstone-registers-from-let-s-make-a-computer` |
| 4 | control ROM | `redstone-cpu` | `redstone-control-rom-from-let-s-make-a-redstone-computer` |
| 5 | instruction memory, tree decoder | `redstone-cpu` | `redstone-instruction-memory-from-let-s-make-a-redstone-computer` |
| 6 | program counter | `redstone-cpu` | `redstone-program-counter-from-let-s-make-a-redstone-computer` |
| 7 | flags, branching | `redstone-cpu` | `redstone-jumping-branching-from-let-s-make-a-redstone-computer` |
| 8 | call stack, bidirectional shift register | `redstone-cpu` | `the-call-stack-from-let-s-make-a-redstone-computer` |
| 9 | data memory | `redstone-cpu` | `data-memory-from-let-s-make-a-redstone-computer` |
| 10 | I/O devices, screen, controller | `redstone-cpu` | `input-and-output-from-let-s-make-a-redstone-computer` |

### Standalone

| Contents | Feeds | Slug |
|---|---|---|
| 5 Hz 8-bit multiplier | `redstone-arithmetic` | `5hz-8-bit-multiplier` |
| UI components, keypads, selectors | `redstone-displays` | `user-interfaces-from-video` |
| **BatPU-2 — the full computer** | `redstone-cpu` | `new-redstone-computer` |

## Highest value first

If you don't want all twenty, these four give the most leverage:

1. **`redstone-binary-addition-lrr-episode-4`** — the CCA, the single most reused component
2. **`combinational-redstone-devices`** — decoders, which every other build depends on
3. **`sequential-redstone-devices-lrr-8`** — registers and counters
4. **`new-redstone-computer`** — the whole CPU, every component in situ and known-working

## After downloading

```bash
cd worlds && unzip '*.zip'
python extract.py survey <world-dir>              # find the builds
python extract.py extract <world-dir> x1 y1 z1 x2 y2 z2 name
```

`survey` locates dense redstone regions and reports bounding boxes, so you don't have
to hunt coordinates by hand.

## Wiring like a pro — mattbatwings

https://www.youtube.com/watch?v=pT-VWjqYli0 — world download harvested 2026-08-26 into
`worlds/primitives/wiring/` (49 builds, no signs). Transcript in `transcripts/`.
Every wiring problem worth knowing: single wires and buses in every direction, the
horizontal↔vertical converter, the hex wire, and the two crossovers. See
`redstone-wiring/SKILL.md`.
