---
name: redstone-logic-gates
description: Turning a logical requirement into gates — boolean algebra, truth tables, De Morgan, and the redstone construction of NOT, OR, AND, XOR, NOR, NAND, XNOR plus bitwise operations across a bus. TRIGGER when the user states a condition in words or a truth table and needs a circuit, asks how to build or shrink a specific gate, wants a boolean expression simplified, or needs the same operation applied bitwise to every bit of a number. DO NOT TRIGGER for arithmetic built from gates (redstone-arithmetic), for selecting/routing signals (redstone-combinational), or for anything with memory (redstone-sequential).
---

# Redstone Logic Gates

## Teaching approach

When someone describes a condition in words, do not jump to redstone. Ask them to
write the truth table first, then the boolean expression, and only then discuss the
circuit. The reason is practical, not pedagogical: **expressions simplify, redstone
doesn't.** A monstrous-looking expression frequently reduces to `A ∧ B`, and you
find that out on paper in seconds or in the world in hours.

Run expressions through an online boolean simplifier before building. Shorter
expression = fewer gates = smaller build.

## Boolean basics

Three primitives, plus XOR which is too useful to omit.

| Op | Symbol | Programming | True when |
|---|---|---|---|
| NOT | ¬A | `!a` | A is false |
| OR | A ∨ B | `a \| b` | at least one is true |
| AND | A ∧ B | `a & b` | both are true |
| XOR | A ⊕ B | `a ^ b` | **exactly one** is true |

A truth table with n variables needs **2ⁿ rows**. Always enumerate all of them.

### Laws worth carrying

- **Identity:** `X ∨ 0 = X`
- **Annihilator:** `X ∨ 1 = 1` — the OR stops caring about the rest
- **Double negation:** `¬¬A = A` — two torches in a row cancel; delete both
- **De Morgan:** `¬(A ∧ B) = ¬A ∨ ¬B` and `¬(A ∨ B) = ¬A ∧ ¬B`

De Morgan is the one that earns its keep: **you may distribute a negation as long
as you swap the operator.** In redstone this often converts an expensive AND into a
cheap OR with inverted inputs.

## Building the gates

### OR — free

Merge two dust lines. That's it. Redstone wire is natively an OR gate.

### NOT — one torch

Dust into a torch. Output is the inverse, 1 tick later.

Alternative: a subtract-mode comparator powered from the rear with the input on the
side. Uncancelled → output on; cancelled → output off.

### AND — three NOTs and an OR

There is no native AND. Build it from De Morgan: `A ∧ B = ¬(¬A ∨ ¬B)`.

In redstone: torches on both inputs, merge into a dust line, one final torch. The
final torch can only light when the dust goes off, which requires *both* input
torches off, which requires *both* inputs powered.

**Better in practice:** a subtract-mode comparator with input A at the rear and
inverted B on the side. Output only survives when A is present and B is not
cancelling. Compact and fast.

### XOR — the two-comparator symmetry trick

No native XOR either. The standard design uses two subtract-mode comparators
exploiting asymmetry:

- **Both inputs on:** each comparator sees 14 rear and 14 side → `14−14 = 0`
- **One input on:** the asymmetric one sees 13 rear and 11 side → `13−11 = 2`

The 2 beats the 0, so you get an output only when exactly one input is on. It is
symmetrical, so it works either way round.

> **Caveat: the output is only signal strength 2.** You must follow it with a
> repeater. An alternative layout gives a stronger output at the cost of size.

### The negated forms

NOR, NAND and XNOR are just the base gate with an inverted output.

- **NOR** — OR plus a torch
- **NAND** — AND plus a torch. But the AND already ends in a torch, so two torches
  in a row cancel: **remove** the final torch instead of adding one.
- **XNOR** — either add a torch, or **invert one input of the XOR**. Inverting a
  single input of XOR inverts its output. This does *not* work for OR or AND.

To get any negated gate's truth table, take the base gate's and flip the output column.

More layouts and variants in `references/gate-designs.md`.

## Bitwise operations

A bitwise operation applies the same gate to each pair of bits independently:

```
0101 AND 0011  =  0001
```

In redstone this is literally **the same gate built at every level** of a vertical
bus. A bitwise OR is a stack of OR gates, one per bit; a bitwise AND is a stack of
ANDs. No carries, no interaction between levels — that independence is the defining
property.

### Bit masks

The main reason bitwise operations matter. `AND` with a mask **keeps** the bits
where the mask is 1 and clears the rest; `OR` with a mask **sets** bits.

```
controller_state AND 00000100   ->  isolates one button
```

This is how CPU programs test a single controller button: mask off everything
else, then branch on whether the result is zero. See `redstone-cpu`.

## Common gotchas

- Two torches in series are a wasted tick and a wasted block — cancel them.
- The XOR output at strength 2 will not travel; repeat it immediately.
- An AND built as three torches costs 2 ticks (two inversion stages); the comparator
  version costs 1. In a clocked machine that difference compounds.
- If a gate "works" but its output is weak, check whether you built it from
  comparators and forgot the repeater.
