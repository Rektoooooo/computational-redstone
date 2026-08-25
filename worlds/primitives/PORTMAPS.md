# I/O port maps

Derived from the interface blocks in each build: levers and buttons are
inputs, lamps and trapdoors are outputs. Collinear runs are multi-bit ports.

**Positions and widths are facts** — read off the blocks. **Bit order is
inferred** (assumed least-significant-first along the run). The source worlds
label bits with `[1][2][4]…[128]` signs, which are the real authority but are
not carried into the `.litematic`. Check ordering before wiring anything.


## addition

- **`3-ticks-8-bit-cca-by-don`** — 17 in / 25 out · ports: out×9(y), inp×8(y), inp×8(y), out×8(y), out×8(y), inp×2(z)
- **`3-ticks-torchless-fearless-8-bit-cca-by`** — 17 in / 25 out · ports: inp×8(y), inp×8(y), out×8(y), out×8(y), out×8(y)
- **`4-ticks-8-bit-cle`** — 17 in / 26 out · ports: inp×2(y), inp×2(y), inp×2(y), inp×2(y), inp×2(y), inp×2(y)
- **`5-ticks-8-bit-cca`** — 17 in / 26 out · ports: inp×8(y), inp×8(y), out×8(y), out×8(y), out×8(y), inp×2(z)
- **`build-02`** — 17 in / 17 out · ports: inp×8(z), inp×8(z), out×8(z), out×8(z)
- **`build-06`** — 9 in / 13 out · ports: inp×2(x), inp×2(x), inp×2(x), inp×2(x), out×2(x)
- **`build-09`** — 2 in / 4 out · ports: inp×2(z), out×2(z)

## alus

- **`build-00`** — 26 in / 34 out · ports: inp×8(y), inp×8(y), out×8(y), out×8(y), out×8(y), inp×2(z)
- **`build-01`** — 27 in / 35 out · ports: inp×11(x), out×11(x), inp×8(y), inp×8(y), out×8(y), out×8(y)
- **`build-02`** — 26 in / 34 out · ports: inp×10(x), out×10(x), inp×8(y), inp×8(y), out×8(y), out×8(y)
- **`build-03`** — 96 in / 144 out · ports: inp×12(x), inp×12(x), inp×12(x), inp×12(x), inp×12(x), inp×12(x)
- **`build-04`** — 18 in / 22 out · ports: inp×10(x), out×10(x)
- **`build-05`** — 21 in / 29 out · ports: inp×8(y), inp×8(y), out×8(y), out×8(y), out×8(y), inp×2(x)
- **`build-06`** — 20 in / 28 out · ports: inp×8(y), inp×8(y), out×8(y), out×8(y), out×8(y), inp×2(x)
- **`build-07`** — 19 in / 27 out · ports: inp×8(y), inp×8(y), out×8(y), out×8(y), out×8(y), inp×2(x)
- **`build-08`** — 17 in / 25 out · ports: inp×8(y), inp×8(y), out×8(y), out×8(y), out×8(y)
- **`build-09`** — 13 in / 17 out · ports: inp×2(z), out×2(z)
- **`build-11`** — 17 in / 25 out · ports: inp×8(y), inp×8(y), out×8(y), out×8(y), out×8(y), inp×2(x)
- **`build-12`** — 17 in / 25 out · ports: inp×8(y), inp×8(y), out×8(y), out×8(y), out×8(y), inp×2(x)
- **`build-14`** — 17 in / 25 out · ports: inp×8(y), inp×8(y), out×8(y), out×8(y), out×8(y), inp×2(x)
- **`build-16`** — 9 in / 14 out · ports: inp×2(y), inp×2(y), inp×2(y), inp×2(y), out×2(y), out×2(y)
- **`build-17`** — 3 in / 4 out · ports: inp×2(x), out×2(x)

## callstack

- **`build-01`** — 12 in / 21 out · ports: inp×10(y), out×10(y), out×10(y), inp×2(y), out×2(z), out×2(z)
- **`build-02`** — 1 in / 2 out · ports: out×2(z)

## combinational

