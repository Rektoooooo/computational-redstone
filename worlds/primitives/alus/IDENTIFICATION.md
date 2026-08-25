# The ALUs world — visual identification

`ALUs by mattbatwings` contains **18 builds and zero signs**. It is the most valuable
world for CPU work and the only one with no ground truth at all.

Most identifications here come from **rendering each build and reading its structure**
against what LMRC #2 says should be there. That is inference, not fact, and two of the
first three builds to be driven turned out wrong.

**Driving a build beats any amount of looking at it**, and now costs seconds:

```bash
python3 verify/drive.py worlds/primitives/alus/build-16.litematic
```

Entries marked **driven** or **measured in game** are results. Everything else carries
an explicit confidence and the evidence it rests on, and should be read as a lead.

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

### `build-15` — a 4-bit adder/subtractor — **driven, all four modes**
**Ten levers: four A/B bit pairs, plus two controls.**

Lever 8 is the **carry-in**; lever 9 **inverts A**. Every one of the four modes checked
over all 256 input pairs:

| carry-in | invert A | computes |
|---|---|---|
| 0 | 0 | `A + B` |
| 1 | 0 | `A + B + 1` |
| 0 | 1 | `~A + B` |
| 1 | 1 | `~A + B + 1` = **`B - A`** |

That last row is two's complement subtraction, which is what makes this an ALU rather
than an adder: invert one operand and set the carry. The "4-bit RCA-based ALU" reading
below was broadly right; this is the precise version.

### The RCA family, driven — one control added at a time

Four of these have now been driven, and they are **successive stages of one device**,
exactly as the guess below supposed. Each adds a single control line to the last:

| build | controls | what it can do |
|---|---|---|
| `build-16` | carry-in | `A+B`, `A+B+1` |
| `build-15` | + invert A | adds `~A+B`, and `B−A` |
| `build-13` | + invert B | adds `A+~B`, `A−B`, `~A+~B` |
| `build-10` | + logic mode | adds bitwise `A XNOR B`, and `A XOR B` with either invert |

Every setting was checked over all 256 operand pairs. The progression is the reason
five near-identical builds of increasing size sit in this world: it is one ALU being
built up on camera, saved at each step.

`build-10`'s fourth control is the interesting one — it switches the adder out of
arithmetic entirely and into bitwise logic, which is what turns an adder into an ALU.

### `build-09`, `build-04` — the same family, further along
**~22×12×27 · 280–638 components · torch-dominant (53–93), few comparators**

All flat (10–12 tall) where the CCA builds are 20+ tall, with long horizontal
distribution rails and four repeating units — a **4-bit ripple-carry** layout.

Component counts climb steadily: 280 → 334 → 359 → 380 → 638. LMRC #2 builds a 4-bit
RCA and then adds control signals one at a time, and driving four of them confirmed
exactly that — see the table above. These two are the remaining stages; `build-04` is
the largest at 638 components, so it is presumably the furthest along.

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

### `build-16` — a 4-bit ripple-carry adder — **driven, all 512 cases**
**23×10×19 · 180 components · 0 comparators, 0 repeaters, 48 torches**

Nine levers: four A/B bit pairs and a carry-in. Nine of the fourteen lamps are input
indicators; the four real outputs are the sum bits.

Driven over every combination of A (0–15), B (0–15) and carry-in: **512/512 produce
`(A + B + Cin) mod 16`.**

> **This entry previously read "a four-gate demonstration board".** The four "parallel
> identical structures" are real — they are the four bit-stages — but they are not
> independent, and that is the whole difference. Each output depends on its own lever
> pair *and every higher-numbered one*, which is a carry chain. A visual read cannot
> see that, because the carry is the one wire that makes four gates into an adder.
> Driving it takes seconds and settles it outright.
>
> **Confirmed in game.** Both levers on at each of the two LEFT stations - A=12, B=12,
> so 12+12=24, which in four bits is 8: only the leftmost lamp. That observation
> refutes the old reading by itself. Those two stations have *identical* local inputs,
> both levers on, so four independent gates would have to give identical outputs. One
> is lit and the other dark, and the only thing separating them is the carry arriving
> from the right: bit 2 is `1 XOR 1 XOR 0` = 0, bit 3 is `1 XOR 1 XOR 1` = 1.

---

## Summary

| Build | Reading | Confidence |
|---|---|---|
| `build-17` | **3-input XOR (odd parity)** | **measured in game** |
| `build-03` | six bitwise gates × 8 bits | high — *unverified* |
| `build-00` | brute-force ALU | high — *unverified* |
| `build-16` | **4-bit ripple-carry adder** | **driven, 512/512** |
| `build-15` | **4-bit adder/subtractor**, +invert-A | **driven, 4×256** |
| `build-13` | **the same**, +invert-B | **driven, 8×256** |
| `build-10` | **4-bit ALU**, +logic mode (XOR/XNOR) | **driven, 16×256** |
| `build-04/09` | same family, further along | medium — *unverified* |
| `build-11/12/14` | 8-bit carry-cancel adders | medium — *unverified* |
| `build-05/06/07/08` | CCA-based ALUs | medium — *unverified* |
| `build-01/02` | ALU with operation selector | medium — *unverified* |

**All 18 accounted for. Five driven, thirteen still guesses.**

Of the five that have been driven, **two came back outright wrong** and three were
the right family but too vague to use:

| build | was read as | actually is |
|---|---|---|
| `build-17` | single AND gate (`high`) | 3-input XOR |
| `build-16` | four-gate demo board (`medium`) | 4-bit ripple-carry adder |
| `build-15` | 4-bit RCA ALU (`medium`) | adder/subtractor: +carry-in, +invert-A |
| `build-13` | 4-bit RCA ALU (`medium`) | the same, +invert-B |
| `build-10` | 4-bit RCA ALU (`medium`) | the same, +logic mode |

Both outright failures share a shape: the visual read saw the *parts* correctly and missed how
they were *joined*. A De Morgan AND and a XOR look alike; four adder stages look like
four gates until you notice the carry between them. Structure is visible in a render;
connection often is not.

Treat every undriven row here as a lead, not a label. In particular:

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
