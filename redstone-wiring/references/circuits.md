# The wiring circuits, as extracted

49 builds harvested from mattbatwings' *Wiring like a pro* world download into
`worlds/primitives/wiring/`. **The world contains no signs**, so nothing here is
labelled by its author — every name below is either *confirmed by driving it in the
simulator* or *inferred from structure*, and the two are kept apart on purpose. A
structural read of this library has been wrong before.

```bash
cd worlds
../.venv/bin/python harvest.py "<world>" primitives/wiring --min 20
```

## Confirmed by driving

| build | what it is | how it was confirmed |
|---|---|---|
| `build-41` | **hex wiring, flat.** Dust line, 11 repeaters reading it from the side, second dust line taking their outputs. | Barrel swept 0–15; output is `in + 4` for every input 1–11, saturating at 15, and 0 for 0. `15 − 11 = 4`, exactly as the video says. |
| `build-15` | **4-bit vertical bus**, repeatered. | Each of the four levers lights its own lamp at the far end and no other. No crosstalk. |
| `build-18` | **horizontal → vertical conversion.** | Input at x = 4, 6, 8 arrives at y = 4, 6, 8 — in order. |
| `build-19` | the same, **mirrored**. | Input at x = 4, 6, 8 arrives at y = 8, 6, 4 — reversed, which is the variant the video offers when the default bit order is wrong. |
| `build-36`, `build-37`, `build-44`, `build-45`, `build-46` | **glass towers**, 27 to 46 blocks tall, extended variously by a torch pair or a repeater. | Bottom lamp off, top lamp on, for each. |
| `build-14` | **zero-tick 3D crossover** — 4 bits by 4 bits, no repeaters at all. | **Fails in our simulator.** Four of the sixteen lamps light regardless of which lever is thrown, and two of the eight inputs do not reach their own output. See below. |

## The one our model gets wrong

`build-14` is the crossover the video describes as *"a zero-tick crossover... kind of
messy, but if you really need that extra speed"*. It uses no repeaters — only dust,
blocks and 3D staggering — so it leans entirely on **diagonal dust behaviour**, which is
the most intricate rule in the whole system and the one our solver most plausibly has
slightly wrong.

Two readings are possible and they have not been separated yet:

1. our `dust_links()` is wrong for some case this circuit uses, or
2. the harvest clipped part of the build and the missing blocks matter.

Until that is settled, **generated builds should use the repeater intersection**, which
is simple enough that there is nothing to get wrong. Chasing this down is worth doing
anyway: a rule the solver has wrong here is a rule it has wrong everywhere.

## Inferred from structure — not confirmed

Grouped by what the census and shape suggest. Treat every one of these as a guess.

- **Tall pairs** `build-01`, `build-02` (8 × 66 × 19/26, ~500 dust and 48 wall torches
  each): banks of glass towers, the multi-bit upward case, extended with torches.
- **Long flat runs** `build-00`, `build-03` (17 × 5 × 84 and 19 × 5 × 67, 500 dust,
  24–35 repeaters): flat multi-bit wiring, the repeater-every-15 case.
- **Tall diagonals** `build-04`, `build-05` (5 × 43 × 52, identical censuses): the
  diagonal multi-bit cases, up and down.
- **The hex section** `build-06` (62 × 12 × 13, 24 comparators, 5 barrels, 4 lamps):
  likely the whole hex demonstration bench rather than one circuit.
- **Hex variants** `build-27`, `build-32`, `build-33`, `build-34` (15 repeaters, 2
  comparators): the full-length version of `build-41`, where `15 − 15 = 0` and the
  output equals the input with nothing to subtract. `build-38`, `build-40`, `build-48`
  are shorter variants.
- **Target-block corner** `build-42` (18 × 5 × 20, one target block, one lamp): the
  "signal runs out on a turn" fix.
- **Spirals** `build-13`, `build-39` and the other tall-and-narrow builds: the downward
  cases.

## Full inventory

