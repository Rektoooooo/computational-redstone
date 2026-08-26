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

from analog import (Build, decay_line, relay, wire, station, gadget,
                    constant)
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
    relay(b, src, [("east", 2), ("south", tgt[2] + 2 - src[2]),
                   ("east", tgt[0] - src[0] - 2), ("north", 2)], why="x2 in")

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

    return {"S": S, "ones": ones, "carry": carry}


# -- checking ---------------------------------------------------------------

def expected(x, y):
    """What the machine should say, worked the way the circuit works."""
    S = 15 - max(0, (15 - x) - y)          # min(15, x + y)
    q = max(0, (15 - y) - 5)               # 10 - y
    r = max(0, x - q)                      # max(0, x + y - 10)
    carry = S >= 10
    return {"S": S, "R": r, "carry": carry,
            "ones": r if carry else S}


def build():
    b = Build()
    readouts, levers = input_panel(b)
    nodes = core(b, readouts)
    b.add_floor()
    return b, levers, nodes


def sweep(limit=None):
    from sim.engine import Sim
    b, levers, nodes = build()
    print(f"cells: {len(b.cells)}   extent: {b.extent()}")

    for pos, side, other, oid in b.interference():
        print(f"  INTERFERENCE {pos} side {side} fed by {oid} at {other} "
              f"({b.notes.get(other, '?')})")
    joins = {("S = min(15, x+y) out", "decay line")}     # the tap grows out of S
    for a, c in b.stray_dust():
        na, nc = b.notes.get(a), b.notes.get(c)
        if na != nc and (na, nc) not in joins and (nc, na) not in joins:
            print(f"  DUST TOUCHING {a} ({na}) - {c} ({nc})")

    grid = b.grid()
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
            got = {k: s.dust_power(v) for k, v in nodes.items()}
            got["carry"] = bool(got["carry"])
            if any(got[k] != want[k] for k in ("S", "ones", "carry")):
                fails += 1
                if fails <= 8:
                    print(f"  {x}+{y}: got  " +
                          " ".join(f"{k}={got[k]}" for k in ("S", "carry", "ones"))
                          + "   want  " +
                          " ".join(f"{k}={want[k]}" for k in ("S", "carry", "ones")))
    print(f"\n{100 - fails}/100 correct")
    return fails == 0


# One wool colour per line, so the build can be traced from above. Painted on the FLOOR
# under each cell, which leaves the redstone itself readable.
COLOURS = {
    "x lever": "light_blue", "y lever": "lime",
    "x in": "light_blue", "x2 in": "cyan",
    "y in": "lime", "y2 in": "green",
    "nx": "orange", "u ": "orange", "u =": "orange", "S ": "orange", "S =": "orange",
    "ny": "magenta", "q ": "magenta", "q =": "magenta", "r ": "magenta", "r =": "magenta",
    "decay line": "white", "carry": "red", "constant": "yellow",
    "ones": "purple", "Sg": "purple",
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
                       ["ANSWER", "ones digit", "0-9 as", "signal strength"], "purple")
    signs[pos] = lines
    pos, lines = label(b, (ones[0] + 2, ones[1] + 3, ones[2]),
                       ["DISPLAY", "goes here", "-- not wired", "yet --"], "red")
    signs[pos] = lines

    out = out or next_version("pipeline/m4-core")
    print(f"cells {len(b.cells)}   extent {b.extent()}   "
          f"interference {len(b.interference())}")
    ox, oy, oz = b.save(out, "M4 core - signal-strength adder",
                        "x + y for two decimal digits, in signal strength. Seven "
                        "comparators. The answer comes out as a strength 0-9 at the "
                        "merge; the display is not attached yet.", colours=COLOURS)
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
