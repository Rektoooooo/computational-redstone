# Multiplication and division

Both are **iterative**: an adder or subtractor on a loop, one cycle per bit. Neither
is combinational, so both need calculate/clear controls and a loop timer.

---

## Multiplication — shift and add

### On paper

Binary long multiplication is easier than decimal, because each partial product is
either a copy of the number or nothing.

`1101 × 1011` (13 × 11):

```
        1101
      × 1011
      ------
        1101     <- bit 0 is 1 -> copy
       0000      <- bit 1 is 0 -> nothing
      1101       <- bit 1 -> copy, shifted
     1101        <- bit 1 -> copy, shifted
     --------
    10001111     = 143
```

So: **take the first number, shift it repeatedly, and include it only where the
second number has a 1.**

### The circuit

An adder whose output feeds back to its own input, plus:

- A **gate on the A input**, controlled by the current lowest bit of B. Bit is 1 →
  A passes. Bit is 0 → cancel A, adding nothing this cycle.
- A **shift register holding B**, shifted right one place per cycle
- A **recorder** capturing the accumulator's lowest bit each cycle — these captured
  bits, in order, are the product

### Worked example — 5 × 5

| Cycle | B's low bit | Adder does | Records |
|---|---|---|---|
| 1 | 1 | 5 + 0 = 5 | 1 |
| 2 | 0 | 0 + 2 = 2 | 0 |
| 3 | 1 | 5 + 1 = 6 | 1 |

Result `11001` = 25.

### Build notes

- Two 8-bit inputs → up to a **16-bit** result (in practice signs are labelled 1
  through 32768).
- The gating tower has **one level per cycle**, each level coded with the
  corresponding bit of B. A spiral connects every level to a cancelling comparator.
- Needs a **loop timer** whose repeater delay exactly matches one cycle's duration,
  and a counter that stops after 8 cycles.
- **Clear** must retract the pistons cutting the loop, unlock the answer registers,
  and drain the lines — otherwise stale values corrupt the next run.

**Debugging tip:** before wiring the per-cycle gate, the machine multiplies A by
`11111111`. If your untested build outputs A × 255, the gating tower simply is not
connected yet — that is the expected intermediate state.

---

## Division — shift and conditional subtract

### On paper

`25 ÷ 5`:

Bring digits down one at a time, and at each step ask whether the divisor fits.

```
 5 ) 11001
     1        -> 5 into 1?  no  -> 0
     11       -> 5 into 3?  no  -> 0
     110      -> 5 into 6?  yes -> 1, subtract -> 1
     ...
```

Reframed for hardware: **shift the dividend in from the left, one bit per cycle,
and each cycle try to subtract the divisor.**

### The key shortcut

A subtractor's **carry-out is already the answer** to "could I subtract?" — it is 1
when the result is non-negative. So:

> **carry-out = quotient bit**

No comparator, no magnitude check. Wire the carry-out straight to the quotient
recorder *and* to the selector that decides whether to keep the difference or the
original value.

### Worked example — 27 ÷ 6

| Cycle | Holding | 6 fits? | Quotient bit | New value |
|---|---|---|---|---|
| 1 | 1 | no | 0 | 1 |
| 2 | 3 | no | 0 | 3 |
| 3 | 6 | yes | 1 | 0 |
| 4 | 1 | no | 0 | 1 |
| 5 | 3 | no | 0 | 3 |

Quotient `00100` = 4, remainder 3. Correct.

### Build notes

- Build the **conditional subtractor** first: a CCA with carry-in on and all B
  inputs inverted. Test it standalone.
- Two cancellation paths, selected by carry-out: one keeps the difference, one keeps
  the original. Four cancellation towers total (two per half of a 16-bit build).
- Chaining two 8-bit halves needs the lower half's carry-out driving the upper
  half's carry-in.
- Loop period in the reference build is **14 ticks**, and a 16-bit divide runs 16
  cycles — about **24 seconds** in vanilla. Division is by far the slowest operation.

### Divide by zero

**The output goes all 1s.** Zero can always be subtracted, so every cycle reports
success. There is no hardware guard — clear with a non-zero divisor, or add an
explicit zero check.

---

## Multiply by a constant — no multiplier needed

Decompose into shifts and adds.

| Constant | Decomposition | Shifts |
|---|---|---|
| ×2 | 2 | 1 |
| ×10 | 8 + 2 | 3, 1 |
| ×100 | 64 + 32 + 4 | 6, 5, 2 |

Two terms need one adder; three terms need two chained adders. This is how the
calculator's BCD input stage and its decimal-faking divider stage both work,
without a multiplier anywhere in sight.
