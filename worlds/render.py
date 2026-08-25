#!/usr/bin/env python3
"""
Render a .litematic as layer-by-layer SVG diagrams.

    python render.py <file.litematic> [out.svg]
    python render.py --dir <primitives/world> [--limit N]

Draws one top-down grid per y-layer, laid out left-to-right, bottom layer first.
Redstone components are colour-coded and directional ones carry a facing arrow, so a
build can be read without opening Minecraft.

Useful for two things: identifying the 152 unlabelled builds, and producing figures.
"""
import os
import sys
import glob
from litemapy import Schematic

CELL = 14
GAP = 18
COLS = 6

# colour, short glyph
STYLE = {
    "redstone_wire":        ("#c1121f", ""),
    "repeater":             ("#dcdcdc", "R"),
    "comparator":           ("#f4a261", "C"),
    "redstone_torch":       ("#e63946", "T"),
    "redstone_wall_torch":  ("#e63946", "t"),
    "redstone_block":       ("#8d0801", "B"),
    "redstone_lamp":        ("#ffd166", "L"),
    "lever":                ("#8ecae6", "v"),
    "target":               ("#e9c46a", "x"),
    "barrel":               ("#a68a64", "b"),
    "note_block":           ("#b5838d", "n"),
    "observer":             ("#6d6875", "o"),
    "sticky_piston":        ("#90a955", "P"),
    "piston":               ("#a3b18a", "P"),
    "piston_head":          ("#a3b18a", "-"),
}
ARROW = {"north": "↑", "south": "↓", "east": "→", "west": "←"}


def style_for(bid, props):
    b = bid.replace("minecraft:", "")
    if b in STYLE:
        return STYLE[b]
    if b.endswith("_trapdoor"):
        return ("#ffe8a3", "d")
    if "glass" in b:
        return ("#cfe8ef", "")
    if b == "air":
        return (None, "")
    return ("#2b3038", "")            # plain solid: dimmed so redstone reads


def render(path, out=None):
    schem = Schematic.load(path)
    reg = list(schem.regions.values())[0]
    W, H, L = reg.width, reg.height, reg.length

    def interesting(y):
        """A layer is worth drawing if it holds redstone, not just floor blocks."""
        for x in range(W):
            for z in range(L):
                b = reg[x, y, z].id.replace("minecraft:", "")
                if b in STYLE or b.endswith("_trapdoor"):
                    return True
        return False

    layers = [y for y in range(H) if interesting(y)]
    if not layers:
        return None

    # A 100k-component build renders to a ~28MB SVG that no one can open. Cap it.
    est = W * L * len(layers)
    if est > 400_000:
        return None

    cols = min(COLS, len(layers))
    rows = (len(layers) + cols - 1) // cols
    lw, lh = W * CELL, L * CELL
    sw = cols * (lw + GAP) + GAP
    sh = rows * (lh + GAP + 16) + GAP + 44

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{sw}" height="{sh}" '
         f'viewBox="0 0 {sw} {sh}" font-family="ui-monospace,monospace">',
         f'<rect width="{sw}" height="{sh}" fill="#14161a"/>',
         f'<text x="{GAP}" y="20" fill="#e8e8e8" font-size="13">'
         f'{os.path.basename(path).replace(".litematic","")} — {W}×{H}×{L}, '
         f'{len(layers)} populated layers (y ascending, left to right)</text>']

    for i, y in enumerate(layers):
        ox = GAP + (i % cols) * (lw + GAP)
        oy = 44 + (i // cols) * (lh + GAP + 16)
        p.append(f'<text x="{ox}" y="{oy - 4}" fill="#8b98a5" font-size="10">y={y}</text>')
        p.append(f'<rect x="{ox}" y="{oy}" width="{lw}" height="{lh}" fill="#1c1f24"/>')
        for x in range(W):
            for z in range(L):
                b = reg[x, y, z]
                colour, glyph = style_for(b.id, None)
                if colour is None:
                    continue
                cx, cy = ox + x * CELL, oy + z * CELL
                p.append(f'<rect x="{cx}" y="{cy}" width="{CELL-1}" height="{CELL-1}" '
                         f'fill="{colour}" opacity="0.92"/>')
                mark = glyph
                try:
                    f = b["facing"]
                    if f in ARROW and glyph in ("R", "C", "t"):
                        mark = ARROW[f]
                except Exception:
                    pass
                if mark:
                    p.append(f'<text x="{cx + CELL/2 - 0.5}" y="{cy + CELL - 3.5}" '
                             f'fill="#14161a" font-size="9" text-anchor="middle">{mark}</text>')
    # legend
    lx = GAP
    p.append(f'<text x="{lx}" y="{sh - 8}" fill="#8b98a5" font-size="9">'
             f'R repeater · C comparator · T/t torch · L lamp · v lever · '
             f'x target · arrows = facing · red = dust · pale blue = glass</text>')
    p.append("</svg>")

    out = out or path.replace(".litematic", ".svg")
    open(out, "w").write("\n".join(p))
    return out


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == "--dir":
        d = sys.argv[2]
        lim = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 9999
        files = sorted(glob.glob(os.path.join(d, "*.litematic")))[:lim]
        n = 0
        for f in files:
            try:
                if render(f):
                    n += 1
                else:
                    print(f"  skip {os.path.basename(f)}: too large to render usefully")
            except Exception as e:
                print(f"  skip {os.path.basename(f)}: {str(e)[:50]}")
        print(f"rendered {n} diagrams in {d}")
    else:
        out = render(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
        print(f"-> {out}")


if __name__ == "__main__":
    main()