- **`a-gt-b`** — 16 in / 19 out · ports: inp×8(y), inp×8(y), out×8(y), out×8(y), out×3(z), inp×2(z)
- **`build-00`** — 3 in / 7 out · ports: out×4(z), inp×3(z), out×3(z)
- **`build-01`** — 7 in / 13 out · ports: inp×7(z)
- **`build-02`** — 4 in / 4 out · ports: inp×4(y), out×4(y)
- **`build-04`** — 0 in / 4 out · ports: out×4(y)
- **`build-05`** — 4 in / 8 out · ports: inp×4(y), out×4(y), out×4(y)
- **`build-06`** — 4 in / 8 out · ports: inp×4(y), out×4(y), out×4(y)
- **`build-07`** — 4 in / 8 out · ports: inp×4(x), out×4(x), out×4(x)
- **`build-08`** — 0 in / 8 out · ports: out×4(x), out×4(z)
- **`build-09`** — 0 in / 14 out · ports: out×14(x)
- **`build-10`** — 4 in / 8 out · ports: inp×4(y), out×4(x), out×4(y)
- **`build-11`** — 4 in / 8 out · ports: inp×4(z), out×4(y), out×4(z)
- **`build-12`** — 3 in / 6 out · ports: inp×3(z), out×3(x), out×3(z)
- **`build-13`** — 6 in / 7 out · ports: inp×4(z), out×4(z), inp×2(y), out×2(y)
- **`build-14`** — 4 in / 5 out · ports: inp×4(z), out×4(z)
- **`build-15`** — 0 in / 16 out · ports: out×8(y), out×8(y)
- **`build-16`** — 3 in / 7 out · ports: out×4(z), inp×3(y), out×3(y)
- **`build-17`** — 4 in / 7 out · ports: inp×4(x), out×4(x), out×3(z)
- **`build-18`** — 0 in / 4 out · ports: out×4(z)
- **`build-19`** — 4 in / 8 out · ports: inp×4(z), out×4(z), out×4(z)

## cpu-ep04-controlrom

- **`build-00`** — 5 in / 24 out · ports: out×8(y), inp×4(y), out×4(y), out×4(y), out×4(y), out×4(y)
- **`build-01`** — 8 in / 19 out · ports: out×4(y), out×4(y), out×4(y)
- **`build-02`** — 22 in / 37 out · ports: inp×8(y), out×8(y), out×8(y), out×8(y), inp×4(y), inp×4(y)
- **`build-03`** — 16 in / 30 out · ports: inp×8(y), inp×8(y), out×8(y), out×8(y), out×8(y), out×6(z)

## cpu-ep05-instrmem

- **`build-00`** — 11 in / 10 out · ports: inp×10(y), out×10(y)
- **`build-01`** — 11 in / 10 out · ports: inp×10(y), out×10(y)
- **`build-02`** — 10 in / 26 out · ports: inp×10(y), out×10(y)
- **`build-03`** — 10 in / 1034 out · ports: inp×10(y), out×10(y)
- **`build-04`** — 10 in / 26 out · ports: inp×10(y), out×10(y)
- **`build-05`** — 17 in / 16 out · ports: inp×4(y), inp×4(y), inp×4(y), inp×4(y), out×4(y), out×4(y)
- **`build-06`** — 10 in / 138 out · ports: out×128(x), inp×10(y), out×10(y)
- **`build-07`** — 4 in / 20 out · ports: out×16(x), inp×4(y), out×4(y)

## cpu-ep06-progcounter

- **`build-00`** — 1 in / 11 out · ports: out×10(y)
- **`build-01`** — 2 in / 10 out · ports: out×10(y)
- **`build-02`** — 11 in / 10 out · ports: inp×10(y), out×10(y)
- **`build-03`** — 1 in / 10 out · ports: out×10(y)
- **`build-04`** — 11 in / 20 out · ports: inp×10(y), out×10(y), out×10(y)
- **`build-05`** — 0 in / 8 out · ports: out×8(y)
- **`build-06`** — 2 in / 2 out · ports: inp×2(z), out×2(z)

## cpu-ep07-branching

