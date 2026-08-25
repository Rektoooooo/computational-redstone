"""
Validate the simulator against the saved state of every extracted build.

    python -m sim.oracle primitives [--limit N] [--max-blocks N] [--verbose]

Each .litematic is a snapshot of a real Minecraft circuit at rest: dust power levels,
repeater/comparator powered flags and lamp lit flags are all recorded. So the test is

    seed the simulator from the saved state, settle, and check it stays there.

Framed as a fixed-point check rather than "reproduce from scratch" on purpose: a
bistable circuit (an SR latch) has more than one valid resting state, and which one it
sits in is history, not a function of the current inputs. Asking "is the saved state
stable under my model?" is both fair and a strong test.

One known blind spot: the schematic records a comparator's powered flag but not its
output LEVEL, so a comparator emitting 7 is indistinguishable from one emitting 15
until the solver works it out. Settling resolves most of these; any that remain show
up as dust mismatches downstream of a comparator.
"""
import glob
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sim.grid import Grid, DUST, LAMP, REPEATER, COMPARATOR, TORCHES, prop, truthy, as_int
from sim.engine import Sim
from sim import components as C


def check_build(path, max_blocks=60000):
    grid = Grid.from_file(path)
    if len(grid.cells) > max_blocks:
        return {"skipped": f"{len(grid.cells)} blocks"}

    sim = Sim(grid)
    converged = sim.settle()
    f, states = sim.field, sim.states

    stats = Counter()
    mismatches = []

    def note(kind, pos, got, want):
        stats[kind + "_bad"] += 1
        if len(mismatches) < 12:
            mismatches.append((kind, pos, got, want))

    for pos, cell in grid.cells.items():
        bid = cell.id
        if bid == DUST:
            want = as_int(prop(cell, "power", "0"))
            got = f.dust.get(pos, 0)
            stats["dust"] += 1
            if got == want:
                stats["dust_ok"] += 1
            else:
                note("dust", pos, got, want)
        elif bid == REPEATER:
            want = truthy(prop(cell, "powered"))
            got = bool(states.get(pos, False))
            stats["repeater"] += 1
            if got == want:
                stats["repeater_ok"] += 1
            else:
                note("repeater", pos, got, want)
        elif bid == COMPARATOR:
            want = truthy(prop(cell, "powered"))
            got = as_int(states.get(pos, 0)) > 0
            stats["comparator"] += 1
            if got == want:
                stats["comparator_ok"] += 1
            else:
                note("comparator", pos, got, want)
        elif bid in TORCHES:
            want = truthy(prop(cell, "lit", "true"))
            got = bool(states.get(pos, True))
            stats["torch"] += 1
            if got == want:
                stats["torch_ok"] += 1
            else:
                note("torch", pos, got, want)
        elif bid == LAMP:
            want = truthy(prop(cell, "lit"))
            got = C.eval_lamp(grid, f, states, pos, cell)
            stats["lamp"] += 1
            if got == want:
                stats["lamp_ok"] += 1
            else:
                note("lamp", pos, got, want)

    total = sum(stats[k] for k in ("dust", "repeater", "comparator", "torch", "lamp"))
    ok = sum(stats[k + "_ok"] for k in ("dust", "repeater", "comparator", "torch", "lamp"))
    return {"total": total, "ok": ok, "stats": stats, "mismatches": mismatches,
            "converged": converged, "blocks": len(grid.cells)}


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "primitives"
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 9999
    maxb = int(sys.argv[sys.argv.index("--max-blocks") + 1]) if "--max-blocks" in sys.argv else 60000
    verbose = "--verbose" in sys.argv

    files = sorted(glob.glob(os.path.join(root, "*", "*.litematic")))[:limit]
    grand = Counter()
    rows, skipped = [], 0

    for path in files:
        try:
            r = check_build(path, maxb)
        except Exception as e:
            print(f"  ERROR {os.path.basename(path)}: {str(e)[:70]}")
            continue
        if "skipped" in r:
            skipped += 1
            continue
        for k, v in r["stats"].items():
            grand[k] += v
        pct = 100.0 * r["ok"] / r["total"] if r["total"] else 100.0
        rows.append((pct, r["total"], os.path.relpath(path, root), r))

    rows.sort()
    print(f"\n{'agree':>7} {'checked':>8}  build")
    print("-" * 76)
    for pct, total, name, r in rows:
        flag = "" if r["converged"] else "  [oscillating]"
        print(f"{pct:6.1f}% {total:8}  {name[:52]}{flag}")

    print(f"\n{'':-<76}")
    tot = sum(grand[k] for k in ("dust", "repeater", "comparator", "torch", "lamp"))
    ok = sum(grand[k + "_ok"] for k in ("dust", "repeater", "comparator", "torch", "lamp"))
    print(f"builds checked: {len(rows)}   skipped (too large): {skipped}")
    print(f"OVERALL AGREEMENT: {ok}/{tot} = {100.0*ok/max(1,tot):.2f}%\n")
    for k in ("dust", "repeater", "comparator", "torch", "lamp"):
        if grand[k]:
            print(f"  {k:12} {grand[k+'_ok']:7}/{grand[k]:<7} "
                  f"{100.0*grand[k+'_ok']/grand[k]:6.2f}%")

    if verbose:
        print("\nsample mismatches (worst builds first):")
        for pct, total, name, r in rows[:4]:
            if not r["mismatches"]:
                continue
            print(f"\n  {name}")
            for kind, pos, got, want in r["mismatches"][:8]:
                print(f"    {kind:11} at {pos}  got {got!r}  want {want!r}")


if __name__ == "__main__":
    main()
