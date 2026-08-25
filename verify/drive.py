#!/usr/bin/env python3
"""
Drive an extracted build through its inputs and report what it actually computes.

    python3 verify/drive.py worlds/primitives/alus/build-16.litematic
    python3 verify/drive.py <path> --exhaustive      # force the full truth table

Written because a label in this library has already been wrong: `alus/build-17` was
read from its shape as "a single AND gate" at confidence `high`, and driving it showed
a 3-input XOR. Seventeen ALU readings are still shape-derived guesses, and driving one
takes seconds, so there is no reason to keep guessing.

Two passes, because exhaustive enumeration does not scale - `build-03` has 96 levers,
which is 2^96 combinations.

**Linear probe** (n+1 runs). Toggle each lever alone against an all-off baseline. That
is enough to find:

  * lamps that merely mirror one lever - the input indicators every one of these builds
    has, which would otherwise clutter every truth table
  * which outputs respond to which inputs at all, so the real function is separated
    from the wiring around it

**Exhaustive** (2^k runs), only over the inputs that survive the probe, and only when
that is small enough to be honest about. A function of few enough inputs is then
matched against the usual suspects rather than left as a table to squint at.
"""
import itertools
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "worlds"))

from sim.grid import Grid, LEVER, LAMP
from sim.engine import Sim

MAX_EXHAUSTIVE = 10          # 1024 runs; beyond this, say so rather than hang


def outputs_for(grid, levers, values):
    """
    Lamp states after driving `levers` to `values` and letting it settle.

    The grid is reused across runs rather than reloaded. That is safe only because
    EVERY lever is written on every call - the sim mutates lever cells in place, so
    setting a subset would silently inherit the previous run's inputs. A fresh Sim
    still reseeds component state from the schematic each time.
    """
    sim = Sim(grid)
    sim.set_levers({p: bool(v) for p, v in zip(levers, values)})
    sim.prime()
    settled = sim.run_until_stable(max_ticks=400)
    return sim.lamp_states(), settled, sim.time


def name_function(bits, table):
    """
    Try to name a boolean function from its truth table.

    `table` is indexed by the integer formed from the input bits, LSB first. Returns
    (label, local_index), where local_index refers to a position within THIS lamp's own
    inputs - the caller maps it back to a lever number. Reporting the local index as if
    it were the lever number reads plausibly and is wrong, which is worse than unnamed.
    """
    n = len(table)
    if all(v == table[0] for v in table):
        return f"constant {int(table[0])}", None

    def col(i):
        return [bool((idx >> i) & 1) for idx in range(n)]

    for i in range(bits):
        c = col(i)
        if table == c:
            return "mirrors lever", i
        if table == [not v for v in c]:
            return "inverts lever", i

    popcount = [bin(idx).count("1") for idx in range(n)]
    cands = {
        "AND": [p == bits for p in popcount],
        "NAND": [p != bits for p in popcount],
        "OR": [p > 0 for p in popcount],
        "NOR": [p == 0 for p in popcount],
        "XOR (odd parity)": [p % 2 == 1 for p in popcount],
        "XNOR (even parity)": [p % 2 == 0 for p in popcount],
    }
    for label, want in cands.items():
        if table == want:
            return label, None
    return None, None