- **`build-00`** — 1 in / 11 out · ports: out×10(y)
- **`build-01`** — 1 in / 11 out · ports: out×10(y)
- **`build-02`** — 0 in / 10 out · ports: out×10(y)
- **`build-03`** — 25 in / 25 out · ports: inp×8(y), inp×8(y), out×8(y), out×8(y), inp×6(z), out×6(z)
- **`build-04`** — 21 in / 24 out · ports: inp×8(y), inp×8(y), out×8(y), out×8(y), inp×4(z), out×4(z)
- **`build-05`** — 23 in / 24 out · ports: inp×8(y), inp×8(y), out×8(y), out×8(y), inp×6(z), out×6(z)
- **`build-06`** — 22 in / 24 out · ports: inp×8(y), inp×8(y), out×8(y), out×8(y), inp×6(z), out×6(z)
- **`build-07`** — 20 in / 22 out · ports: inp×8(y), inp×8(y), out×8(y), out×8(y), inp×4(z), out×4(z)
- **`build-08`** — 8 in / 9 out · ports: inp×8(y), out×8(y)

## cpu-ep09-datamem

- **`build-02`** — 18 in / 17 out · ports: inp×18(y)
- **`build-03`** — 9 in / 519 out · ports: inp×9(y), out×8(y)
- **`build-04`** — 8 in / 264 out · ports: inp×8(y), out×8(y)
- **`build-05`** — 8 in / 20 out · ports: inp×8(y), out×8(y), out×4(y), out×4(y), out×4(y)
- **`build-06`** — 22 in / 37 out · ports: inp×8(y), out×8(y), out×8(y), out×8(y), inp×4(y), inp×4(y)

## cpu-ep10-io

- **`build-03`** — 7 in / 0 out · ports: inp×4(x), inp×2(z)
- **`build-04`** — 7 in / 0 out · ports: inp×4(x), inp×2(z)
- **`build-05`** — 7 in / 0 out · ports: inp×4(x), inp×2(z)
- **`build-06`** — 1 in / 41 out · ports: out×11(z), out×9(z), out×9(z), out×6(z), out×6(z), out×5(y)
- **`build-07`** — 1 in / 256 out · ports: out×16(x), out×16(x), out×16(x), out×16(x), out×16(x), out×16(x)
- **`build-09`** — 14 in / 4111 out · ports: out×64(x), out×64(x), out×64(x), out×64(x), out×64(x), out×64(x)
- **`build-10`** — 8 in / 158 out · ports: out×30(x), out×30(x), out×30(x), out×30(x), out×30(x), inp×5(y)
- **`build-11`** — 10 in / 51 out · ports: out×11(x), out×9(x), out×9(x), inp×8(x), out×8(x), out×6(x)
- **`build-12`** — 64 in / 256 out · ports: out×16(x), out×16(x), out×16(x), out×16(x), out×16(x), out×16(x)
- **`build-13`** — 0 in / 33 out · ports: out×9(x), out×7(x), out×7(x), out×5(x), out×5(x), out×5(y)
- **`build-14`** — 1 in / 8 out · ports: out×8(y)
- **`build-15`** — 4 in / 8 out · ports: out×8(y), inp×4(x)
- **`build-16`** — 1 in / 8 out · ports: out×8(y)

## displays

