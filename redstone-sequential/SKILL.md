---
name: redstone-sequential
description: Circuits with memory and timing — SR and D latches, flip-flops, registers, register files, ripple and synchronous counters, shift registers, stacks, accumulators, memory banks, pulse generators and clocks. TRIGGER when the user needs to store, capture, toggle, count, shift or remember a value, needs a circuit whose output depends on what happened before, or needs a pulse of a specific length, a clock at a specific period, or a long timer. DO NOT TRIGGER for stateless routing (redstone-combinational), for arithmetic (redstone-arithmetic), or for the register file as part of an instruction set (redstone-cpu).
---

# Sequential Redstone Devices

**Sequential means the output depends on internal state, not just the input.** Ask
"what will this output when I press the button?" — if the honest answer is "it
depends what happened before", it is sequential.

## Teaching approach

Almost everything here is built from **one primitive**: the repeater lock. Before
showing any design, get the user to explain what a locked repeater does. Once
"locked = remembering, unlocked = listening" is solid, registers, counters, shift
registers and stacks all follow without new ideas.

## The primitives

### Repeater lock = D latch

A repeater locked from the side by another repeater or comparator **freezes its
current state**. This is not "can be used as" a data latch — it *is* one:

- **Unlocked** → passes data through (listening)
- **Locked** → holds whatever it had (remembering)

To write a bit: put the value behind it, unlock and relock. A **2-tick pulse is the
minimum** that reliably captures. A stone button works but is 10 ticks — far longer
than needed; use a 2-tick pulse generator.

This one component replaces the textbook gated-D-latch entirely.

### SR latch

Two torches (really two NOR gates) cross-coupled, with the second's output fed back
into the first.

- **Set** → output on, permanently
- **Reset** → output off, permanently

You get the **inverted output for free** — the first NOR always outputs the opposite
of the second. The side-by-side layout with crisscrossing feedback makes both
outputs easy to tap, and is the layout you'll see in any digital logic course.
Compact redstone versions exist that are far smaller.

Add an **enable** with two comparators and a torch: enabled → set/reset work
normally; disabled → the latch ignores everything.

**Undefined behaviour:** setting and resetting simultaneously makes the output and
its inverse both 1, which is nonsense. The D latch exists precisely to make that
state unreachable, by deriving reset as the inverse of set.

### Flip-flops

A flip-flop is a latch whose enable is driven by a **clock** rather than by hand.
Same circuit, different intent — a latch is enabled at will; a flip-flop updates
once per clock cycle.

**T flip-flop** — toggles on each pulse. The tiny repeater-lock design is the one to
use. Note it only behaves correctly with a short pulse; hold the input high
continuously and it toggles forever. That is also why a "T latch" isn't a coherent
concept.

## Registers

Stack 8 repeater locks vertically, all unlocked by one **glass tower**. That's an
8-bit register. Vertical is strongly preferred over horizontal — the write line
becomes a single tower reaching all eight bits.

Add a **read function** by putting cancelling comparators on the output: locked
comparators hide the value, uncancelling releases it.

### Register file

Many registers sharing one input bus, one write decoder and one or more read
decoders. Three design decisions matter:

**1. The zero-register trick.** Cancelling a decoder's address input is the same as
addressing 0 — and 0 is a valid address, so the decoder never outputs *nothing*.
Solution: **delete register 0**. Reads of address 0 return 0; writes to it are
discarded. This turns a wiring problem into a genuinely useful feature — a constant
zero source, and a scratch destination for results you want to throw away.

**2. Dual read.** Reading two registers at once, needed to feed a two-input ALU.
- *True dual read* — duplicate the output wiring. One copy of the data, messy wiring.
- *Simulated dual read* — mirror the entire register bank and read each copy
  normally. Much easier in redstone since you just mirror the build; the write
  decoder must write to **both copies** to keep them in sync.

**3. Enable.** Cancel all three address inputs at once. That forces reads to
register 0 (returns zero) and writes to register 0 (discarded), disabling the file
without clearing it.

Advanced stackable write/read designs, and the signal-strength trickery behind them,
are in `references/registers-memory.md`.

## Counters

**Ripple counter** — a T flip-flop per bit, each toggled by a torch on the previous
bit's output (a torch fires on a 1→0 transition). Simple, expandable, but the
toggles ripple, so it gets slower and unsynchronised as it widens — the same flaw as
a ripple carry adder.

**Synchronous counter** — the better design, built on one observation:

> A bit toggles **if and only if all bits below it are 1.**
> Not "because the bit below it toggled."

Implemented by putting torches on all lower bits wired into the T flip-flop's
disable line. Once every lower bit is 1, all those torches go off, permitting the
toggle. Everything fires at once. Compact vertical design using a glass tower,
expandable to 8 bits (you may need a target block at the top).

Add **load** by stacking the repeater locks so a value can be written directly, then
counting on from there.

## Shift registers

A register whose outputs feed the next bit's input. Shift up = **×2**, shift down =
**÷2** — free multiplication and division by powers of two.

Without a load function the only way to get data in is one bit at a time, which is
painful. Add load with a **multiplexer**: cancel either the shifted data or the load
data, and let the repeater locks capture whichever survives.

**Bidirectional** shift registers use a three-way mux between shift-up, shift-down
and load. Two designs: the classic (3 blocks wide per cell, two opposed sets of
repeater locks) and a 2-wide-per-cell variant using a single set.

This is the component a CPU **call stack** is built from — push = shift one way,
pop = shift the other.

**Ring counter** — feed a shift register's output back into its input with a single
bit circulating. Add an encoder and you can step through any arbitrary sequence.

## Larger memory

**Memory bank** — many registers, each with an address. A decoder unlocks exactly
one register's write line and one register's read line. The write signal is offered
to every register but only lands where the decoder permits.

**Accumulator** — a register whose output loops through an adder and back. Feeding
it 1 makes a counter; feeding it all-ones (−1 in two's complement) makes it count
down; swap the adder for another operation and it accumulates that instead.

**Signal-strength memory cell** — two comparators in a loop, storing a whole 0–15
value rather than a bit. Use when hex is more convenient than binary.

## Pulses, clocks and timers

**Pulse generator** — a comparator whose signal is cancelled N ticks later. The
delay sets the pulse length. **It cannot produce a 1-tick pulse** (a consequence of
how comparators update); use an observer if you truly need one, though 1-tick pulses
cause enough problems that avoiding them is usually right.

**Pulse extender** — OR the original pulse with a delayed copy of itself. A 10-tick
button pulse ORed with the same pulse delayed 3 ticks gives 13 ticks.

**Repeaters extend short pulses.** A pulse shorter than the repeater's delay setting
comes out lengthened to that delay. A 1-tick pulse into a 4-tick repeater emerges as
a 4-tick pulse. This is often the cause of mysterious pulse-width changes.

**Clocks** — the good design is a **subtract comparator wired back into its own
side**. Powering the rear starts it; unpowering stops it. No pulse injection, no
piston to break the loop, and it produces a clean alternating signal.

- Loop length = pulse width. Period = 2 × loop length.
- Add a second comparator cancelled after N ticks to shape the output pulse
  independently of the period.

**Decaying timer** — a comparator loop whose value decays by 1 each cycle. Load 15
and it counts 15, 14, 13… to 0, staying on the whole way. A very compact long timer.

Period and frequency are reciprocal: `f = 1/T`. A 5-tick pulse every 10 ticks is a
10-tick period = 1 second = 1 Hz.
