"""
Load a .litematic into an indexed grid and classify its blocks.

Everything downstream asks two questions about a block: can it carry power (is it
conductive), and is it a redstone component. This module answers both, and caches the
whole region into a dict so the solver is not paying litemapy lookup costs per access.

Block set is small and known: a survey of the extracted library found 48 distinct types
across 195 builds, so classification is by explicit rule rather than guesswork.
"""
import re
from collections import namedtuple

Cell = namedtuple("Cell", "id props")

AIR = Cell("air", {})

# Components that participate in redstone logic
DUST = "redstone_wire"
REPEATER = "repeater"
COMPARATOR = "comparator"
TORCH_FLOOR = "redstone_torch"
TORCH_WALL = "redstone_wall_torch"
TORCHES = (TORCH_FLOOR, TORCH_WALL)
REDSTONE_BLOCK = "redstone_block"
LEVER = "lever"
LAMP = "redstone_lamp"
TARGET = "target"

COMPONENTS = {DUST, REPEATER, COMPARATOR, TORCH_FLOOR, TORCH_WALL,
              REDSTONE_BLOCK, LEVER, LAMP, TARGET}

# Constant-output power sources: these power things with no input of their own
SOURCES = {LEVER, REDSTONE_BLOCK}

# Blocks that are solid and full, so they conduct power and cut vertical dust runs.
# Anything not listed here and not a component is treated as non-conductive.
CONDUCTIVE_EXACT = {
    "sandstone", "dropper", "dispenser", "note_block", "observer",
    "piston", "sticky_piston", "barrel", "target", "redstone_lamp",
    "redstone_block", "stone", "smooth_stone", "iron_block", "quartz_block",
}
CONDUCTIVE_SUFFIX = ("_wool", "_concrete", "_terracotta", "_planks", "_log")

# Explicitly non-conductive even though they are "blocks": dust sits on them and
# signal passes through them, which is what makes glass towers work.
TRANSPARENT_SUBSTR = ("glass", "slab", "stairs", "trapdoor", "sign", "banner",
                      "glowstone", "ice", "fence", "pane", "carpet", "rail",
                      "hopper", "ladder", "torch", "button", "pressure_plate")


# -- containers -------------------------------------------------------------

# How full a container looks to a comparator depends on slot count, so the count has
# to be per block type rather than assumed.
CONTAINER_SLOTS = {"barrel": 27, "chest": 27, "trapped_chest": 27, "hopper": 5,
                   "dropper": 9, "dispenser": 9, "furnace": 3, "brewing_stand": 5,
                   "shulker_box": 27}

# Items that do not stack to 64. Anything unlisted is assumed to.
_STACK_16 = ("ender_pearl", "sign", "honey_bottle", "snowball", "egg", "bucket_of_")
_STACK_1 = ("minecart", "boat", "bucket", "saddle", "bed", "banner", "cake", "sword",
            "pickaxe", "axe", "shovel", "hoe", "helmet", "chestplate", "leggings",
            "boots", "bow", "shield", "potion")


def max_stack(item_id):
    name = str(item_id).replace("minecraft:", "")
    if any(k in name for k in _STACK_1):
        return 1
    if any(k in name for k in _STACK_16):
        return 16
    return 64


def _as_int(value, default=1):
    """
    An NBT number as a plain int, whichever library produced it.

    The two readers here disagree about `str()`: anvil-parser renders a byte as "64",
    nbtlib renders it as "64b". Both are int subclasses though, so int() first and only
    fall back to scraping digits out of the text. Going straight to int(str(...))
    silently skipped every item of an nbtlib-loaded container and read it as empty.
    """
    try:
        return int(value)
    except (TypeError, ValueError):
        pass
    digits = re.sub(r"[^0-9-]", "", str(value))
    try:
        return int(digits)
    except ValueError:
        return default


def container_strength(items, slots):
    """
    The comparator output a container holding these items produces.

        strength = floor(1 + (sum(count / maxstack) / slots) * 14)

    Empty reads 0 and full reads 15. Kept here rather than in `containers.py` so the
    simulator and the recovery script cannot drift apart - both ask the same question.
    """
    if not items:
        return 0
    total = 0.0
    for it in items:
        try:
            count = _as_int(it.get("Count", 1))
            iid = str(it.get("id", "minecraft:stone"))
        except (AttributeError, TypeError):
            continue
        total += count / max_stack(iid)
    if total <= 0:
        return 0
    return min(15, int(1 + (total / slots) * 14))


