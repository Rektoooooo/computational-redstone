# Checking against the real game

## Results so far

All nine **passed in Minecraft 1.18.2**. Two corrected labels the project had wrong,
and the last two did not previously exist at all: components composed into a new
device, and then a machine rearranged so its output reads on the same face as its
inputs. This is the first time anything here has been checked against the game
rather than a saved snapshot — an item open since session 2.

| test | predicted | in game |
|---|---|---|
| `decay` | 15, 14, 13, 12, 11, 10, lamp lit | ✅ identical |
| `steps` | lanes 1–3 lit, lane 4 dark at 0 | ✅ identical |
| `alus/build-17` | 3-input XOR, **not** the AND its label claimed | ✅ label corrected |
| `addition/3-ticks-8-bit-cca-by-don` | 37 + 155 = 192 | ✅ identical |
| `comparator` | 8, 8, 0 — reads through stone, not through glass | ✅ identical |
| `alus/build-16` | 4-bit ripple-carry adder, **not** four independent gates | ✅ label corrected |
| `alus/build-13` | 9 − 4 = 5 by two's complement | ✅ identical |
| `m1-two-adders` (**composed**) | (37 + 91) + 64 = 192 | ✅ identical |
| `m2-front-output` (**routed**) | 37 + 91 = 128 with the output moved to the front | ✅ identical |
| `timing` | 8, 16, 24 … 64 ticks | ✅ exact — and **found a missing rule** |

**The adder is the one that matters.** A real mattbatwings circuit, extracted from a
world file, pasted back, and doing correct 8-bit arithmetic — with the simulator
agreeing on both the value and the timing.

It was also an accidentally *better* test than the one designed. The prediction was
written for 37 + 91; the inputs actually set were 37 + 155, one lever off. The machine
produced the right answer for the inputs it was given and the simulator matched them,
which is far stronger than reproducing a pre-computed expectation — there was no way to
tune anything to fit. A bit-ordering error would have shown up as a *permuted* answer,
some other pair of lamps; the correct pair lit instead.

`steps` is the one that carried weight. Lanes 2 and 4 are the same build with the
source at opposite ends, and the same glass block let power climb onto it while
refusing to let it back down. That asymmetry was **derived** by inverting reader-side
logic rather than read off directly, and it underpins the dust fix that moved
agreement from 88.79% to 97.67% — the largest single correction in the project. It
could easily have been backwards. It is not.


## How this works

The oracle checks the simulator against **saved** state — real circuits, but frozen
ones. That is a strong test and it is not the same as the game. The game is the
authority, and until these tests existed nothing here had ever been pasted back and
run.

The constructed schematics are deliberately tiny, so that a disagreement points at one
rule rather than at a haystack. Extracted builds are driven whole, where the question
is not a single rule but whether the parts compose.

```bash
python3 verify/make_test_schematic.py decay     # build it
python3 verify/predict.py verify/decay.litematic # what we expect it to do
```

**Write the prediction down before looking at the game.** A model consulted after the
fact always seems to agree.

## Test 6 — `timing` — the clock itself

Everything else here checks what a circuit settles TO. This checks **when**, which has
never been measured against the game at all.

The tick loop has 14 unit tests, but they only prove it is self-consistent — they would
pass just as happily if the whole model were off by a factor of two. The one piece of
indirect evidence is the CCA adder settling in 3 redstone ticks against a build named
*"3 ticks 8-bit CCA"*, whose numbers never went into the model. Good, but inferred from
a label rather than measured.

This matters now because M3.2 pads a skewed bus using these numbers. A wrong ruler would
produce a wrong alignment that then verifies against itself.

Two levers, two independent questions. 20 game ticks is one second.

**Part A — does delay add up?** Lane `i` has `i+1` repeaters, all at delay 4.

| lane | repeaters | predicted |
|---|---|---|
| A0 | 1 | 8 ticks (0.4 s) |
| A1 | 2 | 16 |
| A2 | 3 | 24 |
| A3 | 4 | 32 |
| A4 | 5 | 40 |
| A5 | 6 | 48 |
| A6 | 7 | 56 |
| A7 | 8 | **64 ticks (3.2 s)** |

