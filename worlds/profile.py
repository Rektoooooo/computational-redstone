#!/usr/bin/env python3
"""
Enrich harvested manifests with measured structural features.

    python profile.py [primitives-dir]

Adds a "profile" block to every manifest and writes PROFILES.md.

Deliberately separates FACT from GUESS:

  measured   - things the blocks actually tell us: input width from lever count,
               output width from lamp count, logic family from component ratios,
               vertical layer period from the y-histogram.
  candidates - plausible device types, with the reason. These are inferences and
               are labelled as such. An in-world sign always beats them; structural
               guessing has already been wrong once (a comparator array that looked
               like a mux turned out to be a magnitude comparator).
"""
import json
import os
import sys
from collections import Counter

from litemapy import Schematic


def layer_period(path):
    """Detect a repeating vertical module (registers/counters stack every N blocks)."""
    try:
        reg = list(Schematic.load(path).regions.values())[0]
    except Exception:
        return None, None
    per_y = Counter()
    for y in range(reg.height):
        n = 0
        for x in range(reg.width):
            for z in range(reg.length):
                bid = reg[x, y, z].id
                if "redstone" in bid or bid.endswith(("repeater", "comparator")):
                    n += 1
        per_y[y] = n
    if not per_y:
        return None, None
    active = [y for y, n in per_y.items() if n > 0]
    if len(active) < 4:
        return None, dict(per_y)
    gaps = [b - a for a, b in zip(active, active[1:])]
    # A stacked design shows a dominant repeating stride among its busy layers
    busy = [y for y, n in per_y.items() if n >= max(per_y.values()) * 0.6]
    strides = Counter(b - a for a, b in zip(busy, busy[1:]))
    period = strides.most_common(1)[0][0] if strides else None
    return (period if period and period > 1 else None), dict(per_y)


def classify(c, total, size, lamps, levers):
    """Return (candidates, measured-notes). Candidates are inferences, not facts."""
    g = lambda *k: sum(c.get(x, 0) for x in k)
    comp = g("comparator") / total
    rep = g("repeater") / total
    torch = g("redstone_torch", "redstone_wall_torch") / total
    w, h, l = size
    cands, notes = [], []

    if torch > 0.25 and comp < 0.02:
        cands.append(("decoder / encoder", "torch-dominant with no comparators — matches "
                                           "'torches on 1s, repeaters on 0s, OR into a torch'"))
    if comp > 0.18:
        cands.append(("comparator logic (mux, cancel-tower, or CCA)",
                      "comparator-dominant — cancelling is the usual mechanism"))
    if rep > 0.22:
        cands.append(("register / counter / shift register",
                      "repeater-dominant — repeater locks are the memory primitive"))
    # A lamp-count rule was tried here and removed: it read the *test rig's* output
    # lamps as if they were decoder output lines, and confidently mislabelled the
    # CLE adder as a "26-output decoder". Lamps and levers indicate harness width,
    # not function.
    if h >= 19 and w <= 16:
        notes.append("tall and narrow — vertical, bit-per-layer construction")
    if h <= 10 and (w > 20 or l > 20):
        notes.append("flat and wide — horizontal construction")

    if levers:
        if levers >= 15:
            notes.append(f"{levers} levers — likely two 8-bit inputs")
        elif levers >= 7:
            notes.append(f"{levers} levers — likely one 8-bit input")
        else:
            notes.append(f"{levers} levers — small input, around {levers} bits")
    return cands, notes


def main(root="primitives"):
    out = []
    for world in sorted(os.listdir(root)):
        wdir = os.path.join(root, world)
        if not os.path.isdir(wdir):
            continue
        for f in sorted(os.listdir(wdir)):
            if not f.endswith(".manifest.json"):
                continue
            p = os.path.join(wdir, f)
            m = json.load(open(p))
            c = m["component_census"]
            total = max(1, m["redstone_components"])
            full = m.get("full_census", {})
            lamps = c.get("redstone_lamp", 0)
            levers = c.get("lever", 0)

            lit = p.replace(".manifest.json", ".litematic")
            period, hist = layer_period(lit)
            cands, notes = classify(c, total, m["size"], lamps, levers)
            if period:
                notes.append(f"repeating vertical module every {period} blocks — "
                             f"stacked per-bit design")

            wool = {k.replace("minecraft:", ""): v for k, v in full.items()
                    if "wool" in k or "concrete" in k}
            m["profile"] = {
                "measured": {
                    "components": total,
                    "size": m["size"],
                    "levers": levers, "lamps": lamps,
                    "targets": c.get("target", 0),
                    "ratios": {
                        "comparator": round(c.get("comparator", 0) / total, 3),
                        "repeater": round(c.get("repeater", 0) / total, 3),
                        "torch": round(sum(c.get(k, 0) for k in
                                       ("redstone_torch", "redstone_wall_torch")) / total, 3),
                        "wire": round(c.get("redstone_wire", 0) / total, 3),
                    },
                    "stack_period": period,
                    "palette": wool,
                },
                "notes": notes,
                "candidates": [{"guess": g, "because": r} for g, r in cands],
                "confidence": "labelled" if not m["name"].startswith("build-") else "inferred",
            }
            json.dump(m, open(p, "w"), indent=2)
            out.append((world, m))

    lines = ["# Structural profiles", "",
             "Measured features for every harvested build.", "",
             "## How much to trust this", "",
             "**`measured` values are facts** — read directly off the blocks. Lever and lamp",
             "counts describe the *test harness* width, ratios and stack period describe the",
             "build itself.", "",
             "**`candidate` values are weak inferences.** Benchmarked against the 18 builds",
             "whose identity is known from in-world signs, the heuristic produced a useful",
             "candidate **50%** of the time, nothing at all 44%, and something actively",
             "misleading 6%. Treat candidates as leads to check, never as labels.", "",
             "A sign always beats a guess. Structural inference has already been wrong twice:",
             "a comparator array that looked like a mux was the magnitude comparator, and the",
             "CLE adder was briefly mislabelled a decoder by a lamp-count rule that has since",
             "been removed.", ""]
    cur = None
    for world, m in out:
        if world != cur:
            cur = world
            lines += ["", f"## {world}", ""]
        pr = m["profile"]; me = pr["measured"]
        tag = "**labelled**" if pr["confidence"] == "labelled" else "inferred"
        lines.append(f"### `{m['name']}` — {tag}")
        if m.get("labels"):
            lines.append(f"Signs: {', '.join(m['labels'][:8])}")
        lines.append(f"{me['components']} components, {me['size'][0]}×{me['size'][1]}×{me['size'][2]}, "
                     f"{me['levers']} levers, {me['lamps']} lamps")
        r = me["ratios"]
        lines.append(f"Ratios — comparator {r['comparator']}, repeater {r['repeater']}, "
                     f"torch {r['torch']}, wire {r['wire']}")
        for n in pr["notes"]:
            lines.append(f"- {n}")
        for cnd in pr["candidates"]:
            lines.append(f"- *candidate:* {cnd['guess']} — {cnd['because']}")
        lines.append("")
    open(os.path.join(root, "PROFILES.md"), "w").write("\n".join(lines))
    print(f"profiled {len(out)} builds -> {root}/PROFILES.md")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "primitives")
