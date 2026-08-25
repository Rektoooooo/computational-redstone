"""
The steady-state power solver.

Three passes, in this order, exploiting a structural fact about redstone:

    Strong power comes only from components. Weak power comes only from dust.
    A weakly powered block cannot power dust.

So strong power never originates from dust, which means dust power and block power are
NOT mutually recursive. That is what lets this be a direct solve instead of an
iterative relaxation over the whole grid.

    1. strong block power  - from component outputs only
    2. dust field          - Dijkstra from sources and strongly powered blocks,
                             decaying 1 per dust block, max wins
    3. weak block power    - from dust; consumed only by mechanisms and by
                             repeaters/comparators facing away

Component OUTPUTS are an input to this solver, not computed by it. They are evaluated
separately (components.py) against the field this produces. That separation is what
makes a bistable circuit expressible: a latch's state is history, not a function of
the current field alone.
"""
import heapq

from .grid import (DIRS, DOWN, UP, DUST, LEVER, REDSTONE_BLOCK, TORCHES,
                   REPEATER, COMPARATOR, OPPOSITE, is_conductive, neighbour, prop,
                   step, truthy, as_int)


class Field:
    """Solved power levels. All values 0-15."""

    def __init__(self):
        self.strong = {}   # conductive block -> strong power level
        self.weak = {}     # conductive block -> weak power level
        self.dust = {}     # dust position -> power level

    def block_power(self, pos):
        """Highest power on a block, regardless of strength class."""
        return max(self.strong.get(pos, 0), self.weak.get(pos, 0))

    def is_strong(self, pos):
        return self.strong.get(pos, 0) > 0


def dust_links(grid, pos, cell):
    """
    Dust positions this dust can push power to.

    Power flow between dust is decided by what is physically in the way, NOT by the
    saved north/east/south/west shape. Those properties describe how the wire is drawn
    and which mechanisms it feeds; the game works out neighbour-to-neighbour power
    separately, from block occupancy. Reading the shape instead used to add a step
    DOWN for any side that was not `none`, and those shortcuts carried power across
    gaps that do not conduct - 4:1 over-powered, concentrated around the glass towers.

    Stated from the READER's side, which is how the game evaluates it. In each case
    the deciding block is the one horizontally beside the reader, in between the two:

        same level        always
        source one UP     that block must BE a conductor - the signal climbs it -
                          and nothing solid may cap the reader
        source one DOWN   that block must NOT be a conductor

    The two diagonal cases demand the OPPOSITE thing of the block between them, which
    is why the relation is asymmetric: a diagonal step that is legal one way need not
    be legal back. This function pushes rather than reads, so each rule appears
    inverted below.
    """
    out = []
    capped = is_conductive(grid.get(step(pos, UP)).id)
    supported = is_conductive(grid.get(step(pos, DOWN)).id)

    for d in DIRS:
        n = neighbour(pos, d)
        between_conductive = is_conductive(grid.get(n).id)

        if grid.get(n).id == DUST:
            out.append(n)

        # A dust one level up steps DOWN onto us: allowed unless we are capped.
        up = step(n, UP)
        if grid.get(up).id == DUST and not capped:
            out.append(up)

        # A dust one level down steps UP onto us: it needs our support to be a
        # conductor to climb, and the block between must not cap it.
        down = step(n, DOWN)
        if grid.get(down).id == DUST and supported and not between_conductive:
            out.append(down)

    return out


