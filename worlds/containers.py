#!/usr/bin/env python3
"""
Recover container fill levels from the source worlds and attach them to manifests.

    python containers.py [primitives-dir]

Why this exists: the harvest copied block ids and properties but NOT block entities, so
every barrel in an extracted build arrived empty. Signal-strength barrels are how this
community generates specific comparator levels, and there are ~3700 comparators reading
one - so the simulator saw them all as zero and got 87% of those comparators wrong.

Rather than re-harvest 195 builds, this reads the original world for each build (using
`source_world` and `source_origin` from its manifest), computes each container's
comparator output, and writes the levels into the manifest as `containers`, keyed by
the build-local coordinate the simulator uses.

Comparator output for a container (Minecraft formula):

    strength = floor(1 + (sum(count_i / maxstack_i) / num_slots) * 14)

with an empty container reading 0 and a full one reading 15.
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract import iter_chunks

# Items that do not stack to 64. Anything unlisted is assumed to be 64.
STACK_16 = {"ender_pearl", "sign", "honey_bottle", "snowball", "egg", "bucket_of_"}
STACK_1 = {"minecart", "boat", "bucket", "lava_bucket", "water_bucket", "saddle",
           "bed", "banner", "cake", "sword", "pickaxe", "axe", "shovel", "hoe",
           "helmet", "chestplate", "leggings", "boots", "bow", "shield", "potion"}

SLOTS = {"barrel": 27, "chest": 27, "trapped_chest": 27, "hopper": 5,
         "dropper": 9, "dispenser": 9, "furnace": 3, "brewing_stand": 5,
         "shulker_box": 27}


def max_stack(item_id):
    name = item_id.replace("minecraft:", "")
    if any(k in name for k in STACK_1):
        return 1
    if any(k in name for k in STACK_16):
        return 16
    return 64


def container_strength(items, slots):
    """The comparator output a container with these items produces."""
    if not items:
        return 0
    total = 0.0
    for it in items:
        try:
            count = int(str(it.get("Count", 1)))
            iid = str(it.get("id", "minecraft:stone"))
        except Exception:
            continue
        total += count / max_stack(iid)
    if total <= 0:
        return 0
    return min(15, int(1 + (total / slots) * 14))


def world_containers(world_dir):
    """position -> comparator strength, for every container in the world."""
    out = {}
    for gcx, gcz, ch in iter_chunks(world_dir):
        for e in (ch.data.get("block_entities") or []):
            bid = str(e.get("id", "")).replace("minecraft:", "")
            slots = SLOTS.get(bid)
            if slots is None:
                continue
            try:
                x, y, z = (int(str(e.get(k, 0))) for k in ("x", "y", "z"))
            except Exception:
                continue
            items = list(e.get("Items") or [])
            out[(x, y, z)] = container_strength(items, slots)
    return out


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "primitives"
    manifests = sorted(glob.glob(os.path.join(root, "*", "*.manifest.json")))

    # group by source world so each world is scanned once
    by_world = {}
    for mp in manifests:
        m = json.load(open(mp))
        by_world.setdefault(m.get("source_world"), []).append((mp, m))

    total_found = 0
    for world, entries in sorted(by_world.items()):
        if not world or not os.path.isdir(world):
            print(f"  skip (world not present): {world}")
            continue
        print(f"scanning {world} ... ", end="", flush=True)
        cont = world_containers(world)
        print(f"{len(cont)} containers")
        for mp, m in entries:
            ox, oy, oz = m.get("source_origin", [0, 0, 0])
            w, h, l = m.get("size", [0, 0, 0])
            local = {}
            for (x, y, z), lvl in cont.items():
                lx, ly, lz = x - ox, y - oy, z - oz
                if 0 <= lx < w and 0 <= ly < h and 0 <= lz < l:
                    local[f"{lx},{ly},{lz}"] = lvl
            if local:
                m["containers"] = local
                json.dump(m, open(mp, "w"), indent=2)
                total_found += len(local)
    print(f"\nattached {total_found} container levels across {len(manifests)} manifests")


if __name__ == "__main__":
    main()