def is_conductive(bid):
    """True if the block can hold power and cuts a vertical dust run."""
    if bid in ("air", DUST, REPEATER, COMPARATOR, LEVER):
        return False
    if any(s in bid for s in TRANSPARENT_SUBSTR):
        return False
    if bid in CONDUCTIVE_EXACT:
        return True
    return bid.endswith(CONDUCTIVE_SUFFIX) or not is_component(bid)


def is_component(bid):
    return bid in COMPONENTS or "button" in bid or "pressure_plate" in bid


def is_button(bid):
    return "button" in bid


class Grid:
    """A region of blocks addressed by (x, y, z). Out of bounds reads as air."""

    CONTAINERS = {"barrel", "chest", "trapped_chest", "hopper", "dropper",
                  "dispenser", "furnace", "brewing_stand"}

    def __init__(self, region=None):
        self.cells = {}
        # position -> comparator strength for containers. Populated from the manifest,
        # because .litematic extraction dropped block entities and every barrel would
        # otherwise read as empty. Signal-strength barrels are load-bearing here.
        self.containers = {}
        self.w = self.h = self.l = 0
        if region is not None:
            self._load(region)

    def _load(self, region):
        self.w, self.h, self.l = region.width, region.height, region.length
        for x in range(self.w):
            for y in range(self.h):
                for z in range(self.l):
                    bs = region[x, y, z]
                    bid = bs.id.replace("minecraft:", "")
                    if bid == "air":
                        continue
                    props = {}
                    for k in ("facing", "delay", "locked", "powered", "mode", "lit",
                              "power", "north", "south", "east", "west", "face", "half"):
                        try:
                            props[k] = bs[k]
                        except Exception:
                            pass
                    self.cells[(x, y, z)] = Cell(bid, props)

    @classmethod
    def from_file(cls, path):
        """
        Load a schematic, and work out what every container in it reads as.

        Two sources, because there are two kinds of file. A schematic written by hand
        carries its containers as block entities, so the levels can be read straight
        out of it and the file stands alone. The 195 harvested builds do NOT - the
        harvest dropped block entities - so their levels were recovered separately by
        `containers.py` and live in the manifest.

        The manifest is applied second and wins. It was read from the source world,
        which is the authority for an extracted build, and letting it override keeps
        the behaviour of the whole library exactly as it was.
        """
        import json, os
        from litemapy import Schematic
        region = list(Schematic.load(path).regions.values())[0]
        g = cls(region)
        g._load_container_entities(region)

        mp = path.replace(".litematic", ".manifest.json")
        if os.path.exists(mp):
            try:
                data = json.load(open(mp)).get("containers") or {}
                for key, level in data.items():
                    x, y, z = (int(v) for v in key.split(","))
                    g.containers[(x, y, z)] = int(level)
            except Exception:
                pass
        return g

    def _load_container_entities(self, region):
        """Comparator strength for any container carrying its own block entity."""
        try:
            entities = region.tile_entities
        except Exception:
            return
        for te in entities:
            try:
                data = te.to_nbt()
                pos = tuple(int(data[k]) for k in ("x", "y", "z"))
            except Exception:
                continue
            if not self.is_container(pos):
                continue
            items = data.get("Items")
            if items is None:
                continue
            level = container_strength(items, CONTAINER_SLOTS.get(self.get(pos).id, 27))
            if level:
                self.containers[pos] = level

    def is_container(self, pos):
        return self.get(pos).id in self.CONTAINERS

    def get(self, pos):
        return self.cells.get(pos, AIR)

    def positions(self):
        return self.cells.keys()

    def of_type(self, *ids):
        want = set(ids)
        return [p for p, c in self.cells.items() if c.id in want]

    def __contains__(self, pos):
        return pos in self.cells

    def __repr__(self):
        return f"<Grid {self.w}x{self.h}x{self.l}, {len(self.cells)} non-air>"


# -- geometry ---------------------------------------------------------------

# Minecraft compass directions as (dx, dy, dz)
DIRS = {"north": (0, 0, -1), "south": (0, 0, 1),
        "east": (1, 0, 0), "west": (-1, 0, 0)}
OPPOSITE = {"north": "south", "south": "north", "east": "west", "west": "east"}
# Turning left/right when facing a direction, used for comparator side inputs
LEFT = {"north": "west", "west": "south", "south": "east", "east": "north"}
RIGHT = {v: k for k, v in LEFT.items()}
UP = (0, 1, 0)
DOWN = (0, -1, 0)


def step(pos, delta):
    return (pos[0] + delta[0], pos[1] + delta[1], pos[2] + delta[2])


def neighbour(pos, direction):
    return step(pos, DIRS[direction])


def prop(cell, name, default=None):
    return cell.props.get(name, default)


def truthy(value):
    """Litematic stores booleans as the strings 'true'/'false'."""
    return value in (True, "true", "True", 1)


def as_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
