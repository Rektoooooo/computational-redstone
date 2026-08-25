#!/usr/bin/env python3
"""
Work out what an ALU-shaped build computes, without enumerating its inputs.

    python3 verify/alu_probe.py worlds/primitives/alus/build-13.litematic

`drive.py` enumerates, which dies at about 13 levers - and the builds left in this
world have 17 to 96. But they are not arbitrary boolean functions. They are adders with
control lines, so the useful question is not "what is this truth table" but "which
levers are the operands, which are the controls, and what arithmetic does each control
setting produce".

Three steps:

1. **Split the levers.** Operand levers sit in pairs at repeating stations along the
   build; controls sit apart from that grid. Position does the splitting, and the guess
   is then checked rather than trusted.
2. **Order the bits.** The carry chain gives the significance for free: the least
   significant output depends on the fewest inputs, and each next one depends on
   everything below it. No need to guess LSB-first or MSB-first.
3. **Name the arithmetic.** For every combination of the control levers, test the sum
   against the usual candidates over every operand pair.

A build that is NOT an adder simply fails every candidate, which is a real answer and
is reported as one rather than dressed up.
"""
import itertools
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "worlds"))

from sim.grid import Grid, LEVER, LAMP
from sim.engine import Sim

MAX_CONTROLS = 6            # 2^6 control settings is still a readable table


def settle(grid, levers, on):
    sim = Sim(grid)
    sim.set_levers({p: (i in on) for i, p in enumerate(levers)})
    sim.prime()
    sim.run_until_stable(max_ticks=400)
    return sim.lamp_states()


def candidates(width):
    mask = (1 << width) - 1
    return {
        "A + B":            lambda a, b: (a + b) & mask,
        "A + B + 1":        lambda a, b: (a + b + 1) & mask,
        "A + ~B":           lambda a, b: (a + (mask - b)) & mask,
        "A + ~B + 1 (A-B)": lambda a, b: (a - b) & mask,
        "~A + B":           lambda a, b: ((mask - a) + b) & mask,
        "~A + B + 1 (B-A)": lambda a, b: (b - a) & mask,
        "~A + ~B":          lambda a, b: ((mask - a) + (mask - b)) & mask,
        "~A + ~B + 1":      lambda a, b: ((mask - a) + (mask - b) + 1) & mask,
        "A AND B":          lambda a, b: a & b,
        "A OR B":           lambda a, b: a | b,
        "A XOR B":          lambda a, b: a ^ b,
        "A NOR B":          lambda a, b: mask & ~(a | b),
        "A NAND B":         lambda a, b: mask & ~(a & b),
        "A XNOR B":         lambda a, b: mask & ~(a ^ b),
        "A":                lambda a, b: a,
        "B":                lambda a, b: b,
        "~A":               lambda a, b: mask - a,
        "~B":               lambda a, b: mask - b,
    }


