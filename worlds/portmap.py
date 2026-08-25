#!/usr/bin/env python3
"""
Derive an I/O port map for every extracted primitive.

    python portmap.py [primitives-dir]

The insight: in these test-rig builds the interface is already visible in the blocks.
Levers and buttons are inputs, lamps and trapdoors are outputs. Their positions are
the port map, and collinear runs of them are multi-bit ports.

Writes a "ports" block into each manifest and a PORTMAPS.md summary.

What is fact and what is not:
  FACT      block type and position - read directly
  FACT      collinearity - geometry
  INFERRED  bit ORDER within a port. Assumed least-significant-first along the run
            (ascending y for vertical ports, ascending x/z for horizontal). The source
            worlds label bits with [1][2][4]...[128] signs; those signs are the real
            authority and are not carried into the .litematic, so ordering here is a
            reasonable guess that should be checked before wiring anything.
"""
import json
import os
import sys
from collections import defaultdict

from litemapy import Schematic

INPUTS = {"lever", "stone_button", "oak_button", "polished_blackstone_button"}
OUTPUTS = {"redstone_lamp"}
OUTPUT_SUFFIX = ("_trapdoor",)


def kind(block_id):
    bid = block_id.replace("minecraft:", "")
    if bid in INPUTS:
        return "input"
    if bid in OUTPUTS or bid.endswith(OUTPUT_SUFFIX):
        return "output"
    return None


def collect(region):
    """All I/O blocks with their local positions."""
    out = []
    for x in range(region.width):
        for y in range(region.height):
            for z in range(region.length):
                b = region[x, y, z]
                k = kind(b.id)
                if k:
                    out.append({"kind": k, "id": b.id.replace("minecraft:", ""),
                                "pos": [x, y, z]})
    return out


def group_ports(blocks):
    """
    Group I/O blocks into ports.

    A port is a run of same-kind blocks sharing two of three coordinates - i.e.
    collinear along one axis. That is how multi-bit buses are physically laid out.
    """
    ports = []
    for k in ("input", "output"):
        items = [b for b in blocks if b["kind"] == k]
        # bucket by each of the three possible axes
        for axis, (a, b_) in enumerate([(1, 2), (0, 2), (0, 1)]):
            buckets = defaultdict(list)
            for it in items:
                p = it["pos"]
                buckets[(p[a], p[b_])].append(it)
            for key, group in buckets.items():
                if len(group) < 2:
                    continue
                group.sort(key=lambda g: g["pos"][axis])
                coords = [g["pos"][axis] for g in group]
                # contiguous-ish run: no gap larger than 3 blocks
                if max(b2 - a2 for a2, b2 in zip(coords, coords[1:])) > 3:
                    continue
                ports.append({
                    "kind": k, "axis": "xyz"[axis], "width": len(group),
                    "positions": [g["pos"] for g in group],
                    "block": group[0]["id"],
                    "bit_order": "inferred: ascending " + "xyz"[axis],
                })
    # drop ports fully contained in a wider one on the same axis
    ports.sort(key=lambda p: -p["width"])
    kept = []
    for p in ports:
        pts = {tuple(q) for q in p["positions"]}
        if any(pts <= {tuple(q) for q in k2["positions"]} for k2 in kept):
            continue
        kept.append(p)
    return kept


def main(root="primitives"):
    lines = ["# I/O port maps", "",
             "Derived from the interface blocks in each build: levers and buttons are",
             "inputs, lamps and trapdoors are outputs. Collinear runs are multi-bit ports.",
             "",
             "**Positions and widths are facts** — read off the blocks. **Bit order is",
             "inferred** (assumed least-significant-first along the run). The source worlds",
             "label bits with `[1][2][4]…[128]` signs, which are the real authority but are",
             "not carried into the `.litematic`. Check ordering before wiring anything.", ""]
    done = 0
    cur = None
    for world in sorted(os.listdir(root)):
        wdir = os.path.join(root, world)
        if not os.path.isdir(wdir):
            continue
        for f in sorted(os.listdir(wdir)):
            if not f.endswith(".litematic"):
                continue
            mp = os.path.join(wdir, f.replace(".litematic", ".manifest.json"))
            if not os.path.exists(mp):
                continue
            try:
                reg = list(Schematic.load(os.path.join(wdir, f)).regions.values())[0]
            except Exception:
                continue
            blocks = collect(reg)
            ports = group_ports(blocks)
            m = json.load(open(mp))
            m["ports"] = {
                "io_blocks": len(blocks),
                "inputs": sum(1 for b in blocks if b["kind"] == "input"),
                "outputs": sum(1 for b in blocks if b["kind"] == "output"),
                "ports": ports,
                "caveat": "positions and widths are measured; bit order is inferred",
            }
            json.dump(m, open(mp, "w"), indent=2)
            done += 1
            if ports:
                if world != cur:
                    cur = world
                    lines += ["", f"## {world}", ""]
                widths = ", ".join(f"{p['kind'][:3]}×{p['width']}({p['axis']})" for p in ports[:6])
                lines.append(f"- **`{m['name']}`** — {m['ports']['inputs']} in / "
                             f"{m['ports']['outputs']} out · ports: {widths}")
    open(os.path.join(root, "PORTMAPS.md"), "w").write("\n".join(lines))
    print(f"port-mapped {done} builds -> {root}/PORTMAPS.md")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "primitives")
