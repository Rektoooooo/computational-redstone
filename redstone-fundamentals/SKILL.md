---
name: redstone-fundamentals
description: The four computational redstone components (dust, repeater, comparator, torch), soft vs hard power, glass towers, tick timing, and world/mod setup. TRIGGER when the user is setting up a redstone world, asks what a component does, asks why a signal is not reaching or a torch will not turn off, asks about signal strength decay or delay in ticks, or is debugging a circuit whose logic is correct but whose wiring or timing misbehaves. DO NOT TRIGGER for building a specific device — route gates to redstone-logic-gates, adders to redstone-arithmetic, decoders to redstone-combinational, memory to redstone-sequential, screens to redstone-displays, CPUs to redstone-cpu.
---

# Redstone Fundamentals

The physical layer everything else is built on. Computational redstone deliberately
uses **four components only** — dust, repeater, comparator, torch. Pistons and
observers are avoided: they add timing hazards and are unnecessary unless you are
physically moving blocks.

> "If you're not moving blocks I feel like you just never need to use pistons.
> No matter what circuit I'm designing I tend to find cleaner solutions using just these guys."

## Teaching approach

Before handing over a wiring fix, ask the user what they think is stopping the
signal. Nearly every fundamentals bug is one of four things, and naming the
category teaches more than the fix does:

1. Signal strength ran out (>15 blocks of dust)
2. Soft power where hard power was needed
3. A timing desync between two paths that should arrive together
4. A wire connecting to something it should not touch

## Ticks — the unit everyone means

**"Tick" always means redstone tick in this field.** 1 redstone tick = 2 game
ticks = 0.1 s. A "4-tick repeater" is 0.4 s. If a source says a stone button is
10 ticks, that is 10 *redstone* ticks = 1 second.

| Component | Delay |
|---|---|
| Dust | none (instant for timing purposes) |
| Repeater | 1–4 ticks, right-click to set |
| Comparator | 1 tick, fixed |
| Torch (inversion) | 1 tick |
| Stone button pulse | 10 ticks |
| Wooden button pulse | 15 ticks |

## Signal strength

Dust carries 0–15 and **decays 1 per block**, so a run dies after 15 blocks. A
repeater restores it to 15. A comparator preserves the exact value — it is the
only component that does analog arithmetic.

Signal strength is the hidden ceiling on almost every large build. It is why
redstone-specific adders cap at 8 bits and why glass towers need extending past
8 layers.

## Soft vs hard power

The single biggest source of "my circuit looks right but doesn't work".

| | Powers adjacent dust | Powers repeater/comparator | Activates lamp/door | Turns a torch off |
|---|---|---|---|---|
| **Hard** (repeater, lever, button, torch powering block above) | yes | yes | yes | yes |
| **Soft** (dust on top of, or pointing into, a block) | **no** | yes | yes | **no** |

Both kinds pass signals through walls into repeaters and comparators. The only
difference is that soft power will not re-power dust and will not flip a torch.

**Classic symptom:** dust runs into a block with a torch on it and the torch stays
lit. Dust only gives soft power. Feed the block with a repeater or lever instead.

## The four components

**Dust** — the wire. Sits on almost any flat surface including glass and upside-down
slabs. Cannot exist without support.

**Repeater** — restores to 15, adds 1–4 ticks, acts as a one-way diode, and can be
**locked** from the side by another repeater or comparator, freezing its state.
That lock is a free 1-bit memory cell (see `redstone-sequential`).

**Comparator** — three inputs (rear + two sides), 1 tick, two modes:
- *Compare* (default): outputs rear unless a side exceeds it, then 0
- *Subtract* (front knob lit): outputs `rear − max(side)`, floored at 0

Subtract mode is the workhorse. **Feed 15 into the side and nothing gets through** —
this "cancelling" is how you build NOT gates, AND gates, multiplexers, register
read/write enables, and mode selectors. Compare mode is rarely used.

Comparators also read container fullness, which lets you produce any signal
strength on demand with a barrel and some items.

**Torch** — a power source that outputs 15 to its sides and the block above, but not
to the block it is attached to. Powering that attachment block turns it off, making
it a **NOT gate** with 1 tick of delay. Torches **burn out** if toggled too fast
and stay out until they receive an update.

## Blocks that matter

**Transparent blocks** (glass, glowstone, ice, upside-down slabs) have two properties
that make them structural, not decorative:

1. Redstone travels **up onto** them but **not down** — a free one-way wire
2. Dust slips *through* them on a staircase, where a solid block would cut it

This gives you the **glass tower**: a vertical bus that is simultaneously a one-way
diode and an OR gate for everything feeding into it. It is the single most-used
structure in computational redstone. Nearly every register, counter, decoder and
adder is built around one.

**Target block** — dust placed next to it automatically points into it. In this field
it is used purely as a redirector for compaction; its projectile behaviour is irrelevant.

**Redstone block** — powers dust next to, above and below it. Always on.

**Containers** — with a comparator, generate any signal strength 0–15 on the fly.

## Inputs and outputs

Inputs: lever (toggle), button (timed pulse), pressure plate. All hard-power their
attachment block.

Outputs: **use trapdoors, not lamps.** Lamps turn on instantly but take **2 ticks to
turn off**, so they lie to you for 2 ticks while you are reading circuit state, and
they ruin animations. Trapdoors update instantly in both directions. Re-texture
side-mounted trapdoors to look like lamps if you want the look.

## Extending a glass tower past 8

Signal strength runs out around 8 layers. Two fixes, and **both require the block
behind them to be solid** — this is a very common oversight:

- A repeater facing backwards into the tower
- A double torch

Then **compensate the timing**: add 1 tick of delay to the lower eight repeaters
for the repeater method, or 2 ticks for the torch method, so the whole tower
arrives synchronised.

## World and tooling setup

See `references/world-setup.md` for the full checklist. In short: creative,
cheats on, peaceful, superflat "Redstone ready" or void, structures off, and
game rules for spawning / block drops / world updates all turned off.

Three Fabric mods do the heavy lifting — WorldEdit (`//set`, `//move`, `//copy`,
`//paste`, `//stack`, the `-a` flag, schematics), Carpet (`/tick rate`,
`/tick freeze`, `/tick step`, creative no-clip), and RedstoneTools. Details and
command reference in `references/worldedit-carpet.md`.

A texture pack that prints signal strength on the dust is close to mandatory for
debugging.

## Debugging techniques

- **Freeze and step.** `/tick freeze` then `/tick step 2` advances exactly one
  redstone tick. This is the only reliable way to see ordering.
- **Measure a pulse.** Run it into a line of repeaters and freeze — the pulse is
  literally N repeaters long. Without Carpet, lock the repeaters instead.
- **Lamp everything.** Put lamps on intermediate lines while building; remove later.
- **Test every case.** For a new component with n inputs, walk all 2^n combinations
  before wiring it into anything larger.
