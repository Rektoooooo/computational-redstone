# Decoder and encoder layouts

## Sequence detection — the underlying rule

Every decoder is a bank of sequence detectors. To detect one pattern:

> Torches on the bits that should be **1**, repeaters on the bits that should be
> **0**, OR all of it into a final torch.

Why it works: a torch on a line that is *off* turns **on**, contributing to the OR
and holding the final torch down. Only when every bit matches its expected value do
all contributions vanish, letting the final torch light.

A naive AND on just the 1-bits is not enough — it stays on when extra bits are set.
The repeaters on the 0-bits are what force exclusivity.

## Decoder layouts

### Vertical input, glass-tower output (recommended)

Input lines vertical; one glass tower per output feeding a torch; torches and
repeaters per the rule. Compact, fast, stackable, decodable from both sides, and
powerable from either end or from behind.

This is the design used for every decoder in the reference CPU.

### Spiral variant

Replaces glass towers with spirals. Use when you need vertical input **and**
vertical output.

### Horizontal to horizontal

Torches on the sides of blocks, repeaters powering the output line beneath.

**Warning:** with a one-block gap between output lines, long runs of repeaters leave
no room for the powering formation, forcing awkward workarounds. **Use a two-block
gap** — the layout then stays clean regardless of the decoding pattern.

## Tree decoders for large address spaces

A straight-line 10-to-1024 decoder is impractical: enormous, and every address
change visits thousands of repeaters and torches, which lags the game badly.

Build a tree: the address propagates into branches, giving a rectangular footprint
and better speed.

**Branch-first optimisation:** use the low bits to pick the branch, then the
remaining bits to locate the position on it. The signal traverses one branch instead
of the whole array. Functionally identical, dramatically cheaper.

## Encoder layouts

Base construction: one line per input with a torch inverting it; output wires
beneath; torches on the sides of the input lines positioned above whichever output
wires that input should activate.

Variants:
- **Horizontal → horizontal** — the classic
- **Horizontal → vertical** — each input powers a glass tower; encode with repeaters
- **Aligned** — adds a layer on top so inputs and outputs line up exactly
- **Vertical → vertical** — uses spirals

> **2×2 barrel spirals** send data both up *and* down from any point on a wire, and
> stack directly against each other when oriented correctly. They are the general
> solution for vertical data movement where a glass tower's one-way behaviour is
> wrong.

## Priority encoder guard

Attach a circuit to the front that permits only one active input, picking (for
example) the rightmost when several are pressed. Without it, two simultaneous inputs
encode to a meaningless mixture of both codes.

## Data compression trick

Encoder → wires → decoder transmits N states over only ⌈log₂ N⌉ wires. Sixteen
signals travel down four wires and come back out as sixteen.

Only works for **one active signal at a time** — you cannot encode two states
simultaneously.

## Sizing

| Inputs | Address bits |
|---|---|
| 4 | 2 |
| 16 | 4 |
| 256 | 8 |
| 1024 | 10 |

For an n-bit address you get 2ⁿ lines. In a CPU this directly sets program length
(10-bit instruction address = 1024 instructions) and data capacity (8-bit data
address = 256 bytes).

Bigger is not automatically better: larger memories are slower and laggier. 1024
instructions was chosen as the point where complex programs fit without Minecraft
falling over.
