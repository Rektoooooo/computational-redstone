# Instruction set and assembly language

Based on the BatPU-2 reference machine. Instruction format is **16 bits**:
4-bit opcode, then operands.

## The 16 instructions

| Op | Mnemonic | Operands | Meaning |
|---|---|---|---|
| 0 | `NOP` | — | do nothing |
| 1 | `HLT` | — | stop the clock |
| 2 | `ADD` | A B C | C = A + B |
| 3 | `SUB` | A B C | C = A − B |
| 4 | `NOR` | A B C | C = A NOR B |
| 5 | `AND` | A B C | C = A AND B |
| 6 | `XOR` | A B C | C = A XOR B |
| 7 | `RSH` | A C | C = A >> 1 |
| 8 | `LDI` | A imm8 | A = immediate |
| 9 | `ADI` | A imm8 | A = A + immediate |
| 10 | `JMP` | addr10 | PC = address |
| 11 | `BRH` | cond addr10 | if condition, PC = address |
| 12 | `CAL` | addr10 | push PC+1, PC = address |
| 13 | `RET` | — | PC = pop |
| 14 | `LOD` | A B [off] | B = memory[A + offset] |
| 15 | `STR` | A B [off] | memory[A + offset] = B |

> **Verified against the machine itself.** The control ROM in the *Computer v2* world
> carries a sign per row at z=−24, in opcode order:
> `nop add sub nor and xor rsh ldi adi jmp brh cal ret lod str`.
> That confirms NOR=4 and AND=5, which the video series never states outright.
> `HLT` (1) has no ROM sign because it stops the clock rather than driving control bits.

Notes:
- `RSH` has no B operand — those bits are forced to zero
- `LOD`/`STR` offsets are **4-bit signed two's complement**, range −8..+7
- The offset is optional in assembly; omitted means 0
- The offset modifies the *pointer only*; register A is unchanged

## Condition codes for BRH

Two bits, four conditions, each with several accepted spellings:

| Condition | Aliases |
|---|---|
| zero flag set | `eq` `=` `z` `zero` |
| zero flag clear | `ne` `!=` `nz` `notzero` |
| carry flag set | `ge` `>=` `c` `carry` |
| carry flag clear | `lt` `<` `nc` `notcarry` |

The comparison spellings only make sense when a `SUB` or `CMP` immediately precedes
the branch.

## Pseudo-instructions

Assembler conveniences that compile to real instructions:

| Written | Becomes | Notes |
|---|---|---|
| `INC rX` | `ADI rX 1` | |
| `DEC rX` | `ADI rX 255` | 255 is −1 in 8-bit two's complement |
| `CMP rX rY` | `SUB rX rY r0` | result discarded into the zero register |

`DEC` is worth understanding rather than memorising: adding 255 to 5 gives 260, and
260 mod 256 = 4. The discarded overflow *is* the decrement. It also explains why
`DEC` sets the carry flag on every value except zero — a detail that enables a
one-instruction-shorter loop idiom.

## Assembly syntax

Opcode first, then operands, **in the same order as the machine code bits**.

```
ADD r1 r2 r3        // r1 + r2 -> r3
```

- **Registers:** `r0` through `r15`
- **Immediates:** decimal, or `0b` binary, or `0x` hex
- **Characters:** `'A'` or `"A"` resolves to its character code
- **Ports:** the port name with underscores — `clear_screen_buffer` → 246
- **Comments:** `//` to end of line

### Labels

Start with a dot. On their own line or before an instruction. Resolve to an
**absolute** address (all jumps are absolute).

```
LDI r1 10
.loop
DEC r1
BRH zero .exit
JMP .loop
.exit HLT
```

Labels are the software fix for direct jumping's weakness: insert a line at the top
and every hardcoded address would break, but labels re-resolve automatically.

### Definitions

```
define my_value 3
```

Can appear anywhere, including after first use — the assembler resolves all symbols
before substituting.

## Memory-mapped I/O ports

Addresses 240–255. All reachable from base pointer 248 with offsets −8..+7.

| Addr | Name | Dir | Purpose |
|---|---|---|---|
| 240 | pixel_x | store | X coordinate (bottom 5 bits) |
| 241 | pixel_y | store | Y coordinate (bottom 5 bits) |
| 242 | draw_pixel | store | draw at (x,y) in buffer |
| 243 | clear_pixel | store | clear at (x,y) in buffer |
| 244 | load_pixel | **load** | read pixel at (x,y) from buffer |
| 245 | buffer_screen | store | push buffer to screen |
| 246 | clear_screen_buffer | store | clear the buffer |
| 247 | write_char | store | write character to text buffer |
| 248 | buffer_chars | store | push text buffer to display |
| 249 | clear_chars_buffer | store | clear text buffer |
| 250 | show_number | store | number to display |
| 251 | clear_number | store | blank the number display |
| 252 | signed_mode | store | interpret as two's complement |
| 253 | unsigned_mode | store | interpret as unsigned |
| 254 | rng | **load** | random 8-bit value |
| 255 | controller_input | **load** | button state |

**Store-only vs load-only** is a deliberate simplification — wiring both directions
for every address is difficult, so each port does one job.

Several ports carry no data at all: storing *anything* to 246 clears the buffer. The
store signal itself is the trigger.

**`load_pixel` (244) is the interesting one.** Being able to read the screen buffer
turns it into extra memory, and makes collision detection possible — reading the
pixels under a Tetris piece tells you whether it has landed.

**Controller** — 8 bits (up/left/down/right/A/B/start/select) behind **SR latches**,
so a short press is captured and held; loading address 255 resets the latches.
Without this, catching a button press is close to impossible.

**RNG** uses a **linear feedback shift register**, not a dropper randomizer, because
MCHPRS does not support droppers and hoppers.

## Program idioms

**Test one button** — mask, then branch:

```
LDI r15 controller_input
LOD r15 r1
LDI r2 0b00000100      // the select bit
AND r1 r2 r1
BRH = .not_pressed     // zero means not pressed
```

**Nested loop, counting down** — `DEC` sets carry on every value but zero:

```
LDI r2 32
.outer
  LDI r1 32
  .inner
    DEC r1
    BRH ge .inner
  DEC r2
  BRH ge .outer
HLT
```

**Draw a pixel:**

```
LDI r15 pixel_x
STR r15 r1
LDI r15 pixel_y
STR r15 r2
LDI r15 draw_pixel
STR r15 r0
LDI r15 buffer_screen
STR r15 r0
```

**Reuse code with subroutines** — `CAL` a label, `RET` at the end. The call stack
makes nesting safe up to 16 deep.

## Scale reference

A full Tetris implementation is roughly **900 instructions**, comfortably inside the
1024-instruction memory.
