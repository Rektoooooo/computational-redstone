# Checking against the real game

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
