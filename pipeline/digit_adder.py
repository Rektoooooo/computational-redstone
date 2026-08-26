#!/usr/bin/env python3
"""
x + y for two decimal digits, in signal strength, on a seven-segment screen.

Eighteen levers - two rows of nine, one per digit - and the sum as a decimal number
0..18 on two digits.

## Why this is arithmetic and not logic

A comparator in subtract mode computes `max(0, rear - side)` on signal STRENGTH. Dust
cannot add, but subtracting twice can:

    S = 15 - ((15 - x) - y) = min(15, x + y)

That gives the sum directly, with no adder, no carry chain and no binary anywhere - as
long as it stays under 16. It does not: 9 + 9 = 18. So the answer is split, exactly as
it is written on paper:

    S    = min(15, x + y)        the sum, clamped
    tens = S >= 10               a tap nine dust blocks along a line fed by S
    r    = max(0, x + y - 10)    the ones digit when there IS a carry
    ones = tens ? r : S

## The input is free

A lever nine blocks from the end of a dust line leaves 6 there; one six blocks away
leaves 9. So a run of dust with nine levers along it turns "which lever" into a number
with no gates at all - and because dust takes the LARGEST signal reaching it, two
levers at once gives the higher of the two rather than nonsense.

The same fact does the routing. A line read `k` cells early reads `v + k`, so a value
can be carried `k` cells of dust and arrive intact. Distance is not a cost here, it is
the arithmetic.

## What made v2 slow, and what this does instead

v2 was correct and took 211 game ticks - 10.5 seconds. 137 of them were ONE wire: a
68-hop comparator relay carrying x across the board, because the two streams had been
pushed apart until they no longer crossed. A relay costs two ticks a hop and there were
a lot of hops. Three changes remove every long haul.

**One comparator for `10 - y`, not two.** v2 built `ny = 15 - y` and then `ny - 5`,
with a twenty-cell relay in between. A constant on the REAR does it in one.

**Both streams read x first and y second.** v2's S stream read x then y while its r
stream read y then x, and opposite orders means the two must cross. Written as

    p = max(0, 10 - x)          r = max(0, y - p) = max(0, x + y - 10)

they agree, and nothing has to cross anything. Same number, different order.

**The r stream lives two levels up, and the drop back down does its arithmetic.** Dust
loses a level per block and CLAMPS AT ZERO, so a two-block descent computes
`max(0, v - 2)` for free. Feed the upper stream `y + 2` - which costs nothing, since a
decay line read two cells early reads exactly that - and

    r'' = max(0, (y + 2) - p) = max(0, x + y - 8)     upstairs
    r   = max(0, r'' - 2)     = max(0, x + y - 10)    after the drop

so the level change is not paid for, it is USED. Two planes also means the streams
cannot interfere, which is what makes the footprint small.

The core is now 21 game ticks instead of 143, in 23 x 4 x 15 instead of 30 x 44.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "worlds"))

from analog import (Build, decay_line, relay, station, gadget, constant,
                    stair, drop, tower, climb, hex_wire, place, wire, boost)
from sim.grid import DIRS, OPPOSITE, neighbour, step

# -- the two planes the arithmetic lives on ---------------------------------
LO, HI = 1, 3
RX = 14                        # both decay lanes read out at this x
XLANE_Z, XLEVER_Z = 2, 1       # the x line, and the blocks its levers stand on
YLANE_Z, YLEVER_Z = 10, 11
ROW = 7                        # the nx/u row, midway between the two lanes
MERGE = (22, LO, 12)

# -- lifting the answer out --------------------------------------------------
# A hex wire moves a signal strength any distance in two ticks and ADDS `15 - length`
# on the way, so a short one is a free adder; the staircase then spends exactly what it
# added. Eleven and four, so the answer arrives unchanged four levels up.
LIFT_HEX, LIFT_CLIMB = 11, 4

BCD = "worlds/primitives/combinational/build-04.litematic"
BCD_IN = (6, 4, 2)             # the barrel cell: left out, and wired instead
CONVERT = (34, 1, 12)          # so the barrel cell lands where the staircase ends

# The seven-segment digit: four BCD levers in, a 5x9 lamp panel out, and - the part
# that costs nothing and saves a whole circuit - BLANK for anything above nine. So the
# tens digit is a second copy fed 1 when there is a carry and 12 when there is not, and
# leading-zero suppression comes for free.
DISPLAY = "worlds/primitives/displays/build-16.litematic"
DISP_LEVERS = [(29, 9, 2 + 2 * i) for i in range(4)]      # bits 1, 2, 4, 8
TENS_AT, ONES_AT = (0, 5, 0), (0, 5, 8)
DRIVE_Y = TENS_AT[1] + 9       # the height every display input sits at
TOWER_X = 32                   # every bit climbs here, one lane per bit
PANEL = [(2, y, z) for y in range(2, 11) for z in range(3, 8)]   # the 5x9 digit


# -- the input panel ---------------------------------------------------------

def input_panel(b):
    """
    The eighteen levers and the two dust lines they drive.

    One line per digit, not two: a single readout cell can feed several comparators at
    once, and anything that needs the value somewhere else taps the line early and pays
    the difference in dust. Halving the lines halves the panel.
    """
    lanes, levers = {}, {"x": {}, "y": {}}
    for digit, lane_z, lever_z in (("x", XLANE_Z, XLEVER_Z), ("y", YLANE_Z, YLEVER_Z)):
        lanes[digit] = decay_line(b, (RX, LO, lane_z), "west", 15)
        for v in range(1, 10):
            b.block((v - 1, LO, lever_z), "purple_wool", f"{digit} lever {v}")
            lv = (v - 1, LO + 1, lever_z)
            b.lever(lv, f"{digit} = {v}")
            levers[digit][v] = lv
    return lanes, levers


# -- the arithmetic ----------------------------------------------------------

def s_stream(b):
    """
    nx = 15 - x, then u = nx - y, then S = 15 - u = min(15, x + y).

    nx and u sit two apart on one row, so nx's OUTPUT cell is literally u's rear cell -
    there is no transport between them at all. x drops in from the lane to the north
    and y rises from the lane to the south, so the two feeds never meet.

    x is tapped two cells early and then walks two cells of dust down to nx's side.
    That costs nothing and saves the comparator a station would have needed: on a decay
    line, distance IS the arithmetic.
    """
    b.comp((12, LO, XLANE_Z + 1), "north", "compare", "x to nx")      # rear = x + 2
    for z in range(XLANE_Z + 2, ROW):                                 # ... and back to x
        b.dust((12, LO, z), "x to nx")
    b.side_nodes.add((12, LO, ROW - 1))
    NX = gadget(b, (12, LO, ROW), "subtract", rear="block", why="nx = 15 - x")

    b.comp((14, LO, YLANE_Z - 1), "south", "compare", "y to u")       # rear = y
    b.dust((14, LO, ROW + 1), "y to u")
    b.side_nodes.add((14, LO, ROW + 1))
    assert NX == (13, LO, ROW), NX                # nx's output IS u's rear
    U = gadget(b, (14, LO, ROW), "subtract", rear="dust", why="u = nx - y")

    arrive = relay(b, U, [("east", 4)], why="u to S")
    assert arrive == (19, LO, ROW), arrive
    station(b, (19, LO, 9), "north", "S side")
    S = gadget(b, (19, LO, 10), "subtract", rear="block", why="S = min(15, x+y)")
    assert S == (20, LO, 10), S
    return NX, U, S


def r_stream(b):
    """
    p = 10 - x and r'' = (y + 2) - p, one level up, where there is nothing to collide
    with.

    Both values climb out of the decay lines on two-block staircases. A staircase costs
    exactly one level per step, so the x line is tapped two cells early (x + 2, arriving
    as x) and the y line four (y + 4, arriving as y + 2). Neither reading costs a thing.
    """
    xs = stair(b, (12, LO, XLANE_Z), 2, "north", why="x climbs")
    ys = stair(b, (10, LO, YLANE_Z), 2, "south", why="y climbs")
    assert xs == (12, HI, 0) and ys == (10, HI, 12), (xs, ys)

    relay(b, xs, [("east", 4)], why="x up top")
    b.comp((16, HI, 1), "north", "compare", "x to p")
    b.dust((16, HI, 2), "x to p")
    b.side_nodes.add((16, HI, 2))
    constant(b, (15, HI, 3), "south", 10, "constant 10")
    P = gadget(b, (16, HI, 3), "subtract", rear="dust", why="p = 10 - x")

    relay(b, ys, [("east", 10), ("north", 2)], why="y up top")
    relay(b, P, [("east", 4), ("south", 6)], why="p to r")
    b.side_nodes.add((21, HI, 9))
    R = gadget(b, (21, HI, 10), "subtract", rear="dust", why="r = x+y-8")
    assert R == (22, HI, 10), R
    return P, R


def back_end(b, S, R):
    """
    The carry, the gate it drives, and the one cell where the two answers meet.

    `carry` is read off a ruler: nine dust blocks along a line fed by S, so the far end
    is lit exactly when S is ten or more. `Sg = S - carry` switches the sum off when
    there is one, and `r` is already zero when there is not - so the merge is a plain
    max on a shared dust cell and needs no second gate.

    Then `r` falls two levels onto that cell, and the fall IS its `max(0, r'' - 2)`.
    """
    rear = relay(b, S, [("south", 2)], why="S to Sg")
    assert rear == (20, LO, 12), rear
    Sg = gadget(b, (21, LO, 12), "subtract", rear="dust", why="Sg = S - carry")
    assert Sg == MERGE, Sg

    tap = decay_line(b, (19, LO, 12), "west", 9)[-1]     # the ruler, back under the panel
    assert tap == (11, LO, 12), tap
    b.rep((11, LO, 13), "north", why="carry")
    carry = b.dust((11, LO, 14), "carry")

    end = wire(b, carry, [("east", 10)], why="carry")    # a row clear of everything
    assert end == (21, LO, 14), end
    b.rep((21, LO, 13), "south", why="carry into Sg")
    b.side_nodes.add((21, LO, 13))

    landed = drop(b, R, 2, "south", why="r falls to the merge")
    assert landed == MERGE, landed
    return carry, MERGE


def lift(b, ones):
    """
    Carry the answer out to the converter, and four levels up, in two ticks.

    A hex wire - a dust line, a row of repeaters reading it from the side, a second dust
    line - arrives two ticks later whatever the distance, and reads `in + (15 - length)`
    because a short run of it is a free adder. Eleven repeaters buy four levels; the
    staircase then spends exactly those four, and what lands at the top is the answer
    again, in the converter's own input cell.
    """
    out = relay(b, ones, [("east", 4)], why="ones out")
    assert out == (26, LO, 12), out
    lifted = hex_wire(b, out, "east", "south", LIFT_HEX, why="ones lift")
    assert lifted == (36, LO, 14), lifted
    landed = stair(b, lifted, LIFT_CLIMB, "east", why="ones lift")
    target = (CONVERT[0] + BCD_IN[0], CONVERT[1] + BCD_IN[1], CONVERT[2] + BCD_IN[2])
    assert landed == target, (landed, target)
    return landed


# -- the screen --------------------------------------------------------------

def digit(b, at, driven, why):
    """
    One seven-segment digit, with drive repeaters in place of its input levers.

    Each of build-16's four inputs is a WALL lever hung on its own indicator lamp, so
    throwing it strongly powers that lamp. A repeater aimed into the same lamp does
    exactly the same thing - but a lever hangs off a wall and a repeater needs a floor,
    and forgetting that is what left M1 with sixteen repeaters in mid-air.

    Bits not in `driven` simply have no lever, which reads as 0.
    """
    place(b, DISPLAY, at, why, skip=set(DISP_LEVERS))
    feeds = {}
    for i, lv in enumerate(DISP_LEVERS):
        if i not in driven:
            continue
        pos = (at[0] + lv[0], at[1] + lv[1], at[2] + lv[2])
        b.rep(pos, "east", why=f"{why} bit {1 << i}")
        b.block((pos[0], pos[1] - 1, pos[2]), "gray_wool", f"{why} support")
        feeds[i] = (pos[0] + 1, pos[1], pos[2])
    return feeds


def bit_tower(b, source, z, why):
    """
    Take one bit up to the drive height in its own lane, and hand it west.

    A glass tower climbs a level per block in two cells of footprint, which is what
    makes four bits fit side by side at all. The footprint is in **x**, so each bit
    keeps its own z lane the whole way up and no two are ever adjacent - the display's
    inputs are two apart, and two apart is exactly enough as long as nothing wanders.

    Nine or eleven levels of dust arrive well under 15, so the line is restored to full
    on the way in; a tower that runs out halfway up looks like a wiring fault and is
    not one.
    """
    b.rep((TOWER_X + 1, source[1], z), "east", why=why)       # rear is further east
    foot = b.dust((TOWER_X, source[1], z), why)
    top = tower(b, foot, DRIVE_Y - source[1], "west", why=why)
    assert top == (TOWER_X - 1, DRIVE_Y, z), top   # odd climb, so it lands clear of glass
    return top


def show(b, bits, carry):
    """Wire the four bits and the carry across to the two digits."""
    ones_feed = digit(b, ONES_AT, {0, 1, 2, 3}, "ones digit")
    # 1 when there is a carry, 12 when there is not - and build-16 blanks above nine,
    # so the leading zero suppresses itself. Bits 4 and 8 are the ones held on, which
    # keeps them four apart from bit 1 and out of its way.
    tens_feed = digit(b, TENS_AT, {0, 2, 3}, "tens digit")

    # -- the four bits ------------------------------------------------------
    for i, lamp in enumerate(bits):
        why = f"bit {1 << i}"
        # tap the block that drives the converter's own indicator lamp, and leave the
        # lamp itself in place - it is worth having something to read in game
        driver = (lamp[0], lamp[1], lamp[2] + 1)
        rep = (driver[0] - 1, driver[1], driver[2])
        b.rep(rep, "east", why=f"{why} tap")
        b.block((rep[0], rep[1] - 1, rep[2]), "gray_wool", f"{why} support")
        pos = b.dust((rep[0] - 1, rep[1], rep[2]), why)
        feed = ones_feed[i]
        # The bits leave the converter at four heights two apart, which is the standard
        # spacing for a bus - so they cross to their own z lanes without touching, and
        # only then climb. Each lane is a column of its own; nothing shares one.
        if feed[2] != pos[2]:
            pos = wire(b, pos, [("south" if feed[2] > pos[2] else "north",
                                 abs(feed[2] - pos[2]))], why=why)
        top = bit_tower(b, pos, feed[2], why)
        wire(b, top, [("west", top[0] - feed[0])], why=why)

    # -- the tens digit -----------------------------------------------------
    #
    # A copy of the carry, taken before the carry reaches Sg, climbs to the empty plane
    # above the core and crosses there. At ground level the band the answer travels in
    # is solid from the merge to the converter, and there is no way through it.
    why = "tens"
    b.rep((carry[0], carry[1], carry[2] + 1), "north", why=f"{why} copy")
    pos = b.dust((carry[0], carry[1], carry[2] + 2), f"{why} copy")
    pos = wire(b, pos, [("east", 13)], why=why)
    pos = climb(b, pos, HI + 2 - pos[1], "east", why=why)
    pos = boost(b, pos, "north", why=why)      # a climb hands on what the height cost it
    # the trunk runs along z = 4, two lanes clear of every tower foot it feeds. One lane
    # is not enough and the reason is worth keeping: a foot sits at a full 15, so a
    # trunk beside it picks that up, carries it round to the repeater that feeds the
    # foot, and the branch latches ON and stays there whatever the carry does.
    pos = wire(b, pos, [("north", pos[2] - 4), ("east", 34 - pos[0])], why=why)
    y5 = pos[1]

    # bit 1 is the carry itself, on a spur two lanes north of the trunk
    wire(b, pos, [("north", 2)], why=f"{why} bit 1")
    b.rep((TOWER_X + 1, y5, 2), "east", why=f"{why} bit 1")
    foot = b.dust((TOWER_X, y5, 2), f"{why} bit 1")
    top = tower(b, foot, DRIVE_Y - y5, "west", why=f"{why} bit 1")
    wire(b, top, [("west", top[0] - tens_feed[0][0])], why=f"{why} bit 1")

    # NOT carry is a repeater into a block with a torch on the far side - off exactly
    # when the block is powered. One torch feeds both of the bits that need it.
    b.rep((34, y5, 5), "north", why=f"{why} invert")
    b.block((34, y5, 6), "gray_wool", f"{why} invert")
    b.put((34, y5, 7), "redstone_wall_torch", {"facing": "south", "lit": "true"},
          f"{why} invert")
    b.dust((34, y5, 8), f"{why} not-carry")
    b.rep((33, y5, 8), "east", why=f"{why} not-carry")
    for z in (8, 7, 6):
        b.dust((TOWER_X, y5, z), f"{why} not-carry")
    for i, z in ((2, 6), (3, 8)):
        top = tower(b, (TOWER_X, y5, z), DRIVE_Y - y5, "west",
                    why=f"{why} bit {1 << i}")
        wire(b, top, [("west", top[0] - tens_feed[i][0])], why=f"{why} bit {1 << i}")
    return ones_feed, tens_feed


# -- putting it together -----------------------------------------------------

def core(b):
    NX, U, S = s_stream(b)
    P, R = r_stream(b)
    carry, ones = back_end(b, S, R)
    place(b, BCD, CONVERT, "strength to binary", skip={BCD_IN})
    lifted = lift(b, ones)
    bits = [(CONVERT[0] + 2, CONVERT[1] + 2 + 2 * i, CONVERT[2] + 3) for i in range(4)]
    ones_feed, tens_feed = show(b, bits, carry)
    return {"nx": NX, "u": U, "S": S, "p": P, "ones": ones, "carry": carry,
            "lifted": lifted, "bits": bits, "tens_feed": tens_feed}


def build():
    b = Build()
    lanes, levers = input_panel(b)
    nodes = core(b)
    b.add_floor()
    return b, levers, nodes


# -- checking ----------------------------------------------------------------

def expected(x, y):
    """What the machine should say, worked the way the circuit works."""
    nx = max(0, 15 - x)
    u = max(0, nx - y)
    S = max(0, 15 - u)                     # min(15, x + y)
    p = max(0, 10 - x)
    rr = max(0, (y + 2) - p)               # upstairs, before the drop
    carry = S >= 10
    return {"nx": nx, "u": u, "S": S, "p": p, "carry": carry,
            "ones": max(0, rr - 2) if carry else S}


def glyphs():
    """
    What each value looks like on `build-16`, read off the component itself.

    Driven rather than written down, so the check at the end is against the real thing:
    the right PICTURE, not the right bits.
    """
    from sim.grid import Grid
    from sim.engine import Sim
    out = {}
    for v in range(16):
        g = Grid.from_file(DISPLAY)
        s = Sim(g)
        for i, lv in enumerate(DISP_LEVERS):
            s._set_lever(lv, bool((v >> i) & 1))
        s.settle()
        lit = s.lamp_states()
        out[v] = frozenset(p for p in PANEL if lit.get(p))
    return out


def render(cells):
    return ["".join("#" if (2, y, z) in cells else "." for z in range(3, 8))
            for y in range(10, 1, -1)]


JOINS = {("Sg = S - carry out", "r falls to the merge"),
         ("S to Sg", "decay line"), ("ones out", "ones lift in"),
         ("tens not-carry", "tens bit 4"), ("tens not-carry", "tens bit 8"),
         ("tens", "tens bit 1"), ("tens copy", "tens")}


def audit(b):
    """Every side input nobody asked for, and every pair of lines that touch."""
    inside = {p for p, note in b.notes.items()
              if note.endswith("digit") or note == "strength to binary"}
    bad = 0
    for pos, side, other, oid in b.interference():
        if pos in inside and other in inside:
            continue                       # an extracted component's own wiring
        bad += 1
        print(f"  INTERFERENCE {pos} side {side} <- {oid} at {other} "
              f"({b.notes.get(other, '?')})")
    seen = set()
    for a, c in b.stray_dust():
        na, nc = b.notes.get(a), b.notes.get(c)
        if na == nc or (na, nc) in JOINS or (nc, na) in JOINS:
            continue
        if a in inside and c in inside:
            continue
        if (na, nc) in seen:
            continue
        seen.add((na, nc))
        bad += 1
        print(f"  DUST TOUCHING {a} ({na}) - {c} ({nc})")
    return bad


def sweep(limit=None):
    from sim.engine import Sim
    b, levers, nodes = build()
    print(f"cells: {len(b.cells)}   extent: {b.extent()}")
    audit(b)

    glyph = glyphs()
    blank = glyph[12]
    fails = 0
    for x in range(10):
        for y in range(10):
            s = Sim(b.grid())
            if x:
                s._set_lever(levers["x"][x], True)
            if y:
                s._set_lever(levers["y"][y], True)
            s.settle()
            want = expected(x, y)
            lamps = s.lamp_states()

            def panel(at):
                return frozenset(c for c in PANEL
                                 if lamps.get((at[0] + c[0], at[1] + c[1],
                                               at[2] + c[2])))
            shown = {"ones": panel(ONES_AT), "tens": panel(TENS_AT)}
            expect = {"ones": glyph[want["ones"]],
                      "tens": glyph[1] if want["carry"] else blank}
            if shown != expect:
                fails += 1
                if fails <= 3:
                    print(f"  {x}+{y} = {x + y}: showing")
                    for a, e in zip(render(shown["tens"]) + [""] + render(shown["ones"]),
                                    render(expect["tens"]) + [""] + render(expect["ones"])):
                        print(f"      {a:7} want {e}")
    print(f"\n{100 - fails}/100 show the right digits")
    return fails == 0


# One wool colour per line, so the build can be traced from above. Painted on the FLOOR
# under each cell, which leaves the redstone itself readable. Order matters - the first
# prefix that matches wins - so the specific ones come before the general.
COLOURS = {
    "tens": "red",                       # everything carrying the carry or its inverse
    "bit 1": "white", "bit 2": "light_blue", "bit 4": "yellow", "bit 8": "orange",
    "x lever": "light_blue", "y lever": "lime",
    "x to nx": "light_blue", "x climbs": "cyan", "x up top": "cyan", "x to p": "cyan",
    "y to u": "lime", "y climbs": "green", "y up top": "green",
    "nx": "orange", "u ": "orange", "u =": "orange", "S ": "orange", "S =": "orange",
    "p ": "magenta", "p =": "magenta", "r ": "magenta", "r =": "magenta",
    "constant": "yellow", "decay line": "white", "carry": "red", "Sg": "purple",
    "ones": "purple", "strength to binary": "gray",
}


def label(b, pos, lines, colour="white"):
    """A standing sign on its own block, clear of the circuit. Text goes in after."""
    b.block((pos[0], pos[1] - 1, pos[2]), f"{colour}_wool", "label post")
    b.put(pos, "oak_sign", {"rotation": "8"}, "label")
    return pos, lines


def emit(out=None):
    """Write the build out, in the state it will actually paste in."""
    from compose import next_version
    from signs import embed

    b, levers, nodes = build()
    signs = {}
    for digit_name, colour in (("x", "light_blue"), ("y", "lime")):
        for v, lv in levers[digit_name].items():
            pos, lines = label(b, (lv[0], lv[1] + 2, lv[2]), [str(v)], colour)
            signs[pos] = lines
        first = levers[digit_name][1]
        pos, lines = label(b, (first[0] - 2, first[1] + 2, first[2]),
                           [digit_name.upper(), "flip ONE", "lever", "1 to 9"], colour)
        signs[pos] = lines
    for at, name in ((TENS_AT, "TENS"), (ONES_AT, "ONES")):
        pos, lines = label(b, (at[0] + 4, at[1] + 12, at[2] + 5), [name], "gray")
        signs[pos] = lines
    pos, lines = label(b, (CONVERT[0], CONVERT[1] + 13, CONVERT[2] + 10),
                       ["strength", "to binary", "build-04"], "gray")
    signs[pos] = lines

    out = out or next_version("pipeline/m4-decimal-adder")
    # Put every block into the state it will settle into, and then check that it did.
    # Without this the file records whatever state each part happened to be saved in -
    # and Minecraft only re-evaluates a component when something pokes it, so the parts
    # nothing touches stay wrong. The simulator cannot catch it: settle() recomputes
    # from scratch and always finds the right answer.
    assert b.rest(), "the build does not settle; refusing to write a resting state"
    stale = b.stale()
    assert not stale, f"{len(stale)} blocks would paste wrong, e.g. {stale[:3]}"
    assert not audit(b), "the build has stray side feeds or lines that touch"
    print(f"cells {len(b.cells)}   extent {b.extent()}")
    ox, oy, oz = b.save(
        out, "Decimal adder - two digits in, the sum on a screen",
        "x + y for two digits 1-9, shown as a decimal number 0-18. The arithmetic is "
        "six comparators working on signal strength, on two levels so the two streams "
        "never cross; the converter and both digits are lifted whole out of the "
        "library.", colours=COLOURS)
    shifted = {(x - ox, y - oy, z - oz): v for (x, y, z), v in signs.items()}
    written = embed(out, shifted)
    assert written == len(signs), f"only {written} of {len(signs)} signs took"
    print("signs written:", written)
    print("wrote", out)
    return out


if __name__ == "__main__":
    if "--emit" in sys.argv:
        emit()
    else:
        sys.exit(0 if sweep() else 1)
