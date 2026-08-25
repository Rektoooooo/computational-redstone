"""
Timing micro-circuits with known answers.

Everything here counts in GAME ticks: one redstone tick is two of them, so a repeater
on its default setting takes 2 and a "4" takes 8. Written from the rules rather than
from the engine, for the reason recorded in test_units.py - fixtures that agree with
the code they test prove only that both are consistent.

Run:  python -m sim.tests.test_ticks
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sim.grid import Grid, Cell
from sim.engine import Sim
from sim.ticks import TickQueue, EXTREMELY_HIGH, VERY_HIGH, HIGH, NORMAL

PASS, FAIL = [], []


def check(name, got, want):
    if got == want:
        PASS.append(name)
        print(f"  PASS  {name}")
    else:
        FAIL.append(name)
        print(f"  FAIL  {name}\n          got  {got}\n          want {want}")


def build(cells):
    g = Grid()
    for pos, (bid, props) in cells.items():
        g.cells[pos] = Cell(bid, props)
    xs = [p[0] for p in cells] or [0]
    ys = [p[1] for p in cells] or [0]
    zs = [p[2] for p in cells] or [0]
    g.w, g.h, g.l = max(xs) + 1, max(ys) + 1, max(zs) + 1
    return g


def ticks_until(sim, want, pos, limit=40):
    """Game ticks until `pos` reaches `want`, or None."""
    for i in range(1, limit + 1):
        sim.tick()
        if sim.states.get(pos) == want:
            return i
    return None


# -- the queue itself -------------------------------------------------------

q = TickQueue()
check("scheduling a position returns True", q.schedule((0, 0, 0), 5), True)
check("scheduling it again is refused - the pending guard",
      q.schedule((0, 0, 0), 3), False)
check("and it is still queued only once", len(q), 1)

q = TickQueue()
q.schedule(("a",), 5, NORMAL)
q.schedule(("b",), 5, EXTREMELY_HIGH)
q.schedule(("c",), 5, HIGH)
q.schedule(("d",), 5, VERY_HIGH)
check("same tick drains in priority order",
      q.drain_due(5), [("b",), ("d",), ("c",), ("a",)])

q = TickQueue()
q.schedule(("first",), 5, NORMAL)
q.schedule(("second",), 5, NORMAL)
check("equal priority falls back to insertion order",
      q.drain_due(5), [("first",), ("second",)])

q = TickQueue()
q.schedule(("late",), 9)
q.schedule(("early",), 4)
check("nothing drains before it is due", q.drain_due(3), [])
check("earlier tick comes out first", q.drain_due(4), [("early",)])


# -- component delays -------------------------------------------------------

def repeater_line(delay):
    """lever -> dust -> repeater -> dust, all off to begin with."""
    return {(0, 0, 0): ("purple_wool", {}),
            (0, 1, 0): ("lever", {"powered": "false", "face": "floor"}),
            (1, 0, 0): ("purple_wool", {}),
            (1, 1, 0): ("redstone_wire", {"east": "side", "west": "side",
                                          "north": "none", "south": "none"}),
            (2, 0, 0): ("purple_wool", {}),
            (2, 1, 0): ("repeater", {"facing": "west", "delay": str(delay),
                                     "powered": "false", "locked": "false"}),
            (3, 0, 0): ("purple_wool", {}),
            (3, 1, 0): ("redstone_wire", {"east": "side", "west": "side",
                                          "north": "none", "south": "none"})}


for setting, expected in ((1, 2), (2, 4), (4, 8)):
    sim = Sim(build(repeater_line(setting))).prime()
    sim.set_lever((0, 1, 0), True)
    check(f"repeater on {setting} takes {expected} game ticks",
          ticks_until(sim, True, (2, 1, 0)), expected)

# a comparator is always 2 game ticks, whatever is in front of it
cells = repeater_line(1)
cells[(2, 1, 0)] = ("comparator", {"facing": "west", "mode": "compare",
                                   "powered": "false"})
sim = Sim(build(cells)).prime()
sim.set_lever((0, 1, 0), True)
check("comparator takes 2 game ticks", ticks_until(sim, 15, (2, 1, 0)), 2)

# a torch inverts after 2 game ticks. Lever is mounted on the torch's own support,
# so powering it puts the torch out.
torch_cells = {(2, 0, 0): ("purple_wool", {}),
               (2, 1, 0): ("redstone_torch", {"lit": "true"}),
               (1, 0, 0): ("lever", {"powered": "false", "face": "wall",
                                     "facing": "west"})}
sim = Sim(build(torch_cells)).prime()
sim.set_lever((1, 0, 0), True)
check("torch goes out 2 game ticks after its support is powered",
      ticks_until(sim, False, (2, 1, 0)), 2)


# -- a circuit with no steady state ----------------------------------------

# Wall torch feeding dust that runs back onto its own support: the classic torch
# clock. It has no resting state, so the test is that it oscillates on period rather
# than that it settles.
clock = {(0, 1, 0): ("purple_wool", {}),                    # the torch's support
         (1, 1, 0): ("redstone_wall_torch", {"facing": "east", "lit": "true"}),
         (1, 2, 0): ("redstone_wire", {"west": "side", "east": "none",
                                       "north": "none", "south": "none"}),
         (0, 2, 0): ("redstone_wire", {"east": "side", "west": "none",
                                       "north": "none", "south": "none"})}
sim = Sim(build(clock)).prime()
torch = (1, 1, 0)
trace = []
for _ in range(12):
    sim.tick()
    trace.append(bool(sim.states.get(torch)))

check("a torch clock does not settle", sim.run_until_stable(max_ticks=20), False)
check("and it toggles every 2 game ticks",
      trace, [True, False, False, True, True, False,
              False, True, True, False, False, True])

# -- a lamp is not symmetric ------------------------------------------------

# It lights the instant it is powered and waits 4 game ticks before going dark, which
# is deliberate anti-flicker behaviour. Both halves were measured in game with tick
# stepping; the steady state is identical either way, so nothing but timing reveals it.
lamp_cells = {(0, 1, 0): ("redstone_lamp", {"lit": "false"}),
              (1, 1, 0): ("lever", {"powered": "false", "face": "wall",
                                    "facing": "west"}),
              (1, 0, 0): ("purple_wool", {})}
LAMP_POS = (0, 1, 0)

sim = Sim(build(lamp_cells)).prime()
sim.set_lever((1, 1, 0), True)
# No tick needed: flipping the lever reaches the lamp at once. Confirmed in game -
# with the world frozen, the dust lit the moment the lever moved, before any step.
check("a lamp lights immediately, with no tick at all",
      sim.lamp_states().get(LAMP_POS), True)

sim.set_lever((1, 1, 0), False)
start = sim.time
off_after = None
for _ in range(20):
    sim.tick()
    if not sim.lamp_states().get(LAMP_POS):
        off_after = sim.time - start
        break
check("a lamp waits 4 game ticks before going dark", off_after, 4)

# and if the power comes back inside that window, it never goes dark at all
sim = Sim(build(lamp_cells)).prime()
sim.set_lever((1, 1, 0), True)
sim.run(2)
sim.set_lever((1, 1, 0), False)
sim.tick()
sim.set_lever((1, 1, 0), True)      # back on well inside the 4-tick wait
sim.run(6)
check("power returning inside the window leaves the lamp lit",
      sim.lamp_states().get(LAMP_POS), True)

print(f"\n{len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    print("failed:", ", ".join(FAIL))
sys.exit(1 if FAIL else 0)
