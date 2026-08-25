---
name: redstone-arithmetic
description: Circuits that compute numbers — half and full adders, ripple carry, the carry-cancel adder, subtraction via two's complement, adder/subtractor toggles, shift-and-add multipliers and shift-and-subtract dividers. TRIGGER when the user wants to add, subtract, multiply, divide, increment, negate, or double/halve values in hardware, or asks why an adder is slow, unsynchronised, or stops working past 8 bits. DO NOT TRIGGER for the number representation itself (redstone-number-systems), for comparing magnitudes without computing (redstone-combinational), or for the ALU as a CPU component (redstone-cpu).
---

# Redstone Arithmetic

## Teaching approach

Do the operation on paper first, in binary, by hand. Every circuit here is a direct
transcription of a pencil-and-paper algorithm, and users who skip that step end up
copying designs they cannot debug. Ask them to walk one example through — long
division especially — before showing any redstone.

## Addition

### Half adder

Two bits in, sum and carry out.

- **Sum = A XOR B**
- **Carry = A AND B**

The truth tables match exactly, which is the whole derivation.

### Full adder

Three bits in (A, B, carry-in), sum and carry out. Built from two half adders plus
an OR:

- Half-add A and B
- Half-add that sum with carry-in
- OR the two carries together

Equivalently: **Sum = A ⊕ B ⊕ C**, **Carry = (A ∧ B) ∨ ((A ⊕ B) ∧ C)**.

The compact redstone full adder implements that carry equation cleverly: the XOR
layout exposes an AND for free via a torch on top, so both terms come almost free
and merge on a dust line.

### Ripple carry adder (RCA)

Chain full adders, carry-out into carry-in. Simple, correct, expandable to any width.

**Its fatal flaw is speed.** Carries must physically propagate along the chain, so
worst-case time grows with width and — worse — the time *varies with the input*.
Anything clocked needs a predictable duration, so RCAs are unsuitable for CPUs.

### Carry cancel adder (CCA) — the standard

The community answer, and what you should use. Vertical, pistonless, synchronous.

The insight behind every fast adder:

> Compute all the carries at once. Once the carries are known, each column's sum is
> independently `A ⊕ B ⊕ C` — fully parallel, no dependencies.

**The carry-cancel process:** a column with two 1s emits a *carry* signal that
propagates left forever. A column with two 0s emits a *cancel* signal that kills it.
Carries beat earlier cancels; cancels beat earlier carries. The resulting string is
the carry row, shifted by one.

Built as two glass towers of subtract-mode comparators — carry tower at the rear,
cancel tower on the side. Resolves in **one tick** because every comparator works in
parallel.

Full construction, including the XNOR-instead-of-AND shortcut, in
`references/adders.md`.

> **The 8-bit ceiling.** Signal strength runs out. Almost every redstone-specific
> adder caps at 8 bits for this reason. You can stack two 8-bit modules and chain
> carry-out to carry-in, but you lose speed and synchronisation. 8 bits covers
> ~99% of uses.

## Subtraction

Do not build a subtractor. **Reuse the adder.**

`A − B` = `A + (~B) + 1`, so:

1. Invert every bit of the B input (torches)
2. Turn on the carry-in

That's it. The overflow you discard *is* the modular arithmetic doing the work.

### Reading the result

The carry-out doubles as a **sign bit**: 1 means the result is positive, 0 means
negative. When negative, the raw output is the two's complement of the answer, so
to display it as a magnitude you must invert-and-add-one **again** — which needs a
second adder and a selector choosing which result to show.

### Adder/subtractor toggle

To switch modes at runtime, use **XOR as a conditional inverter**: tie one input of
each XOR to a control line. Control 0 → the bit passes through unchanged. Control 1
→ inverted. Wire that same control line to the carry-in and one lever flips the
whole device between add and subtract.

## Multiplication

Long multiplication in binary is unusually simple: each partial product is either
**the whole number** (multiply by 1) or **nothing** (multiply by 0), shifted left
one place per step. So multiplication is **shift and add**.

The circuit is an **adder on a loop**:

- Feed A into the adder, gated by the current lowest bit of B
- If that bit is 0, cancel A so nothing is added this cycle
- Each cycle, shift B right and record the accumulator's lowest bit as one bit of
  the answer
- After 8 cycles the recorded bits are the product

Because it loops, it needs **calculate** and **clear** buttons rather than being
purely combinational. Two 8-bit inputs produce up to a 16-bit result.

Worked examples and build notes in `references/multiply-divide.md`.

## Division

Long division, mechanised. Shift the dividend in from the left one bit at a time,
and at each step ask one question:

> Can I subtract the divisor from what I'm holding?
> **No** → quotient bit 0, change nothing.
> **Yes** → quotient bit 1, and replace the value with the difference.

The elegant part: a subtractor's **carry-out already answers that question**. Carry
out = 1 means the result was non-negative, i.e. the subtraction was possible. So the
carry-out *is* the quotient bit. No extra comparison circuitry.

This is a **conditional subtractor** on a loop. What remains at the end is the
remainder.

### Faking decimals

There is no fractional arithmetic. To show `2 ÷ 3 = 0.66`, multiply the dividend by
100 first and print a decimal point that is purely cosmetic — `200 ÷ 3 = 66`, shown
as `0.66`.

Multiply by 100 with shifts, not a multiplier:

> **×100 = (shift 2) + (shift 5) + (shift 6)** — that is 4 + 32 + 64

Two chained adders sum the three terms. Note this forces the divider to 16 bits,
since 255 × 100 = 25500.

## Shifts — free arithmetic

- **Shift left n places = multiply by 2ⁿ**
- **Shift right n places = divide by 2ⁿ**

A shift is pure wiring — connect bit *i* to output *i+n*. It costs nothing.

Two consequences worth internalising:
- An ALU can left-shift with no shift hardware at all: feed the same value into
  both inputs and add, since `x + x = 2x`.
- Any multiply-by-constant decomposes into shifts and adds. ×10 = shift1 + shift3.

## Common failures

| Symptom | Cause |
|---|---|
| Adder works small, breaks past 8 bits | signal strength in the carry/cancel towers |
| Result is right but timing varies | you built a ripple carry adder; use a CCA |
| Subtraction shows 11 instead of 3 | reading the raw two's complement; check the sign bit |
| Divider outputs all 1s | divisor is 0 — it can always subtract 0, forever |
| Multiplier gives A × 255 | the per-cycle cancel gate is not wired; every bit reads as 1 |
| Intermittent wrong answers under load | torch burnout; consider a torchless design |