def component_sources(grid, states):
    """
    What each powered component emits.

    Returns (strong_on_blocks, dust_seeds) where both map position -> level.
    strong_on_blocks is the strong power a component puts onto a conductive block;
    dust_seeds is the level it delivers directly to an adjacent dust.
    """
    strong, seeds = {}, {}

    def put(table, pos, level):
        if level > table.get(pos, 0):
            table[pos] = level

    for pos, cell in grid.cells.items():
        bid = cell.id
        out = states.get(pos)

        if bid == REDSTONE_BLOCK:
            # A redstone block strongly powers every block touching it.
            for delta in list(DIRS.values()) + [UP, DOWN]:
                n = step(pos, delta)
                if is_conductive(grid.get(n).id):
                    put(strong, n, 15)
                elif grid.get(n).id == DUST:
                    put(seeds, n, 15)
            continue

        if bid == LEVER:
            if not truthy(prop(cell, "powered")):
                continue
            # A lever strongly powers ONLY the block it is mounted on, but delivers 15
            # to every adjacent dust. (LeverBlock.getDirectSignal is non-zero only
            # toward getConnectedDirection; getSignal is 15 in all six directions.)
            # It used to strongly power every adjacent block, which let a lever start
            # a dust run from a block it merely touched.
            support = lever_attachment(grid, pos, cell)
            if is_conductive(grid.get(support).id):
                put(strong, support, 15)
            for delta in list(DIRS.values()) + [UP, DOWN]:
                n = step(pos, delta)
                if grid.get(n).id == DUST:
                    put(seeds, n, 15)
            continue

        if bid in TORCHES:
            if not (out if out is not None else truthy(prop(cell, "lit", "true"))):
                continue
            attached = torch_attachment(grid, pos, cell)
            # strongly powers the block above; weakly powers other neighbours
            above = step(pos, UP)
            if is_conductive(grid.get(above).id):
                put(strong, above, 15)
            for delta in list(DIRS.values()) + [UP, DOWN]:
                n = step(pos, delta)
                if n == attached:
                    continue
                if grid.get(n).id == DUST:
                    put(seeds, n, 15)
            continue

        if bid == REPEATER:
            # No entry in states means "use the state the schematic recorded" - the
            # same fallback the torch branch uses. Treating a missing entry as off
            # silently disables every diode when solving a bare grid.
            powered = out if out is not None else truthy(prop(cell, "powered"))
            if not powered:
                continue
            front = neighbour(pos, OPPOSITE[prop(cell, "facing", "north")])
            fid = grid.get(front).id
            if is_conductive(fid):
                put(strong, front, 15)
            elif fid == DUST:
                put(seeds, front, 15)
            continue

        if bid == COMPARATOR:
            if out is None:
                level = 15 if truthy(prop(cell, "powered")) else 0
            else:
                level = as_int(out, 0)
            if level <= 0:
                continue
            front = neighbour(pos, OPPOSITE[prop(cell, "facing", "north")])
            fid = grid.get(front).id
            if is_conductive(fid):
                put(strong, front, level)
            elif fid == DUST:
                put(seeds, front, level)
            continue

    return strong, seeds


def lever_attachment(grid, pos, cell):
    """The block a lever is mounted on - the only one it strongly powers."""
    face = prop(cell, "face", "wall")
    if face == "floor":
        return step(pos, DOWN)
    if face == "ceiling":
        return step(pos, UP)
    return neighbour(pos, OPPOSITE[prop(cell, "facing", "north")])


def torch_attachment(grid, pos, cell):
    """The block a torch is mounted on - the one block it never powers."""
    if cell.id == "redstone_wall_torch":
        facing = prop(cell, "facing", "north")
        # a wall torch's 'facing' is the direction it points AWAY from its support
        from .grid import OPPOSITE
        return neighbour(pos, OPPOSITE[facing])
    return step(pos, DOWN)


def solve(grid, states):
    """
    Solve the power field given current component output states.

    states: pos -> output. Bool for torch/repeater (lit/powered), int 0-15 for
    comparator. Missing entries fall back to the block's saved state.
    """
    f = Field()
    strong, seeds = component_sources(grid, states)
    f.strong.update(strong)

    # Pass 2: dust field. Seed from direct component output and from strongly powered
    # blocks, then propagate along saved dust connections, losing 1 per dust block.
    heap = []
    for pos, level in seeds.items():
        if level > f.dust.get(pos, 0):
            f.dust[pos] = level
            heapq.heappush(heap, (-level, pos))

    for bpos, level in strong.items():
        for delta in list(DIRS.values()) + [UP, DOWN]:
            n = step(bpos, delta)
            if grid.get(n).id != DUST:
                continue
            if level > f.dust.get(n, 0):
                f.dust[n] = level
                heapq.heappush(heap, (-level, n))

    while heap:
        neg, pos = heapq.heappop(heap)
        level = -neg
        if level < f.dust.get(pos, 0):
            continue
        if level <= 0:
            continue
        for n in dust_links(grid, pos, grid.get(pos)):
            nxt = level - 1
            if nxt > f.dust.get(n, 0):
                f.dust[n] = nxt
                heapq.heappush(heap, (-nxt, n))

    # Pass 3: weak block power from dust. Dust powers the block beneath it and any
    # block it points into. A dot (no connections) powers only the block beneath.
    for pos, level in f.dust.items():
        if level <= 0:
            continue
        cell = grid.get(pos)
        below = step(pos, DOWN)
        if is_conductive(grid.get(below).id) and level > f.weak.get(below, 0):
            f.weak[below] = level
        for d in DIRS:
            if prop(cell, d, "none") == "none":
                continue
            n = neighbour(pos, d)
            if is_conductive(grid.get(n).id) and level > f.weak.get(n, 0):
                f.weak[n] = level

    return f
