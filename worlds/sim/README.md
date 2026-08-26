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
| **overall** | **97.59%** (226,794 / 232,399 blocks) | 88.71% |
| dust | 97.67% | 88.79% |
| repeater | 97.83% | 92.06% |
| torch | 98.49% | 92.63% |
| comparator | 94.44% | 82.64% |
| lamp | 96.72% | 69.66% |

**153 of 175 builds reproduce at exactly 100%**, up from 68.

`was` is the state before the four fixes below.

**The tick loop is built.** Steady state answers "where does this rest"; the tick loop
answers "what does it do", which is what sequential circuits need.

```
python -m sim.tests.test_units          # 28 steady-state micro-circuits
python -m sim.tests.test_ticks          # 14 timing micro-circuits
python -m sim.oracle primitives         # per-block diff against 175 real builds
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

Dust-to-dust power flow is worked out from **block occupancy**, not from the wire's
saved `north/east/south/west` shape. Those properties say how the wire is drawn and
which mechanisms it feeds, and reading them to decide power flow was bug 7 below. The
shape is still what decides which blocks and mechanisms a dust *feeds*.

## Time

Steady state answers "where does this rest". The tick loop answers "what does it do",
which is what anything sequential needs.

Dust is instantaneous and never schedules, so the solver above is reused unchanged as
the "settle the field" step. Only the stateful components — torch, repeater,
comparator — are scheduled. Each game tick:

1. drain everything due now, in order, re-solving the field before each one, because
   an earlier component in the same drain can change what a later one reads
2. re-solve
3. queue any component whose target now differs from its state, unless one is pending

Three things fix the order, and all three matter:

| | |
|---|---|
| **trigger tick** | one redstone tick is two game ticks; everything here counts in game ticks |
| **priority** | which of several due on the same tick goes first |
| **insertion order** | the tie-break within a priority |

A diode goes to the front of the queue when the block it outputs into is another diode
*not* pointing back at it — the "repeater facing into another's side" case. That is
what makes diode ordering deterministic instead of dependent on update order. Otherwise
one turning off outranks one turning on. Delays are `delay × 2` game ticks for a
repeater, always 2 for a comparator and a torch.

The other load-bearing rule is that a component with a tick already pending does not
get another, so two neighbours changing at once cannot make one repeater fire twice.

**It resolved three builds that steady state could not.** Of the four builds where
`settle()` never converges, three are bistable latches that simply come to rest once
time exists. The fourth, `displays/convert`, genuinely clocks — 13 repeaters and 10
torches toggling — which is what an animation driver should do.

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

## Seven bugs the oracle caught

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

**7. Dust power flow follows block occupancy, not the saved wire shape.** `dust_links`
read the `north/east/south/west` properties and, for any side that was not `none`,
also followed a step DOWN. Those properties describe how the wire is *drawn* and which
mechanisms it feeds; the game works out neighbour-to-neighbour power separately, from
what is physically in the way. The extra downward steps carried power across gaps that
do not conduct — errors ran 4:1 over-powered, concentrated around the glass towers.

Rewritten to the real rule. Per horizontal direction, from the reader's side, the
deciding block is the one beside the reader, in between the two:

| source | condition on the block between |
|---|---|
| same level | none |
| one level UP | must **be** a conductor — the signal climbs it — and nothing solid may cap the reader |
| one level DOWN | must **not** be a conductor |

The two diagonal cases demand the opposite thing of that block, so the relation is
asymmetric: a diagonal step legal one way need not be legal back. Dust **88.8% →
97.7%**, and overall **92.2% → 97.6%** — dust is two thirds of every build, so it
carries everything else with it.

## An eighth bug — found by measuring, not by the oracle

**A lamp is not symmetric in time.** It lights the instant it is powered, but when power
goes away it waits **4 game ticks** before going dark, re-checking on arrival so a signal
returning inside that window leaves it lit. Deliberate anti-flicker behaviour.

The oracle could never have caught this: the steady state is identical either way. It
took stepping the real game a tick at a time — all eight repeaters in a chain dark, the
lamp still lit, four ticks later it goes out. Modelled now, with the on/off asymmetry
and the re-check.

Two smaller mistakes surfaced while implementing it, both from `prime()`:

- it re-seeded lamp state on every call, and `set_lever` re-primes — so flipping an input
  wiped any lamp mid-way through its wait and the delay silently vanished
- then, seeding once, the wait started on the first tick rather than at the moment power
  was lost, putting everything one tick late

## A correction to the skill library

Building this surfaced an error in `redstone-fundamentals`: it claimed a weakly powered
block leaves an attached torch lit. That is **Bedrock** behaviour. In Java, a torch is
off whenever its support carries any power, weak or strong — weak vs strong only decides
whether a block can start a new dust run. Corrected.

## The blindness that cost a paste

`settle()` recomputes from scratch and iterates to a fixed point, so for a combinational
circuit it reaches the right answer **whatever state it started from**. That is normally
a virtue. It also means the simulator **cannot tell you what a build will do when it is
pasted**, because Minecraft only re-evaluates a component when something pokes it, and a
schematic records a state.

A build can therefore pass every sweep here and be wrong the instant it lands in a world.
It happened: `pipeline/m4-decimal-adder-v1` showed 7 with every lever off, because an
extracted component carried the state its author left it in.

The check is not in the simulator, it is in the generator: `Build.rest()` in
`pipeline/analog.py` settles with nothing switched on and writes that state into every
block, and `Build.stale()` reports any that disagree.

## A circuit we get wrong

`primitives/wiring/build-14` — mattbatwings' **zero-tick 3D crossover**, four bits by four
bits. Driven here, four of its sixteen lamps light regardless of which lever is thrown,
and two inputs never reach their own output.

It uses **no repeaters at all** — only dust, blocks and 3D staggering — so it rests
entirely on diagonal dust behaviour, which is the most intricate rule in the system.
Either `dust_links()` is wrong for some case it uses, or the harvest clipped part of it.
Worth settling either way: **a rule we have wrong there is a rule we have wrong
everywhere.**

## Known gaps

- **The tick loop is unvalidated against real builds.** Its rules are checked against
  the game's own and its micro-circuits pass, but nothing has yet driven a whole
  extracted build through time and compared the result. That is the next thing: an AND
  truth table through `alus/build-17`, then 37+91 through the CCA adder.
- **Only hand-built circuits have been checked in the actual game**, not extracted
  builds. Two so far, both passing exactly — see [`../../verify/`](../../verify/). One
  of them confirmed the asymmetric dust-stepping rule directly, which matters because
  that rule was derived rather than read off and the largest correction here rests on
  it.
- **Torch burnout is not modelled** — 8 toggles inside a 60-tick window burns a torch
  out for 160 ticks. Only reachable now that time exists, and only bites fast clocks.
- **Comparators are the weakest category at 94.44%**, and the schematic records only
  powered/not, never the output LEVEL, so levels have to be re-derived by settling.
  In comparator-heavy builds one wrong level corrupts everything downstream.
- **Four builds oscillate** rather than settling. Worth a look: some will be genuine
  clocks, which cannot have a steady state and are not failures.
- 20 of 195 builds skipped as too large.
- Torch burnout not modelled.
- The remaining disagreement is concentrated rather than spread — 153 of 175 builds
  are exact, so the residue sits in a handful of builds. `displays/blank`,
  `displays/build-02` and `cpu-ep07-branching/build-07` are the worst.
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
| `engine.py` | public API — `Sim.from_file`, `set_lever`, `settle`, `tick`, `lamp_states` |
| `ticks.py` | the scheduled-tick queue: trigger tick, priority, insertion order |
| `oracle.py` | validation against the saved state of the whole library |
| `lampdiag.py` | lamp mismatches split by direction and correlated with neighbours |
| `probe_lamp.py` | a 2D slice around one cell, showing computed against saved |
| `tests/test_units.py` | hand-built steady-state micro-circuits |
| `tests/test_ticks.py` | hand-built timing micro-circuits |
