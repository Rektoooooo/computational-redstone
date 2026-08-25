#!/usr/bin/env python3
"""
Read Minecraft world files and pull redstone builds out as .litematic primitives.

    python extract.py survey  <world-dir>
    python extract.py extract <world-dir> x1 y1 z1 x2 y2 z2 <name>

survey   locates chunks containing redstone components, so you don't have to hunt
         coordinates by hand. Reports a component census per cluster.
extract  pulls a bounding box into a .litematic plus a JSON manifest describing
         what's inside it.

Requires:  pip install anvil-parser2 litemapy
Reads Java worlds; anvil-parser2 covers roughly 1.14-1.19, which includes the
1.18.2 worlds these builds ship in. Read-only - nothing is written back to the world.
"""
import json
import os
import re
import sys
from collections import Counter

try:
    import anvil
    from litemapy import Region, BlockState
except ImportError:
    sys.exit("Missing deps. Run:  pip install anvil-parser2 litemapy")

# What counts as "a redstone build" when hunting for clusters.
COMPONENTS = {
    "redstone_wire", "repeater", "comparator", "redstone_torch",
    "redstone_wall_torch", "redstone_block", "redstone_lamp", "lever",
    "stone_button", "target", "observer", "piston", "sticky_piston",
    "barrel", "note_block", "trapdoor",
}
IS_COMPONENT = lambda bid: bid in COMPONENTS or bid.endswith("_trapdoor")


def region_files(world_dir):
    rdir = os.path.join(world_dir, "region")
    if not os.path.isdir(rdir):
        # Some zips nest the world one level down
        for entry in sorted(os.listdir(world_dir)):
            cand = os.path.join(world_dir, entry, "region")
            if os.path.isdir(cand):
                return cand, sorted(f for f in os.listdir(cand) if f.endswith(".mca"))
        sys.exit(f"No region/ directory under {world_dir}")
    return rdir, sorted(f for f in os.listdir(rdir) if f.endswith(".mca"))


def iter_chunks(world_dir):
    """Yield (chunk_x, chunk_z, chunk) for every generated chunk."""
    rdir, files = region_files(world_dir)
    for fn in files:
        m = re.match(r"r\.(-?\d+)\.(-?\d+)\.mca", fn)
        if not m:
            continue
        rx, rz = int(m.group(1)), int(m.group(2))
        try:
            region = anvil.Region.from_file(os.path.join(rdir, fn))
        except Exception:
            continue
        for cx in range(32):
            for cz in range(32):
                try:
                    chunk = anvil.Chunk.from_region(region, cx, cz)
                except Exception:
                    continue  # ungenerated
                yield rx * 32 + cx, rz * 32 + cz, chunk


# stream_chunk() yields 384 layers x 256 blocks, y-major, starting at y=-64.
# Verified against get_block on a real 1.18.2 world (see probe --verify).
MIN_Y = -64
LAYER = 256


def stream_with_coords(chunk):
    """Yield (x, y, z, block) in chunk-local x/z with global y."""
    for i, block in enumerate(chunk.stream_chunk()):
        y = MIN_Y + i // LAYER
        rem = i % LAYER
        yield rem % 16, y, rem // 16, block


def chunk_signs(chunk):
    """Sign text placed by the build's author - the most reliable label there is."""
    out = []
    be = chunk.data.get("block_entities")
    if not be:
        return out
    for e in be:
        if "sign" not in str(e.get("id", "")).lower():
            continue
        texts = [t for t in re.findall(r'"text"\s*:\s*"([^"]*)"', str(dict(e))) if t.strip()]
        if texts:
            out.append((int(str(e.get("y", 0))), " ".join(texts)))
    return out


def chunk_profile(chunk):
    """Component counts plus the y-range they occupy."""
    counts, ys = Counter(), []
    for x, y, z, block in stream_with_coords(chunk):
        if IS_COMPONENT(block.id):
            counts[block.id] += 1
            ys.append(y)
    return counts, (min(ys), max(ys)) if ys else (None, None)


def survey(world_dir):
    """Report which chunks hold redstone, and what's in them."""
    print(f"Surveying {world_dir}\n")
    found, total = [], Counter()

    for gcx, gcz, chunk in iter_chunks(world_dir):
        try:
            counts, yr = chunk_profile(chunk)
        except Exception:
            continue
        if sum(counts.values()) >= 20:  # ignore incidental blocks
            found.append((gcx, gcz, counts, yr, chunk_signs(chunk)))
            total.update(counts)

    if not found:
        print("No redstone-dense chunks found.")
        return

    found.sort(key=lambda f: -sum(f[2].values()))
    print(f"{'blocks':>7}  {'world x/z':>16}  {'y range':>12}  label / top components")
    print("-" * 92)
    for gcx, gcz, counts, (y0, y1), signs in found[:40]:
        n = sum(counts.values())
        if signs:
            label = "[" + "] [".join(dict.fromkeys(t for _, t in signs)) + "]"
        else:
            label = ", ".join(f"{k.replace('minecraft:','')}:{v}" for k, v in counts.most_common(3))
        print(f"{n:7}  {gcx*16:7},{gcz*16:7}  {str(y0)+'..'+str(y1):>12}  {label[:52]}")

    print(f"\n{len(found)} dense chunks. Totals:")
    for k, v in total.most_common(12):
        print(f"   {v:7}  {k}")
    print("\nEach row covers a 16x16 area starting at the world x/z shown.")
    print("Extract with:  extract.py extract <world> x y0 z x+15 y1 z+15 <name>")