**Part B — does the delay SETTING mean what we think?** Eight repeaters each, at
settings 1–4. This is the one M3.2 depends on.

| lane | setting | predicted |
|---|---|---|
| B d1 | 1 | 16 ticks (0.8 s) |
| B d2 | 2 | 32 (1.6 s) |
| B d3 | 3 | 48 (2.4 s) |
| B d4 | 4 | **64 (3.2 s)** |

**Result: the clock is right.** Measured exactly with `/tick freeze` + `/tick step`
rather than by eye, which turned a rough check into a precise one.

| | predicted | measured |
|---|---|---|
| A0 … A7 | 8, 16, 24 … 64 | **9, 17, 25 … 65** |
| B d1 … d4 | 16, 32, 48, 64 | **17, 33, 49, 65** |

Three things confirmed exactly: **delay setting N is 2N game ticks** (B's spacing is 16
for eight delay-1 repeaters), **delays add linearly** (A's spacing is 8, eight times
over), and the **order** is strictly correct.

The sharpest data point was B d1: seven of eight repeaters powered at step 15, still
seven at 16, lamp at 17 — the chain advancing repeater by repeater, one tick later than
predicted.

**Every lane is exactly one tick late**, systematically and never variably. The lever is
flipped while the game is frozen, so the neighbour update that schedules the first
repeater is processed on the first stepped tick rather than instantly, and the chain
starts one tick after the simulator's `time = 0`.

That offset does **not** affect alignment, because skew is a difference between lanes and
a constant cancels. It would have mattered if the spacing varied, or if the whole thing
came out at half or double — either of which would have meant the tick model was wrong
and M3.2 was building on sand.

## Test 5 — `comparator`

Three lanes feeding a comparator from a barrel of 14 stacks (strength 8), identical
but for the block between barrel and comparator.

| lane | between | dust after the comparator | lamp |
|---|---|---|---|
| 1 | nothing | **8, 7, 6** | lit |
| 2 | stone | **8, 7, 6** | lit |
| 3 | **glass** | **0, 0, 0** | **dark** |

**Result: passed exactly.** Confirmed in game.

Lanes 1 and 2 only show that a comparator can reach a barrel through a block. Lane 3
shows *why*: it looks one step further **only when the block between is a genuine
conductor**, and glass never is. Without lane 3 the rule would be indistinguishable
from "a comparator sees two blocks back".

This was the largest fix still resting on a reading of the game's source rather than on
evidence — it moved comparators from 83.5% to 93.4%.

The barrels and the lane signs both carry real block entity data, which is what the
sign work made possible. The F3 panel while pointing at a comparator showed
`Schematic: powered: false` against `Client: powered: true` — the schematic stores the
cold state it was written with, and the live block turned on from the barrel, so
nothing was pre-baked.

## Test 4 — `addition/3-ticks-8-bit-cca-by-don`

An extracted build rather than a constructed one: 517 blocks, 17 levers, 25 lamps.

Two 8-bit input ports of levers, a 9-lamp output port, and a lone wall lever outside
both ports which turns out to be the **carry-in** — it adds exactly 1 to every sum,
which is what two's-complement subtraction needs.

Bit order is **measured, not inferred**: `signs.py` recovers the author's own
`1 2 4 … 128` signs with their coordinates, and they run bottom-up on both the input
and output ports.

**Result: 37 + 155 = 192, correct in game**, lamps 7 and 8 lit, carry-out off.

Two things make this the strongest test in the project:

- **The timing matched the author's own labels.** Sums settle in 6 game ticks and
  carry-out in 8 — 3 and 4 redstone ticks, against a build named *"3 ticks 8-bit CCA by
  Don"* whose carry-out sign reads *"COUT (4 ticks)"*. Those numbers were never given to
  the model. A steady-state solver cannot fake that; only a tick loop can produce it.
- **The inputs were not the ones predicted.** The prediction was written for 37 + 91;
  one lever landed a row off, making it 37 + 155. The machine gave the right answer for
  the inputs it actually had and the simulator matched them, which is worth more than
  reproducing a pre-computed expectation — nothing could have been tuned to fit. A
  bit-ordering error would have lit some *other* pair of lamps.

