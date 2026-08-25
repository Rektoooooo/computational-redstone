#!/usr/bin/env python3
"""
Recover sign text and position from the source worlds, and write them back into the
extracted .litematic files so pasted signs actually read.

    python signs.py [primitives-dir] [--no-embed]

Two problems, one cause. The harvest copied block ids and properties but not block
entities, and a sign's text lives entirely in its block entity:

  * the text was kept only as a flat list of `labels` used to name builds, with the
    POSITIONS thrown away - and the positions are the valuable half. mattbatwings
    labels a port's bits with signs reading 1, 2, 4 ... 128, so without coordinates
    `portmap.py` can measure where the levers are but not which one is the low bit,
    and has to fall back on "inferred: ascending y". Driving a build with the bit order
    guessed wrong gives a confidently wrong answer, which is the worst kind.
  * every sign in an extracted build pastes into Minecraft BLANK, so the author's own
    labelling - the most reliable identification in the whole library - is invisible
    exactly where it would be most useful.

This reads each build's source world, finds every sign inside its bounding box, records
text plus build-local coordinates in the manifest as `signs`, and then embeds them as
tile entities in the `.litematic`.

Same post-process shape as `containers.py`, and for the same reason: re-harvesting 195
builds to recover one class of data is not worth it when the source worlds are still
there to be read.

Only worlds that have been unpacked can be scanned. `cd worlds && unzip '*.zip'`.
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract import iter_chunks

SIGN_IDS = {"sign", "wall_sign", "hanging_sign", "wall_hanging_sign"}
LINE_KEYS = ("Text1", "Text2", "Text3", "Text4")


def sign_lines(entity):
    """
    A sign's four lines, blanks preserved so the layout can be restored exactly.

    1.18 stores each line as a JSON text component, so a line is usually
    {"text":"128"} rather than a bare string. Older or hand-edited signs can be either,
    so both are handled and anything unparseable is left alone rather than guessed at.
    """
    out = []
    for key in LINE_KEYS:
        raw = entity.get(key)
        if raw is None:
            out.append("")
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
        out.append(s.strip())
    return out


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
    """position -> four lines of text, for every sign in the world."""
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
            lines = sign_lines(e)
            if any(lines):
                out[(x, y, z)] = lines
    return out


def embed(litematic_path, signs):
    """
    Write sign text into a .litematic as tile entities.

    Only positions that really hold a sign block are written, so a stray coordinate
    cannot produce a tile entity with nothing to attach to. Existing sign tile entities
    are dropped first, which keeps re-runs idempotent instead of accumulating copies.
    """
    from litemapy import Schematic
    from litemapy.schematic import TileEntity
    from nbtlib.tag import Compound, String, Int, Byte

    schem = Schematic.load(litematic_path)
    region = list(schem.regions.values())[0]

    sign_at = {}
    for pos, lines in signs.items():
        x, y, z = pos
        try:
            bid = region[x, y, z].id.replace("minecraft:", "")
        except Exception:
            continue
        if "sign" in bid:
            sign_at[pos] = lines
    if not sign_at:
        return 0

    keep = [t for t in region.tile_entities
            if tuple(int(t.get_tag(k)) for k in ("x", "y", "z")) not in sign_at]
    region.tile_entities.clear()
    region.tile_entities.extend(keep)

    for (x, y, z), lines in sorted(sign_at.items()):
        data = {
            "id": String("minecraft:sign"),
            "x": Int(x), "y": Int(y), "z": Int(z),
            "Color": String("black"),
            "GlowingText": Byte(0),
        }
        for key, text in zip(LINE_KEYS, lines):
            data[key] = String(json.dumps({"text": text}))
        region.tile_entities.append(TileEntity(Compound(data)))

    schem.save(litematic_path)
    return len(sign_at)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = args[0] if args else "primitives"
    do_embed = "--no-embed" not in sys.argv

    manifests = sorted(glob.glob(os.path.join(root, "*", "*.manifest.json")))
    by_world = {}
    for mp in manifests:
        m = json.load(open(mp))
        by_world.setdefault(m.get("source_world"), []).append((mp, m))

    attached = embedded = builds = 0
    for world, entries in sorted(by_world.items()):
        if not world or not os.path.isdir(world) or not has_region(world):
            # The directory can exist without region files - the zips are unpacked on
            # demand. Skip rather than abandoning the run; note that `region_files`
            # calls sys.exit, which no ordinary except clause would catch.
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
                    local[(lx, ly, lz)] = lines
            if not local:
                continue
            m["signs"] = {f"{x},{y},{z}": [t for t in lines if t]
                          for (x, y, z), lines in local.items()}
            m["signs_raw"] = {f"{x},{y},{z}": lines for (x, y, z), lines in local.items()}
            json.dump(m, open(mp, "w"), indent=2)
            attached += len(local)
            builds += 1

            if do_embed:
                lp = mp.replace(".manifest.json", ".litematic")
                if os.path.exists(lp):
                    try:
                        embedded += embed(lp, local)
                    except Exception as e:
                        print(f"    embed failed for {os.path.basename(lp)}: {str(e)[:60]}")

    print(f"\nattached {attached} signs to {builds} manifests")
    if do_embed:
        print(f"embedded {embedded} signs into .litematic files - pasted signs now read")


if __name__ == "__main__":
    main()
