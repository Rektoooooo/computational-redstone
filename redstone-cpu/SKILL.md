---
name: redstone-cpu
description: Building a general-purpose programmable computer in redstone — ALU, register file, control ROM, instruction memory, program counter, flags and branching, call stack, data memory, memory-mapped I/O, plus the instruction set and assembly language that drive it. TRIGGER when the user wants a machine that runs programs rather than one fixed task, mentions an ALU, opcode, instruction set, program counter, assembler, machine code, jump/branch/call/return, or asks how a computer actually works at the gate level. DO NOT TRIGGER for single-purpose arithmetic circuits (redstone-arithmetic), standalone memory (redstone-sequential), or screens not wired as CPU ports (redstone-displays).
---

# Redstone CPU

## The decision to make first

There are two ways to get a game running in redstone:

1. **Single-purpose circuit** — days to weeks each, and fast, because you can
   optimise for the one task
2. **General-purpose computer** — months once, then each new program takes about a
   day

A computer is **orders of magnitude slower** — often 1000× — than a purpose-built
circuit, because it cannot exploit anything specific to the problem. It is a large
up-front investment that pays off only if you want to run *many* programs.

Say this plainly before anyone starts. It is the single most consequential choice in
the project.

## Teaching approach

Build strictly bottom-up, and get each component fully tested standalone before
connecting it. The series' own advice is worth repeating: **give every new
instruction many test cases before continuing.** A bug in the ALU discovered after
the call stack is wired in is brutal to isolate.

Ask the user to hand-execute a two-instruction program on the diagram before you
build anything. If they can trace opcode → control ROM → operands → clock, the rest
of the series makes sense. If not, nothing later will.

## Architecture at a glance

```
Instruction Memory --> [15..12] --> Control ROM --> control bits
        ^              [11..8]  --> Reg A read
        |              [7..4]   --> Reg B read
   Program Counter     [3..0]   --> Write address
        ^                 |
        |                 v
   Call Stack        Register File --> ALU --> (mux) --> back to Register File
        ^                                |         ^
        |                             Flags        |
        +-- jump / branch / return       |    Data Memory <--> memory-mapped I/O
```

**Harvard architecture** — instructions live in their own memory, separate from
data. Chosen because it is far easier to build in Minecraft.

**Single cycle** — every instruction completes in exactly one clock cycle. Simplest
possible design, with one real cost: **the clock must be as slow as the slowest
instruction.** One slow instruction slows everything.

The alternative is **multicycle/pipelined** — split instructions into fetch, decode,
execute stages so several instructions are in flight at once. Three instructions
through a 3-stage pipeline take 5 cycles instead of 9. Powerful, and out of scope
for a first build; the reference machine is single cycle throughout.

## The components

**ALU** — two 8-bit inputs, one 8-bit output, a control setting. Combinational.
Built from a **single carry-cancel adder** modified by six control signals to give
its full operation set. This is the cleverest part of the machine; full derivation in
`references/alu.md`, along with the complete 22-line control map read off the
reference machine.

**Register file** — 16 registers × 8 bits, dual read, register 0 hardwired to zero.
See `redstone-sequential` for construction; the CPU-specific parts are dual read and
the enable signal.

**Control ROM** — takes the 4-bit opcode, outputs the control bits for that
instruction. A 4-to-16 decoder with torches placed to match your instruction table.
This is where the instruction set physically lives.

**Instruction memory** — 10-bit address = **1024 instructions**. Combinational:
address in, instruction out. Needs a **tree decoder** (see `redstone-combinational`)
— a straight-line 10-to-1024 decoder is unusably long and laggy. Storage is a glass
tower per address with repeaters placed where the 1 bits are.

> Empty instruction memory is not empty — it is **full of NOPs**. Loading a program
> replaces some of those zeros with real instructions.

**Program counter** — a 10-bit register plus an adder wired to add 1 and feed back.
Its input mux is three-way: increment, jump target, or return address.

