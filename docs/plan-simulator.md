# Redstone simulator for the computational subset

## Context

The project has knowledge (an 8-skill library from 32 transcripts), data (195 components
extracted from 19 published worlds, with port maps), and rendering (layer plates with
real textures). What it does not have is a **feedback loop**.

Concretely: I cannot tell what a circuit does by looking at it, and I cannot check
myself. That has already produced two wrong calls — a comparator array read as a
multiplexer that was actually a magnitude comparator, and a structural classifier that
labelled the CLE adder a "26-output decoder". Both were caught by something external.
Of the 195 extracted builds, 152 remain unlabelled and the 18 ALU builds carry no signs
at all, so their identifications are inference stacked on inference.

Every downstream goal — verifying primitives, composing them, generating builds — is
blocked on the same thing: no way to determine whether a circuit works.

A simulator closes that loop. It turns "probably an AND gate" into a truth table, makes
composition checkable, and lets behaviour be observed rather than read about.

### Why this is tractable here

Computational redstone deliberately restricts itself to **dust, repeater, comparator and
torch** — no pistons, observers, 0-tick tricks or quasi-connectivity — precisely because
that subset is deterministic and position-independent. A simulator for it is achievable
where a general Minecraft simulator would not be.

### The decisive discovery: the saved state is an oracle

The extracted `.litematic` files preserve **live circuit state**, not just block layout:

```
dust power levels: {'15': 32, '14': 22, '0': 81}
repeaters: (powered, locked, delay)   comparators: (mode, powered)   lamps: (lit)
levers: (powered)
```

Every build is a snapshot of a real, settled Minecraft circuit. That means the simulator
can be validated **per block, against roughly 100,000 blocks of ground truth**, for free.
This is what turns the project from "write a simulator and hope" into test-driven
development where failures point at a specific coordinate.

---

## Approach

### Core model: solve, don't event-simulate

Do **not** model Minecraft's tick queue, block-update ordering or tile-tick priorities.
That reproduces exactly the locationality and ordering fragility the discipline avoids,
and is very hard to get right.

Instead, exploit a structural fact from the mechanics:

> Strong power comes only from components (lever, button, torch, redstone block, powered
> repeater, powered comparator). Weak power comes only from dust. **A weakly powered
> block cannot power dust.**

Strong power therefore never originates from dust, so **dust power and block power are
not mutually recursive**. The steady state can be solved directly in three passes:

1. **Strong block power** — from components only
2. **Dust power** — Dijkstra-style from sources and strongly powered blocks, decaying 1
   per dust block, taking the max
3. **Weak block power** — from dust; consumed only by mechanisms and by
   repeaters/comparators facing away

Delayed elements (repeater, comparator, torch) are then evaluated against that solved
field. Dust genuinely has zero delay in Minecraft, so solving it to a fixed point within
a tick is faithful rather than an approximation.

### Free simplification

Dust connection shape is **already in the saved data** (`north/east/south/west` each
`none`/`side`/`up`). Minecraft's connection logic does not need reimplementing — only
how power flows along connections that already exist. This removes the single most
error-prone part.

### Build order: steady state first, time second

A settled circuit's resting state needs no timing. So:

- **Steady state** can be built and validated against all 195 builds *before* any tick
  loop exists. This is the bulk of the correctness risk and nearly all of the value.
- **Time** (delays, scheduling, sequential behaviour) is added afterwards, on a
  foundation already proven correct.

---

## Rules to implement

Researched and confirmed against the Minecraft Wiki:

**Strong power** — a power component (lever/button/pressure plate on the block), a
powered repeater's front, a powered comparator's front, a redstone block (every touching
block), a torch to the block **above** it.
A strongly powered block powers adjacent dust including dust on top of and beneath it.

**Weak power** — dust on top of, or pointing into, a conductive block.
A weakly powered block cannot power adjacent dust, but does activate mechanisms and
power repeaters/comparators facing away.

**Dust** — decays 1 per dust block; **no** decay from dust to a block or component.
Connects to dust one block up or down unless an opaque block cuts it. Powers the block
beneath it and blocks it points into. A dot powers only the block under it. A mechanism
is activated only by dust pointing at it or by directionless dust.

