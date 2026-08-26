# Lessons

Corrections worth not repeating. Newest first.

## When two lines have to cross, change the ALGEBRA, not the layout

**This one wire was 65% of M4's runtime.** v2 took 211 game ticks, and 137 of them were
a single 68-hop comparator relay carrying x from one side of the board to the other.
It was that long because the two streams had been pushed apart until they no longer
crossed, and pushing things apart is the expensive way to solve a crossing.

The crossing was not geometric, it was **arithmetic**. The S stream read x and then y;
the r stream, written `q = 10 - y` then `r = x - q`, read y and then x. Opposite orders
means the streams must swap sides, and swapping sides in one plane means crossing.
Written the other way round,

    p = 10 - x        r = y - p

is the same number and reads x then y, like the other stream. Nothing has to cross.
The relay went from 68 hops to zero, and the core from 30 x 44 to 23 x 15.

**How to apply:** before routing anything, write down the order each stream consumes
its inputs in. If two streams disagree, look for an algebraically equal form that makes
them agree - it is usually free. Reach for geometry only when the algebra genuinely
cannot be reordered. A layout problem that will not solve is often an algebra problem
wearing a hat.

## A descent is not transport, it is `max(0, v - n)`

Dust loses a level per block going down exactly as it does going along - but a descent
**clamps at zero**, and that clamp is a gate you get for free.

M4's ones digit needs `max(0, x + y - 10)`. Rather than build that and then move it,
the r stream sits two levels up computing `max(0, x + y - 8)` and simply falls two
blocks. The fall does the last subtraction, in no ticks and no components, and the
level change stops being a cost.

Paying for a climb works the same way in reverse and was already known - `hex_wire`
adds, a decay line read `k` cells early reads `v + k`. What is new is that the change of
level can be the arithmetic rather than something the arithmetic has to survive.

**How to apply:** when a value has to change level anyway, check whether the decay it
would cost is a term you already wanted subtracted. `drop()` in `pipeline/analog.py`,
with the clamp tested at and past the boundary.

## A tower foot sits at 15, so a trunk beside it latches ON

**Found by the tens digit reading 1 with no levers thrown.** A bit's line ran east past
the foot of the glass tower it was about to feed. Dust one block away is the same wire,
so the foot's full 15 flowed back into the trunk, round to the repeater that feeds the
foot, and into the foot again. A loop with a repeater in it is a latch: once on, it
stayed on whatever the carry did.

Nothing about it looked wrong. The line was correct, the tower was correct, and the
repeater was correct; only the one-block gap between two of them was.

**How to apply:** a line that feeds something restored to full must stay **two** cells
clear of it, not one - the usual "lines two apart do not touch" rule is about signals
merging, and this is worse than merging because it closes a loop. Same for a repeater's
output cell and anything routed past it.

## Dust has no direction, so a merge feeds backwards too

A probe of `r` read the wrong value for half the input range, and the circuit was fine.
`r` falls onto the cell where it merges with `Sg`, and dust conducts both ways - so
`Sg`'s value climbs back up the staircase and sits in `r`'s output cell. The merge is
still `max(Sg, r)`, which is what was wanted; the cell just no longer reads what its
name says.

**How to apply:** downstream of a merge, a cell's reading is the max of everything that
reaches it, not the value the code put there. Probe upstream of the join - or expect the
max - and check the thing that matters, which was `ones`, not `r`.

## A schematic records a STATE, and the game will not fix it for you

**Found in game.** The build passed 100/100 in the simulator, pasted, and showed **7**
with every lever off. The arithmetic was fine; three of the four bits feeding the
display were simply stuck on.

`combinational/build-04` was extracted from a world where its input barrel held 15, so
every torch and repeater inside it went into the file in the "input is 15" state. On
paste, Minecraft re-evaluates a component only when something **pokes** it - and nothing
poked most of that circuit, so it sat there answering a question from another world.
Enough of it updated to drop the top bit; the other three stayed on. 4 + 2 + 1 = 7.

**Why the simulator is blind to it, and this is the important part:** `settle()`
recomputes from scratch and iterates to a fixed point, so it arrives at the right answer
*whatever state it started from*. A build can therefore pass every sweep and still be
wrong the instant it is pasted. The sweep and the paste were testing different things
and nobody noticed, because for a combinational circuit the fixed point is unique - the
simulator is right, and the world is simply not obliged to agree.

**552 blocks** in this build would have pasted in the wrong state.

**How to apply:** before saving, settle the build with nothing switched on and write
that state into every block - `power` on dust, `powered` on diodes, `lit` on torches and
lamps. `Build.rest()` does it and `Build.stale()` checks it, and both now run on every
emit. This applies with double force to anything lifted out of an extracted world, which
carries whatever state its author left it in.

Only valid for combinational builds: anything with a latch has more than one resting
state, and which one it should hold is a decision, not a computation.

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