**Flags** — 1-bit registers capturing properties of the last ALU result.
- **Zero flag** — OR all output bits into a torch; torch on means the result was zero
- **Carry flag** — the adder's carry-out

Only instructions that actually use the ALU should set the flags; that is a column in
your instruction table. The other two common flags (negative, overflow) matter only
for signed arithmetic and are omitted here.

**Call stack** — a **bidirectional shift register**, 10 bits wide, 16 deep. Push on
call, pop on return. A plain return *register* fails as soon as one subroutine calls
another; a stack is what makes nesting work. Exceeding its depth is a **stack
overflow** — there is no guard.

**Data memory** — 8-bit address = **256 bytes**. Addressed by a register's contents
plus a signed offset, which is why widening the register file is not the answer to
wanting more memory (see `redstone-sequential/references/registers-memory.md`).

## Instruction format

**16 bits, fixed width.** 4-bit opcode + 12 bits of operands.

| Bits | Use |
|---|---|
| 15–12 | opcode → control ROM |
| 11–8 | register A (read 1) |
| 7–4 | register B (read 2) |
| 3–0 | register C (write address) |

Operand meaning varies by opcode — `LDI` uses bits 7–0 as an 8-bit immediate, `JMP`
uses bits 9–0 as an address. Two multiplexers handle the variation: one choosing the
write-data source (ALU output vs immediate), one choosing the destination register
(C vs A).

A 4-bit opcode caps you at **16 instruction types**. The full set, encodings and
assembly syntax are in `references/isa-and-assembly.md`.

## Jumping, branching, and why it matters

**JMP** overrides the program counter. **Direct** jumping (absolute address) is
simpler in hardware; **relative** jumping (offset) survives code edits better. The
reference machine uses direct jumping and solves the editing problem in software with
**labels**, which the assembler resolves — a much cheaper fix than extra hardware.

**BRH** is a conditional jump: a 2-bit condition code plus an address. Implementation
is simpler than it sounds — the PC's mux already chooses between increment and new
address, so you just **feed the condition into that mux**.

After a subtraction, the flags carry comparison meaning:

| Flags after `SUB a b` | Means |
|---|---|
| zero set | a == b |
| zero clear | a != b |
| carry set | a >= b |
| carry clear | a < b |

> **Conditional branching is what makes the machine Turing complete.** Before it you
> have a calculator; after it you have a computer.

## Input and output

Two approaches:

- **Port-based (isolated)** — dedicated port registers between CPU and devices.
  Clean separation, but needs extra instructions to talk to the ports.
- **Memory-mapped** — reserve addresses in data memory and wire devices directly.
  **No instruction set changes at all** — `LOD` and `STR` already work. Costs you
  those memory addresses permanently.

The reference machine is memory-mapped, reserving the top 16 addresses (240–255) —
chosen so that all of them are reachable from a single base pointer using the signed
offset range of −8..+7.

Devices, port map and protocol design in `references/isa-and-assembly.md`.

## Toolchain

Programs are written in assembly, run through an **assembler** producing machine
code, then through a **schematic generator** producing a WorldEdit `.schem` to paste
into the instruction memory.

For actually running programs, **use the emulator**, not Minecraft. The Minecraft
CPU completes roughly **one instruction every 10 seconds** at vanilla speed. Carpet's
`/tick rate 500` gives 25× (about 2.5 instructions/sec). MCHPRS is the only route to
usable speeds and is what showcases use.

Note MCHPRS **does not support droppers and hoppers**, which is why CPU-grade
randomness uses a linear feedback shift register rather than a dropper randomizer.

## Sanity checks

| Symptom | Likely cause |
|---|---|
| Instruction does nothing | register file enable is 0 — check the control ROM row |
| Every instruction writes to the wrong register | destination mux stuck on C instead of A |
| Branch never taken | flags not being set — is this instruction marked as flag-setting? |
| Return goes to the wrong place | using a return register instead of a stack, with nested calls |
| Program runs then wanders | no `HLT`, so it runs off into the NOPs |
| Works stepped, fails clocked | clock faster than the slowest instruction |
