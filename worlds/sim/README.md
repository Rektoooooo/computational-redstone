# Redstone simulator

A simulator for the **computational subset** of redstone — dust, repeater, comparator,
torch, lever, redstone block, lamp. Pistons, observers, 0-tick pulses and
quasi-connectivity are deliberately out, because computational redstone avoids them by
construction, and that restriction is what makes this subset deterministic enough to
simulate at all.

It exists to close a feedback loop: without it, an extracted build can be described but
not *checked*, and structural guesses about what a circuit does have already been wrong
twice.

## Status

**Steady-state solving works.** Measured against the saved state of 175 real builds:

| | agreement | was |
|---|---|---|
| **overall** | **92.23%** (214,352 / 232,399 blocks) | 88.71% |
| dust | 89.91% | 88.79% |
| repeater | 96.88% | 92.06% |
| torch | 98.03% | 92.63% |
| comparator | 93.37% | 82.64% |
| lamp | 95.14% | 69.66% |

The tick loop is not built yet.

`was` is the state before the point-source and container-read fixes below. **Dust is
now the largest gap by a wide margin** — 15,252 of the 18,047 remaining wrong blocks.

```
python -m sim.tests.test_units          # 13 hand-built micro-circuits
python -m sim.oracle primitives         # per-block diff against 173 real builds
```

## How it works

Three passes, exploiting one structural fact:

> Strong power comes only from components. Weak power comes only from dust.
> A weakly powered block cannot power dust.

Strong power therefore never originates from dust, so dust power and block power are
**not mutually recursive**. That allows a direct solve rather than whole-grid relaxation:

1. **strong block power** — from component outputs only
2. **dust field** — Dijkstra from sources and strongly powered blocks, −1 per dust, max wins
3. **weak block power** — from dust; only feeds mechanisms and diodes facing away

Component outputs are an *input* to the solver, evaluated separately against the field
it produces. That separation is what lets a bistable circuit exist: an SR latch's state
is history, not a function of the current field.

Dust connection shape is read from the saved blockstate (`north/east/south/west`), so
Minecraft's connection logic is not reimplemented — only how power flows along
connections that already exist.

## The oracle

Extracted `.litematic` files preserve **live circuit state** — dust power levels,
repeater/comparator powered flags, lamp lit flags. Every build is a snapshot of a real
settled Minecraft circuit, giving ~170,000 blocks of free ground truth.

The test is framed as a **fixed-point check** — seed from the saved state, settle,
verify it stays there — not "reproduce from scratch". A bistable circuit has more than
one valid resting state, so asking whether the saved state is *stable* under the model
is both fair and strong.

## Checking against the game's own rules

The first three bugs were found from data alone. The next three were found by pulling
the 1.18.2 client and its official mappings, remapping and decompiling the ten
redstone classes, and reading what the game actually does.

That reference lives **outside this repository** — Mojang's code is not ours to
redistribute, so nothing from it is committed here. Only the rules are, in our own
words. To rebuild it, take the 1.18.2 entry from Mojang's public version manifest,
download `client.jar` and `client_mappings`, convert the ProGuard mappings to TSRG,
remap with SpecialSource and decompile with Vineflower.

It settled three things that had been argued from the wiki rather than checked, and
it will matter more for the tick loop, where exact scheduling and priority semantics
decide the answer.

## Six bugs the oracle caught

Worth recording, because none would have been found by reading code or by the
hand-written unit tests.

**1. `facing` on a diode points at the INPUT, not the output.** Minecraft's `DiodeBlock`
reads its signal from `pos.relative(facing)` and outputs from the opposite side. Having
it backwards silently reversed every repeater and comparator in the library.
**72.7% → 94.1%** on the sample.

The unit tests did not catch this: the fixtures were written from the same wrong
assumption as the code, so they agreed with each other. Only real-world data disagreed.

**2. Extraction dropped container contents.** `region.tile_entities` came out empty, so
every signal-strength barrel read as empty — and 3737 comparators take their rear input
from a barrel, 87% of which were wrong. Recovered from the source worlds with
`../containers.py`. Comparators **39.6% → 82.3%**.

**3. Dust only activates a mechanism it points at.** Lamps were being lit by any
adjacent powered dust, including dust merely running past. This lifted lamps from 65%
to 92% **on the arithmetic builds**, but did nothing library-wide — the display worlds
were failing for a different reason, which turned out to be the next bug.

**4. Nothing fed a diode or a lamp from a torch, a lever or a button.** `input_from`
had cases for dust, redstone blocks and diodes, then fell through to `return 0`, so a
repeater sitting directly against a torch read as unpowered — and 1799 diodes in the
library sit against one. On a lamp screen the driver torch stays lit, so every lamp
stays on: `displays` agreed on 28% of its lamps and one build lit all 256 of them.
`eval_lamp` had the same hole for levers, which are mounted straight onto lamps 1311
times. Lamps **69.7% → 95.0%**, torches **92.6% → 98.0%**.

Found by splitting mismatches by direction — 2321 over-lit against 280 under-lit says
spurious source, not missing one — then correlating against neighbouring block types
and printing a slice. `lampdiag.py` and `probe_lamp.py` do those two steps.

**5. A lever strongly powers only the block it is mounted on.** It was strongly
powering all six neighbours, which let a lever start a fresh dust run from a block it
merely sat beside.

**6. A comparator reads a container THROUGH a solid block.** If the block behind it is
a full conductor and the reading is under 15, it looks one step further for a
container and takes that instead. Keeping a signal-strength barrel one block back,
out of the wiring, is a normal thing to build, and those comparators were reading
whatever power the block in between happened to carry. Comparators **83.5% → 93.4%**.

## A correction to the skill library

Building this surfaced an error in `redstone-fundamentals`: it claimed a weakly powered
block leaves an attached torch lit. That is **Bedrock** behaviour. In Java, a torch is
off whenever its support carries any power, weak or strong — weak vs strong only decides
whether a block can start a new dust run. Corrected.

## Known gaps

- **No tick loop.** Steady state only; sequential timing is unbuilt.
- **Dust at 89.91% is now the largest gap** — 15,252 of the 18,047 remaining wrong
  blocks, simply because dust is two thirds of the library. The errors run 4:1
  **over**-powered (12,158 against 3,094), so this is a spurious connection rather
  than a missing source, and the commonest neighbour of a wrong dust by far is
  stained glass — the glass towers. The prime suspect is `dust_links`, which follows a
  connection one level DOWN for any side that is not `none`. Vanilla only steps down
  when the block in between does not occlude, so the solver is probably carrying power
  across shortcuts that do not exist. Not yet confirmed.
- **Residual disagreement in comparator-heavy CCA builds**, where precise signal
  levels compound: one wrong level corrupts everything downstream.
- **Comparator output level is not recorded** in the schematic, only powered/not, so
  levels must be re-derived by settling.
- 22 of 195 builds skipped as too large.
- Torch burnout not modelled.

## Files

| File | Role |
|---|---|
| `grid.py` | load a `.litematic`, classify blocks, attach container levels |
| `power.py` | the three-pass steady-state solver |
| `components.py` | torch / repeater / comparator / lamp evaluation |
| `engine.py` | public API — `Sim.from_file`, `set_lever`, `settle`, `lamp_states` |
| `oracle.py` | validation against the saved state of the whole library |
| `lampdiag.py` | lamp mismatches split by direction and correlated with neighbours |
| `probe_lamp.py` | a 2D slice around one cell, showing computed against saved |
| `tests/test_units.py` | hand-built micro-circuits |
