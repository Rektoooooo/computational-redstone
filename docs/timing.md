# Redstone timing reference

Timing is most of computational redstone, and it is the part where a wrong number does
not look wrong — a circuit with a mistimed bus computes confident nonsense. This is the
concrete data, with the evidence for each line stated, because a wiki claim has already
misled this project once.

## Evidence levels used below

| mark | meaning |
|---|---|
| **measured** | observed in Minecraft 1.18.2 with `/tick freeze` + `/tick step` |
| **source** | read from the decompiled 1.18.2 client (see `CLAUDE.md`) |
| **wiki** | community documentation, agreeing with the above |

Nothing here rests on the wiki alone. The one rule this project got wrong early — "a
weakly powered block leaves a torch lit" — came from applying Bedrock behaviour to Java,
which is exactly the failure mode cross-checking prevents.

## The units

**20 game ticks per second. 1 redstone tick = 2 game ticks.**

Everything in this repository counts in **game ticks**, because that is what the game
schedules in and the factor of two is an easy thing to lose.

## Component delays

| component | delay | evidence |
|---|---|---|
| **redstone dust** | none — propagates within the tick | source: never schedules |
| **repeater** | `setting × 2` game ticks → **2, 4, 6, 8** | source (`DELAY * 2`), **measured** |
| **comparator** | always **2** game ticks, both directions | source (returns 2), wiki |
| **redstone torch** | **2** game ticks | source (`scheduleTick(..., 2)`) |
| **redstone lamp ON** | **0** — immediate | source, **measured** |
| **redstone lamp OFF** | **4** game ticks | source, **measured** |

### The lamp is the trap

A lamp lights the instant it is powered and waits **4 game ticks** before going dark,
re-checking when the wait expires — so a signal returning inside the window leaves it
lit at all. That is deliberate anti-flicker behaviour.

This matters far more than it looks, because **a steady-state check cannot see it**: the
settled picture is identical either way. It went unnoticed across 175 builds and nine
in-game tests, and only appeared when someone stepped the game one tick at a time and
watched a lamp stay lit with every repeater behind it already dark.

If you measure a circuit's output by its lamps, you are reading a value that is **up to
4 ticks stale on the falling edge only**.

## Ordering within a tick

Several components can be due on the same tick. Three things decide who goes first, and
all three matter (source: `ScheduledTick`):

1. **trigger tick**
2. **priority** — lower runs first
3. **insertion order** — the tie-break

Diodes choose their priority as follows (source: `DiodeBlock`):

| situation | priority |
|---|---|
| the block it outputs into is a diode **not** pointing back at it | highest |
| otherwise, currently powered (so turning **off**) | higher |
| otherwise (turning **on**) | high |
| torches | normal |

That first case is the "repeater facing into another's side" rule, and it is what makes
diode ordering deterministic rather than dependent on update order.

**The pending guard:** a component that already has a tick scheduled does not get
another. Without it, two neighbours changing in the same tick would schedule the same
repeater twice and it would fire twice.

## A repeater stretches a pulse shorter than its own delay

**source, and confirmed by community documentation.** When a repeater's scheduled tick
arrives and it is currently off, it turns on **unconditionally** — even if the input that
scheduled it has already gone away — and then schedules its own turn-off one delay later.

So a **1-tick pulse through a delay-4 repeater comes out 8 game ticks wide**. A repeater
set to 2–4 also swallows shorter *off*-pulses the same way.

This has a direct consequence for padding a bus: **one 4-tick repeater is not equivalent
to four 1-tick repeaters.** They delay a steady signal identically, but the single slow
repeater distorts any pulse narrower than itself. Where pulse width has to survive, pad
with chained short repeaters rather than by turning one up.

The simulator originally re-checked the input when the tick fired, which is the obvious
implementation and is wrong — short pulses vanished entirely, since they scheduled a
turn-on and then the input disappeared before it arrived. Every clock and edge detector
depends on this behaviour. Fixed and tested.

## Repeater locking, as a way to release a whole bus at once

Community practice, worth recording because it solves the problem padding cannot.

A repeater is **locked** by a powered repeater or comparator facing into its side, and
while locked it holds its output regardless of its input. So: run one control signal into
the side of every output repeater, let the data lines settle at their own unequal speeds
while locked, then unlock — and every line transitions **together**, whatever the skew
upstream.

That works on **data-dependent** skew too, which no amount of fixed padding can flatten.
It is the natural answer for sampling something like a ripple-carry adder, and the
obvious tool when M4 needs to feed a register.

