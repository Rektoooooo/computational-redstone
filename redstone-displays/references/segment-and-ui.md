# Seven-segment detail and interface polish

## BCD → seven segment

One converter per decimal digit. Internally: a decoder detecting each value 0–9
(or 0–F), and a glass tower per value encoding which segments to light.

Values above 9 show blank if you only decode 0–9. Adding six more lines for A–F
turns it into a **hex to seven segment** converter with **no extra input bits** —
4 bits already spans 0–F exactly.

### Multi-digit numbers

Place converters side by side, one per BCD digit. Feeding `1`, `2`, `3` displays
"123".

Combine with a signal-strength-to-binary converter and you can display a raw dust
signal: strength 12 displays as `C`.

## Leading-zero suppression

Untreated, a display shows `00123`. Fixing it:

1. **Always cancel the leading digit's zero** — there is no case where the leftmost
   digit should display a zero.
2. **Build a chain**: OR all segments of a digit into a torch to detect "this digit
   is non-zero". If digit *n* is blank, permit digit *n+1* to blank too.

The chain propagates left to right so `00123` shows `123`, while `10000` still shows
all five digits — a zero after a non-zero digit must stay visible.

With a decimal point present the logic shifts: digits after the point must always
show, so force those lines on.

## Decimal points and symbols

A decimal point is just a block with a torch, placed between two digits and gated by
whichever mode needs it. In a calculator it can be entirely **cosmetic** — the
divider computes `200 ÷ 3 = 66` and the point is switched on by division mode,
displaying `0.66` without any fractional arithmetic existing.

### Symbol switcher

Showing `+`, `−`, `×`, `÷` in one 5×5 area. Decompose into nine controllable
segments (three rows of three), then encode each symbol as a combination:

| Symbol | Segments |
|---|---|
| `+` | top-middle, all of middle row, bottom-middle |
| `−` | middle row only |
| `×` | four corners plus centre |
| `÷` | the diagonal |

An encoder maps the four mode lines to these combinations.

### Negative sign

Reuse a segment of a digit position that the operation doesn't need. Drive it from
the subtractor's **carry-out, inverted** — carry-out 0 means the result is negative.
Then cancel that line whenever any other mode is active, so it only appears during
subtraction.

## Mode selection wiring

A mode selector usually has to do several things at once. Map them explicitly before
wiring — a table like this prevents most of the mistakes:

| Mode | Show symbol | Unlock answers | Trigger | Clear others |
|---|---|---|---|---|
| Add | `+` | adder | — | multiplier, divider |
| Subtract | `−` | subtractor | — | multiplier, divider |
| Multiply | `×` | multiplier | calculate | divider |
| Divide | `÷` | divider | calculate + decimal point | multiplier |

**Pulse-length mismatch:** a mode line stays high for as long as the mode is
selected, but iterative units expect a **10-tick button pulse**. Put a 10-tick pulse
generator between the mode line and each calculate/clear input, or the multiplier
and divider will never trigger correctly.

**Always clear the units you are not using.** Switching modes while a divider holds
stale state produces confusing wrong answers.

## Master bus

With several units producing answers, run one shared output bus and give each unit a
**cancellation tower**. Only the selected mode's tower is released. Line every unit's
output up to the correct bit level on the bus — this is fiddly, error-prone wiring
and worth testing one bit at a time.

## Testing discipline

For any wide converter or reverser, **test each line individually**: activate one
input, confirm exactly the one expected output responds, then walk down the whole
array. Bit-order reversal between stages is extremely common — both the digit order
*and* the bit order within each digit frequently come out backwards — and finding
that after everything is connected is miserable.
