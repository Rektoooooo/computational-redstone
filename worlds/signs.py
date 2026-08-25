#!/usr/bin/env python3
"""
Recover sign text AND POSITION from the source worlds and attach them to manifests.

    python signs.py [primitives-dir]

Why this exists: the harvest read sign text to name builds, but kept only the strings.
The positions were thrown away, and the positions are the valuable half.

mattbatwings labels the bits of a port with signs reading 1, 2, 4, 8 ... 128. Without
their coordinates, a port map can measure where the levers are and how many there are,
but not which lever is the low bit - so `portmap.py` has to fall back on
"inferred: ascending y". Driving a build with the bit order guessed wrong produces a
confidently wrong answer, which is the worst kind.

This reads each build's source world, finds every sign inside its bounding box, and
writes text plus build-local coordinates into the manifest as `signs`. That turns
inferred bit order into a measured one wherever the author labelled the port.
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract import iter_chunks

SIGN_IDS = {"sign", "wall_sign", "hanging_sign", "wall_hanging_sign"}


def sign_text(entity):
    """
    The four lines of a sign, flattened.

    1.18 stores each line as a JSON text component, so a line is usually
    {"text":"128"} rather than a bare string. Older or hand-edited signs can be either,
    so both are handled and anything unparseable is skipped rather than guessed at.
    """
    lines = []
    for key in ("Text1", "Text2", "Text3", "Text4"):
        raw = entity.get(key)
        if raw is None:
            continue
        s = str(raw)
        try:
            parsed = json.loads(s)
            if isinstance(parsed, dict):
                s = parsed.get("text", "")
            elif isinstance(parsed, list):
                s = "".join(p.get("text", "") if isinstance(p, dict) else str(p)
                            for p in parsed)
            else:
                s = str(parsed)
        except (ValueError, TypeError):
            s = re.sub(r'^\{"text":"|"\}$', "", s)
        s = s.strip()
        if s:
            lines.append(s)
    return lines


def has_region(world_dir):
    """True if this world has actually been unpacked, one level of nesting allowed."""
    if os.path.isdir(os.path.join(world_dir, "region")):
        return True
    try:
        return any(os.path.isdir(os.path.join(world_dir, e, "region"))
                   for e in os.listdir(world_dir))
    except OSError:
        return False


def world_signs(world_dir):
    """position -> list of text lines, for every sign in the world."""
    out = {}
    for _gcx, _gcz, ch in iter_chunks(world_dir):
        for e in (ch.data.get("block_entities") or []):
            bid = str(e.get("id", "")).replace("minecraft:", "")
            if bid not in SIGN_IDS:
                continue
            try:
                x, y, z = (int(str(e.get(k, 0))) for k in ("x", "y", "z"))
            except (TypeError, ValueError):
                continue
            lines = sign_text(e)
            if lines:
                out[(x, y, z)] = lines
    return out


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "primitives"
    manifests = sorted(glob.glob(os.path.join(root, "*", "*.manifest.json")))

    by_world = {}
    for mp in manifests:
        m = json.load(open(mp))
        by_world.setdefault(m.get("source_world"), []).append((mp, m))

    total = 0
    for world, entries in sorted(by_world.items()):
        if not world or not os.path.isdir(world):
            print(f"  skip (world not present): {world}")
            continue
        if not has_region(world):
            # The world directory can exist without its region files, because the zips
            # are unpacked on demand. Skip rather than abandoning the whole run -
            # `region_files` calls sys.exit, which no ordinary except clause catches.
            print(f"  skip (not unpacked): {world}")
            continue
        print(f"scanning {world} ... ", end="", flush=True)
        found = world_signs(world)
        print(f"{len(found)} signs")
        for mp, m in entries:
            ox, oy, oz = m.get("source_origin", [0, 0, 0])
            w, h, l = m.get("size", [0, 0, 0])
            local = {}
            for (x, y, z), lines in found.items():
                lx, ly, lz = x - ox, y - oy, z - oz
                if 0 <= lx < w and 0 <= ly < h and 0 <= lz < l:
                    local[f"{lx},{ly},{lz}"] = lines
            if local:
                m["signs"] = local
                json.dump(m, open(mp, "w"), indent=2)
                total += len(local)
    print(f"\nattached {total} signs across {len(manifests)} manifests")


if __name__ == "__main__":
    main()
