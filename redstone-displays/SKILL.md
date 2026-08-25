---
name: redstone-displays
description: Getting information out to a human — pixel screens, matrix decoders, buffered and pass-through displays, seven-segment digits, leading-zero logic, colour displays, and input surfaces like keypads, keyboards and mode selectors. TRIGGER when the user needs to show a number, letter, image or animation, plot pixels by coordinate, build a screen or digit display, or design the buttons and levers a person will actually operate. DO NOT TRIGGER for converting the value before display (redstone-number-systems for BCD, redstone-combinational for decoders in general) or for memory-mapped screen ports on a CPU (redstone-cpu).
---

# Redstone Displays and Interfaces

The output layer, plus the input surfaces that sit alongside it. This is usually the
last thing built and the first thing a stranger judges.

## Teaching approach

Ask who the display is for. A debugging readout and a screen someone else will
download are different products — the first should be legible to the builder, the
second self-explanatory to a stranger with no help available. Most UI mistakes come
from building the first and shipping it as the second.

## Use trapdoors, not lamps

Redstone lamps turn on instantly but take **2 ticks to turn off**. For static
readouts that is tolerable. For **animation it is fatal**, and while debugging it
means the display actively lies to you for 2 ticks.

Trapdoors respond instantly in both directions. Re-texture side-mounted trapdoors to
look like lamps and you lose nothing.

## Pixel displays

### Density

**Use 2×2 density** — each pixel is 2 blocks by 2 blocks, four lamps. 1×1 density
displays are hard to build even at 4×4, need convoluted techniques, and lag badly.
The 2×2 module is a simple stackable unit; an 8×8 screen is 64 copies of it.

**Stay at 8×8 unless you genuinely need more.** A working screen is infinitely more
impressive than a big broken one.

### Matrix decoder — plotting by coordinate

To light the pixel at (x, y): one decoder for X, one for Y, and a grid of torches
detecting the intersection. Each torch is powered from two places — its row and its
column — so only the torch where both go off will light.

### Persistent plotting

A bare matrix decoder lights one pixel at a time. To accumulate an image, put a
latch on every pixel:

- **SR latch per pixel** — a plotted pixel stays on until reset. Wire all reset
  signals to one button for clear-screen. Simple; can only turn pixels *on*.
- **D latch (repeater lock) per pixel** — the decoder briefly unlocks the addressed
  pixel, which captures whatever a shared data line holds. This lets you set a pixel
  to **0 or 1**, not just on.

The D-latch version appears to lose clear-screen, but there is a neat recovery:
add circuitry that forces **all** rows and columns unpowered at once, making the
matrix decoder fire every torch simultaneously. Every pixel then captures the data
line together, giving you *fill screen* and *clear screen* for free. Four operations
total: set one pixel to 0 or 1, set every pixel to 0 or 1.

### Buffered displays

For animation, never show a half-drawn frame. Draw into **SR latches** the screen
cannot see, then on command push that frame into **D latches** driving the screen
and reset the SR latches for the next frame. One glass tower per column can do both
jobs — flashing the D latch on one side, resetting the SR latch on the other.

### Pass-through

Plotting from **several matrix decoders onto one screen simultaneously**. The trick:
the passed signal is forced to **signal strength 1**, which the decoder line's own
repeaters do not pick up, so it rides through without corrupting anything.

Chain decoders behind one another and each can plot its own point in the same frame.
A 3D renderer built this way used six layers of pass-through plus a buffer.

### Scaling past 8×8

Signal strength in the glass towers becomes the limit. Extend a tower with either a
backwards repeater or a double torch — **the block behind must be solid**, an
extremely common oversight — then compensate timing: **+1 tick** on the lower eight
repeaters for the repeater method, **+2 ticks** for the torch method, so the whole
tower arrives synchronised.

### Colour

There is no true RGB. Three approaches worth knowing:

- **Map displays** — a Minecraft map renders a region's majority colour per pixel;
  pistons swap blocks to change the majority
- **Trapdoor RGB** — each pixel has red, green and blue slices, each maskable by a
  number of trapdoors, giving up to 64 colours with a texture pack making open
  trapdoors invisible
- **Re-textured signal strength** — each dust strength textured as a distinct colour,
  giving 16 clean colours, changeable purely by swapping the pack

## Seven-segment displays

Seven segments show 0–9 **and A–F**, so one digit displays one hex digit — which
pairs exactly with 4 bits.

Build: a decoder for each value, then a **glass tower per value** encoding which
segments that value lights, with repeaters.

- The glass-tower design is fast and stacks tightly horizontally
- A flat-decoder alternative stacks well in both directions but is **unsynchronised**,
  showing garbage briefly while it settles

**Showing hex is easy** — chunk the binary into 4-bit groups, one converter each.
**Showing decimal is hard** — you must convert binary → BCD first (see
`redstone-number-systems`), then feed each BCD digit to a converter.

Extreme designs exist that abandon segments entirely, using diagonal
comparator-and-barrel patterns brute-forced by software to find item counts
producing the desired glyphs — smaller and prettier than any segment display.

Leading-zero suppression, the decimal point, and symbol switchers are covered in
`references/segment-and-ui.md`.

## Input surfaces

**Two modes** — use a **lever**, not two buttons. A lever physically cannot be in
both states, so the user learns the rule by looking at it. Two buttons need
indicator lamps and an RS NOR latch behind them and still don't communicate
exclusivity.

**Eight modes** — an **item frame selector**. Eight rotations, an arrow pointing at
exactly one label. Self-explanatory, and it outputs a distinct signal strength.

**N modes** — an expandable selector built from RS NOR latches: pressing one button
selects it and clears the rest. Expandable as long as every input powers the shared
reset line. Rising-edge triggered, so it fires on press rather than release.

**Keypads and keyboards** — a 10-button keypad is simple and can be synchronised to
1 tick. Keyboards either emit a 6-bit character code per key, or a per-key signal
strength on one of several coloured lines (more compact). Either way, special keys
like backspace and enter are usually easier as dedicated wires than as codes.

### Design principles

- **Clear** — someone downloading your world has no one to ask
- **Communicative** — give feedback fast, or people lose interest
- Prefer a control whose *shape* encodes the rule over one that needs a sign
- Note blocks make good clickable targets: bigger hitbox than a button
