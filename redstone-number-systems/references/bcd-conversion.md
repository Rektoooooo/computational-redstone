# BCD conversion algorithms

## Binary → BCD: double dabble (shift and add 3)

Needed whenever a binary result must appear on a decimal display.

### The rule

Feed the binary number in from the left, one bit at a time, shifting through a
chain of 4-bit BCD digit cells. At each stage, **every 4-bit cell asks one question:**

> If my value is greater than 4, add 3 to it. Otherwise do nothing.

That is the entire algorithm. Repeated for every bit, across every digit, it emits
correct BCD.

### Why add 3

A BCD digit must roll over at 10, but a 4-bit binary cell rolls over at 16. Adding
3 before a shift (which doubles the value) pre-compensates: `(x+3)×2 = 2x+6`, and 6
is exactly the gap between 16 and 10. The `>4` test identifies the values that are
about to exceed 9 after the shift.

### Worked example — 16

The cell sees `8`. 8 > 4, so add 3 → 11, which is `1011` = an 8, a 2 and a 1.
Reading the digit columns out gives **1** and **6**. Correct.

### Worked example — 64

Bits propagate right to left. The cells see 1, 2, 4 in turn and pass them through
unchanged (all ≤ 4). The next sees 8 → 8 > 4 → outputs 11.
Then one cell sees 6 → 6 > 4 → 6 + 3 = 9; the neighbour sees 1 and passes it.
Next stage: a cell sees 3 (unchanged), one sees 2 (unchanged).
Final BCD digits: `0110` `0100` = **6** and **4**.

### In redstone

Build **one** "if >4 add 3" cell and replicate it across the schematic grid. A
16-bit input needs a large array producing five BCD digits, but each individual
cell can be as fast as **2 ticks**, so the whole converter stays quick despite its
size.

Two build options: copy a known-optimal cell design, or build your own from a
decoder plus encoder — bigger and slower, but it works as long as the array layout
follows the schematic.

### Wiring warning

Both the overall digit order and the bit order *within* each 4-bit digit commonly
come out reversed relative to the display's inputs. You will likely need a
reversing stage at both levels. **Test each output line individually** — light one
input, confirm exactly one expected repeater responds, and walk down the whole
array. Debugging this after the fact is miserable.

---

## BCD → binary: ×10 accumulation

Needed to turn keypad digits into a number you can compute with. This is Horner's
method: `123 = ((1 × 10) + 2) × 10 + 3`.

### The loop

Keep a running total. For each new digit typed:

```
total = (total × 10) + new_digit
```

One adder, with its output routed back to its own input through a ×10 stage.

| Typed | Fed back | Adder | Total |
|---|---|---|---|
| 1 | 0 | 0 + 1 | 1 |
| 2 | 10 | 10 + 2 | 12 |
| 3 | 120 | 120 + 3 | 123 |

### ×10 without a multiplier

Do not build a multiplier. **Shifting up n places multiplies by 2ⁿ**, so:

> ×10 = (shift up 1) + (shift up 3) — that is ×2 + ×8

Wire the output into the adder's two inputs at offsets of 1 and 3 bits. Free.

The same trick generalises. The calculator's division stage needs ×100:

> ×100 = (shift up 2) + (shift up 5) + (shift up 6) — that is ×4 + ×32 + ×64

which needs two chained adders to sum three terms.

### The 8-bit ceiling

With an 8-bit accumulator the maximum is 255. Typing a fourth digit overflows
silently. This is why calculators of this design cap input at 255 — it is a direct
consequence of accumulator width, not an arbitrary limit.

### Clearing

Letting the loop drain naturally is slow — the value circulates for a long time.
Instead, cut the loop physically (a piston retracting the feedback line, or
cancelling comparators) so the value flows out and dies immediately.
