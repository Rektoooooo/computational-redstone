---
name: redstone-number-systems
description: How numbers are represented before any circuit exists — binary, hexadecimal, signal-strength encoding, two's complement negatives, and BCD. TRIGGER when converting between bases, deciding how many bits a value needs, representing negative numbers, interpreting an unexpected result as overflow or wraparound, or converting between binary and decimal digits for a display. DO NOT TRIGGER for building the circuit that does the arithmetic — that is redstone-arithmetic; for the display hardware itself use redstone-displays.
---

# Redstone Number Systems

Representation decisions come before circuit decisions. Choosing the wrong encoding
costs far more than a slow circuit, because the instruction set, the memory width
and the display pipeline all inherit it.

## Teaching approach

When a user hits a "wrong answer" that is actually a representation problem —
`5 + 255 = 4`, or a subtraction that reads as 11 instead of 3 — do not correct the
number. Ask what they think the extra bit means. Overflow and two's complement
click permanently once someone works out for themselves that the discarded carry
*is* the mechanism.

## Which base, and why

Redstone offers exactly two natural encodings:

- **Binary (base 2)** — a wire is on or off. One wire = one bit.
- **Hexadecimal (base 16)** — signal strength is 0–15, which is precisely one hex
  digit. A single dust carries a whole hex digit.

Binary dominates because it is what logic gates operate on. Hex earns its place
whenever you are working with signal strength directly, and conversion between the
two is free: **split binary into groups of 4 bits from the right; each group is one
hex digit.** No arithmetic required.

```
0110 1111 0100  ->  6 F 4
```

## Bits and capacity

**n bits represent 2ⁿ distinct values**, ranging 0 to 2ⁿ−1.

| Bits | Values | Range |
|---|---|---|
| 4 | 16 | 0–15 |
| 8 (one byte) | 256 | 0–255 |
| 10 | 1024 | 0–1023 |
| 16 | 65536 | 0–65535 |

Bit width is a design decision with real consequences. In a CPU, 4-bit register
operands cap you at **16 registers** — wanting a 17th forces 5-bit operands and a
complete instruction-set redesign. Decide width early.

Note that a value's bit-length is not intrinsic: 25 is `11001` (5 bits) and also
`00011001` (8 bits). Always state the width you are working in.

## Two's complement — negatives

The key insight is that **overflow is the mechanism, not a bug**.

Working in n bits is arithmetic mod 2ⁿ. In 4 bits (mod 16), adding 14 and
subtracting 2 are the same operation, because 6 + 14 = 20, and 20 mod 16 = 4.

> **negative x = 2ⁿ − x**

So in 4 bits, −2 is 14 (`1110`), −5 is 11 (`1011`).

### Invert and add one

```
2ⁿ − x  =  (2ⁿ−1 − x) + 1
        =  (all-ones − x) + 1      ← subtracting from all 1s IS bit inversion
        =  ~x + 1
```

Because `1−0 = 1` and `1−1 = 0`, subtracting each bit from 1 flips it. That is the
whole proof. Worth showing rather than asserting — most people carry
"invert and add one" as a magic incantation for years.

### Properties worth knowing

- **The top bit is a sign bit** — 0 for positive, 1 for negative
- **Zero is its own complement** — invert gives all ones, +1 wraps back to zero
- **Range in n bits is −2ⁿ⁻¹ to 2ⁿ⁻¹−1** — 4 bits gives −8..+7, 8 bits −128..+127
- **The sign bit can be read as a negative place value.** `1101` = −8 + 4 + 1 = −3.
  Works for any width and any value.
- **The complement of a complement is the original**

### Why it wins

It lets you reuse an adder for subtraction: `A − B` becomes `A + (~B) + 1`, which
in hardware means inverting the B input and turning on the carry-in. One circuit,
both operations.

Contrast **signed magnitude** (top bit = sign, rest = magnitude), which is more
intuitive to read but breaks under addition: +5 plus −5 gives 2, not 0. And
**one's complement** (invert only, no +1), used historically, which has two
representations for zero.

### The rule that catches everyone

**Notation exists only for the developer.** The hardware does not know whether your
bits are signed. An adder is a logic circuit that adds; interpreting the result is
your job. Landing outside the representable range gives a wrong answer with no
warning — `−7 + −7 = −14` is outside 4-bit range and will silently produce garbage.

## BCD — binary coded decimal

Each decimal digit stored as its own 4-bit group. 347 in BCD is `0011 0100 0111`.

BCD exists because **displays are decimal and arithmetic is binary**. You need it
at the boundary, and only there.

- Showing a binary number in **hex** is trivial — chunk it into 4-bit groups and
  feed each to a hex-to-7-segment converter.
- Showing a binary number in **decimal** is genuinely hard — you must convert
  binary → BCD first, then each BCD digit → seven segments.

Both conversion algorithms are in `references/bcd-conversion.md`:
**double dabble** (binary → BCD, the shift-and-add-3 method) and
**×10 accumulation** (BCD → binary, Horner's method built from shifts).