def main():
    path = sys.argv[1]
    force = "--exhaustive" in sys.argv

    grid = Grid.from_file(path)
    levers = sorted(grid.of_type(LEVER))
    lamps = sorted(grid.of_type(LAMP))
    print(f"\n{path}")
    print(f"  {grid.w}x{grid.h}x{grid.l}, {len(grid.cells)} blocks, "
          f"{len(levers)} levers, {len(lamps)} lamps\n")

    # -- linear probe ------------------------------------------------------
    base, settled, _ = outputs_for(grid, levers, [0] * len(levers))
    if not settled:
        print("  NOTE: does not settle with all inputs off - a clock, or unstable\n")

    responds = {p: set() for p in lamps}
    mirrors = {}
    for i, lev in enumerate(levers):
        vals = [0] * len(levers)
        vals[i] = 1
        out, _, _ = outputs_for(grid, levers, vals)
        changed = [p for p in lamps if out.get(p) != base.get(p)]
        for p in changed:
            responds[p].add(i)
        if len(changed) == 1 and out.get(changed[0]) and not base.get(changed[0]):
            mirrors.setdefault(changed[0], i)

    indicators = {p: i for p, i in mirrors.items() if responds[p] == {i}}
    real = [p for p in lamps if p not in indicators]
    dead = [p for p in real if not responds[p]]
    live = [p for p in real if responds[p]]

    print(f"  input indicators : {len(indicators)} lamps mirror a single lever")
    print(f"  live outputs     : {len(live)}")
    if dead:
        print(f"  unmoved outputs  : {len(dead)} (never changed under any single input)")
    print()

    if not live:
        print("  nothing responded to a single input - the function may need "
              "combinations, so try --exhaustive\n")

    for p in live:
        deps = sorted(responds[p])
        print(f"  lamp {str(p):14} depends on levers {deps}")

    # -- exhaustive over the inputs that matter ----------------------------
    used = sorted({i for p in live for i in responds[p]})
    if not used:
        used = list(range(len(levers)))
    if len(used) > MAX_EXHAUSTIVE and not force:
        print(f"\n  {len(used)} relevant inputs - 2^{len(used)} combinations is too "
              f"many to enumerate.\n  Re-run with --exhaustive to force it, or drive "
              f"it by port instead.\n")
        return

    print(f"\n  exhaustive over {len(used)} inputs ({2**len(used)} runs)...")
    # Index every table by an explicit LSB-first key: bit j is `used[j]`. Relying on
    # itertools.product's own ordering is a trap - it varies the FIRST element slowest,
    # so `idx >> j` addresses the inputs in reverse and every answer comes out subtly
    # wrong rather than obviously broken.
    tables = {p: [False] * (2 ** len(used)) for p in live}
    for combo in itertools.product([0, 1], repeat=len(used)):
        vals = [0] * len(levers)
        for slot, v in zip(used, combo):
            vals[slot] = v
        key = sum(v << j for j, v in enumerate(combo))
        out, _, _ = outputs_for(grid, levers, vals)
        for p in live:
            tables[p][key] = bool(out.get(p))

    def true_deps(p):
        """
        Which inputs actually influence this lamp, taken from the exhaustive data.

        The linear probe cannot answer this. It toggles one lever at a time against an
        all-off baseline, and a gate like AND does not move under any single input -
        so the probe reports no dependency where there is one. Here an input counts if
        flipping it EVER changes the output, which is the real definition.
        """
        out = []
        for bit in range(len(used)):
            for idx in range(len(tables[p])):
                if not (idx >> bit) & 1:
                    if tables[p][idx] != tables[p][idx | (1 << bit)]:
                        out.append(used[bit])
                        break
        return out

    named, mirrors_lever = [], []
    for p in live:
        deps = true_deps(p)
        sub = list(deps)
        # Collapse the table down to just this lamp's own inputs. Same LSB-first
        # convention as `tables`: bit j of `full` is input `used[j]`.
        folded = [None] * (2 ** len(sub))
        ok = True
        for full in range(2 ** len(used)):
            key = 0
            for bit, slot in enumerate(sub):
                if (full >> used.index(slot)) & 1:
                    key |= 1 << bit
            if folded[key] is None:
                folded[key] = tables[p][full]
            elif folded[key] != tables[p][full]:
                ok = False

        if not ok:
            named.append((p, deps, "inconsistent - depends on more than its probe set",
                          folded))
            continue
        label, local = name_function(len(sub), folded)
        if local is not None:
            # translate back to a real lever number; the local index is meaningless
            # outside this lamp's own subset
            label = f"{label} {sub[local]}"
            if label.startswith("mirrors"):
                mirrors_lever.append(p)
        named.append((p, deps, label, folded))

    if mirrors_lever:
        print(f"\n  {len(mirrors_lever)} of those simply mirror a lever "
              f"(input indicators), leaving {len(live) - len(mirrors_lever)} real "
              f"output{'s' if len(live) - len(mirrors_lever) != 1 else ''}")

    print(f"\n  {'lamp':16} {'depends on':22} function")
    print("  " + "-" * 64)
    for p, deps, label, folded in named:
        if p in mirrors_lever:
            continue
        print(f"  {str(p):16} {str(deps):22} {label or 'UNNAMED'}")
        if label is None:
            print(f"      truth table, LSB = lever {sorted(deps)[0]}: "
                  f"{''.join('1' if v else '0' for v in folded)}")
    for p in mirrors_lever:
        deps = sorted(responds[p])
        print(f"  {str(p):16} {str(deps):22} indicator")
    print()


if __name__ == "__main__":
    main()
