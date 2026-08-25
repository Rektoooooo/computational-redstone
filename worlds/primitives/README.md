# Primitive library

**195 components** harvested from 19 of mattbatwings' published world downloads.
**43 are named from in-world signs** and are reliably identified; the rest are
extracted and measured but unlabelled.

Each build has a `.litematic` (paste with Litematica) and a `.manifest.json` with
origin, size, sign labels, full block census and a measured structural profile.
`MASTER-INDEX.json` lists everything; `PROFILES.md` has the structural detail.

## Reliability

| Source | Trust |
|---|---|
| **Sign labels** | reliable — the author's own words |
| **Measured features** (size, census, ratios, stack period) | reliable — read off the blocks |
| **`candidate` guesses in PROFILES.md** | weak — benchmarked at **50%** useful, **6%** actively misleading |

Structural inference has been wrong twice already: a comparator array that looked
like a mux was the magnitude comparator, and a lamp-count rule mislabelled the CLE
adder as a decoder. Treat candidates as leads to check, never as labels.

## Inventory

| World | Builds | Named | Notable contents |
|---|---|---|---|
| `addition/` | 10 | 5 | all five adders, with tick counts |
| `alus/` | 18 | 0 | **no signs at all** — the ALU designs from LMRC #2 |
| `callstack/` | 4 | 0 | 103k components |
| `combinational/` | 22 | 1 | magnitude comparator; rest unidentified |
| `cpu-ep04-controlrom/` | 4 | 0 | control ROM |
| `cpu-ep05-instrmem/` | 8 | 0 | instruction memory |
| `cpu-ep06-progcounter/` | 7 | 0 | program counter |
| `cpu-ep07-branching/` | 9 | 0 | flags and branching |
| `cpu-ep09-datamem/` | 7 | 0 | data memory |
| `cpu-ep10-io/` | 14 | 0 | I/O devices |
| `displays/` | 23 | 11 | pixel displays, buffers, animation |
| `gamedesign/` | 5 | 1 | Lights Out / Connect 4 |
| `gates/` | 12 | 0 | individual logic gates |
| `latches/` | 8 | 10 | latches, flip-flops, pulse gens, clocks |
| `multiplier/` | 1 | 0 | the 5 Hz 8-bit multiplier, whole |
| `registers/` | 18 | 0 | register file designs |
| `sequential/` | 15 | 12 | registers, counters, shift registers |
| `subtraction/` | 1 | 1 | adder/subtractor toggle |
| `uis/` | 7 | 2 | keypads, keyboards, selectors |
| `cpu/` | 0 | — | see below |

## The highest-value named builds

**Arithmetic**
- `addition/3-ticks-8-bit-cca-by-don` — fastest and smallest CCA, the default choice
- `addition/3-ticks-torchless-fearless-8-bit-cca-by` — near-torchless, for CPU use
- `addition/5-ticks-8-bit-cca` · `4-ticks-8-bit-cle` · `yellowbunny-4-digit-hexcca-by`
- `subtraction/on-a-b-off-a-plus-b` — **adder/subtractor toggle**, sign reads
  `ON = A − B  OFF = A + B`. The conditional-inverter design from LRR #5.

**Sequential** — `sequential/read` (register file, 1296c), `add-to-total`
(accumulator), `shift-down` (bidirectional shift register), `count` (counter with
load), plus three more counter variants.

**Latches and timing** — `latches/pulse-generator-4-tick` (also carries 2- and 3-tick
variants), `5t-output-pulse-10t-period` (a clock, period stated on the sign),
`not-output` ×3 (SR latches, `NOT Output | Output | Reset`), `enable` (gated latch).

**Displays** — `displays/buffer` (1618c), `plot-pixel`, `data` (`Plot Pixel | Plot All
Pixels`), `play-animation` (3445c), `convert` (3156c), and the image display whose
signs read `Smiley | Sad | Surprised` — straight out of LRR #9.

**Combinational** — `combinational/a-gt-b`, the magnitude comparator
(`A > B | A == B | A < B`).

## Two worlds worth special mention

**`alus/` has zero signs.** Eighteen builds, none labelled — and it is the most
valuable world for CPU work.

All 18 have now been **identified visually** by rendering each build and reading its
structure against LMRC #2. Three are high confidence: `build-03` is the six bitwise
gates at 8 bits each (six columns × eight layers = 48 two-input units, matching its 96
levers and 144 lamps), `build-00` is the brute-force ALU (full-width distribution rails
into ~8 parallel units, 474 repeaters of cancel tower), and `build-17` is a single AND
gate. The rest group into RCA-based ALU stages, plain carry-cancel adders, CCA-based
ALUs, and two ALUs carrying an operation-selector port.

See [`alus/IDENTIFICATION.md`](alus/IDENTIFICATION.md). **These are inferences, not
signs** — each carries its confidence and evidence, and ten minutes in-game would
settle them properly.

**`cpu/` is empty, deliberately.** *Computer v2* clusters as one build of
227×136×183 = 5.6M blocks, because the whole machine is electrically connected.
That is the correct result: it is one integrated computer, not separable parts.

Its value was its 113 signs, which gave the real control architecture and are now
folded into `../../redstone-cpu/references/alu.md`:

- Control ROM at z=−24 lists opcodes in order, **confirming NOR=4 and AND=5**
- ALU has **six** control signals, not the five previously documented
- 22 control lines total, including three-way destination and write-back selects

Subsystem coordinates, if you want to extract by hand:

| Subsystem | Region |
|---|---|
| Instruction memory | x −16..47, z −96..−65, y 125..228 |
| Character ROM | x −16..47, z −112..−97, y 137..228 |
| 32×32 screen | x 80..175, z 0..63, y 105..153 |
| Control ROM | x ≈176..190, z −24 |

## A lesson about thresholds

The first pass used a minimum of 20 components per chunk and **badly under-harvested
the small-build worlds** — Logic Gates found 3 builds, Latches 3. A logic gate is a
torch and some dust, perhaps 10 components. Re-running those with `--min 4` gave
**12 and 8** respectively, and the latches re-run picked up 10 sign labels that the
first pass missed entirely.

If a world returns implausibly few builds, lower the threshold before concluding it
is sparse.

## Still to do

- **Identify the unlabelled builds** — 152 of them. Best done in-game, not by heuristic.
- **Record I/O port maps.** The blocker for programmatic wiring: each primitive needs
  its input/output block positions captured. The `[1][2][4]…[128]` bit signs in the
  source worlds give bit ordering and are the way in.
- **Nothing has been pasted back into Minecraft and tested.** Block-level fidelity is
  verified; in-world behaviour is not.

## Regenerating

```bash
../.venv/bin/python ../harvest.py "LRR Addition" primitives/addition
../.venv/bin/python ../harvest.py "LRR Logic Gates" primitives/gates --min 4
../.venv/bin/python ../profile.py primitives
```
