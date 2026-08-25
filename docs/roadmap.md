# Roadmap — towards generating builds

The goal: given a task in words — *"an 8-bit sum calculator with a decimal display"* —
produce a `.litematic` that works when pasted into Minecraft.

## Where this stands

`BUILD-PIPELINE-RESEARCH.md` framed it as three problems: delivery, generation, and
verification, with **verification as the crux**. That judgement has held up, and
verification is now the part that is finished.

| stage | state |
|---|---|
| emit a `.litematic` | **done** — blocks, properties, signs, container contents all round-trip |
| simulate and check | **done** — 97.59% per-block, tick loop, seven in-game confirmations |
| component library | **partly** — 195 extracted, ~48 named by their author's signs, 5 ALUs driven |
| **place and route** | **not started** — this is the blocker |
| timing alignment | **not started** — the tick model exists, no tooling uses it |
| spec → design | **not started** |

Everything above the blocker is proven. Everything below it is unbuilt.

## The thing that makes composition harder than it looks

The extracted ports are **human interfaces, not machine interfaces**.

Every build in this library takes input from **levers** and reports output on **lamps**.
A lever is a hand-operated source and a lamp is a dead end — neither can be wired to
anything. Two components cannot be connected by joining a lamp to a lever, because
nothing flows between them.

Composition therefore needs a conversion step at every join:

- **at the source** — the output lamp is only an indicator. The real signal is whatever
  drives it, and that is what must be tapped.
- **at the sink** — the input lever must be removed and replaced by something that
  delivers the same power to the block the lever was feeding.

This is the actual first problem, ahead of any routing. It is also why `portmap.py`
finding "8 levers here, 9 lamps there" was necessary but not sufficient: it located the
ports without describing how to *drive* them.

## Milestones

### M1 — join two components and have it work — **DONE**

Two 8-bit adders chained into `(A + B) + C`. Verified over 512 bus cases and 517
arithmetic cases, then pasted and confirmed in game: `(37 + 91) + 64 = 192`.

`pipeline/compose.py` does the work — placement, port conversion, a coloured bus, and
both a collision check and a structural check.

Two things it taught, beyond proving composition works:

- **Ports need converting, not connecting.** The tap has to be a repeater, because the
  block driving an output lamp is only ever *weakly* powered — at levels as low as 1,
  which dust cannot pick up at all. Measured, not assumed.
- **The simulator models signal, not physics.** The first version passed all 1029 cases
  with sixteen repeaters floating in mid-air, and fell apart on paste. A composed build
  now gets a structural check as well as a behavioural one.

### M2 — route around obstacles — **DONE**

The adder was inside-out for whoever used it: inputs on the west face, sum lamps on the
east, so you set the numbers and then walked around 517 blocks to read the answer. All
eight bits are now routed round to the front, giving
`(Input A) (Input B) (Output)` side by side.

517 cases, 0 wrong, and confirmed in game. `route_plane()` and `lay_route()` in
`pipeline/compose.py`.

What made it tractable: **each bit routes inside its own horizontal plane**, so the
search is two-dimensional. The bits sit 2 apart in `y`, and a support block over a live
wire does not leak — simulated directly before relying on it — so the eight lines cannot
reach each other. In any one plane the adder occupies only ~26 cells, leaving plenty of
room to go around.

The bug worth remembering: the drive repeater's facing was **hardcoded** to east, on the
assumption the wire would arrive from the east. The router approached from the north
instead, and the signal travelled the entire route and then died at the last block. A
repeater takes its input from one specific side, so the arrival direction is not
something a router may choose freely. Fixed by routing to the cell east of the repeater
rather than to the repeater itself — making the approach a fact rather than a hope.

### M3 — timing alignment — **DONE**

Split in two, because the ruler had to be checked before it was used.

**M3.1 — verify the clock.** The tick model had never been compared to the game. Measured
with `/tick freeze` and `/tick step`: repeater delays, chained delays and the
setting-to-ticks mapping all exact. It also found a rule the simulator was missing
entirely — a lamp lights instantly but waits **4 game ticks** to go dark, which a
steady-state check cannot see by construction.

**M3.2 — align a skewed bus.** `arrival_ticks()`, `settle_profile()` and `align()` in
`pipeline/compose.py`. A staggered readout with 0/1/2 repeaters per route skewed by
4 ticks; alignment flattened it to 0 at no block cost, by turning up delay settings on
repeaters already in place. Correctness unchanged — 512 cases still exact.

The distinction that came out of it is in `docs/timing.md`: **structural** skew is fixed
and paddable, **data-dependent** skew from a carry chain is not, and the only answer
there is to wait for the worst case.

### M4 — spec to build — **next**

Choose components for a described task, lay them out, wire them, verify. Only sensible
once M1–M3 are real.

## What would make M4 easier, done early

- **Drive the rest of the library.** 13 of 18 ALU builds are still guesses, and the
  displays and sequential worlds have barely been touched. A component whose behaviour
  is unknown cannot be chosen for a task.
- **Record how to drive each port**, not just where it is — which block a lever feeds,
  which block drives a lamp. That is the conversion step above, and it belongs in the
  manifest next to the port map.

## The one advantage this project has

Every attempt is checkable before it is pasted. A wrong route, a mistimed bus, a
misidentified port — all show up in the simulator, against a model that has been
confirmed against the real game seven times. The loop is: compose, simulate, fix, and
only then hand it over.