**Torch** — off when its attachment block is powered. Lit: **strongly** powers the block
above, **weakly** powers other neighbours, never its attachment block. 1 redstone tick.
Burnout after >8 state changes in 60 game ticks — stub initially, note the omission.

**Repeater** — input from the back; outputs 15 strongly to the block it faces; delay 1–4.
**Locked only by a powered repeater or comparator facing into its side** — no other
source works. While locked the output is frozen entirely.

**Comparator** — rear plus two sides input, front output, 1 redstone tick.
`compare`: `out = rear if (left <= rear and right <= rear) else 0`.
`subtract`: `out = max(0, rear - max(left, right))`.
Side inputs accepted only from dust, redstone block, repeater or comparator — **a
weakly powered block on the side does not feed it**.

**Explicitly out of scope** — pistons, observers, 0-tick pulses, quasi-connectivity,
update suppression, locationality, container comparator reads (barrels). Each is absent
from computational redstone by design and would cost more than it returns.

---

## Files

New package `worlds/sim/`, following the single-purpose-module style of the existing
tools (`extract.py`, `harvest.py`, `portmap.py`, `render_png.py`):

| File | Responsibility |
|---|---|
| `sim/grid.py` | load a `.litematic` into an indexed grid; block classification (conductive / transparent / source / delayed); property access helpers |
| `sim/power.py` | the three-pass steady-state solver: strong block power, dust field, weak block power |
| `sim/components.py` | per-component evaluation — torch, repeater (incl. locking), comparator (both modes) |
| `sim/engine.py` | public API: `load()`, `set_inputs()`, `settle()`, `read_outputs()`; tick loop added in phase 4 |
| `sim/oracle.py` | validation harness: diff solved state against the saved state across the library |
| `sim/tests/test_units.py` | hand-built micro-circuits with known answers |

Reuse rather than re-derive:
- Block properties come straight from `litemapy` `BlockState` (`bs.id`, `bs["facing"]`)
- Input/output positions come from the existing **port maps** already written into every
  `*.manifest.json` by `worlds/portmap.py` (`ports.ports[]`, with `kind` and `positions`)
- `worlds/render_png.py` can render a solved power field for visual debugging by tinting
  dust to its computed level — a solver bug becomes visible rather than abstract

---

## Verification

Three levels, in order. Each must pass before the next is meaningful.

### 1. Units — hand-built micro-circuits
- lit torch inverts its input; unpowered attachment block leaves it lit
- dust decays 15 → 0 across exactly 15 blocks
- repeater restores to 15 and is a one-way diode
- comparator subtract: rear 8, side 3 → 5; rear 3, side 8 → 0
- comparator compare: side equal to rear still passes
- weakly powered block does **not** re-power adjacent dust (the classic gotcha)
- repeater locked by a side repeater ignores its input entirely

### 2. The oracle — all 195 builds
```
python -m sim.oracle worlds/primitives
```
For each build: set levers to their saved states, solve, then diff **every** dust power
level, repeater `powered`, comparator `powered` and lamp `lit` against the saved values.

Report per-build agreement and a global percentage. Expect a small number of legitimate
disagreements (a world saved mid-settle), so the target is **high agreement with
mismatches clustered in a few builds** — not a perfect score. Widespread disagreement
would mean the *model* is wrong, which is precisely the finding worth having.

Mismatches must be reported with coordinates so they can be inspected in a render.

### 3. Behavioural — does it compute the right answer
- `primitives/alus/build-17` — drive its two levers through all four combinations and
  check the output lamp follows **AND**
- `primitives/latches/not-output` — set/reset and confirm the SR latch holds state
- `primitives/addition/3-ticks-8-bit-cca-by-don` — drive both 8-bit input ports from the
  port map with real numbers and check the 9-bit output equals the sum, including carry

Level 3 on the adder is the headline test: if the simulator computes 37 + 91 correctly
from nothing but extracted blocks, both the simulator and the understanding behind it
are validated at once.

### Final check against reality
The user will compare selected results against real Minecraft when back at their machine.
Any divergence there outranks the oracle, since the oracle is a saved snapshot while the
game is the actual authority.