## Torch burnout — real, and NOT modelled here

Source (`RedstoneTorchBlock`): a torch tracks its recent toggles, and more than
**8 within a 60-game-tick window** burns it out. It then stays off and ignores changes,
rescheduling **160 game ticks** later.

Only reachable once time exists, and only bites fast clocks. `worlds/sim/` does not
model it — the one place it would show up is a torch clock running faster than the
burnout threshold, which would run forever in simulation and stall in the game.

## Two kinds of skew, and only one is paddable

When bits of a bus arrive on different ticks, the cause matters, because the fixes are
different. Both were measured on real builds.

**Structural** — fixed, caused by the wiring. One route carries more repeaters than
another, and each repeater is 2 game ticks. Measured on a staggered readout: routes with
0, 1 and 2 repeaters arrived at 10, 12 and 14 ticks, and the 4-tick spread was
**identical for every input**.

Fix: pad the fast lines by turning **up delay settings on repeaters already there**. A
setting runs 1 to 4, so each existing repeater buys up to 6 game ticks at no block cost.
`align()` in `pipeline/compose.py`.

**Data-dependent** — varies with the input, caused by carry chains. Measured on the
4-bit ripple-carry adder across all 256 input pairs:

| settle time | cases |
|---|---|
| 8 ticks | 162 |
| 14 ticks | 60 |
| 18 ticks | 24 |
| **22 ticks** | 8 |

Fix: there isn't one. No fixed padding flattens a delay that depends on the data. The
only correct answer is to **wait for the worst case** before sampling — 22 ticks here,
even though nearly two thirds of inputs are done in 8. That is the ordinary digital
design rule that a clock period must clear the worst-case propagation delay.

`settle_profile()` sweeps inputs and reports that worst case.

**Length alone does nothing.** Dust carries within the tick, so a longer route is not a
slower one — only the repeaters it forces are. A plan built on "stagger the lamps to
create skew" fails for exactly this reason until the routes cross a repeater threshold.

## What the simulator models

| | modelled |
|---|---|
| repeater delay, including the setting | yes |
| comparator delay | yes |
| torch delay | yes |
| lamp on/off asymmetry | yes |
| scheduling priority and the pending guard | yes |
| torch burnout | **no** |
| pistons, observers, 0-tick, quasi-connectivity | **no** — out of scope by design |

## Measured against the game

`/tick freeze`, flip a lever, `/tick step` one at a time. Eight repeaters at delay 1
through 4, and chains of 1–8 repeaters at delay 4:

| | predicted | measured |
|---|---|---|
| chain of *n* repeaters at delay 4 | 8*n* | 8*n* + 1 |
| 8 repeaters at delay *d* | 16*d* | 16*d* + 1 |
| lamp going dark | last repeater + 4 | last repeater + 4 |

Spacing exact in every case. The constant **+1** is where tick-stepping begins counting
— the lever is flipped while frozen, so the neighbour update that schedules the first
repeater lands on the first stepped tick rather than instantly. It cancels in any
difference, which is what alignment cares about.

## What a finished machine costs — M4 measured

`pipeline/m4-decimal-adder-v2.litematic`, from flipping a lever to the digits settling:

| input | game ticks | seconds |
|---|---|---|
| 5 + 5 | 136 | 6.8 |
| 4 + 3 | 158 | 7.9 |
| 2 + 9 | 204 | 10.2 |
| 9 + 9 | 210 | 10.5 |

Nearly all of that is the **comparator relays** in the arithmetic core, which cost
**two ticks per hop** and are used dozens of times. The `hex_wire` circuit does the same
job — carrying a signal strength any distance — in **two ticks total**, so replacing
those relays is the obvious win and the primitive already exists.

The lesson generalises: when moving signal strength, count hops, not blocks. Distance is
free and hops are not.

## Sources

- [Redstone Repeater](https://minecraft.wiki/w/Redstone_Repeater)
- [Redstone Comparator](https://minecraft.wiki/w/Redstone_Comparator)
- [Redstone Torch](https://minecraft.wiki/w/Redstone_Torch)
- [Redstone Lamp](https://minecraft.wiki/w/Redstone_Lamp)
- [Redstone circuits/Clock](https://minecraft.wiki/w/Redstone_circuits/Clock)

Each cross-checked against the decompiled 1.18.2 client, which is the authority where
they disagree.
