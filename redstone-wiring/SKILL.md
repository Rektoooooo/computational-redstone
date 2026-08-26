---
name: redstone-wiring
description: Getting a signal from one place to another — single wires and multi-bit buses, flat, up, down and diagonal; converting between horizontal and vertical stacking; carrying signal STRENGTH (hex) over distance without a slow comparator chain; and crossing two buses without them interfering. TRIGGER when a signal has to travel, when a route runs out of signal strength, when two lines need to cross, when a bus must change from stacked-sideways to stacked-upwards, or when a build is "correct but does not fit". DO NOT TRIGGER for what the signal MEANS (redstone-number-systems), for the circuits at either end (redstone-combinational, redstone-arithmetic), or for timing alignment between lines (docs/timing.md).
---

# Redstone Wiring

Wiring is the part nobody plans for and everybody spends their time on. A build that
computes the right answer and cannot be wired is not finished, it is stuck — and the
usual reason is that two lines need to occupy the same place and neither will move.

Everything below is from mattbatwings' *Wiring like a pro*, and every circuit named has
been **extracted from his world download and driven in our simulator**. The numbers are
measured, not quoted.

## Ask this first: does it have to be hex?

Signal strength is the expensive thing to move. Binary is not.

> Converting hex → binary → hex costs about **2–3 ticks** total. So over any real
> distance, **convert to binary, wire the bits, and convert back at the far end.**

This is the single highest-leverage rule in the file, and it is easy to miss because
each individual hex-wiring circuit is perfectly good. The point is that binary lines
can be **repeatered, crossed, stacked and turned freely**, and a hex line can do none of
those without changing its own value.

Our own `pipeline/digit_adder.py` was blocked for a whole session by exactly this — an
analog value with nowhere to go — and the fix was not a cleverer route.

## One bit

**Flat.** Dust, with a repeater every 15 blocks. Putting a solid block behind *and* in
front of the repeater buys a little more length. The only thing that catches people out
is **turning**: if the strength runs out on a corner, the dust is no longer pointing
into the block. A **target block** on the corner fixes it — target accepts power from
any direction.

**Upwards — a glass tower.** Small and fast: a block and a dust cell alternating, so the
signal climbs **one level per block** inside a 2×1 footprint. That is the whole reason
to prefer it over a staircase, which costs a block of floor for every level.

When it runs out of strength, extend it with a repeater turned back on itself, or with
**two torches** — a double negation. And if the tower is tall, the two torches do not
have to be adjacent: **one negation here and another one much further up** is still a
double negation, and it is faster than a torch pair at every step.

**Downwards.** In Java a glass tower only sends signal *up*. Down needs a staircase, and
the clean form is a **spiral**, which keeps the footprint small. The same extensions
apply, and any **even** number of negations works. Spirals also go up, so if one wire
has to carry a signal both ways, a spiral is the only thing that will.

**Diagonal.** There is no shame in doing it in two parts, horizontal then vertical — it
is usually the cleanest answer. Going up on a diagonal, a staircase with a repeater
shifts the line over by one block; putting **torches on the sides of the blocks**
avoids the shift. Going *down* a diagonal there is only one thing to know: a **repeater
firing into a block** carries the signal down without shifting the line at all.

## Many bits

Buses are stacked either **sideways** or **upwards**. Sideways looks more like a circuit
diagram and was what everyone did first; **upwards turns better** — every wire in a
vertical bus turns through the same number of blocks, where a horizontal bus gives every
wire a different length and therefore a different delay.

Two blocks of spacing is normal. They can be squeezed to **one block apart** by
staggering, and it behaves identically.

- **Up:** one glass tower per bit, side by side; stagger to squeeze, but check the
  extensions do not reach into the neighbouring tower.
- **Down:** spirals. Side by side they normally need a block of space between them —
  unless you **alternate clockwise and counter-clockwise**, which lets them touch.
