#!/usr/bin/env python3
"""
Bulk-extract every distinct build in a world.

    python harvest.py <world-dir> [out-dir] [--min N]

Scans the world once, groups components into separate builds by spatial proximity,
computes a tight bounding box around each, names it from any in-world signs sitting
inside that box, and writes a .litematic plus a manifest.

Clustering is spatial rather than chunk-based on purpose: these worlds lay builds out
in tightly-spaced rows, so chunk adjacency merges everything into one blob.
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract import iter_chunks, stream_with_coords, IS_COMPONENT, to_blockstate
from litemapy import Region

MARGIN = 2              # blocks of context kept around each build
CELL = 4                # voxel size; builds separated by more than this split apart
MAX_VOLUME = 3_000_000  # guard against harvesting an entire CPU as one object

SYMBOLS = [(">=", " ge "), ("<=", " le "), ("==", " eq "), ("!=", " ne "),
           (">", " gt "), ("<", " lt "), ("+", " plus "), ("*", " x ")]
PIN_LABEL = re.compile(r"\[?\d{1,3}\]?|[A-Z]|SPACE|CIN|COUT|IN|OUT", re.I)


def safe_name(text, fallback):
    t = text.lower()
    for sym, word in SYMBOLS:
        t = t.replace(sym, word)
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return re.sub(r"-+", "-", t)[:60] or fallback


def scan(world_dir, min_blocks):
    """One pass. Returns component points (with block id) and positioned signs."""
    pts, signs = [], []
    for gcx, gcz, chunk in iter_chunks(world_dir):
        local = []
        try:
            for lx, y, lz, block in stream_with_coords(chunk):
                if IS_COMPONENT(block.id):
                    local.append((gcx * 16 + lx, y, gcz * 16 + lz, block.id))
        except Exception:
            continue
        if len(local) < min_blocks:
            continue
        pts.extend(local)
        be = chunk.data.get("block_entities")
        for e in (be or []):
            if "sign" not in str(e.get("id", "")).lower():
                continue
            texts = [t for t in re.findall(r'"text"\s*:\s*"([^"]*)"', str(dict(e))) if t.strip()]
            if texts:
                signs.append((int(str(e.get("x", 0))), int(str(e.get("y", 0))),
                              int(str(e.get("z", 0))), " ".join(texts)))
    return pts, signs


def cluster(pts):
    """Voxelise to CELL and flood-fill occupied cells (26-connected)."""
    cells = defaultdict(list)
    for p in pts:
        cells[(p[0] // CELL, p[1] // CELL, p[2] // CELL)].append(p)
    seen, groups = set(), []
    for start in cells:
        if start in seen:
            continue
        stack, group = [start], []
        seen.add(start)
        while stack:
            cx, cy, cz = stack.pop()
            group.extend(cells[(cx, cy, cz)])
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        n = (cx + dx, cy + dy, cz + dz)
                        if n in cells and n not in seen:
                            seen.add(n)
                            stack.append(n)
        groups.append(group)
    return groups


def harvest(world_dir, out_dir, min_blocks):
    os.makedirs(out_dir, exist_ok=True)
    print(f"Scanning {world_dir} ...")
    pts, signs = scan(world_dir, min_blocks)
    print(f"  {len(pts):,} components, {len(signs)} signs")

    groups = [g for g in cluster(pts) if len(g) >= min_blocks]
    groups.sort(key=len, reverse=True)
    print(f"  {len(groups)} distinct builds\n")

    wanted = {(p[0] >> 4, p[2] >> 4) for g in groups for p in g}
    chunks = {(a, b): c for a, b, c in iter_chunks(world_dir) if (a, b) in wanted}

    index, used = [], Counter()
    for gi, group in enumerate(groups):
        xs = [p[0] for p in group]; ys = [p[1] for p in group]; zs = [p[2] for p in group]
        x1, x2 = min(xs) - MARGIN, max(xs) + MARGIN
        y1, y2 = min(ys) - MARGIN, max(ys) + MARGIN
        z1, z2 = min(zs) - MARGIN, max(zs) + MARGIN
        w, h, l = x2 - x1 + 1, y2 - y1 + 1, z2 - z1 + 1
        counts = Counter(p[3] for p in group)

        # Signs inside this build's box (slightly widened) name it
        near = [t for sx, sy, sz, t in signs
                if x1 - 2 <= sx <= x2 + 2 and y1 - 2 <= sy <= y2 + 2 and z1 - 2 <= sz <= z2 + 2]
        titles = [t for t in dict.fromkeys(near) if not PIN_LABEL.fullmatch(t.strip())]
        base = safe_name(titles[0], f"build-{gi:02d}") if titles else f"build-{gi:02d}"
        used[base] += 1
        name = base if used[base] == 1 else f"{base}-{used[base]}"

        if w * h * l > MAX_VOLUME:
            print(f"  SKIP {name:44} {w}x{h}x{l} = {w*h*l:,} (over limit)")
            continue

        reg = Region(0, 0, 0, w, h, l)
        placed = Counter()
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    ch = chunks.get((x >> 4, z >> 4))
                    if ch is None:
                        continue
                    try:
                        b = ch.get_block(x & 15, y, z & 15)
                    except Exception:
                        continue
                    if b is None or b.id == "air":
                        continue
                    reg[x - x1, y - y1, z - z1] = to_blockstate(b)
                    placed[b.id] += 1

        reg.as_schematic(name=name, author="extracted",
                         description=f"{os.path.basename(world_dir)} @ {x1},{y1},{z1}"
                         ).save(os.path.join(out_dir, f"{name}.litematic"))

        entry = {
            "name": name, "labels": list(dict.fromkeys(near)),
            "source_world": os.path.basename(world_dir.rstrip("/")),
            "source_origin": [x1, y1, z1], "size": [w, h, l],
            "non_air_blocks": sum(placed.values()),
            "redstone_components": sum(counts.values()),
            "component_census": dict(counts.most_common()),
            "full_census": dict(placed.most_common()),
        }
        with open(os.path.join(out_dir, f"{name}.manifest.json"), "w") as f:
            json.dump(entry, f, indent=2)
        index.append(entry)
        lbl = (" | ".join(near[:3]))[:34]
        print(f"  {name:42} {w:3}x{h:3}x{l:3} {sum(counts.values()):5}c  {lbl}")

    with open(os.path.join(out_dir, "index.json"), "w") as f:
        json.dump(index, f, indent=2)
    print(f"\n{len(index)} builds -> {out_dir}/")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    out = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else "primitives"
    mn = int(sys.argv[sys.argv.index("--min") + 1]) if "--min" in sys.argv else 20
    harvest(sys.argv[1], out, mn)