| build | size | blocks | components |
|---|---|---|---|
| `build-00` | 17x5x84 | 2380 | wire 525, repeater 35 |
| `build-01` | 8x66x19 | 1264 | wire 496, wall_torch 48 |
| `build-02` | 8x66x26 | 1320 | wire 496, wall_torch 48 |
| `build-03` | 19x5x67 | 2209 | wire 468, repeater 24 |
| `build-04` | 5x43x52 | 768 | wire 360, repeater 24 |
| `build-05` | 5x43x52 | 768 | wire 360, repeater 24 |
| `build-06` | 62x12x13 | 699 | wire 269, repeater 43, comparator 24, barrel 5 |
| `build-07` | 21x12x9 | 336 | wire 112, repeater 26, comparator 16, lamp 4 |
| `build-08` | 8x7x40 | 950 | wire 120, lamp 8, repeater 6, lever 4 |
| `build-09` | 11x6x39 | 666 | wire 120, lamp 8, repeater 4, lever 4 |
| `build-10` | 6x11x39 | 510 | wire 120, lamp 8, repeater 4, lever 4 |
| `build-11` | 11x30x8 | 412 | wire 104, lamp 8, lever 4, repeater 4 |
| `build-12` | 11x30x8 | 392 | wire 96, lamp 8, wall_torch 8, lever 4 |
| `build-13` | 8x31x10 | 348 | wire 88, lamp 8, torch 8, lever 4 |
| `build-14` | 13x13x13 | 361 | wire 72, lamp 16, lever 8 |
| `build-15` | 15x12x15 | 355 | wire 60, lamp 16, repeater 8, lever 4 |
| `build-16` | 6x25x23 | 294 | wire 60, lamp 8, repeater 8, lever 4 |
| `build-17` | 11x20x21 | 602 | wire 60, lamp 8, lever 4 |
| `build-18` | 13x13x13 | 296 | wire 56, lamp 8, repeater 4, lever 4 |
| `build-19` | 13x13x13 | 296 | wire 56, lamp 8, repeater 4, lever 4 |
| `build-20` | 7x24x21 | 283 | wire 58, lamp 8, lever 4 |
| `build-21` | 7x24x21 | 283 | wire 58, lamp 8, lever 4 |
| `build-22` | 8x21x21 | 468 | wire 56, lamp 8, lever 4 |
| `build-23` | 8x20x21 | 468 | wire 56, lamp 8, lever 4 |
| `build-24` | 7x21x15 | 132 | wire 56, lamp 8, lever 4 |
| `build-25` | 6x17x19 | 238 | wire 52, lamp 8, lever 4 |
| `build-26` | 11x7x16 | 466 | wire 46, lamp 8, repeater 4, lever 4 |
| `build-27` | 13x20x7 | 173 | wire 38, repeater 15, comparator 2, barrel 1 |
| `build-28` | 11x21x21 | 457 | wire 48, lamp 5, lever 1 |
| `build-29` | 5x16x17 | 179 | wire 48, lamp 4 |
| `build-30` | 8x11x15 | 200 | wire 36, lamp 6, repeater 4, lever 4 |
| `build-31` | 15x12x8 | 96 | wire 38, lamp 8, lever 4 |
| `build-32` | 11x19x6 | 158 | wire 31, repeater 15, comparator 2, barrel 1 |
| `build-33` | 7x19x22 | 251 | wire 31, repeater 15, comparator 2 |
| `build-34` | 6x20x25 | 224 | wire 31, repeater 15, comparator 2 |
| `build-35` | 6x17x19 | 152 | wire 24, repeater 11, target 10, comparator 1 |
| `build-36` | 5x48x8 | 147 | wire 39, lamp 2, torch 2, lever 1 |
| `build-37` | 6x45x6 | 79 | wire 36, lamp 2, wall_torch 2, lever 1 |
| `build-38` | 7x17x19 | 194 | wire 27, repeater 13, comparator 1 |
| `build-39` | 5x30x15 | 210 | wire 35, lamp 2, wall_torch 2, lever 1 |
| `build-40` | 10x15x7 | 139 | wire 23, repeater 11, comparator 3, barrel 1 |
| `build-41` | 7x5x17 | 175 | wire 22, repeater 11, comparator 1, barrel 1 |
| `build-42` | 18x5x20 | 318 | wire 26, repeater 2, target 1, lamp 1 |
| `build-43` | 9x10x9 | 51 | wire 11, comparator 8, barrel 5, lamp 4 |
| `build-44` | 6x31x6 | 51 | wire 22, lamp 2, wall_torch 2, lever 1 |
| `build-45` | 5x30x7 | 121 | wire 21, lamp 2, torch 2, lever 1 |
| `build-46` | 6x29x7 | 50 | wire 21, lamp 2, repeater 1, lever 1 |
| `build-47` | 6x22x9 | 49 | wire 19, lamp 4, lever 2 |
| `build-48` | 6x5x17 | 108 | wire 11, repeater 11, comparator 1, barrel 1 |
