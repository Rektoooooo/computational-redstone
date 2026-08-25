---
name: redstone-combinational
description: Stateless devices that route, select, translate or compare signals — decoders, encoders, priority encoders, multiplexers, demultiplexers, magnitude comparators, redcoders and hex/binary converters. TRIGGER when the user needs to turn an address or code into one selected line, compress many lines into a code, choose between several inputs, route one input to one of several outputs, or test whether one number is greater/equal/less than another. DO NOT TRIGGER when the device must remember anything between cycles (redstone-sequential), when it computes a numeric result (redstone-arithmetic), or for driving a screen (redstone-displays).
---

# Combinational Redstone Devices

**Combinational means no memory.** Output is a pure function of input — give it the
same inputs and you always get the same outputs, with no dependence on history. A
full adder is combinational; a counter is not.

These are the routing and translation primitives. Almost every large build is mostly
made of them.

## Teaching approach

Ask which of two things the user actually needs: **selection** (one of N lines
becomes active) or **translation** (a value in one encoding becomes a value in
another). Most confusion between decoders, encoders and multiplexers dissolves once
that distinction is explicit.

## Decoder — the workhorse

Takes an n-bit code, activates exactly one of 2ⁿ output lines.

### The one rule that builds every decoder

To detect a specific bit pattern:

> **Torches on the bits that should be 1, repeaters on the bits that should be 0,
> OR everything into a final torch.**

The final torch can only light when every contributing line is off, which happens
for exactly one input pattern.

To detect `1100`: torch, torch, repeater, repeater → merge → final torch.

### The standard build

Input lines run vertically. For each output, a **glass tower** feeding a torch, with
torches/repeaters placed per the rule above. Each tower detects one pattern.

This design is compact, fast, powerable from either end, and decodable on both
sides. It is the design used throughout the reference CPU — worth treating as the
default rather than shopping around.

Alternative layouts (spirals for vertical-to-vertical, horizontal-to-horizontal) are
in `references/decoder-encoder.md`, along with the two-wide-gap variant that avoids
the spacing problems the compact horizontal design suffers.

### Scaling: tree decoders

A straight-line decoder becomes unusable at large widths — a 10-to-1024 decoder
would be enormously long and would visit thousands of components on every address
change, which is a serious lag source.

Build it as a **tree** instead: the address spreads out and propagates into branches.
More rectangular footprint, faster, far less laggy.

Further optimisation: use the **bottom bits to select the branch first**, then the
remaining bits to locate the position within that branch. The signal then only
traverses one branch rather than searching every address.

## Encoder

The inverse: one active input line becomes a multi-bit code.

Build: run each input line with a torch to invert it, then place torches on the
sides of those lines positioned above the output wires, coding each input's value.
Moving the torches changes the encoding — it is completely arbitrary and yours to
choose.

**Encoders assume exactly one active input.** Two at once produces nonsense.

### Priority encoder

An encoder with a guard circuit on the front that enforces the one-input rule in
hardware — if several inputs are active it picks one (e.g. the rightmost). Use this
whenever inputs come from something you don't control, like a keypad.

## The brute-force pattern

Decoder → encoder chained together implements **any function whatsoever**: decode
every possible input, then encode whatever output you want for each case.

Example: a 4-bit "add one" built with no adder at all — decode all 16 inputs, encode
each to its successor.

> **It scales terribly.** An 8-bit-to-8-bit function needs a 256-line decoder *and*
> a 256-line encoder. Reach for logic gates and boolean simplification first; use
> brute force only for small, irregular mappings that resist simplification.

## Multiplexer (mux) — selection

Several inputs, one output, plus selector bits choosing which input passes.

In redstone this is trivially built with **cancelling comparators**: cancel every
input except the selected one. For more than two inputs, put a decoder on the
selector bits and use it to uncancel exactly one path.

n inputs need ⌈log₂ n⌉ selector bits.

Real-world logic diagrams build muxes from AND gates, since "cancelling" has no
electrical equivalent — but in Minecraft, comparators are always the right answer.

## Demultiplexer (demux) — routing

The inverse: one input, several outputs, selector bits choosing the destination.
Think of a train track switch. Same construction as a mux, same decoder trick to
scale beyond two outputs.

## Magnitude comparator

Two numbers in; three outputs: `A > B`, `A = B`, `A < B`.

- **Equality** — a tower of XOR gates, one per bit pair, ORed into a glass tower with
  a final torch. XOR outputs 0 when bits match, so any mismatch anywhere kills the
  torch.
- **Greater than** — conceptually: compare the highest bit; if they differ you have
  your answer; if equal, move down. In redstone there is a faster way that reuses the
  **carry-cancel process** from the adder, repurposed for comparison. Runs in 3 ticks
  and produces `A > B` **and** `A = B` from one circuit.
- **Less than** — derive it free: `A < B` is `NOR(A > B, A = B)`. No third circuit.

**Alternative:** subtract and inspect. `A − B = 0` means equal; carry-out set means
`A ≥ B`. This is what CPUs do, since the subtractor already exists. A dedicated
comparator is smaller and faster when you are not building a CPU.

## Signal-strength devices

**Redcoder** — takes a signal strength and lights the corresponding lamp (input 7 →
7th lamp). Works by splitting the input into two lines offset by one, so exactly one
column has the bottom line powered and the top line unpowered. Detect that column,
typically with XOR gates. Available in vertical form for compact builds.

**Hex ↔ binary converters** — 4 bits of binary and one hex digit have identical
range (0–15), so conversion is direct. Both directions run in **2 ticks**.

## Choosing between approaches

| Need | Use |
|---|---|
| Address → one line | Decoder |
| One line → code | Encoder |
| Untrusted inputs → code | Priority encoder |
| Pick one of several inputs | Mux (cancelling comparators) |
| Send one input to one of several places | Demux |
| Small irregular mapping | Decoder → encoder |
| Large regular mapping | Logic gates + simplification |
| Compare two numbers, no CPU | Magnitude comparator |
| Compare two numbers, CPU exists | Subtract, read zero and carry flags |
