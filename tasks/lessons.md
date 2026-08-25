# Lessons

Corrections worth not repeating. Newest first.

## Steady state hides timing behaviour entirely

**Found by the user**, stepping the game one tick at a time: a redstone lamp lights
immediately but takes **4 game ticks** to go dark.

The oracle compares settled states, so it is blind to this by construction — the final
picture is the same whether the lamp waits or not. 175 builds and nine in-game tests
never touched it. It appeared the moment someone measured *when* instead of *what*.

**How to apply:** where a component's behaviour depends on time, a steady-state check
cannot verify it and its passing means nothing. Ask what the component does on the way
to its answer, not just at the end. Anything with an asymmetry between rising and
falling edges is a candidate.

## A written blockstate must describe every real neighbour

**Correction:** the wire at each end of a route pasted pointing the wrong way — drawn as
a straight line past the repeater beside it instead of turning into it.

The route code gave each cell connections toward its path neighbours, and the cells at
the two ends have only one path neighbour each. A wire with a single connection draws as
a straight line *through*, not as a turn. The repeaters at either end are real
neighbours, they were simply not part of the path list.

**Why it hid:** the game recomputes wire shape on the next block update, so it corrects
itself and behaves properly. Only the pasted file looks wrong, which means the
simulator, the sweeps, and the arithmetic all pass. It took someone looking at it.

**How to apply:** when writing blockstates directly rather than letting the game derive
them, the state has to describe the world as it will be — including neighbours that the
generating loop does not happen to iterate over. `lay_route` now takes `enter_from` and
`exit_to` for exactly this. Shape also decides which blocks a wire powers, so this is
not purely cosmetic.

## Version generated schematics, never overwrite them

**Correction:** I rebuilt M1 in place, overwriting the file the user had already pasted.

When a build misbehaves in game, the previous version is exactly what you want — to
diff against, to fall back to, and to keep the record of what was actually tested
straight. Overwriting destroys all three, and it destroyed the broken v1 of M1 before
anyone could look at what had gone wrong.

**How to apply:** `next_version()` in `pipeline/compose.py` picks the next unused
`-vN` and every run writes a new file. Keep the numbering aligned with what the user
has actually pasted, so "the one that broke" and "v1" mean the same thing to both of us.

## The simulator models SIGNAL, not PHYSICS

**Correction:** M1 shipped with 16 repeaters floating in mid-air. It passed 1029
simulator cases, then fell apart the moment it was pasted.

The simulator has no concept of block support. A repeater hanging over nothing solves
perfectly and simply cannot exist in the game. **Passing the sweep does not mean the
build is placeable.**

**How it happened, which is the part worth remembering:** the swap looked like a
like-for-like replacement. An output *lamp* and a *wall* lever both need no floor —
a wall lever hangs off the side of a block — but a repeater does. Replacing one with
the other silently introduced a requirement that neither original had.

**How to apply:** a composed build needs a **structural** check as well as a
behavioural one. `Composition.floating()` in `pipeline/compose.py` does this: it scans
for anything needing a floor that has not got one. Run it before every save, and treat
a swap as introducing whatever requirements the NEW block has, not inheriting the old
one's.

## Build with wool, and colour-code every line

**Correction:** I used `stone` as the structural block for generated schematics.

Use **wool**, and give **each signal line its own colour**. This is normal practice in
computational redstone and the source builds do it throughout — `light_blue_wool` in the
CCA adder, `light_gray_wool` and `orange_wool` in the displays.

**Why it matters:** colour is how you trace a wire in a build with dozens of parallel
lines. When a bus carries eight bits side by side, a wrong bit is *visible* if each line
has its own colour, and requires counting blocks in F3 if they are all grey. The whole
point of these composed builds is that they get inspected in game when something looks
wrong, and stone throws that away.

**How to apply:** one wool colour per bus line, ordered so the bit order is readable at
a glance — LSB to MSB as a spectrum rather than an arbitrary set. Keep the mapping in
one place in the code so a build and its documentation cannot disagree.

## Validate a tool against a known answer after every change

Three separate bugs in `verify/drive.py`, and three more in `verify/alu_probe.py`, all
produced **plausible output** rather than crashing: a truth table indexed backwards, a
lever index printed as if it were a different lever, control levers mistaken for
operands, bit significance reversed.

Every one was caught by re-running a build whose answer was already confirmed in game.
Keep at least one known-good case and re-run it after every change, however small the
change looks.

## Prefer measurement over structure

Structural inference has now been wrong three times — `build-17` read as an AND gate
when it is a XOR, `build-16` read as four independent gates when it is an adder, and a
comparator array once read as a mux. In every case the visual read got the *parts* right
and missed how they were *joined*.

Where a reading contradicts a measurement — a census, a port map, a driven result — the
measurement wins. Drive the build; it costs seconds.

## Ask for the reading rather than recovering it from a screenshot

A 22-block-tall build photographed at an angle is not reliably readable, and guessing
from ambiguous crops risks reporting a confirmation that did not happen. Say so and ask
for the values. Small flat builds are fine to read directly.
