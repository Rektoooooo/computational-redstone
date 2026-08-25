# Lessons

Corrections worth not repeating. Newest first.

## Two lines in one plane cannot cross, and a router will not tell you that

**Cost most of a session.** The signal-strength adder is seven comparators. Placing them
took perhaps thirty attempts, and every failure had the same shape: a line laid early
took the shortest route straight across the middle, and the lines laid after it found
the board cut in half.

A breadth-first router makes this *worse*, not better. It finds the shortest path, which
is exactly the path most likely to be a wall. Reserving corridors in advance does not
fix it either — a three-wide reserved corridor is itself a wall, and a one-wide one is
useless because the next line can park against it and poison the cells either side.

**What actually worked:** stop searching and write the topology down. Order the lines so
they cannot cross:

- every input line turns off its lane at its own column, and a column crosses every lane
  south of its own — so the northernmost line must turn **last**
- the last stage of each stream ends at the same place, so put the merge where both can
  reach it from opposite sides rather than in the middle of the board

**How to apply:** for a planar build, decide the crossing order before the coordinates.
If two lines genuinely have to cross, one of them has to leave the plane — a boolean can
go up two levels and back down for free, an analog value cannot, and that difference
decides which one moves.

## An analog value is not a signal, it is a distance

Redstone dust loses one level per block, so **where a wire goes changes what it says**.
An extra cell is not a longer wire, it is a different number.

Three consequences, all of which cost time before they were understood:

- a **comparator** relays a value losslessly and a **repeater** destroys it, flattening
  everything to 15. The two kinds of line need different code, and mixing them up is
  silent.
- a chain of comparators alternates comparator, dust, comparator, dust, and a comparator
  cannot turn — so a value can only reach cells an **even** distance away in both axes.
  Space is divided into four classes and no route moves a value between them. A design
  that needs an odd offset is not a longer route, it is an impossible one.
- a stray dust cell or redstone block beside a comparator feeds its side input and
  changes the arithmetic, while looking completely normal in the schematic. The redstone
  block a gadget puts behind itself is placed *last*, so it never collides with
  anything — it just quietly powers whatever was routed alongside it.

**How to apply:** `interference()` and `stray_dust()` in `pipeline/analog.py` look for
exactly these. Run them before believing any sweep, and give every gadget's rear block
its own clearance rather than trusting that nothing was routed there.

Corrections worth not repeating. Newest first.

## Give the user a way to tell two builds apart in world

**Cost an entire test round.** M3's staggered and aligned builds differ by five block
properties and nothing else — same size, same block count, same layout. I said as much,
then handed both over with no way to identify which was which once pasted, and the
aligned one got tested twice.

The evidence was recoverable — the firing sequence identified the build unambiguously
after the fact — but only because the tick-by-tick data happened to be detailed enough.

**How to apply:** when two builds are meant to be compared and look alike, build the
difference in visibly. A sign, a marker block, a distinct wool colour on one component.
Failing that, say up front exactly what to look at to tell them apart — for these, the
repeater behind the white lamp has its torches far apart when aligned and close together
when not.

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