- **`blank`** — 3 in / 13 out · ports: out×5(y), out×5(y), inp×3(x), out×3(y), out×3(z), out×3(z)
- **`buffer`** — 1 in / 256 out · ports: out×16(y), out×16(y), out×16(y), out×16(y), out×16(y), out×16(y)
- **`build-02`** — 12 in / 268 out · ports: out×16(y), out×16(y), out×16(y), out×16(y), out×16(y), out×16(y)
- **`build-03`** — 12 in / 201 out · ports: out×21(z), out×21(z), out×21(z), out×21(z), out×21(z), out×21(z)
- **`build-09`** — 6 in / 262 out · ports: out×16(y), out×16(y), out×16(y), out×16(y), out×16(y), out×16(y)
- **`build-11`** — 4 in / 49 out · ports: out×9(y), out×9(y), out×9(y), out×9(y), out×9(y), out×5(z)
- **`build-12`** — 4 in / 49 out · ports: out×9(y), out×9(y), out×9(y), out×9(y), out×9(y), out×5(z)
- **`build-14`** — 0 in / 256 out · ports: out×16(y), out×16(y), out×16(y), out×16(y), out×16(y), out×16(y)
- **`build-15`** — 4 in / 49 out · ports: out×9(y), out×9(y), out×9(y), out×9(y), out×9(y), out×5(z)
- **`build-16`** — 4 in / 49 out · ports: out×9(y), out×9(y), out×9(y), out×9(y), out×9(y), out×5(z)
- **`build-17`** — 11 in / 35 out · ports: inp×11(x), out×7(y), out×7(y), out×7(y), out×7(y), out×7(y)
- **`build-19`** — 1 in / 13 out · ports: out×5(y), out×5(y), out×3(y), out×3(z), out×3(z), out×3(z)
- **`build-21`** — 2 in / 24 out · ports: out×12(y), out×12(y)
- **`build-22`** — 8 in / 0 out · ports: inp×2(y), inp×2(y), inp×2(y), inp×2(z), inp×2(z), inp×2(z)
- **`convert`** — 9 in / 198 out · ports: out×21(z), out×21(z), out×21(z), out×21(z), out×21(z), out×21(z)
- **`data`** — 9 in / 263 out · ports: out×16(y), out×16(y), out×16(y), out×16(y), out×16(y), out×16(y)
- **`default-0`** — 10 in / 35 out · ports: inp×9(x), out×7(y), out×7(y), out×7(y), out×7(y), out×7(y)
- **`play-animation`** — 1 in / 256 out · ports: out×16(y), out×16(y), out×16(y), out×16(y), out×16(y), out×16(y)
- **`plot-pixel-2`** — 8 in / 263 out · ports: out×16(y), out×16(y), out×16(y), out×16(y), out×16(y), out×16(y)
- **`plot-pixel`** — 8 in / 262 out · ports: out×16(y), out×16(y), out×16(y), out×16(y), out×16(y), out×16(y)
- **`reset`** — 1 in / 52 out · ports: out×12(z), out×12(z), out×12(z), out×8(z), out×8(z), out×5(y)
- **`sad`** — 3 in / 259 out · ports: out×16(y), out×16(y), out×16(y), out×16(y), out×16(y), out×16(y)
- **`surprised`** — 3 in / 259 out · ports: out×16(y), out×16(y), out×16(y), out×16(y), out×16(y), out×16(y)

## gamedesign

- **`build-01`** — 0 in / 392 out · ports: out×21(x), out×21(x), out×21(x), out×21(x), out×21(x), out×21(x)
- **`build-02`** — 0 in / 200 out · ports: out×15(x), out×15(x), out×15(x), out×15(x), out×15(x), out×15(x)
- **`build-03`** — 0 in / 71 out · ports: out×9(x), out×9(x), out×9(x), out×9(x), out×9(x), out×9(z)
- **`build-04`** — 0 in / 8 out · ports: out×3(x), out×3(x), out×3(z), out×3(z), out×2(x), out×2(z)
- **`reset`** — 1 in / 378 out · ports: out×21(x), out×21(x), out×21(x), out×21(x), out×21(x), out×21(x)

## gates

- **`build-00`** — 12 in / 18 out · ports: inp×4(x), inp×2(x), out×2(x), out×2(x)
- **`build-02`** — 4 in / 6 out · ports: inp×2(x), inp×2(y), out×2(y)
- **`build-03`** — 4 in / 6 out · ports: inp×2(y), out×2(y)
- **`build-04`** — 2 in / 3 out · ports: inp×2(x), out×2(x)
- **`build-05`** — 2 in / 3 out · ports: inp×2(x), out×2(x)
- **`build-06`** — 2 in / 2 out · ports: inp×2(x), out×2(x)
- **`build-07`** — 2 in / 3 out · ports: inp×2(x), out×2(x)
- **`build-08`** — 2 in / 3 out · ports: inp×2(x), out×2(x)
- **`build-10`** — 2 in / 3 out · ports: inp×2(y), out×2(y)

## latches

- **`enable`** — 4 in / 3 out · ports: inp×2(x), out×2(x)
- **`not-output-2`** — 3 in / 4 out · ports: inp×2(x)
- **`not-output-3`** — 0 in / 2 out · ports: out×2(x)

## multiplier

