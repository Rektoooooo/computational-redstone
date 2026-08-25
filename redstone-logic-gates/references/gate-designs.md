# Gate construction reference

## Quick table

| Gate | Cheapest redstone form | Delay | Notes |
|---|---|---|---|
| OR | merge two dust lines | 0 | native |
| NOT | torch | 1 tick | burns out if toggled too fast |
| NOT (alt) | subtract comparator, powered rear, input on side | 1 tick | no burnout |
| AND | comparator: A rear, ¬B side | 1 tick + inverter | compact |
| AND (classic) | torch, torch → dust → torch | 2 ticks | pure torch logic |
| XOR | two subtract comparators, symmetry | 1 tick | **output strength 2** |
| NOR | OR then torch | 1 tick | |
| NAND | AND with the final torch **removed** | 1 tick | double negation cancels |
| XNOR | XOR with one input inverted | 1 tick | only valid for XOR |

## The XOR trick in detail

Two comparators in subtract mode, fed so that each sees the other's input on its side.

**Both inputs high:** both comparators receive 14 at the rear and 14 on the side.
`14 − 14 = 0`. Neither outputs.

**One input high:** the arrangement is no longer symmetric. One comparator still
sees 14/14 and outputs 0, but the other sees **13 rear, 11 side** → `13 − 11 = 2`.

The two outputs are merged (OR), and 2 beats 0. Output present.

Because the design is symmetric, it behaves identically whichever input is high.

**The catch:** an output of signal strength 2 dies after two blocks of dust. Always
follow with a repeater. If you need a strong output directly, use the larger
alternative layout.

## Free AND from an XOR

Some XOR layouts expose an AND for free. In the compact full adder design, a torch
placed on top of the XOR structure gives you `A ∧ B` at no extra cost. This is
exploited heavily in adder construction — see `redstone-arithmetic`.

## The sequence detector

Not a gate, but the most reusable gate *pattern* in the field. To detect one
specific bit pattern:

> **Torches on the bits that should be 1, repeaters on the bits that should be 0,
> OR everything into a final torch.**

To detect `1011`: torch, repeater, torch, torch → all merged → final torch.

The final torch lights only when every contributing line is off, which happens only
for the exact target pattern. This single rule builds every decoder in a CPU.

## Multi-input gates

- **Multi-input OR** — merge as many dust lines as you like, or feed them all into
  one glass tower. The tower *is* the OR.
- **Multi-input AND** — chain, or use De Morgan: invert every input, OR them, invert
  the result. Usually smaller than chaining pairs.
- **Zero detection** (all bits are 0) — OR every bit into a single torch. Torch on
  means the value is zero. This is exactly how a CPU's zero flag is built.

## IMPLY

Uncommon but occasionally handy: `A → B` is false only when A is true and B is
false. It falls out of certain ALU control-signal combinations for free rather than
needing its own construction.

## Choosing between torch and comparator logic

**Torches** are compact and intuitive but **burn out** when toggled rapidly. In a
circuit that runs continuously — a CPU adder, a fast clock — burnout causes
intermittent, maddening failures.

**Comparators** never burn out. Some high-end designs are deliberately
*torchless* for exactly this reason, trading size for reliability. If you are
building something that must be 100% dependable under sustained load, prefer
comparator logic.
