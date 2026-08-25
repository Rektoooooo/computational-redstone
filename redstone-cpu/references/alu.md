# The ALU

## Two approaches

### Brute force — easiest

Duplicate both inputs into every function unit (one adder, one subtractor, six
bitwise gate stacks), then put a cancelling comparator on each output and release
only the one you want. The ALU computes everything every time; you discard the rest.

Straightforward, and adding or removing an operation is easy. Recommended if you
just want a working ALU without much thought.

### One modified adder — what to actually build

Far smaller and faster. **Six control signals** turn a single carry-cancel adder into
its full operation set. Five of them shape the adder; the sixth selects the shifted
output path.

| Signal | Effect |
|---|---|
| `invert A` | inverters on the A input |
| `invert B` | inverters on the B input |
| `carry in` | power the bottom of the carry tower |
| `flood carry` | force **every** carry-in to 1 |
| `OR` (xor → or) | convert the first XOR to an OR **and** force all carries to 0 |
| `right shift` | select the right-shifted output instead of the normal one |

> **Verified in-world.** The *Computer v2* ALU carries exactly these six labels on
> signs at x=161: `Right Shift`, `Flood Carry`, `Carry In`, `OR`, `Invert A`,
> `Invert B`. Note the machine treats right shift as a control bit alongside the
> other five, rather than as separate hardware.

## The function table

| Operation | invert A | invert B | carry in | flood carry | xor→or |
|---|---|---|---|---|---|
| ADD | | | | | |
| SUB | | ✓ | ✓ | | |
| XOR | | | | ✓ | |
| XNOR | | ✓ | | ✓ | |
| OR | | | | | ✓ |
| NOR | | | | ✓ | ✓ |
| AND | ✓ | ✓ | | ✓ | ✓ |
| NAND | ✓ | ✓ | | | ✓ |

Plus `IMPLY` and its negation as a bonus from other combinations, and a right shift
handled separately (below).

## Why each trick works

### Subtraction

`A − B = A + (~B) + 1`. Invert B, set carry in. Standard two's complement.

### Flood carry gives XOR

Each sum bit computes `A ⊕ B ⊕ C`. Forcing every `C` to 1 gives `A ⊕ B ⊕ 1`, and
XOR with 1 is inversion — so the output becomes `XNOR(A, B)`.

To get plain **XOR**, invert one of the inputs as well: inverting one input of an
XOR inverts its output, so `XNOR` becomes `XOR`.

This is the same identity used to build XNOR in `redstone-logic-gates`, applied
across a whole bus.

### xor→or is doing two jobs

Powering one dust in the first XOR structure converts it into an OR. But it *also*
disables the AND torch that forms the first term of the carry equation.

That second effect is the important one and is easy to miss. With that torch
disabled, the carry-out equation changes so that if the first carry-in is 0, the
first carry-out is 0 — which makes the next carry 0, and so on. **Every carry
becomes 0.**

Carries are exactly what makes an adder *not* bitwise. Killing them turns the adder
into eight independent gates. That is why one control signal gives you the whole
OR/NOR/AND/NAND family: they are all an OR with different inversions.

- **OR** — no inversions
- **NOR** — invert the output (flood carry)
- **AND** — invert inputs and output (De Morgan)
- **NAND** — invert inputs only

## Applying it to a carry cancel adder

The reference CPU uses the CCA version. Each control signal maps cleanly:

| Signal | On a CCA |
|---|---|
| carry in | power the bottom of the carry tower |
| invert A / invert B | inverters on the front of each input |
| flood carry | a tower of repeaters forcing all carries to 1 in the final XOR |
| xor → or | remove the dust that makes the XOR, wire it to the output; when the comparator is uncancelled it overrides with the OR |

## Shifting

**Left shift needs no hardware.** `x + x = 2x`, so feed the same value into both
inputs and add.

**Right shift does.** Split the output into two paths — normal and right-shifted —
and select between them with a control bit. Doing the shift at the *output* means it
can compose with any other operation, though a CPU normally performs one at a time.

## Control ROM

Rather than setting five levers by hand, build a **ROM**: a decoder on the operation
selector with torches placed to raise the correct control lines. Selecting `SUB`
automatically raises `invert B` and `carry in`.

In a full CPU this ROM is driven by the instruction's opcode, and it *is* the
physical embodiment of the instruction set — changing which torches are placed
changes what the machine's instructions do.

## The machine's full control-signal set

Beyond the ALU's own six, the *Computer v2* control ROM drives 22 labelled lines,
read off the signs at x=175. Useful as a checklist when designing your own control ROM
— it shows exactly what a working single-cycle machine needs to control:

| Group | Signals |
|---|---|
| ALU | `right shift`, `flood carry`, `carry in`, `or`, `invert a`, `invert b` |
| Operand routing | `B/(imm/offset)`, `imm/offset` |
| Destination select | `dest A`, `dest B`, `dest C` |
| Write-back source | `ir data mem`, `ir alu`, `ir imm` |
| Program counter | `pc+1`, `jmp/cal`, `return` |
| Call stack | `push`, `pop` |
| Memory | `mem read`, `enable mem wb` |
| Flags | `set flags` |

Three observations worth carrying into your own design:

- **Destination is a three-way select** (`dest A/B/C`), not the two-way mux the video
  series describes. `LOD` writes to register B, which needs its own path.
- **Write-back source is also three-way** (`ir data mem` / `ir alu` / `ir imm`) —
  results can come from memory, the ALU, or an immediate.
- **`set flags` is an explicit control bit**, confirming that only ALU-using
  instructions disturb the flags.
