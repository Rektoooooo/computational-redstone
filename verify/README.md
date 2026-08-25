# Checking against the real game

## Results so far

Both tests **passed in Minecraft 1.18.2, exactly as predicted**. This is the first time
anything in this project has been checked against the game rather than a saved
snapshot — an item open since session 2.

| test | predicted | in game |
|---|---|---|
| `decay` | 15, 14, 13, 12, 11, 10, lamp lit | ✅ identical |
| `steps` | lanes 1–3 lit, lane 4 dark at 0 | ✅ identical |

`steps` is the one that carried weight. Lanes 2 and 4 are the same build with the
source at opposite ends, and the same glass block let power climb onto it while
refusing to let it back down. That asymmetry was **derived** by inverting reader-side
logic rather than read off directly, and it underpins the dust fix that moved
agreement from 88.79% to 97.67% — the largest single correction in the project. It
could easily have been backwards. It is not.


Everything the simulator knows has been checked against **saved** state — real
circuits, but frozen ones. The oracle is a snapshot; the game is the authority. Nothing
from this project had ever been pasted back into Minecraft and run.

These schematics are deliberately tiny, so that a disagreement points at one rule
rather than at a haystack.

```bash
python3 verify/make_test_schematic.py decay     # build it
python3 verify/predict.py verify/decay.litematic # what we expect it to do
```

**Write the prediction down before looking at the game.** A model consulted after the
fact always seems to agree.

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

Schematics live in `.minecraft/schematics/`. On this Mac:

```bash
cp verify/decay.litematic ~/Library/Application\ Support/minecraft/schematics/
```

Then, in a creative flat world:

1. `M` opens the Litematica menu (default key)
2. **Load Schematics** → pick `decay` → **Load Schematic**, which creates a placement
3. **Schematic Placements** → move it where you want it
4. Paste it into the world — this needs creative mode. The paste operation lives under
   the Litematica tool/operation modes; the exact key depends on your config

If the paste fights you, **just build it by hand** — it is sixteen blocks and takes
about a minute. The point is the redstone behaviour, not the file format.

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
