#!/usr/bin/env python3
"""
x + y for two decimal digits, in signal strength.

Eighteen levers - two rows of nine, one per digit - and the sum as a number 0..18.
The output is a signal strength `ones` (0..9) and a boolean `tens`, which is what a
seven-segment decoder wants.

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

`r` is computed from a SECOND reading of the y line, taken five blocks early so it
reads `y + 5`; inverting that gives `10 - y` with no constant to build. That trick is
the reason this fits in nine comparators.

## The input is free

A lever nine blocks from the end of a dust line leaves 6 there; one six blocks away
leaves 9. So a run of dust with nine levers along it turns "which lever" into a number
with no gates at all - and because dust takes the LARGEST signal reaching it, two
levers at once gives the higher of the two rather than nonsense.

Each digit drives two parallel lines from the same lever blocks, since a powered block
feeds every dust cell touching it.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "worlds"))

from analog import (Build, decay_line, relay, wire, hex_wire, stair, climb,
                    tower, place, station, gadget, constant)
from sim.grid import DIRS, OPPOSITE, neighbour, step

Y = 1                      # the logic plane; floor goes in at Y-1

# -- the input panel --------------------------------------------------------
#
# Two lines per digit so the value can be read twice without a splitter, and one short
# line per digit tapped five blocks early to read v+5. All four run WEST from an east
# readout, with the levers to the west, so a row reads 1..9 left to right.

READOUT_X = 14             # east end of every line - where the value is
LANES = {"y": 0, "y2": 2, "x": 6, "x2": 8}
LEVER_Z = {"y": 1, "x": 7}      # lever blocks sit between the pair of lines


def input_panel(b):
    """
    The eighteen levers and the four dust lines they drive.

    Two lines per digit, either side of the lever blocks. A powered block feeds every
    dust cell touching it, so one lever drives both of its digit's lines at once - which
    is how the value is read twice with no splitter and no loss.
    """
    lines = {digit: decay_line(b, (READOUT_X, Y, z), "west", 15)
             for digit, z in LANES.items()}
    levers = {"x": {}, "y": {}}
    for digit, lz in LEVER_Z.items():
        for v in range(1, 10):
            b.block((v - 1, Y, lz), "purple_wool", f"{digit} lever {v}")
            lv = (v - 1, Y + 1, lz)
            b.lever(lv, f"{digit} = {v}")
            levers[digit][v] = lv
    return {k: cells[0] for k, cells in lines.items()}, levers


# -- the arithmetic core ----------------------------------------------------
#
# Each step is one comparator, with the value on its SIDE and either a redstone block
# (a constant 15) or the previous step on its rear.
#
# Two rules decide where they can go, and between them they fix almost every number
# below.
#
# **Parity.** A relay of comparators alternates comparator, dust, comparator, dust, and
# a comparator cannot turn - so only the dust cells may, and every move covers two
# cells. A value can therefore only reach cells an even distance away in BOTH axes.
# That splits the board into four classes, and gives one rule worth stating plainly:
#
#     a gadget's REAR source and its OUTPUT are in one class;
#     its SIDE source is in the class diagonally opposite.
#
# It is also why `q` is built from a constant rather than by reading the y line five
# blocks early, which would be cheaper: the early tap lands one block off, in the wrong
# class, and no amount of relaying moves a value between classes.
#
# **Crossing.** Two lines in one plane cannot cross. The x of each gadget fed by an
# input line IS the column that line turns south at, and a column crosses every lane
# south of its own - so the northernmost line has to turn last: 28 > 24 > 20 for y, y2
# and x. x2 turns almost at once and runs along the bottom instead. Everything after
# that is placed so that no two lines ever need to meet.
GADGETS = {
    "nx": (20, 13),      # 15 - x            side: x  turns south at 20
    "u":  (24, 17),      # nx - y            side: y2 turns south at 24, rear: nx
    "ny": (28, 13),      # 15 - y            side: y  turns south at 28
    "q":  (38, 25),      # ny - 5 = 10 - y   side: 5,  rear: ny
    "S":  (33, 32),      # 15 - u            side: u,  rear: 15
    "r":  (49, 56),      # x - q             side: q,  rear: x2 up from the bottom
}
TAP_LENGTH = 9           # dust blocks off S: the far end is lit exactly when S >= 10
# r puts the answer straight into the merge cell, so only S has to travel to reach it.
MERGE = (48, 56)
# 9 repeaters gives `ones + 6`, and six is what the climb costs. Any more and 9 + k
# would run past 15 and be capped, which loses the top of the range.
HEX_LEN, CLIMB = 9, 6

# The strength-to-binary converter, lifted whole out of the library. Its input is the
# barrel at this local coordinate; we leave the barrel out and wire the answer in.
BCD = "worlds/primitives/combinational/build-04.litematic"
BCD_IN = (6, 4, 2)
CONVERT = (66, 3, 58)    # so the barrel cell lands at y = 7, where the climb ends

# The seven-segment digit, also lifted whole: four BCD levers in, a 5x9 lamp panel out,
# and - the part that costs nothing and saves a whole circuit - BLANK for anything above
# nine. So the tens digit is a second copy fed 1 when there is a carry and 10 when there
# is not, and leading-zero suppression comes for free.
DISPLAY = "worlds/primitives/displays/build-16.litematic"
DISP_LEVERS = [(29, 9, 2 + 2 * i) for i in range(4)]      # bits 1, 2, 4, 8
TENS_AT, ONES_AT = (0, 10, 0), (0, 10, 12)   # tens on the left, looking east
TURN_X, DRIVE_Y = 52, 19     # where the bits turn north, and the height they end at
CARRY_TURN = 44            # the carry climbs at one x and turns for the tens at another


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


def boost(b, pos, direction, why):
    """
    A repeater, then dust: back to 15 before the next stretch.

    Needed between segments because each run of dust starts counting again from
    whatever is left, not from full - and a line that is fine over two legs separately
    dies where they join.
    """
    d = DIRS[direction]
    b.rep(step(pos, d), OPPOSITE[direction], why=why)
    return b.dust(step(step(pos, d), d), why)


def show(b, bits, carry):
    """Wire the four bits and the carry across to the two digits."""
    ones_feed = digit(b, ONES_AT, {0, 1, 2, 3}, "ones digit")
    tens_feed = digit(b, TENS_AT, {0, 1, 3}, "tens digit")

    for i, lamp in enumerate(bits):
        # tap the block that drives the converter's own indicator lamp, and leave the
        # lamp itself in place - it is worth having something to read in game
        driver = (lamp[0], lamp[1], lamp[2] + 1)
        rep = (driver[0] - 1, driver[1], driver[2])
        b.rep(rep, "east", why=f"bit {1 << i} tap")
        b.block((rep[0], rep[1] - 1, rep[2]), "gray_wool", f"bit {1 << i} support")
        pos = b.dust((rep[0] - 1, rep[1], rep[2]), f"bit {1 << i}")
        feed, why = ones_feed[i], f"bit {1 << i}"
        # The four bits leave the converter at four different heights, two apart, which
        # is the standard spacing for a bus - so they can run the whole way home side
        # by side without touching. Each one only climbs at the very end, in its own
        # z lane, a few blocks short of its drive point.
        #
        # Climbing earlier does not work, and the reason is worth keeping: the line
        # home would then have to pass back over its own staircase, laying a floor on
        # top of it, and a block above dust stops that dust reaching diagonally upwards.
        # The signal climbs to within two of the top and dies, with nothing in the
        # schematic looking wrong.
        pos = wire(b, pos, [("west", pos[0] - TURN_X),
                            ("north", pos[2] - feed[2])], why=why)
        pos = boost(b, pos, "west", why)
        pos = climb(b, pos, DRIVE_Y - pos[1], "west", why=why)
        pos = boost(b, pos, "west", why)
        wire(b, pos, [("west", pos[0] - feed[0])], why=why)

    # -- the tens digit -----------------------------------------------------
    #
    # It only ever shows 1 or nothing, so it is fed 1 when there is a carry and 10 when
    # there is not - and build-16 blanks for anything above nine, so the leading zero
    # suppresses itself. That is bits 1 = carry, and 2 and 8 = NOT carry.
    why = "tens"
    # straight up out of the plane on a glass tower, because at ground level the core
    # is solid in every direction from here - two cells of footprint is all it needs
    b.rep((carry[0] + 1, carry[1], carry[2]), "west", why=f"{why} copy")
    pos = b.dust((carry[0] + 2, carry[1], carry[2]), f"{why} copy")
    pos = tower(b, pos, 14, "east", why=why)
    # step aside rather than along: a tower fills the cells either side of itself with
    # glass as it zigzags, so the only clear way off it is perpendicular
    pos = boost(b, pos, "south", why)
    pos = tower(b, pos, DRIVE_Y - pos[1], "east", why=why)
    pos = boost(b, pos, "north", why)
    pos = wire(b, pos, [("north", pos[2] - 10), ("west", pos[0] - CARRY_TURN)], why=why)

    # bit 1 is the carry itself, and it turns for the display east of everything else,
    # so it never crosses the two lines carrying its inverse
    one = boost(b, pos, "north", f"{why} bit 1")
    wire(b, one, [("north", one[2] - tens_feed[0][2]),
                  ("west", one[0] - tens_feed[0][0])], why=f"{why} bit 1")

    # bits 2 and 8 are NOT carry, which is a repeater into a block and a torch on the
    # far side of it - off exactly when the block is powered. One torch feeds both,
    # since they carry the same thing.
    b.rep((pos[0] - 1, pos[1], pos[2]), "east", why=f"{why} invert")
    b.block((pos[0] - 2, pos[1], pos[2]), "gray_wool", f"{why} invert")
    b.put((pos[0] - 3, pos[1], pos[2]), "redstone_wall_torch",
          {"facing": "west", "lit": "true"}, f"{why} invert")
    n = b.dust((pos[0] - 4, pos[1], pos[2]), f"{why} not-carry")
    n = wire(b, n, [("north", n[2] - tens_feed[3][2]),
                    ("west", n[0] - tens_feed[3][0])], why=f"{why} bit 8")
    branch = boost(b, (tens_feed[1][0] + 6, n[1], tens_feed[3][2]), "north",
                   f"{why} bit 2")
    wire(b, branch, [("north", branch[2] - tens_feed[1][2]),
                     ("west", branch[0] - tens_feed[1][0])], why=f"{why} bit 2")
    return ones_feed, tens_feed


def core(b, readouts):
    """
    Build the arithmetic. Returns the cells the rest of the machine reads.

    Seven comparators, each one line of the sum written out:

        nx = 15 - x
        u  = nx - y
        S  = 15 - u          the sum, clamped at 15
        ny = 15 - y
        q  = ny - 5          which is 10 - y
        r  = x - q           which is x + y - 10, or 0
        Sg = S - carry       S, switched off when there is a carry

    and then `ones = max(Sg, r)` on a single shared dust cell.

    The merge needs no second gate, which is worth saying because it looks like it
    should: when there is no carry, `r` is `max(0, x + y - 10)` and x + y < 10, so r is
    **already zero**. One branch or the other is always dead on its own.

    Every line is spelled out leg by leg rather than searched for. A search finds the
    SHORTEST route, and a short route across the middle of the board walls off
    everything that has not been laid yet - so the last few lines always end up with
    nowhere to go. Written out, the whole thing is planar by construction: no two lines
    ever need to cross.
    """
    def side(name):
        gx, gz = GADGETS[name]
        station(b, (gx, Y, gz - 1), "north", f"{name} side")
        return (gx, Y, gz - 3)

    def out(name):
        return (GADGETS[name][0] + 1, Y, GADGETS[name][1])

    def rear(name):
        return (GADGETS[name][0] - 1, Y, GADGETS[name][1])

    def put(name, has_rear=False, facing="west", why=""):
        gx, gz = GADGETS[name]
        return gadget(b, (gx, Y, gz), "subtract", facing=facing,
                      rear="dust" if has_rear else "block", why=why or name)

    arrive = {n: side(n) for n in GADGETS if n != "Sg"}

    # -- the four input lines, east along their own lane and then south ------
    #
    # A column crosses every lane south of its own, so the northernmost line has to
    # turn last: 28 > 24 > 20 for y, y2 and x. x2 turns almost at once and runs east
    # along the bottom instead, which keeps it clear of all three.
    for lane, target in (("x", arrive["nx"]), ("y2", arrive["u"]), ("y", arrive["ny"])):
        src = readouts[lane]
        relay(b, src, [("east", target[0] - src[0]), ("south", target[2] - src[2])],
              why=f"{lane} in")
    # r faces EAST so its answer leaves to the west, straight into the merge; its rear
    # is therefore on its east side, and x2 comes up to it from below
    src = readouts["x2"]
    tgt = (GADGETS["r"][0] + 1, Y, GADGETS["r"][1])
    # right down the west side and along the bottom, so it stays clear of the strip
    # that lifts the answer out at the south-east corner
    relay(b, src, [("east", 2), ("south", 66 - src[2]), ("east", 66 - src[0] - 2),
                   ("north", 66 - tgt[2]), ("west", 66 - tgt[0])], why="x2 in")

    # -- the S stream -------------------------------------------------------
    NX = put("nx", why="nx = 15 - x")
    # south first, then east: going east along nx's own row would run this line right
    # up against the y2 column and feed its comparators from the side
    relay(b, NX, [("south", rear("u")[2] - NX[2]), ("east", rear("u")[0] - NX[0])],
          why="nx to u")
    U = put("u", has_rear=True, why="u = nx - y")
    relay(b, U, [("east", arrive["S"][0] - U[0]), ("south", arrive["S"][2] - U[2])],
          why="u to S")
    S = put("S", why="S = min(15, x+y)")

    # -- the r stream -------------------------------------------------------
    NY = put("ny", why="ny = 15 - y")
    # down a column of its own, two clear of the one carrying u to S, then across
    relay(b, NY, [("east", 6), ("south", rear("q")[2] - NY[2]),
                  ("east", rear("q")[0] - NY[0] - 6)], why="ny to q")
    constant(b, arrive["q"], "east", 5)
    Q = put("q", has_rear=True, why="q = 10 - y")
    relay(b, Q, [("east", arrive["r"][0] - Q[0]), ("south", arrive["r"][2] - Q[2])],
          why="q to r")
    R = put("r", has_rear=True, facing="east", why="r = x+y-10")

    # -- the carry ----------------------------------------------------------
    #
    # Nine dust blocks off S, each losing a level, so the far end is lit exactly when
    # S is 10 or more: the carry, read off a ruler rather than computed.
    # the tap runs EAST, towards the merge, and S itself goes south - the other way
    # round leaves the carry on the wrong side of S's own line with no way across
    tap = decay_line(b, (S[0] + 1, Y, S[2]), "east", TAP_LENGTH)[-1]
    b.rep((tap[0], Y, tap[2] + 1), "north", why="carry")
    carry = b.dust((tap[0], Y, tap[2] + 2), "carry")

    # -- the merge ----------------------------------------------------------
    #
    # r already writes into the merge cell, so Sg only has to come down onto it from
    # the north. Nothing has to cross anything.
    mx, mz = MERGE
    assert R == (mx, Y, mz), R
    ones = R
    # the carry comes at Sg from the WEST, because the cell on its east is already
    # r's own side station
    b.rep((mx - 1, Y, mz - 1), "north", why="carry into Sg")
    b.side_nodes.add((mx - 1, Y, mz - 1))
    relay(b, S, [("south", mz - S[2]), ("east", mx - 2 - S[0])], why="S across")
    b.comp((mx - 1, Y, mz), "west", "subtract", "Sg = S - carry")

    # along the merge row rather than the one above it: the line bringing S across runs
    # at mz-2, and dust one block away from dust is the same wire
    wire(b, carry, [("south", mz - 2 - carry[2]), ("east", mx - 1 - carry[0])],
         why="carry")

    # -- out of the plane ---------------------------------------------------
    #
    # The answer is a signal STRENGTH, and strength cannot be routed: every dust block
    # takes one off it. So it leaves on a hex wire - a dust line, nine repeaters, and a
    # second dust line - which arrives two ticks later reading `ones + 6`, because a
    # short run of that circuit is a free adder. The six is then spent climbing six
    # levels, since a staircase costs exactly one per step, and what lands at the top
    # is `ones` again, in an empty plane where the display can be wired without
    # crossing anything.
    b.comp((mx, Y, mz + 1), "north", "compare", "ones out")
    node = b.dust((mx, Y, mz + 2), "ones out")
    lifted = stair(b, hex_wire(b, node, "east", "south", HEX_LEN, why="ones lift"),
                   CLIMB, "east", why="ones lift")

    # -- strength to binary -------------------------------------------------
    #
    # `combinational/build-04`, straight out of the library and verified exact for all
    # sixteen strengths. Its input is a barrel read by a comparator; the barrel is left
    # out and the wire drops the answer into that cell instead. From here on everything
    # is BOOLEAN, which is the whole point - bits can be repeatered, crossed, stacked
    # and turned, and a strength can do none of those.
    # round the front of the converter rather than straight at it: its own output
    # lamps sit one block off the direct line, and dust running past a lamp lights it
    target = (CONVERT[0] + BCD_IN[0], CONVERT[1] + BCD_IN[1], CONVERT[2] + BCD_IN[2])
    relay(b, lifted, [("north", 2), ("east", target[0] - lifted[0]), ("south", 2)],
          why="into the converter")
    place(b, BCD, CONVERT, "strength to binary", skip={BCD_IN})
    bits = [(CONVERT[0] + 2, CONVERT[1] + 2 + 2 * i, CONVERT[2] + 3) for i in range(4)]

    ones_feed, tens_feed = show(b, bits, carry)

    return {"S": S, "ones": ones, "carry": carry, "lifted": lifted, "bits": bits,
            "tens_feed": tens_feed}


# -- checking ---------------------------------------------------------------

def expected(x, y):
    """What the machine should say, worked the way the circuit works."""
    S = 15 - max(0, (15 - x) - y)          # min(15, x + y)
    q = max(0, (15 - y) - 5)               # 10 - y
    r = max(0, x - q)                      # max(0, x + y - 10)
    carry = S >= 10
    ones = r if carry else S
    return {"S": S, "R": r, "carry": carry, "ones": ones, "lifted": ones,
            "binary": ones}


def build():
    b = Build()
    readouts, levers = input_panel(b)
    nodes = core(b, readouts)
    b.add_floor()
    return b, levers, nodes


PANEL = [(2, y, z) for y in range(2, 11) for z in range(3, 8)]   # the 5x9 digit


def glyphs():
    """
    What each value looks like on `build-16`, read off the component itself.

    Driven rather than written down, so the check at the end is against the real
    thing: the right PICTURE, not the right bits.
    """
    from sim.grid import Grid, LEVER
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


def sweep(limit=None):
    from sim.engine import Sim
    b, levers, nodes = build()
    print(f"cells: {len(b.cells)}   extent: {b.extent()}")

    inside = {p for p, note in b.notes.items() if note.endswith("digit")
              or note == "strength to binary"}
    for pos, side, other, oid in b.interference():
        if pos in inside and other in inside:
            continue                       # an extracted component's own wiring
        print(f"  INTERFERENCE {pos} side {side} fed by {oid} at {other} "
              f"({b.notes.get(other, '?')})")
    joins = {("S = min(15, x+y) out", "decay line"), ("ones out", "ones lift in"),
             ("tens bit 8", "tens not-carry"), ("tens bit 2", "tens bit 8")}
    for a, c in b.stray_dust():
        na, nc = b.notes.get(a), b.notes.get(c)
        if na != nc and (na, nc) not in joins and (nc, na) not in joins:
            if not (a in inside and c in inside):
                print(f"  DUST TOUCHING {a} ({na}) - {c} ({nc})")

    glyph = glyphs()
    blank = glyph[10]
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
    "x2 in": "cyan", "x in": "light_blue",
    "y2 in": "green", "y in": "lime",
    "nx": "orange", "u ": "orange", "u =": "orange", "S ": "orange", "S =": "orange",
    "ny": "magenta", "q ": "magenta", "q =": "magenta", "r ": "magenta", "r =": "magenta",
    "decay line": "white", "carry": "red", "constant": "yellow",
    "ones": "purple", "Sg": "purple", "into the converter": "purple",
}


def label(b, pos, lines, colour="white"):
    """A standing sign on its own block, clear of the circuit. Text goes in after."""
    b.block((pos[0], pos[1] - 1, pos[2]), f"{colour}_wool", "label post")
    b.put(pos, "oak_sign", {"rotation": "8"}, "label")
    return pos, lines


def emit(out=None):
    """
    Write the current state of the build out for a look in game.

    Signs and one colour per line, because this one is being looked at rather than
    tested: the point of handing it over now is to SEE where it stops.
    """
    import sys as _sys
    _sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "worlds"))
    from compose import next_version
    from signs import embed

    b, levers, nodes = build()
    signs = {}
    for digit, colour in (("x", "light_blue"), ("y", "lime")):
        for v, lv in levers[digit].items():
            pos, lines = label(b, (lv[0], lv[1] + 2, lv[2]), [str(v)], colour)
            signs[pos] = lines
        first = levers[digit][1]
        pos, lines = label(b, (first[0] - 2, first[1] + 2, first[2]),
                           [digit.upper(), "flip ONE", "lever", "1 to 9"], colour)
        signs[pos] = lines
    ones = nodes["ones"]
    pos, lines = label(b, (ones[0], ones[1] + 3, ones[2]),
                       ["the answer,", "0-9 as", "signal", "strength"], "purple")
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
    inside = {q for q, note in b.notes.items()
              if note.endswith("digit") or note == "strength to binary"}
    stray = [i for i in b.interference() if not (i[0] in inside and i[2] in inside)]
    print(f"cells {len(b.cells)}   extent {b.extent()}   stray side inputs {len(stray)}")
    ox, oy, oz = b.save(
        out, "Decimal adder - two digits in, the sum on a screen",
        "x + y for two digits 1-9, shown as a decimal number 0-18. The arithmetic is "
        "seven comparators working on signal strength; the converter and both digits "
        "are lifted whole out of the library.", colours=COLOURS)
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