- **`build-00`** — 129 in / 305 out · ports: out×16(y), out×16(y), out×16(y), out×16(y), out×16(y), out×16(y)

## registers

- **`build-00`** — 22 in / 37 out · ports: inp×8(y), out×8(y), out×8(y), out×8(y), inp×4(y), inp×4(y)
- **`build-01`** — 21 in / 36 out · ports: inp×8(y), out×8(y), out×8(y), out×8(y), inp×4(y), inp×4(y)
- **`build-02`** — 17 in / 24 out · ports: inp×8(y), out×8(y), out×8(y), inp×4(y), inp×4(y), out×4(y)
- **`build-04`** — 15 in / 30 out · ports: inp×8(y), out×8(y), out×8(y), out×8(y), inp×2(y), inp×2(y)
- **`build-05`** — 15 in / 120 out · ports: out×8(y), out×8(y), out×8(y), out×8(y), out×8(y), out×8(y)
- **`build-06`** — 15 in / 30 out · ports: inp×8(y), out×8(y), out×8(y), out×8(y), inp×2(y), inp×2(y)
- **`build-07`** — 13 in / 20 out · ports: inp×8(y), out×8(y), out×8(y), inp×2(y), inp×2(y), out×2(y)
- **`build-08`** — 11 in / 42 out · ports: inp×8(y), out×8(y), out×8(y), out×8(y), out×8(y), out×8(y)
- **`build-09`** — 12 in / 40 out · ports: inp×8(y), out×8(y), out×8(y), out×8(y), out×8(y), out×8(y)
- **`build-10`** — 11 in / 34 out · ports: inp×8(y), out×8(y), out×8(y), out×8(y), out×8(y), inp×2(y)
- **`build-11`** — 9 in / 16 out · ports: inp×8(y), out×8(y), out×8(y)
- **`build-12`** — 1 in / 8 out · ports: out×8(y)
- **`build-13`** — 3 in / 2 out · ports: inp×2(y), out×2(y)
- **`build-14`** — 9 in / 16 out · ports: inp×8(y), out×8(y), out×8(y), out×2(x), out×2(x), out×2(x)
- **`build-15`** — 3 in / 2 out · ports: inp×2(y), out×2(y)
- **`build-16`** — 2 in / 2 out · ports: inp×2(y), out×2(y)

## sequential

- **`add-to-total`** — 10 in / 16 out · ports: inp×9(y), out×8(y), out×8(y), out×2(z), out×2(z), out×2(z)
- **`build-04`** — 2 in / 8 out · ports: out×8(z)
- **`build-14`** — 1 in / 5 out · ports: out×4(z)
- **`count-2`** — 1 in / 8 out · ports: out×8(y)
- **`count-4`** — 1 in / 4 out · ports: out×4(y)
- **`count`** — 10 in / 16 out · ports: inp×10(y), out×8(y), out×8(y)
- **`load-2`** — 10 in / 16 out · ports: inp×8(y), out×8(y), out×8(y), inp×2(z)
- **`load-3`** — 10 in / 16 out · ports: inp×8(y), out×8(y), out×8(y), inp×2(z)
- **`load`** — 20 in / 36 out · ports: inp×8(y), inp×8(y), out×8(y), out×8(y), out×8(y), out×8(y)
- **`read`** — 13 in / 21 out · ports: inp×13(y), out×13(y), out×8(y)
- **`shift-down-2`** — 2 in / 9 out · ports: out×8(y)
- **`shift-down`** — 11 in / 16 out · ports: inp×8(y), out×8(y), out×8(y), inp×3(z)
- **`shift-up`** — 2 in / 9 out · ports: out×8(y), inp×2(y)

## subtraction

- **`on-a-b-off-a-plus-b`** — 9 in / 13 out · ports: inp×4(y), inp×4(y), out×4(y), out×4(y), out×4(y), inp×2(z)

## uis

- **`1`** — 44 in / 9 out · ports: inp×12(x), inp×11(x), inp×11(x), inp×10(x), out×5(z), out×4(y)
- **`backspace`** — 54 in / 2 out · ports: out×2(y)
- **`build-06`** — 8 in / 7 out · ports: inp×4(x), inp×4(x), out×3(x), inp×2(y), inp×2(y), inp×2(y)