"""
Diagnose lamp disagreement across the library.

    python -m sim.lampdiag primitives [--limit N]

Applies the technique that found all three earlier bugs: never stare at one
coordinate. Instead split mismatches by DIRECTION (over- vs under-powered, which
separates a spurious source from a missing one) and CORRELATE them against the
block types around the lamp, so the culprit component names itself.
"""
import glob
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sim.grid import (Grid, DIRS, DUST, LAMP, UP, DOWN, is_conductive,
                      prop, step, truthy)
from sim.engine import Sim
from sim import components as C


def neighbours(pos):
    for delta in list(DIRS.values()) + [UP, DOWN]:
        yield step(pos, delta)


def analyse(path, max_blocks=60000):
    grid = Grid.from_file(path)
    if len(grid.cells) > max_blocks:
        return None
    sim = Sim(grid)
    sim.settle()
    f, states = sim.field, sim.states

    out = {"n": 0, "ok": 0, "over": [], "under": []}
    for pos, cell in grid.cells.items():
        if cell.id != LAMP:
            continue
        want = truthy(prop(cell, "lit"))
        got = C.eval_lamp(grid, f, states, pos, cell)
        out["n"] += 1
        if got == want:
            out["ok"] += 1
            continue
        # got=True want=False -> we lit a lamp the game left dark -> OVER-powered
        ctx = []
        for n in neighbours(pos):
            c = grid.get(n)
            if c.id == "air":
                continue
            tag = c.id
            if c.id == DUST:
                tag = f"dust(p={f.dust.get(n, 0)},act={C.dust_activates(grid, n, pos)})"
            elif is_conductive(c.id):
                tag = f"{c.id}(blk={f.block_power(n)},s={f.strong.get(n,0)},w={f.weak.get(n,0)})"
            ctx.append(tag)
        (out["over"] if got else out["under"]).append((pos, ctx))
    return out


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "primitives"
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 9999

    files = sorted(glob.glob(os.path.join(root, "*", "*.litematic")))[:limit]
    per_world = defaultdict(Counter)
    cause_over, cause_under = Counter(), Counter()
    samples = {"over": [], "under": []}

    for path in files:
        try:
            r = analyse(path)
        except Exception as e:
            print(f"  ERROR {path}: {str(e)[:60]}")
            continue
        if r is None or r["n"] == 0:
            continue
        world = os.path.basename(os.path.dirname(path))
        per_world[world]["n"] += r["n"]
        per_world[world]["ok"] += r["ok"]
        per_world[world]["over"] += len(r["over"])
        per_world[world]["under"] += len(r["under"])
        for kind, bucket in (("over", cause_over), ("under", cause_under)):
            for pos, ctx in r[kind]:
                # correlate: which block families sit next to a wrong lamp
                fams = sorted({t.split("(")[0] for t in ctx})
                bucket["+".join(fams) or "<isolated>"] += 1
                if len(samples[kind]) < 14:
                    samples[kind].append((os.path.relpath(path, root), pos, ctx))

    print(f"\n{'world':<24} {'lamps':>6} {'agree':>7}  {'over':>5} {'under':>6}")
    print("-" * 60)
    rows = sorted(per_world.items(), key=lambda kv: kv[1]["ok"] / max(1, kv[1]["n"]))
    tot = Counter()
    for world, c in rows:
        tot.update(c)
        print(f"{world:<24} {c['n']:6} {100.0*c['ok']/c['n']:6.1f}%  "
              f"{c['over']:5} {c['under']:6}")
    print("-" * 60)
    print(f"{'TOTAL':<24} {tot['n']:6} {100.0*tot['ok']/max(1,tot['n']):6.1f}%  "
          f"{tot['over']:5} {tot['under']:6}")

    for label, bucket in (("OVER-lit (we lit it, game dark)", cause_over),
                          ("UNDER-lit (we left dark, game lit)", cause_under)):
        print(f"\n{label} - neighbour block families:")
        for fams, n in bucket.most_common(12):
            print(f"  {n:6}  {fams}")

    for kind in ("over", "under"):
        print(f"\nsample {kind}:")
        for name, pos, ctx in samples[kind][:8]:
            print(f"  {name} {pos}")
            print(f"      {ctx}")


if __name__ == "__main__":
    main()
