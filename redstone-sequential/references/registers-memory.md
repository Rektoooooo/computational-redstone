# Registers, register files and memory banks

## Basic register

Eight repeater locks stacked vertically, unlocked together by one glass tower.

Write: place the value behind the locks, pulse the tower. **2 ticks minimum** — a
2-tick pulse generator is the correct source, not a stone button (10 ticks).

## Stackable write design

For dense register files, the plain design wastes space. The compact version uses
**comparators at signal strength 1 locking every repeater**; powering a glass tower
cancels them from the side, unlocking the whole register at once.

The payoff: it stacks **every two blocks** provided the registers are staggered.

## Stackable read design

Reading is two inversions, which cancel out.

- First inversion: comparators
- Second inversion: torches

When the glass tower is powered it forces all the torches off, so the register is
not read. Unpowered, any active comparator produces **signal strength 2** — just
enough to reach exactly one output and be inverted again.

It looks absurdly convoluted, and it is, but it buys **two-wide stackability** via
the same staggering trick. In a 16-register dual-read file that saving is the
difference between buildable and not.

## Register file assembly

1. Decide register count — **16** is standard, addressed by 4 bits
2. Delete register 0 → it becomes the **zero register**
3. Write decoder (4→16) driven by the clock/write signal
4. Read decoder(s) (4→16)
5. For dual read, **mirror the whole bank** and drive both copies from the same
   write decoder

### Signals

| Signal | Width | Meaning |
|---|---|---|
| R1 | 4 | first read address |
| R2 | 4 | second read address |
| W | 4 | write address |
| Data | 8 | value to write |
| Clock | 1 | perform the write |
| Enable | 1 | 0 disables reads and writes entirely |

**The write signal *is* the clock signal.** They are the same wire under two names —
worth stating explicitly, because diagrams label it "clock" while build tutorials
call it "write".

**Enable** is implemented by cancelling all three address inputs: reads fall through
to register 0 (zero) and writes land on register 0 (discarded). Disabling does **not**
clear stored values; re-enabling resumes exactly where you left off.

## Why the zero register is not a hack

It starts as a workaround — you cannot make a decoder output *nothing*, and
cancelling its input is indistinguishable from addressing 0. Deleting register 0
resolves that. But it then earns its place:

- A constant source of 0 for comparisons and clearing
- A discard destination — `SUB r1 r2 r0` compares without keeping the result
- Makes `NOP` expressible as `ADD r0 r0 r0`
- Makes disable trivial

## Memory bank (data memory)

Larger, address-per-byte storage.

1. Decoder sized to the address width — 8 bits → 256 slots
2. Split every decoder output into **two** lines: one write, one read
3. A single mode bit selects which line is permitted
4. Storage cells reuse the register design, replicated 256 times
5. Reads OR back together through a second tree

The write signal is broadcast to every address and lands only where the decoder
permits. Reads collect onto a shared tree and emerge on one output bus.

Replicating the register design 256 times is admittedly lazy, but it is entirely
adequate for a single-cycle machine where every instruction takes the same time
regardless.

## Memory hierarchy

Real machines stack memory in a pyramid — small and fast at the top, large and slow
at the bottom:

```
registers      (tiny, fastest)
main memory    (bigger, slower)
drive          (huge, slowest)
```

The library analogy: books in a backpack (seconds), on a shelf at home (minutes), at
the library (an hour). Most accesses hit the fastest tier; you only pay the slow
cost occasionally.

**In a single-cycle redstone CPU the speed argument does not apply** — every
instruction takes the same time regardless of which memory it touches. The hierarchy
survives for a different reason: **operand width**. 4-bit register operands cap you
at 16 registers. A 17th register forces 5-bit operands and a full instruction-set
redesign. A separate data memory addressed by a *register's contents* sidesteps that
entirely — 256 bytes reachable without widening a single operand.

That is the real reason for the split, and it is worth stating plainly because the
speed rationale is the one everyone repeats and the one that doesn't hold here.
