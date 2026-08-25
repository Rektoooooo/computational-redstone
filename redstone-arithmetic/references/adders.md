# Adder designs

## Full adder equations

```
Sum      = A XOR B XOR Cin
CarryOut = (A AND B) OR ((A XOR B) AND Cin)
```

Truth table (8 rows, three inputs):

| A | B | Cin | Sum | Cout |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 0 |
| 0 | 1 | 0 | 1 | 0 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 1 | 1 |

Sum is high when **one or three** inputs are high — hence the triple XOR.
Carry is high when **at least two** are high.

**Always test all eight cases** before chaining full adders into anything.

## The compact redstone full adder

The long-standing community design implements the above with a trick: its XOR
layout produces an **AND for free** from a torch placed on top of the structure.

- First torch = `A AND B`
- Second torch = `(A XOR B) AND Cin`
- The two merge on a dust line = carry out

So both terms of the carry equation come almost free from structure you needed
anyway.

Standard orientation for chaining: A and B on the bottom, sum on top, carry-in on
the right, carry-out on the left.

## Carry cancel adder (CCA)

### The process on paper

For `5 + 3`:

- A column with **two 1s** → emit a **carry** signal, travelling left forever
- A column with **two 0s** → emit a **cancel** signal, killing any carry
- Carries override earlier cancels; cancels override earlier carries

The resulting string of 1s and 0s **is the carry row**, shifted one place.

Once you have the carries, every column's sum is `A ⊕ B ⊕ C`, computed in parallel.

### The redstone

**Two glass towers of subtract-mode comparators**, stacked vertically:

- **Rear tower** carries the carry signals
- **Side tower** carries the cancel signals

A carry signal travels up the glass tower but not down — which, in a vertical adder,
is exactly "left but not right" on paper. Where a cancel is present, the side input
exceeds the rear at every layer, so all those comparators output 0.

Resolves in **one tick**: every comparator evaluates simultaneously.

### Generating the two signals

- **Cancel** (both bits 0) → a torch, i.e. a **NOR** gate
- **Carry** (both bits 1) → *should* be AND, but the design uses **XNOR** instead

XNOR is wrong for the 0,0 case — but 0,0 already emits a cancel, which overrides,
so the error is unreachable. The XOR gate is already present for the sum, so
inverting it is free. **This is a deliberate, safe shortcut**, not a bug.

### Carry in / carry out

- **Carry in** — power the bottom of the carry tower
- **Carry out** — the top output of the carry tower

### Performance

| Design | Ticks | Notes |
|---|---|---|
| Basic CCA | 5 | straightforward build |
| Optimised CCA | 3 | heavily engineered |
| Torchless CCA | 3 | near-zero torches, so effectively immune to burnout — best for CPUs |
| Hex CCA | — | operates on signal strength rather than bits |

### Measured block census

Extracted from the LRR Addition world and counted directly, so these are observed
numbers rather than reported ones. All 8-bit, comparable bounding boxes.

| Design | Blocks | Torches | Comparators | Repeaters | Wire | Height |
|---|---|---|---|---|---|---|
| CCA 5-tick | 733 | 18 | 41 | 41 | 215 | 21 |
| CCA 3-tick | 517 | 24 | 39 | 17 | 135 | 20 |
| CCA 3-tick torchless | 608 | **1** | **65** | 10 | 153 | 20 |
| CLE 4-tick | 936 | 113 | **0** | 19 | 319 | 22 |
| ICA 4-tick | 547 | 64 | **0** | 31 | 136 | **8** |

What the numbers show:

- **"Torchless" is a name, not a literal spec.** The Fearless design contains exactly
  one torch, against 24 in the standard 3-tick. The point stands — burnout stops being
  a concern — but do not expect zero.
- **The trade is visible.** Torchless carries 65 comparators against 39, buying
  reliability with size. Comparators never burn out; torches do.
- **CLE and ICA use no comparators at all** — both are pure torch logic, which is why
  the CLE needs 113 torches to do what a CCA does with 41.
- **ICA is 8 blocks tall against the CCAs' 20–21**, confirming it is a horizontal
  design where the CCAs are vertical. That dictates how each one tiles.
- **The 3-tick CCA is the smallest of all of them** at 517 blocks — faster *and*
  smaller than the 5-tick, purely through better engineering.

## Other synchronous adders

**Carry look-everywhere** — 4 ticks, 8-bit. Uses glass towers to combine carry
signals from several places at once and control their propagation. Diagonal I/O.

**Instant carry** — 4 ticks, 8-bit. Uses **pistons** to physically block carry
propagation at a chosen point. Horizontal I/O. Pistons introduce timing risk, which
is why CCAs displaced it.

**Carry lookahead (CLA)** — the real-electronics answer; adds logic at the back to
compute all carries at once. Rarely built in redstone because the CCA is better
suited to the medium.

All of these are redstone-specific exploits that have no real-world equivalent —
they abuse signal strength and one-way vertical transmission, which real circuits
don't have.
