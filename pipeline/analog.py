#!/usr/bin/env python3
"""
Signal-strength arithmetic in redstone: the primitives, and the checks that keep them
honest.

A redstone comparator in subtract mode computes `max(0, rear - side)` on SIGNAL
STRENGTH, not on bits. That makes small decimal arithmetic almost free - the whole of
`x + y` for two digits is eight comparators - but it comes with one hazard that binary
logic does not have:

  **an analog value loses one per dust block, so where a wire goes changes what it
  says.** An extra cell of dust is not a longer wire, it is a different number.

Two facts make it workable anyway, and both are verified in `selftest()` below:

  * a comparator relays a value with NO loss - its output cell carries exactly the
    level it read - so a chain of comparator/dust/comparator/dust carries a value any
    distance. Comparators, not repeaters: a repeater would flatten it to 15.
  * a comparator only ever reads its SIDE from dust, a redstone block, or a diode
    pointing into it. A powered solid block on the side contributes nothing, which is
    what makes it safe to run these past ordinary structure.

The second fact is also the trap: a stray dust cell or redstone block beside a
comparator is invisible in a schematic and silently changes the answer. `interference()`
looks for exactly that, because the simulator will happily reproduce the wrong number
without complaint.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "worlds"))

from sim.grid import (Grid, Cell, DIRS, LEFT, RIGHT, OPPOSITE, UP, step,
                      neighbour)

DUST_PROPS = {"north": "side", "south": "side", "east": "side", "west": "side"}

# Anything that feeds a comparator's side input. A solid block does not, however
# strongly it is powered - which is why structure can be run right past these.
SIDE_FEEDERS = ("redstone_wire", "redstone_block", "repeater", "comparator")

# Blocks a route must not run alongside. Wool and other structure is fine - a solid
# block feeds nothing sideways however hard it is powered.
LIVE = ("redstone_wire", "redstone_block", "repeater", "comparator",
        "redstone_torch", "redstone_wall_torch", "lever")


class Collision(Exception):
    pass


class Build:
    """
    Blocks under construction, as `pos -> (id, props)`.

    Deliberately plain: it holds the same shape the simulator wants and the same shape
    `pipeline/compose.py` can emit, so one layout is checked and built from one source.
    """

    def __init__(self, floor="gray_wool"):
        self.cells = {}
        self.floor_colour = floor
        self.notes = {}          # pos -> what it is meant to be, for error messages
        self.side_nodes = set()  # cells that are SUPPOSED to feed a comparator side
        self.reserved = set()    # clearance around routed lines; routing only

    # -- placement ---------------------------------------------------------

    def put(self, pos, bid, props=None, why=""):
        if pos in self.cells:
            have = self.cells[pos][0]
            raise Collision(f"{pos}: {why or bid} wants a cell already holding "
                            f"{have} ({self.notes.get(pos, '?')})")
        self.cells[pos] = (bid, dict(props or {}))
        if why:
            self.notes[pos] = why
        return pos

    def reserve(self, *positions):
        """Keep the router out of these cells. Explicit placement ignores it."""
        self.reserved.update(positions)

    def release(self, *positions):
        """Give reserved ground back, for the line it was being held for."""
        self.reserved.difference_update(positions)

    def claim(self, pos):
        """Reserve `pos` and the cells around it, so nothing is routed against it."""
        self.reserved.add(pos)
        for d in DIRS.values():
            self.reserved.add(step(pos, d))

    def dust(self, pos, why="dust"):
        return self.put(pos, "redstone_wire", DUST_PROPS, why)

    def comp(self, pos, facing, mode="compare", why=None):
        """`facing` points at the REAR input; the output leaves the opposite side."""
        return self.put(pos, "comparator",
                        {"facing": facing, "mode": mode, "powered": "false"},
                        why or f"comparator {mode}")

    def rep(self, pos, facing, delay=1, why="repeater"):
        return self.put(pos, "repeater", {"facing": facing, "delay": str(delay),
                                          "locked": "false", "powered": "false"}, why)

    def block(self, pos, bid=None, why="structure"):
        return self.put(pos, bid or self.floor_colour, {}, why)

    def torch_block(self, pos, why="redstone block"):
        return self.put(pos, "redstone_block", {}, why)

    def lever(self, pos, why="lever"):
        return self.put(pos, "lever",
                        {"powered": "false", "face": "floor", "facing": "north"}, why)

    def lamp(self, pos, why="lamp"):
        return self.put(pos, "redstone_lamp", {"lit": "false"}, why)

    # -- support -----------------------------------------------------------

    NEEDS_FLOOR = ("redstone_wire", "comparator", "repeater", "redstone_torch")

    def add_floor(self, colour=None):
        """A block under everything that would otherwise fall out of the world."""
        added = 0
        for pos, (bid, props) in list(self.cells.items()):
            needs = bid in self.NEEDS_FLOOR or (bid == "lever" and
                                                props.get("face") == "floor")
            below = (pos[0], pos[1] - 1, pos[2])
            if needs and below not in self.cells:
                self.block(below, colour or self.floor_colour, "floor")
                added += 1
        return added

    # -- checking ----------------------------------------------------------

    def interference(self):
        """
        Every comparator whose SIDE is fed by something the design did not intend.

        This is the failure this whole file exists to prevent. A comparator reads its
        two side cells, and dust, a redstone block or a diode pointing in on either one
        silently changes the arithmetic. Nothing about the schematic looks wrong; the
        number is just different.

        Nodes built by `station()` are the intended side inputs and are skipped; what
        is left is always a mistake.
        """
        out = []
        for pos, (bid, props) in self.cells.items():
            if bid != "comparator":
                continue
            facing = props.get("facing", "north")
            for side in (LEFT[facing], RIGHT[facing]):
                n = neighbour(pos, side)
                other = self.cells.get(n)
                if not other:
                    continue
                oid, oprops = other
                if oid not in SIDE_FEEDERS:
                    continue
                if oid in ("repeater", "comparator"):
                    # only counts if it is actually pointing at us
                    if neighbour(n, OPPOSITE[oprops.get("facing", "north")]) != pos:
                        continue
                if n in self.side_nodes:
                    continue                      # this one is the whole point
                out.append((pos, side, n, oid))
        return out

    def stray_dust(self):
        """
        Dust cells that touch other dust they were never meant to touch.

        Two analog lines running one block apart merge into one, and the answer becomes
        the larger of the two. Reported as pairs so a deliberate junction can be
        filtered out.
        """
        out = []
        dusts = {p for p, (b, _) in self.cells.items() if b == "redstone_wire"}
        for p in sorted(dusts):
            for d in DIRS.values():
                q = step(p, d)
                if q in dusts and q > p:
                    out.append((p, q))
        return out

    # -- output ------------------------------------------------------------

    def grid(self):
        g = Grid()
        for pos, (bid, props) in self.cells.items():
            g.cells[pos] = Cell(bid, dict(props))
        g.containers = {}
        g.w = max(p[0] for p in self.cells) + 2
        g.h = max(p[1] for p in self.cells) + 2
        g.l = max(p[2] for p in self.cells) + 2
        return g

    def extent(self):
        xs = [p[0] for p in self.cells]
        ys = [p[1] for p in self.cells]
        zs = [p[2] for p in self.cells]
        return (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))

    def rest(self):
        """
        Write every component's RESTING state into its block properties.

        A schematic stores each block's state, and Minecraft only re-evaluates a
        component when something pokes it. Paste a build whose stored states are wrong
        and whatever nothing happens to touch stays wrong - it will sit there showing a
        number that was true in some other world.

        The simulator cannot see this, by construction: `settle()` recomputes from
        scratch and always arrives at the right answer whatever it started from. So a
        build can pass every sweep and still be wrong the moment it is pasted, which is
        exactly what happened - `build-04` was extracted with a barrel holding 15, and
        went into the file with all four of its output bits stuck on.

        Only valid for combinational builds. Anything with a latch has more than one
        resting state and the choice belongs to the caller.
        """
        from sim.engine import Sim
        s = Sim(self.grid())
        s.settle()
        for pos, (bid, props) in self.cells.items():
            if bid == "redstone_wire":
                props["power"] = str(s.dust_power(pos))
            elif bid in ("repeater", "comparator"):
                props["powered"] = "true" if s.states.get(pos) else "false"
            elif bid in ("redstone_torch", "redstone_wall_torch"):
                props["lit"] = "true" if s.states.get(pos, True) else "false"
            elif bid == "redstone_lamp":
                props["lit"] = "true" if s.lamp_states().get(pos) else "false"
        return s.converged

    def stale(self):
        """
        Components whose stored state is not the one they will settle into.

        The check that would have caught the pasted build showing 7 with nothing
        switched on. Run it after `rest()`; anything it still reports is a block that
        will sit in the world lying about itself until something happens to touch it.
        """
        from sim.engine import Sim
        s = Sim(self.grid())
        s.settle()
        out = []
        for pos, (bid, props) in self.cells.items():
            if bid == "redstone_wire":
                have, want = props.get("power", "0"), str(s.dust_power(pos))
            elif bid in ("repeater", "comparator"):
                have = props.get("powered", "false")
                want = "true" if s.states.get(pos) else "false"
            elif bid in ("redstone_torch", "redstone_wall_torch"):
                have = props.get("lit", "true")
                want = "true" if s.states.get(pos, True) else "false"
            elif bid == "redstone_lamp":
                have = props.get("lit", "false")
                want = "true" if s.lamp_states().get(pos) else "false"
            else:
                continue
            if have != want:
                out.append((pos, bid, have, want))
        return out

    def save(self, path, name, description, colours=None):
        """
        Write the build out as a `.litematic`, so it can be looked at in the game.

        `colours` maps the start of a cell's note to a wool colour, and it paints the
        FLOOR beneath each cell rather than the cell itself - so every line in the build
        is a different colour seen from above, and a wrong route is visible at a glance
        instead of having to be counted out in F3. That convention came from the user
        and has already paid for itself twice.
        """
        from litemapy import Region, BlockState

        (x0, y0, z0), (x1, y1, z1) = self.extent()
        region = Region(0, 0, 0, x1 - x0 + 1, y1 - y0 + 1, z1 - z0 + 1)
        for pos, (bid, props) in self.cells.items():
            if colours and bid.endswith("_wool"):
                above = self.notes.get((pos[0], pos[1] + 1, pos[2]), "")
                hit = next((c for p, c in colours.items() if above.startswith(p)), None)
                if hit:
                    bid = f"{hit}_wool"
            region[pos[0] - x0, pos[1] - y0, pos[2] - z0] = BlockState(
                f"minecraft:{bid}", **{k: str(v) for k, v in props.items()})
        region.as_schematic(name=name, author="computational-redstone",
                            description=description).save(path)
        # the file is indexed from its own corner, so anything that wants to point at a
        # cell afterwards - sign text, for one - has to be shifted by the same amount
        return (x0, y0, z0)


# -- the primitives ---------------------------------------------------------

def decay_line(b, start, direction, length, colour=None):
    """
    A run of dust. Level falls by one per block, which is the whole point of it here:
    distance IS arithmetic.

    Returns the cells in order, so a caller can inject at a chosen distance and read at
    the far end.
    """
    cells = []
    d = DIRS[direction]
    pos = start
    for _ in range(length):
        b.dust(pos, "decay line")
        cells.append(pos)
        pos = step(pos, d)
    return cells


def relay(b, source, legs, why="relay"):
    """
    Carry an analog value from `source` along `legs`, losing nothing.

    `source` must already be a dust cell holding the value. Each leg is
    `(direction, cells)` and **every leg length must be even**, because the chain
    alternates comparator, dust, comparator, dust: a comparator has to be straight
    through (its input and output are opposite faces), so only the dust cells may turn.

    Returns the final dust cell - the value node, carrying exactly what `source` held.
    """
    pos = source
    i = 0
    for direction, count in legs:
        if count % 2:
            raise ValueError(f"relay leg {direction}x{count} must be an even length")
        d = DIRS[direction]
        for _ in range(count):
            pos = step(pos, d)
            i += 1
            if i % 2:
                # a comparator reads its rear from where we just came
                b.comp(pos, OPPOSITE[direction], "compare", why)
            else:
                b.dust(pos, why)
    return pos


def relay_route(b, source, target, why="relay", margin=30, limit=400000):
    """
    Find a comparator chain from `source` to `target` and lay it, going round whatever
    is in the way.

    The search moves in PAIRS of cells - comparator, then dust - which is exactly the
    constraint the chain is under: a comparator's input and output are opposite faces,
    so it can never turn, and only the dust cells between them may. That also explains
    the parity rule this whole file keeps running into. Each move shifts one coordinate
    by two, so a relay can only ever reach cells an even distance away in BOTH axes.
    An odd target is not a longer route, it is an unreachable one.

    No cell is ever placed next to live redstone, because a comparator with a stray dust
    cell beside it reads a different number and looks perfectly fine doing it. Solid
    structure is not live and may be routed against freely.
    """
    if (target[0] - source[0]) % 2 or (target[2] - source[2]) % 2:
        raise ValueError(f"relay {source} -> {target}: both offsets must be even")

    # keep the search in a box around the two ends - without it a breadth-first walk
    # over an empty grid wanders off and never comes back
    lo = (min(source[0], target[0]) - margin, min(source[2], target[2]) - margin)
    hi = (max(source[0], target[0]) + margin, max(source[2], target[2]) + margin)

    def free(pos, exclude, is_target=False):
        """Empty, unclaimed, and with no live redstone touching it."""
        if pos in b.cells:
            return False
        if is_target:
            return True                    # the caller knows what is around it
        if pos in b.reserved:
            return False
        if not (lo[0] <= pos[0] <= hi[0] and lo[1] <= pos[2] <= hi[1]):
            return False
        for d in DIRS.values():
            n = step(pos, d)
            if n in exclude:
                continue
            cell = b.cells.get(n)
            if cell and cell[0] in LIVE:
                return False
        return True

    from collections import deque
    seen = {source: None}
    q = deque([source])
    steps = 0
    while q and steps < limit:
        cur = q.popleft()
        steps += 1
        if cur == target:
            break
        for name, d in DIRS.items():
            mid = step(cur, d)
            nxt = step(mid, d)
            if nxt in seen:
                continue
            # the comparator cell must be clear of anything that could feed its sides,
            # and the dust cell clear of anything it could join
            if not free(mid, {cur, nxt}):
                continue
            if not free(nxt, {mid}, is_target=(nxt == target)):
                continue
            seen[nxt] = (cur, name)
            q.append(nxt)
    if target not in seen:
        raise ValueError(f"no relay route from {source} to {target} - "
                         f"searched {steps} cells")

    path = []
    cur = target
    while seen[cur] is not None:
        prev, name = seen[cur]
        path.append((prev, name))
        cur = prev
    for prev, name in reversed(path):
        d = DIRS[name]
        mid = step(prev, d)
        b.comp(mid, OPPOSITE[name], "compare", why)
        b.dust(step(mid, d), why)
    return target


def wire_route(b, source, target, why="wire", margin=30, max_run=12):
    """
    Route a plain ON/OFF line from `source` to `target`, going round obstacles.

    The boolean twin of `relay_route`. It moves one cell at a time rather than two,
    because a repeater can be put anywhere on a straight stretch - there is no parity
    to respect, and no level to preserve. Everything else is the same: never adjacent to
    live redstone, never through claimed ground.
    """
    lo = (min(source[0], target[0]) - margin, min(source[2], target[2]) - margin)
    hi = (max(source[0], target[0]) + margin, max(source[2], target[2]) + margin)

    def free(pos, exclude, is_target=False):
        if pos in b.cells:
            return False
        if is_target:
            return True
        if pos in b.reserved:
            return False
        if not (lo[0] <= pos[0] <= hi[0] and lo[1] <= pos[2] <= hi[1]):
            return False
        for d in DIRS.values():
            n = step(pos, d)
            if n in exclude:
                continue
            cell = b.cells.get(n)
            if cell and cell[0] in LIVE:
                return False
        return True

    from collections import deque
    seen = {source: None}
    q = deque([source])
    while q:
        cur = q.popleft()
        if cur == target:
            break
        for name, d in DIRS.items():
            nxt = step(cur, d)
            if nxt in seen or not free(nxt, {cur}, is_target=(nxt == target)):
                continue
            seen[nxt] = (cur, name)
            q.append(nxt)
    if target not in seen:
        raise ValueError(f"no wire route from {source} to {target}")

    path = []
    cur = target
    while seen[cur] is not None:
        prev, name = seen[cur]
        path.append((cur, name))
        cur = prev
    path.reverse()
    run = 0
    for i, (pos, name) in enumerate(path):
        run += 1
        straight = i + 1 < len(path) and path[i + 1][1] == name
        if run >= max_run and straight and pos != target:
            b.rep(pos, OPPOSITE[name], why=why)
            run = 0
        elif pos != target:
            b.dust(pos, why)
    return target


def constant(b, end, direction, level, why=None):
    """
    A dust stub that reads exactly `level` at `end`.

    A redstone block sets the dust touching it to 15 and every further block loses one,
    so the constant is built out of distance: the stub is `15 - level` blocks long with
    the block on the far end. `direction` is the way to walk from `end` towards that
    block.
    """
    why = why or f"constant {level}"
    d = DIRS[direction]
    pos = end
    for _ in range(16 - level):
        b.dust(pos, why)
        pos = step(pos, d)
    b.torch_block(pos, f"{why} source")
    return end


def place(b, path, offset, why, skip=()):
    """
    Copy an extracted `.litematic` into the build at `offset`.

    `skip` names local coordinates to leave out - a container whose reading is going to
    be supplied by wire instead, for one. Everything lands in the same `cells` dict as
    the generated circuitry, so one checker, one simulator and one save cover both.
    """
    src = Grid.from_file(path)
    ox, oy, oz = offset
    n = 0
    for pos, cell in src.cells.items():
        if pos in skip:
            continue
        b.put((pos[0] + ox, pos[1] + oy, pos[2] + oz), cell.id, dict(cell.props), why)
        n += 1
    return n


def hex_wire(b, source, along, side, length, why="hex wire"):
    """
    Carry a signal STRENGTH a long way, fast, and add a constant while you are at it.

    A dust line, a row of repeaters reading it from the side, and a second dust line
    taking their outputs. It works because **a signal of strength X travels exactly X
    blocks**: X lights the first X repeaters, the last lit one is X along, and the
    output line then decays over whatever distance is left.

        out = in + (15 - length)      for in >= 1;  0 for in = 0;  capped at 15

    So a full 15-long run moves a value unchanged, and a SHORT run is a free adder -
    which is how you pay for a climb, since a staircase costs one level per block.

    Two game ticks, whatever the distance. A comparator relay costs two ticks per hop,
    which is why this replaced it. From mattbatwings' "Wiring like a pro"; verified
    against `worlds/primitives/wiring/build-41`.
    """
    d, p = DIRS[along], DIRS[side]
    back = OPPOSITE[side]
    pos = source
    for i in range(length):
        if i:
            b.dust(pos, f"{why} in")
        b.rep(step(pos, p), back, why=f"{why} repeater")
        b.dust(step(step(pos, p), p), f"{why} out")
        pos = step(pos, d)
    return step(step(step(source, p), p), tuple(c * (length - 1) for c in d))


def stair(b, source, steps, direction, why="stair"):
    """
    Carry a value up out of its plane, one level per block.

    Dust reaches diagonally to the block above the one beside it, so a staircase is just
    a step of solid blocks with dust on top. It costs exactly one level per step -
    measured, not assumed - which for an analog value means the climb has to be paid for
    in advance: send `v + steps` and it arrives as `v`.

    That is the whole reason this exists. Two lines in one plane cannot cross, and a
    boolean can leave the plane for free while an analog value cannot. Being able to buy
    the climb turns "impossible" into "two comparators and a stub".
    """
    d = DIRS[direction]
    pos = source
    for _ in range(steps):
        b.block(step(pos, d), why=why)
        pos = step(step(pos, d), UP)
        b.dust(pos, why)
    return pos


GLASS = "light_blue_stained_glass"


def tower(b, source, levels, side, why="tower"):
    """
    A glass tower: straight up, one level per block, in a two-block footprint.

    The blocks have to be GLASS and that is the whole trick. Dust reaches the block
    diagonally above the one beside it, but only if nothing solid is sitting on top of
    the dust itself - and in a vertical tower something always is, namely the next step.
    Glass is not a conductor, so it does not count as a lid and the signal keeps going.

    Where a staircase costs a block of floor for every level, this costs two cells
    total, which is what makes it the standard way up. Fifteen levels is the limit, the
    same as flat dust; chain two with a repeater between for anything taller.
    """
    if levels > 14:
        raise ValueError(f"a tower of {levels} outruns its own signal; chain two")
    a, away = source, True
    for _ in range(levels):
        d = DIRS[side] if away else DIRS[OPPOSITE[side]]
        for cell in (step(a, d), step(a, UP)):
            if cell not in b.cells:
                b.put(cell, GLASS, {}, why)
        a = step(step(a, d), UP)
        b.dust(a, why)
        away = not away
    return a


def climb(b, source, levels, direction, max_run=10, why="climb"):
    """
    Take a BOOLEAN up, one level per block, with a repeater before it dies.

    A staircase costs a level per step just like flat dust, so a long climb needs
    restoring the same way a long run does - the difference is only that there is
    nowhere to put a repeater on a slope, so the climb pauses on a flat pair of blocks
    and starts again.

    For booleans only. An analog value cannot be restored this way; pay for its climb up
    front with a short `hex_wire` instead.
    """
    d = DIRS[direction]
    pos, run = source, 0
    for level in range(levels):
        b.block(step(pos, d), why=why)
        pos = step(step(pos, d), UP)
        b.dust(pos, why)
        run += 1
        if run >= max_run and level < levels - 1:
            b.rep(step(pos, d), OPPOSITE[direction], why=why)
            pos = step(step(pos, d), d)
            b.dust(pos, why)
            run = 0
    return pos


def wire(b, start, legs, max_run=12, why="wire"):
    """
    A plain ON/OFF line: dust, with a repeater before the signal would die.

    For booleans only. It restores to 15 at every repeater, which is exactly what an
    analog value must never have done to it - so the two kinds of line are built by
    different functions on purpose, and mixing them up is a bug you want loud.

    Returns the last cell.
    """
    pos = start
    run = 0
    for direction, count in legs:
        d = DIRS[direction]
        for i in range(count):
            pos = step(pos, d)
            run += 1
            straight = i < count - 1        # never put a repeater on a corner
            if run >= max_run and straight:
                b.rep(pos, OPPOSITE[direction], why=why)
                run = 0
            else:
                b.dust(pos, why)
    return pos


def relay_to(b, source, target, order="zx", why="relay"):
    """
    Relay a value from `source` to `target`, turning at most once.

    Both offsets must be EVEN. The chain alternates comparator, dust, comparator, dust
    and a comparator has to be straight through, so a turn can only happen on a dust
    cell - which lands on an even step. An odd offset is a layout mistake, not something
    to paper over, so it raises rather than quietly costing a level.

    `order` picks which axis is travelled first: "zx" goes along z then x, "xz" the
    other way. Use it to keep a run clear of something in the way.
    """
    dx = target[0] - source[0]
    dz = target[2] - source[2]
    if dx % 2 or dz % 2:
        raise ValueError(f"relay {source} -> {target}: offsets ({dx}, {dz}) must both "
                         f"be even; a comparator chain can only turn on an even step")
    x_leg = ("east" if dx > 0 else "west", abs(dx))
    z_leg = ("south" if dz > 0 else "north", abs(dz))
    legs = [z_leg, x_leg] if order == "zx" else [x_leg, z_leg]
    return relay(b, source, [l for l in legs if l[1]], why)


def station(b, node, from_side, why="side feed"):
    """
    Turn a value arriving in a straight line into a **side** input.

    A comparator's sides are the two cells perpendicular to its facing, and the awkward
    part of laying these out is that the thing feeding a side tends to land exactly
    where the next gadget's rear wants to be. This is the arrangement that does not:

        value ->  relay at node+from_side, pointing back at the value
                  node                      <- the side cell
                  gadget at node-from_side, facing west

    so the feed and the gadget approach the node from OPPOSITE sides, and the gadget's
    own rear and output sit two blocks clear of the feed's side cells.

    `node` is where the value should end up; `from_side` is the direction the value
    arrives from. Returns `node`.
    """
    feed = neighbour(node, from_side)
    b.comp(feed, from_side, "compare", why)      # rear points back the way it came
    b.dust(node, why)
    b.side_nodes.add(node)
    return node


def gadget(b, pos, mode="subtract", rear="dust", facing="west", why="gadget"):
    """
    One arithmetic step: `rear - side` (subtract) or `rear` gated by side (compare).

    `rear="block"` puts a redstone block behind it, giving a constant 15 - which is how
    `15 - v` is built, and `15 - v` is how addition is done at all: dust cannot add, but
    inverting twice around a subtraction can.

        S = 15 - ((15 - x) - y)  =  min(15, x + y)

    Returns the output cell.
    """
    b.comp(pos, facing, mode, why)
    rear_cell = neighbour(pos, facing)
    if rear == "block":
        b.torch_block(rear_cell, f"{why} rear = 15")
    out = neighbour(pos, OPPOSITE[facing])
    b.dust(out, f"{why} out")
    return out


# -- self-test --------------------------------------------------------------

def _settle(b, levers=()):
    from sim.engine import Sim
    g = b.grid()
    s = Sim(g)
    for p in levers:
        s._set_lever(p, True)
    s.settle()
    return s


def selftest():
    """
    Every claim this module makes, checked against the simulator.

    Run after any change: these are cheap, and every one of them is a rule that a
    layout silently depends on.
    """
    ok = True

    def check(name, got, want):
        nonlocal ok
        if got != want:
            ok = False
            print(f"  FAIL  {name}\n          got  {got}\n          want {want}")
        else:
            print(f"  PASS  {name}")

    # a decay line turns "which lever" into a number, and the highest lever wins
    b = Build()
    line = decay_line(b, (0, 1, 0), "east", 15)
    levers = {}
    for v in range(1, 10):
        blk = (15 - v, 1, 1)
        b.block(blk, "purple_wool", f"lever {v}")
        levers[v] = (15 - v, 2, 1)
        b.lever(levers[v], f"lever {v}")
    b.add_floor()
    got = [_settle(b, [levers[v]]).dust_power(line[0]) for v in range(1, 10)]
    check("decay line: lever v reads v", got, list(range(1, 10)))
    check("decay line: nothing on reads 0", _settle(b).dust_power(line[0]), 0)
    check("decay line: 3 and 7 on reads 7 (highest wins)",
          _settle(b, [levers[3], levers[7]]).dust_power(line[0]), 7)
    check("decay line: a tap 5 short reads v+5",
          [_settle(b, [levers[v]]).dust_power(line[5]) for v in range(1, 10)],
          [v + 5 for v in range(1, 10)])

    # a comparator relay carries a value any distance without losing any of it.
    # The line runs east from the readout, so the relay leaves southward.
    def seven_line(b):
        """A decay line reading 7 at its west end, with the lever that sets it."""
        line = decay_line(b, (0, 1, 0), "east", 15)
        b.block((15 - 7, 1, 1), "purple_wool", "lever 7")
        lv = (15 - 7, 2, 1)
        b.lever(lv, "lever 7")
        return line, lv

    for legs, label in (([("south", 6)], "6 south"),
                        ([("south", 4), ("east", 4), ("south", 2)], "round two corners")):
        b = Build()
        line, lv = seven_line(b)
        end = relay(b, line[0], legs)
        b.add_floor()
        check(f"relay {label} keeps the value", _settle(b, [lv]).dust_power(end), 7)

    # station + gadget: 15 - v, with the value arriving as a side input
    def inv_rig(extra=None):
        b = Build()
        line, lv = seven_line(b)
        end = relay(b, line[0], [("south", 2), ("east", 2)])
        station(b, (2, 1, 4), "north")               # fed from where the relay ended
        out = gadget(b, (2, 1, 5), "subtract", rear="block", why="INV")
        if extra:
            extra(b)
        b.add_floor()
        return b, lv, out

    b, lv, out = inv_rig()
    check("INV gadget: 15 - 7", _settle(b, [lv]).dust_power(out), 8)
    check("...and the layout has no unintended side feeds",
          [i for i in b.interference() if i[2] != (2, 1, 4)], [])

    # a comparator ignores a powered solid block on its side, which is what makes it
    # safe to run these lines right past ordinary structure
    def beside(b):
        b.block((2, 1, 6), "purple_wool", "structure beside the comparator")
        b.lever((2, 2, 6), "a lever powering that structure")

    b, lv, out = inv_rig(beside)
    check("a powered solid block on a comparator side feeds it nothing",
          _settle(b, [lv, (2, 2, 6)]).dust_power(out), 8)

    print()
    return ok


if __name__ == "__main__":
    sys.exit(0 if selftest() else 1)
