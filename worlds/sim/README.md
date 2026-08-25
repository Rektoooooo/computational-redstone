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

**Steady-state solving works.** Measured against the saved state of 173 real builds:

| | agreement |
|---|---|
| **overall** | **88.09%** (149,573 / 169,790 blocks) |
| dust | 89.67% |
| repeater | 89.95% |
| torch | 88.88% |
| comparator | 82.33% |
| lamp | 65.42% |

**68 of 173 builds reproduce at exactly 100%.** The tick loop is not built yet.

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

## Three bugs the oracle caught

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
to 92% **on the arithmetic builds** — but library-wide lamps are still 65%, so the
display-heavy worlds are failing for a different, unfound reason. That is the first
thing to chase next.

## A correction to the skill library

Building this surfaced an error in `redstone-fundamentals`: it claimed a weakly powered
block leaves an attached torch lit. That is **Bedrock** behaviour. In Java, a torch is
off whenever its support carries any power, weak or strong — weak vs strong only decides
whether a block can start a new dust run. Corrected.

## Known gaps

- **No tick loop.** Steady state only; sequential timing is unbuilt.
- **Lamps at 65% library-wide** are the largest single gap, concentrated in the
  display worlds. The pointing-direction fix did not move them, so the cause is
  something else — likely lamps driven through blocks or by adjacent lamps.
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
| `tests/test_units.py` | hand-built micro-circuits |