def main():
    path = sys.argv[1]
    grid = Grid.from_file(path)
    levers = sorted(grid.of_type(LEVER))
    lamps = sorted(grid.of_type(LAMP))
    print(f"\n{path}")
    print(f"  {len(levers)} levers, {len(lamps)} lamps\n")

    # -- 1. indicators and dependencies, from single-lever probes ----------
    base = settle(grid, levers, set())
    responds = defaultdict(set)
    indicator_of = {}
    for i in range(len(levers)):
        out = settle(grid, levers, {i})
        changed = [p for p in lamps if out.get(p) != base.get(p)]
        for p in changed:
            responds[p].add(i)
    for p in lamps:
        if len(responds[p]) == 1:
            indicator_of.setdefault(next(iter(responds[p])), p)
    outputs = [p for p in lamps if p not in set(indicator_of.values())]

    live = [p for p in outputs if responds[p]]
    unmoved = [p for p in outputs if not responds[p]]
    print(f"  {len(indicator_of)} input indicators, {len(live)} live outputs, "
          f"{len(unmoved)} never moved")
    for p in live:
        print(f"    {str(p):16} responds to {len(responds[p]):2} levers {sorted(responds[p])}")

    # -- 3. operands vs controls, from behaviour --------------------------
    # Grouping levers by position looks obvious and is wrong: control levers can share
    # an (x,z) with each other and get mistaken for an operand pair. Ask instead what
    # each lever DOES. An operand bit lights exactly one sum bit on its own; a control
    # moves many outputs or none, so the split falls out and checks itself.
    lights = {}
    for i in range(len(levers)):
        out = settle(grid, levers, {i})
        lights[i] = frozenset(p for p in live if out.get(p) != base.get(p))

    by_output = defaultdict(list)
    for i, lit in lights.items():
        if len(lit) == 1:
            by_output[next(iter(lit))].append(i)

    # A station is two levers driving one sum bit - except the least significant, where
    # the carry-in lights that same bit on its own. At that stage `A XOR B XOR Cin` is
    # symmetric, so no amount of probing separates the three; position is the only thing
    # that can, and it is used ONLY to break that one tie. The pair sharing an (x,z)
    # with each other are the operands, and the odd one out is the carry-in.
    stations_by_out = {}
    for o, v in by_output.items():
        if len(v) == 2:
            stations_by_out[o] = v
        elif len(v) == 3:
            pos = {i: (levers[i][0], levers[i][2]) for i in v}
            pair = [i for i in v if list(pos.values()).count(pos[i]) == 2]
            if len(pair) == 2:
                stations_by_out[o] = pair
    operands = sorted(i for v in stations_by_out.values() for i in v)
    controls = [i for i in range(len(levers)) if i not in operands]
    width = len(stations_by_out)
    if width < 2:
        print("\n  no lever pairs each driving a single output - "
              "not an operand/operand layout\n")
        return
    if len(controls) > MAX_CONTROLS:
        print(f"\n  {len(controls)} control levers is too many to sweep\n")
        return
    by_station = {o: v for o, v in stations_by_out.items()}
    paired = list(by_station.keys())

    # -- bit significance, from two structural probes ----------------------
    # Counting probe-dependencies does NOT work here: a single-lever probe misses every
    # dependency that only appears in combination, so the most significant output looks
    # like the least. Ask the adder instead.
    #
    #   one lever at station s   ->  sum bit s alone lights: that is s's own output
    #   both levers at station s ->  s sums to 0 and carries: the NEXT bit up lights
    # A station is already keyed by the output its own bit drives, so only the carry
    # needs probing: both levers on makes that stage sum to 0 and carry, lighting the
    # next bit up.
    own = {s: s for s in paired}
    nxt = {}
    for s in paired:
        a, b = by_station[s]
        out = settle(grid, levers, {a, b})
        lit = [p for p in live if out.get(p) != base.get(p)]
        if len(lit) == 1:
            nxt[s] = lit[0]

    # a station is the LSB if no other station carries into it
    carried_into = {nxt[s] for s in nxt}
    starts = [s for s in paired if own[s] not in carried_into]
    if len(starts) != 1:
        print(f"\n  carry chain is ambiguous ({len(starts)} candidate LSBs)\n")
        return

    stations, seen = [starts[0]], {starts[0]}
    while True:
        s = stations[-1]
        following = [t for t in paired if t not in seen and own[t] == nxt.get(s)]
        if not following:
            break
        stations.append(following[0])
        seen.add(following[0])

    if len(stations) != width:
        print(f"\n  carry chain covers {len(stations)} of {width} stations\n")
        return

    A = [by_station[s][0] for s in stations]
    B = [by_station[s][1] for s in stations]
    sum_bits = [own[s] for s in stations]

    print(f"\n  {width}-bit operands")
    print(f"    A levers {A}\n    B levers {B}\n    controls {controls}")
    print(f"    sum lamps (LSB first) {sum_bits}\n")

    def read(a, b, ctrl):
        on = set(ctrl)
        for i, li in enumerate(A):
            if (a >> i) & 1:
                on.add(li)
        for i, li in enumerate(B):
            if (b >> i) & 1:
                on.add(li)
        out = settle(grid, levers, on)
        return sum(1 << i for i, p in enumerate(sum_bits) if out.get(p))

    cands = candidates(width)
    print(f"  {'controls on':22} computes")
    print("  " + "-" * 52)
    for r in range(len(controls) + 1):
        for combo in itertools.combinations(controls, r):
            # Sweep the inputs ONCE and compare the table against every candidate.
            # Calling read() inside the per-candidate check re-ran the whole sweep for
            # each one, which is the same answer at sixteen times the cost.
            observed = {(a, b): read(a, b, combo)
                        for a in range(1 << width) for b in range(1 << width)}
            hits = [name for name, f in cands.items()
                    if all(v == f(a, b) for (a, b), v in observed.items())]
            label = " / ".join(hits) if hits else "no candidate matched"
            print(f"  {str(list(combo)):22} {label}")
    print()


if __name__ == "__main__":
    main()