def probe(world_dir, cx, cz, verify=False):
    """Detail one chunk: per-layer component profile, and optionally verify coords."""
    for gcx, gcz, chunk in iter_chunks(world_dir):
        if (gcx, gcz) != (cx, cz):
            continue
        if verify:
            bad = 0
            for x, y, z, block in stream_with_coords(chunk):
                if IS_COMPONENT(block.id):
                    if chunk.get_block(x, y, z).id != block.id:
                        bad += 1
                    if bad > 3:
                        break
            print(f"coordinate check: {'FAIL' if bad else 'PASS'} "
                  f"({'stream and get_block disagree' if bad else 'stream matches get_block'})\n")
        layers = {}
        for x, y, z, block in stream_with_coords(chunk):
            if IS_COMPONENT(block.id):
                layers.setdefault(y, Counter())[block.id] += 1
        print(f"chunk {cx},{cz}  world x {cx*16}..{cx*16+15}, z {cz*16}..{cz*16+15}\n")
        print(f"{'y':>5}  {'n':>5}  components")
        for y in sorted(layers):
            c = layers[y]
            top = ", ".join(f"{k.replace('minecraft:','')}:{v}" for k, v in c.most_common(4))
            print(f"{y:5}  {sum(c.values()):5}  {top}")
        return
    print(f"chunk {cx},{cz} not found")


def to_blockstate(block):
    """anvil Block -> litemapy BlockState, preserving properties."""
    bid = block.id if ":" in block.id else f"{block.namespace}:{block.id}"
    props = {}
    for k, v in (block.properties or {}).items():
        val = getattr(v, "value", v)          # unwrap NBT tags
        props[str(k)] = str(val).lower() if isinstance(val, bool) else str(val)
    try:
        return BlockState(bid, **props)
    except Exception:
        return BlockState(bid)                # drop bad props rather than fail


def extract(world_dir, x1, y1, z1, x2, y2, z2, name):
    x1, x2 = sorted((x1, x2))
    y1, y2 = sorted((y1, y2))
    z1, z2 = sorted((z1, z2))
    w, h, l = x2 - x1 + 1, y2 - y1 + 1, z2 - z1 + 1
    print(f"Extracting {w}x{h}x{l} = {w*h*l:,} blocks from ({x1},{y1},{z1})")

    # Cache the chunks we need
    needed = {(x >> 4, z >> 4) for x in range(x1, x2 + 1) for z in range(z1, z2 + 1)}
    chunks = {}
    for gcx, gcz, chunk in iter_chunks(world_dir):
        if (gcx, gcz) in needed:
            chunks[(gcx, gcz)] = chunk
    print(f"Loaded {len(chunks)}/{len(needed)} chunks")

    reg = Region(0, 0, 0, w, h, l)
    census, air = Counter(), 0
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            for z in range(z1, z2 + 1):
                chunk = chunks.get((x >> 4, z >> 4))
                if chunk is None:
                    air += 1
                    continue
                try:
                    b = chunk.get_block(x & 15, y, z & 15)
                except Exception:
                    air += 1
                    continue
                if b is None or b.id == "air":
                    air += 1
                    continue
                reg[x - x1, y - y1, z - z1] = to_blockstate(b)
                census[b.id] += 1

    schem = reg.as_schematic(name=name, author="extracted", description=f"from {os.path.basename(world_dir)}")
    out = f"{name}.litematic"
    schem.save(out)

    manifest = {
        "name": name,
        "source_world": os.path.basename(world_dir.rstrip("/")),
        "source_origin": [x1, y1, z1],
        "size": [w, h, l],
        "non_air_blocks": sum(census.values()),
        "component_census": dict(census.most_common()),
    }
    with open(f"{name}.manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nSaved {out} + {name}.manifest.json")
    print(f"  {sum(census.values()):,} blocks placed, {air:,} air")
    for k, v in census.most_common(10):
        print(f"    {v:6}  {k}")


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd == "survey":
        survey(sys.argv[2])
    elif cmd == "probe":
        if len(sys.argv) < 5:
            sys.exit("usage: extract.py probe <world> <chunkX> <chunkZ> [--verify]")
        probe(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), "--verify" in sys.argv)
    elif cmd == "extract":
        if len(sys.argv) != 10:
            sys.exit("usage: extract.py extract <world> x1 y1 z1 x2 y2 z2 <name>")
        w = sys.argv[2]
        coords = [int(v) for v in sys.argv[3:9]]
        extract(w, *coords, sys.argv[9])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
