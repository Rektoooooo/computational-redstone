#!/usr/bin/env python3
"""
Render a .litematic as layer-by-layer PNG plates using real Minecraft block textures.

    python render_png.py <file.litematic> [out.png] [--pack DIR] [--scale N]
    python render_png.py --dir <primitives/world> [--pack DIR]

Replaces the SVG renderer for display purposes. Two reasons:

  * **Real assets.** Composites the actual block textures from a resource pack, so a
    repeater looks like a repeater instead of a lettered square.
  * **Speed.** The SVG version emitted ~7 elements per dust cell; a large plate ran to
    tens of thousands of DOM nodes and made a page crawl. A PNG is one image.

Dust is composited the way the game does it: a centre dot plus a half-line per
connection, tinted. Connections that climb to the layer above are tinted amber rather
than red, because that is the one thing a flat top-down slice cannot otherwise show.
"""
import os
import sys
import glob

from PIL import Image, ImageDraw
from litemapy import Schematic

DEFAULT_PACK = os.path.expanduser(
    "~/Downloads/redstone-skills/worlds/.textures/assets/minecraft/textures/block")

T = 16            # native texture size
GAP = 10
COLS = 6
LABEL_H = 14

DUST_SIDE = (196, 24, 28)     # flat run
DUST_UP = (255, 176, 0)       # climbs to the layer above
GROUND = (20, 22, 26)
PANEL = (28, 31, 36)
SOLID = (46, 51, 60)
INK = (228, 231, 236)
MUTED = (139, 148, 163)

# block id -> texture file, and how the texture should be rotated for a given facing
TEX = {
    "repeater": "repeater", "comparator": "comparator",
    "redstone_torch": "redstone_torch", "redstone_wall_torch": "redstone_torch",
    "redstone_lamp": "redstone_lamp", "redstone_block": "redstone_block",
    "lever": "lever_base", "glass": "glass", "target": "target_top",
    "observer": "observer_top", "sticky_piston": "piston_top_sticky",
    "piston": "piston_top", "note_block": "note_block", "barrel": "barrel_top",
}
# facing -> degrees to rotate the texture so it points the right way on the plate
ROT = {"north": 0, "east": 270, "south": 180, "west": 90}


FONT_PATHS = ["/System/Library/Fonts/Menlo.ttc",
              "/System/Library/Fonts/SFNSMono.ttf",
              "/System/Library/Fonts/Supplemental/Andale Mono.ttf"]


def _fonts(scale):
    """A real monospace face if one is available; PIL's bitmap default otherwise."""
    from PIL import ImageFont
    for p in FONT_PATHS:
        if os.path.exists(p):
            try:
                return (ImageFont.truetype(p, int(11 * scale)),
                        ImageFont.truetype(p, int(9 * scale)))
            except Exception:
                continue
    f = ImageFont.load_default()
    return f, f


class Textures:
    def __init__(self, pack):
        self.pack, self.cache = pack, {}

    def get(self, name):
        if name in self.cache:
            return self.cache[name]
        p = os.path.join(self.pack, name + ".png")
        img = None
        if os.path.exists(p):
            img = Image.open(p).convert("RGBA")
            if img.size != (T, T):                 # animated textures are tall strips
                img = img.crop((0, 0, T, T))
        self.cache[name] = img
        return img

    def tinted(self, name, rgb):
        key = (name, rgb)
        if key in self.cache:
            return self.cache[key]
        base = self.get(name)
        if base is None:
            return None
        r, g, b, a = base.split()
        solid = Image.new("RGBA", base.size, rgb + (255,))
        solid.putalpha(a)
        # the dust atlas is greyscale; multiply keeps its shading under the tint
        out = Image.composite(solid, base, a)
        self.cache[key] = out
        return out