## Test 3 — `alus/build-17`

Driven through its truth table. It is a **3-input XOR (odd parity)**, not the *"single
AND gate"* its manifest claimed at confidence `high`. Both inputs on gives output off,
which an AND gate cannot do. See `worlds/primitives/alus/IDENTIFICATION.md`.

## Test 2 — `steps`

Four lanes, differing in only two things: whether the block the dust steps over is
**stone** or **glass**, and whether the source is **below** the step or **above** it.
Each ends in a lamp.

| lane | step | source | reader dust | lamp |
|---|---|---|---|---|
| 1 | stone | below | 13 | lit |
| 2 | glass | below | 13 | lit |
| 3 | stone | above | 13 | lit |
| 4 | **glass** | **above** | **0** | **dark** |

The obvious guess is that a step either works or it does not, so glass ought to behave
the same in lanes 2 and 4. It does not:

- reading a source **one level down** needs the block between to be a **non-conductor**
- reading a source **one level up** needs it to **be** a conductor

Glass is never a conductor, so power climbs onto a glass step but will not come back
down off one. Lanes 1–3 are controls; they also prove the paste fired block updates.

**Result: passed exactly.** Confirmed in game.

## Test 1 — `decay`

A redstone block, six dust running east, and a lamp. 8 × 2 × 1, sixteen blocks.

Dust is written with `power=0` on purpose. If the levels were baked in, the game would
just show us what we put there; starting cold makes the numbers a real prediction.

**Predicted:**

| position | block | expected |
|---|---|---|
| (1,1,0) | dust | power **15** |
| (2,1,0) | dust | power **14** |
| (3,1,0) | dust | power **13** |
| (4,1,0) | dust | power **12** |
| (5,1,0) | dust | power **11** |
| (6,1,0) | dust | power **10** |
| (7,1,0) | lamp | **lit** |

Positions are relative to the schematic corner, running east from the redstone block.

What each part of this actually tests:

- **15 at the first dust** — a redstone block hands out full strength to dust touching it
- **one lost per block** — the decay rule, the single most load-bearing thing in the solver
- **the lamp lit** — and this one is subtler than it looks. Dust does *not* connect to a
  lamp, because a lamp is not a signal source. It reaches the lamp only because a wire
  with nothing to its north or south straightens itself into a line, which gives the
  last dust an eastward connection. If that rule were wrong the lamp would sit dark
  with power 10 right next to it.

**Result: passed exactly.** Confirmed in game.

## Getting it into the world

The game runs through **ModrinthApp**, not the vanilla launcher, so schematics belong
in the instance:

```bash
cp verify/decay.litematic \
   ~/Library/Application\ Support/ModrinthApp/profiles/Redstone/schematics/
```

Then, in a creative flat world:

1. `M` → **Load Schematics** → pick it → **Load Schematic**, creating a placement
2. `M` → **Schematic Placements** → select the placement, so the HUD names it rather
   than showing `<none>`; the paste acts on the *selected* placement
3. Hold the tool item (a stick) and **Left Ctrl + scroll** to reach the
   **Paste Schematic in World** mode
4. Press the **Execute Operation** key

**`executeOperation` ships unbound**, which makes pasting look broken when nothing is
wrong. Bind it under `M` → **Configuration Menu** → **Hotkeys**. Those defaults are
readable rather than guessable: `javap -c` on
`fi/dy/masa/litematica/config/Hotkeys.class` inside the mod jar pairs every hotkey
with its default.

**Under ~50 blocks, skip all of this and use `to_commands.py`.** `/setblock` fires
block updates; a paste does not always, and an un-updated redstone paste reads as all
zeros and looks exactly like a broken model.

## Reading the answer

Press **F3** and look at each dust. The *Targeted Block* panel on the right lists the
blockstate, including `power`. That is the number to compare.

**If every dust reads 0**, the paste placed blocks without triggering a redstone
update. Break the redstone block and put it back — that forces one.

## What a disagreement means

The game wins. Any divergence is a bug in the simulator, and a divergence here would
be a big one, because these are the rules everything else is built on. Record the
actual values, then work backwards from the first position that disagrees — the ones
after it are just consequences.