- **Diagonal, vertical bus:** alternate glass and solid blocks so each bit climbs
  independently. That only gains one level per two blocks across; stagger to get a true
  diagonal. Or make the run **exactly 15 blocks and all glass** — then only the bit that
  is actually on has the strength to reach its repeater. That trick has no downward
  equivalent.

## Turning a bus on its side

Horizontal ↔ vertical conversion is glass towers of increasing height — the cleanest
form of it. Watch the bit order: the **leftmost bit arrives at the bottom**. If you want
the opposite, either build it with downward spirals or run it to the right instead of
the left. Both flip the output.

Verified: `primitives/wiring/build-18` converts in that order and `build-19` is the
mirrored one, bit for bit.

## Carrying signal strength — the circuit worth memorising

A chain of comparators works and is **very slow**. The fast way exploits one fact:

> **a signal of strength X travels exactly X blocks.**

So: a **dust line**, a **row of repeaters** reading it from the side, and a **second dust
line** taking their outputs. Strength X lights the first X repeaters; the last lit one is
X blocks along; from there the output line decays over the remaining distance.

With **N repeaters** the output is:

```
out = in + (15 - N)        for in >= 1;  out = 0 for in = 0;  saturating at 15
```

so a **full 15-repeater run reproduces the input exactly**, and a shorter run needs the
difference subtracted at the far end. Measured on `primitives/wiring/build-41`, which has
11 repeaters and comes out at `in + 4` for every input from 1 to 11.

**Two things follow, and the second is not obvious:**

1. It takes **two game ticks** — a repeater delay — however long the run is. A comparator
   relay takes two ticks *per hop*.
2. **A short run is a free adder.** If you need `v + k`, use a run of `15 - k` repeaters.
   That is how you pay for a climb: a glass tower or staircase costs one level per block,
   so send `v + height` and it arrives as `v`, with no extra components at all.

The same circuit works in every direction — it is always a dust line, repeaters, and a
dust line. Upwards, the dust lines are glass towers. Downwards, they are spirals.
Diagonally, the whole thing is staircased; there are three-wide and two-wide versions.

## Crossing

- **Two single wires:** run one over the other. That is the whole solution.
- **Two multi-bit buses:** an **intersection built from repeaters**, which is stackable
  every two blocks, so it crosses vertical buses as well.
- There is also a **zero-tick crossover** using 3D space and heavy staggering. It is
  messy and only worth it when the ticks matter.

> **Our simulator gets the zero-tick crossover wrong.** Driven on
> `primitives/wiring/build-14`, four of the eight lamps light regardless of input. That
> circuit depends on precise dust-diagonal behaviour, which is exactly where a model is
> most likely to be wrong — so do not use it in a generated build until the discrepancy
> is chased down. The repeater intersection is fine.

## Building these

Do not place them by hand. WorldEdit plus **Redstone Tools** (mattbatwings' own mod) is
the normal workflow — the useful part is `//rstack`, which stacks a selection with an
offset, so a glass tower is "build two blocks, stack 30 up 2", and eight of them is
"select the tower, stack 7".

Our equivalent is `pipeline/analog.py` and `pipeline/compose.py`, which generate the
blocks directly and check them before anything is pasted.

## Where the verified circuits are

`worlds/primitives/wiring/` — 49 builds harvested from the world download, no signs, so
they are identified by structure and by driving them. The ones already confirmed:

| build | what it is | confirmed |
|---|---|---|
| `build-41` | **hex wiring, flat** — dust, 11 repeaters, dust | `out = in + 4`, all inputs |
| `build-48` | the same circuit without its output line | structure only |
| `build-15` | 4-bit vertical bus | each bit reaches its own lamp, no crosstalk |
| `build-18` / `build-19` | horizontal ↔ vertical conversion, and the mirrored one | bit order confirmed both ways |
| `build-36`/`37`/`44`/`45`/`46` | glass towers, 27–46 blocks tall, extended by torches or a repeater | signal reaches the top |
| `build-14` | zero-tick 3D crossover | **fails in our simulator** — see above |

More detail, and the full list, in `references/circuits.md`.