def dust_tile(tex, block):
    """Centre dot plus a half-line per connection, matching how the game draws it."""
    tile = Image.new("RGBA", (T, T), (0, 0, 0, 0))
    dot = tex.tinted("redstone_dust_dot", DUST_SIDE)
    line0 = "redstone_dust_line0"      # runs north-south
    line1 = "redstone_dust_line1"      # runs east-west
    halves = {                          # direction -> (texture, crop box)
        "north": (line0, (0, 0, T, T // 2)),
        "south": (line0, (0, T // 2, T, T)),
        "west":  (line1, (0, 0, T // 2, T)),
        "east":  (line1, (T // 2, 0, T, T)),
    }
    for d, (tname, box) in halves.items():
        try:
            v = block[d]
        except Exception:
            v = "none"
        if v == "none":
            continue
        img = tex.tinted(tname, DUST_UP if v == "up" else DUST_SIDE)
        if img is None:
            continue
        part = img.crop(box)
        tile.alpha_composite(part, (box[0], box[1]))
    if dot is not None:
        tile.alpha_composite(dot)
    return tile


def block_tile(tex, block):
    bid = block.id.replace("minecraft:", "")
    if bid == "air":
        return None
    if bid == "redstone_wire":
        return dust_tile(tex, block)

    name = TEX.get(bid)
    if name is None:
        if bid.endswith("_trapdoor"):
            name = "oak_trapdoor"
        elif "glass" in bid:
            name = "glass"
        else:
            return "solid"
    img = tex.get(name)
    if img is None:
        return "solid"
    try:
        f = block["facing"]
        if f in ROT and bid in ("repeater", "comparator", "redstone_wall_torch"):
            img = img.rotate(ROT[f])
    except Exception:
        pass
    return img


def render(path, out=None, pack=DEFAULT_PACK, scale=1):
    reg = list(Schematic.load(path).regions.values())[0]
    W, H, L = reg.width, reg.height, reg.length
    tex = Textures(pack)

    def interesting(y):
        for x in range(W):
            for z in range(L):
                b = reg[x, y, z].id.replace("minecraft:", "")
                if b in TEX or b == "redstone_wire" or b.endswith("_trapdoor"):
                    return True
        return False

    layers = [y for y in range(H) if interesting(y)]
    if not layers:
        return None

    cols = min(COLS, len(layers))
    rows = (len(layers) + cols - 1) // cols
    lw, lh = W * T, L * T
    sw = GAP + cols * (lw + GAP)
    sh = 26 + rows * (lh + GAP + LABEL_H) + GAP

    canvas = Image.new("RGB", (sw, sh), GROUND)
    d = ImageDraw.Draw(canvas)
    placements = []

    for i, y in enumerate(layers):
        ox = GAP + (i % cols) * (lw + GAP)
        oy = 26 + (i // cols) * (lh + GAP + LABEL_H) + LABEL_H
        placements.append((ox, oy, y))
        d.rectangle([ox, oy, ox + lw - 1, oy + lh - 1], fill=PANEL)
        for x in range(W):
            for z in range(L):
                t = block_tile(tex, reg[x, y, z])
                if t is None:
                    continue
                px, py = ox + x * T, oy + z * T
                if t == "solid":
                    d.rectangle([px, py, px + T - 1, py + T - 1], fill=SOLID)
                else:
                    canvas.paste(t, (px, py), t)

    # Upscale the pixel art with NEAREST so blocks stay sharp, then draw the labels on
    # top at real size - text scaled with the image would be unreadable mush.
    if scale != 1:
        canvas = canvas.resize((int(sw * scale), int(sh * scale)), Image.NEAREST)
    d = ImageDraw.Draw(canvas)
    font, small = _fonts(scale)
    d.text((GAP * scale, 6 * scale),
           f"{os.path.basename(path).replace('.litematic','')}  -  "
           f"{W}x{H}x{L}, {len(layers)} populated layers", fill=INK, font=font)
    for ox, oy, y in placements:
        d.text((ox * scale, (oy - LABEL_H + 1) * scale), f"y={y}", fill=MUTED, font=small)

    out = out or path.replace(".litematic", ".png")
    canvas.save(out, optimize=True)
    return out


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    pack = sys.argv[sys.argv.index("--pack") + 1] if "--pack" in sys.argv else DEFAULT_PACK
    scale = int(sys.argv[sys.argv.index("--scale") + 1]) if "--scale" in sys.argv else 2
    if not os.path.isdir(pack):
        sys.exit(f"texture pack not found: {pack}")

    if sys.argv[1] == "--dir":
        n = 0
        for f in sorted(glob.glob(os.path.join(sys.argv[2], "*.litematic"))):
            try:
                if render(f, pack=pack, scale=scale):
                    n += 1
            except Exception as e:
                print(f"  skip {os.path.basename(f)}: {str(e)[:60]}")
        print(f"rendered {n} plates in {sys.argv[2]}")
    else:
        print("->", render(sys.argv[1], pack=pack, scale=scale))


if __name__ == "__main__":
    main()
