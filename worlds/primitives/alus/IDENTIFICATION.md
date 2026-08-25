# The ALUs world — visual identification

`ALUs by mattbatwings` contains **18 builds and zero signs**. It is the most valuable
world for CPU work and the only one with no ground truth at all.

These identifications come from **rendering each build and reading its structure**
against what LMRC #2 says should be there. That is inference, not fact. Structural
inference has been wrong before, so each entry carries an explicit confidence and the
evidence it rests on. **An in-world sign would beat any of this** — none exist here.

Renders: `build-XX.svg` alongside each manifest. Regenerate with `render.py`.

---

## High confidence

### `build-03` — the six bitwise logic gates, 8 bits each
**34×19×15 · 776 components · 96 inputs / 144 outputs**

The render is unambiguous: **six identical columns across eight layers = 48 units**,
each with two levers and an output lamp. 6 × 8 × 2 = 96 levers, 48 × 3 = 144 lamps —
matching the measured port map exactly.

LMRC #2: *"these six circuits are the six main kinds of bitwise logic — OR, AND, XOR,
NOR, NAND, XNOR."* Six gate types applied bitwise across a byte.

### `build-00` — the brute-force ALU
**41×24×27 · 2986 components · 178 comparators, 474 repeaters**

The largest build in the world. The render shows **long horizontal dust rails spanning
the full width** with regular vertical drops feeding roughly eight parallel vertical
units, and a dense comparator block on one side.

That is precisely the described construction: *"this circuit duplicates A into all the
A inputs and then does the same for B… then I have comparators on every output with
each one being cancelled by a tower of repeaters."* The 474 repeaters are those cancel
towers.

### `build-17` — a 3-input XOR (odd parity) — **measured in game**
**9×8×18 · 44 components · 0 comparators, 0 repeaters, 12 torches**

**Three** levers, four lamps. Two levers sit at one end, each with an indicator lamp
directly beneath it; the third is mounted on top of its own indicator lamp off to one
side, and feeds the same circuit. The remaining lamp, alone at the far end, is the
output.

Output is on when an **odd** number of inputs is on — consistent with the SUM output of
a full adder, which is exactly what belongs in an ALU world.

Driven through its truth table in Minecraft 1.18.2 on 2026-08-25. Both inputs on gives
output **off**; each single input on gives output **on**. Five of the eight rows were
observed directly, with A and B read off their indicator lamps and C inferred from the
output. The simulator predicted every observed row correctly.

> **This entry previously read "a single AND gate", at confidence `high`.** That was
> wrong, and instructively so. It was inferred from visual structure — "the textbook De
> Morgan construction" — and the shape of an AND gate and a XOR gate built this way are
> genuinely similar. Two things should have caught it earlier: the reading claimed *two*
> levers when the build plainly has three, and no one had ever driven it. Both inputs
> on producing an output of **off** rules an AND gate out outright.

---

## Medium confidence

### `build-09`, `build-10`, `build-13`, `build-15`, `build-04` — the RCA-based ALU, in stages
**~22×12×27 · 280–638 components · torch-dominant (53–93), few comparators**

All flat (10–12 tall) where the CCA builds are 20+ tall, with long horizontal
distribution rails and four repeating units — a **4-bit ripple-carry** layout.

Component counts climb steadily: 280 → 334 → 359 → 380 → 638. LMRC #2 builds a 4-bit
RCA and then adds control signals one at a time (invert B and carry-in for subtraction,
then invert A, then flood carry, then xor→or). These look like **successive stages of
that same device**, which would explain five near-identical builds of increasing size.

*Weaker point:* the mapping of which build is which stage is not established.

### `build-11`, `build-12`, `build-14` — 8-bit carry-cancel adders
**~8×23×21 · 307–357 components · 41 comparators each**

Tall and narrow, with an 18-layer structure repeating on a strict **2-block period** —
one module per bit, eight bits. Glass columns plus subtract-mode comparators is the
carry-cancel signature from `redstone-arithmetic`.

All three carry exactly 41 comparators, suggesting three variants of one design rather
than three different devices.

### `build-05`, `build-06`, `build-07`, `build-08` — CCA-based ALUs
**~13×23×23 · 481–576 components · 57–81 comparators**

Same vertical bit-stacked form as the group above but consistently larger, with 57–81
comparators against 41. Reads as **a CCA with ALU control logic added** — which is the
design the series settles on for the actual computer.

### `build-01`, `build-02` — ALU with operation selector
**35–37×24×26 · 853–1100 components**

Alone among the 8-bit builds, these carry an **extra wide port** (`in11` and `in10`)
beyond the two 8-bit data inputs. That is the shape of an operation selector or control
ROM output feeding the ALU's control lines.

### `build-16` — a four-gate demonstration board
**23×10×19 · 180 components · 0 comparators, 0 repeaters, 48 torches**

Four parallel identical structures, each with a lever pair and lamp; port map reads
`in2 in2 in2 in2`. Pure torch logic, so from the OR/NOR/NOT family rather than anything
comparator-based.

---

## Summary

| Build | Reading | Confidence |
|---|---|---|
| `build-17` | **3-input XOR (odd parity)** | **measured in game** |
| `build-03` | six bitwise gates × 8 bits | high — *unverified* |
| `build-00` | brute-force ALU | high — *unverified* |
| `build-04/09/10/13/15` | 4-bit RCA ALU, successive stages | medium |
| `build-11/12/14` | 8-bit carry-cancel adders | medium |
| `build-05/06/07/08` | CCA-based ALUs | medium |
| `build-01/02` | ALU with operation selector | medium |
| `build-16` | four-gate demo board | medium |

**All 18 accounted for. One measured, seventeen still guesses.**

`build-17` is the only one that has been driven, and it came back **wrong** — read as a
single AND gate at confidence `high`, and it is a 3-input XOR. Treat every remaining
row here as a lead, not a label. In particular:

- **`high` did not mean reliable.** The two remaining `high` readings deserve the same
  suspicion as the `medium` ones until something drives them.
- **The tell was in the data, not the shape.** The wrong entry described *two* levers
  for a build with three. Where a reading contradicts the measured port map or census,
  the measurement wins.
- **Driving a build is cheap now.** `verify/` predicts a truth table offline and the
  build pastes into the game in a couple of minutes. That is how these get settled.

## How to settle it

Open `ALUs by mattbatwings` in Minecraft and fly the row. Ten minutes there beats any
amount of structural inference — and if the builds turn out to carry item-frame or
book labels rather than signs, the harvester could be extended to read those too.
