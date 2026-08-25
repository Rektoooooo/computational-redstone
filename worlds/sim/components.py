"""
Per-component evaluation against a solved power field.

Each function answers "given this field, what should this component be outputting?"
At steady state, delay is irrelevant - a settled repeater outputs whatever its input
was, because the input stopped changing. Delay only matters once time is introduced.

Two rules here are easy to get wrong and were checked against the wiki rather than
assumed:

  * In JAVA, a weakly powered block DOES turn off a torch attached to it. Weak vs
    strong only decides whether a block can power new dust. ("Torches ignore weak
    power" is Bedrock behaviour and does not apply here.)
  * A repeater can be locked ONLY by a powered repeater or comparator facing into its
    side. No lever, torch, dust or powered block will do it.
  * `facing` on a repeater/comparator points at its INPUT. The output leaves the
    OPPOSITE side. This is the single most consequential convention in the file.
"""
from .grid import (COMPARATOR, DOWN, DUST, LEFT, LEVER, OPPOSITE, REDSTONE_BLOCK,
                   REPEATER, RIGHT, TORCHES, UP, is_button, is_conductive, neighbour,
                   prop, step, truthy, as_int)
from .power import torch_attachment


def _diode_output(grid, field, states, pos, cell):
    """Level a repeater/comparator at `pos` is emitting, per current states."""
    out = states.get(pos)
    if cell.id == REPEATER:
        powered = out if out is not None else truthy(prop(cell, "powered"))
        return 15 if powered else 0
    level = out if out is not None else (15 if truthy(prop(cell, "powered")) else 0)
    return as_int(level, 0)


def source_signal(grid, states, n, toward):
    """
    Signal a point source at `n` emits toward the neighbouring position `toward`.

    Covers the sources that are not dust, not a diode and not a powered block:
    torches, levers, buttons and pressure plates. Returns None when `n` is none of
    those, so callers can fall through to their own handling.

    These were missing from the diode input path entirely, which made every repeater
    fed directly by a torch read 0. A torch behind a repeater is one of the most
    common patterns there is - 1799 diodes in the library sit against one - and it
    left whole lamp screens stuck on.
    """
    cell = grid.get(n)
    bid = cell.id

    if bid in TORCHES:
        lit = states.get(n)
        if lit is None:
            lit = truthy(prop(cell, "lit", "true"))
        # A torch powers all six neighbours EXCEPT the block it is mounted on.
        return 15 if lit and torch_attachment(grid, n, cell) != toward else 0

    if bid == LEVER or is_button(bid) or "pressure_plate" in bid:
        return 15 if truthy(prop(cell, "powered")) else 0

    return None


def input_from(grid, field, states, pos, direction, sides_only=False):
    """
    Power arriving at `pos` from its neighbour in `direction`.

    sides_only applies the comparator's stricter side rule: a powered block on the
    side does not feed it, only dust, a redstone block, or a diode pointing in.
    """
    n = neighbour(pos, direction)
    cell = grid.get(n)
    bid = cell.id

    if bid == DUST:
        return field.dust.get(n, 0)
    if bid == REDSTONE_BLOCK:
        return 15
    if bid in (REPEATER, COMPARATOR):
        # only counts if it is actually pointing at us
        if neighbour(n, OPPOSITE[prop(cell, "facing", "north")]) == pos:
            return _diode_output(grid, field, states, n, cell)
        return 0
    if sides_only:
        return 0
    # Torch / lever / button / plate feeding the rear directly. Deliberately below the
    # sides_only gate: a comparator's SIDE accepts only dust, a redstone block or a
    # diode pointing in, so a torch beside one must keep reading 0.
    sig = source_signal(grid, states, n, pos)
    if sig is not None:
        return sig
    # A container behind a comparator feeds its rear with the container's fill level.
    # Only the rear reads containers, never the sides.
    if bid in grid.CONTAINERS:
        return grid.containers.get(n, 0)
    if is_conductive(bid):
        return field.block_power(n)
    return 0


# -- torch ------------------------------------------------------------------

def eval_torch(grid, field, states, pos, cell):
    """Lit unless its attachment block carries any power, weak or strong."""
    attached = torch_attachment(grid, pos, cell)
    if not is_conductive(grid.get(attached).id):
        return True                      # nothing that can hold power -> always lit
    return field.block_power(attached) == 0


# -- repeater ---------------------------------------------------------------

def repeater_locked(grid, field, states, pos, cell):
    """Locked only by a powered repeater or comparator facing into either side."""
    facing = prop(cell, "facing", "north")
    for side in (LEFT[facing], RIGHT[facing]):
        n = neighbour(pos, side)
        c = grid.get(n)
        if c.id not in (REPEATER, COMPARATOR):
            continue
        if neighbour(n, OPPOSITE[prop(c, "facing", "north")]) != pos:
            continue
        if _diode_output(grid, field, states, n, c) > 0:
            return True
    return False


def eval_repeater(grid, field, states, pos, cell):
    """
    Output at steady state. Returns bool.

    IMPORTANT: for repeaters and comparators, `facing` points at the INPUT, not the
    output. Minecraft's DiodeBlock reads its signal from pos.relative(facing), and the
    output goes to the OPPOSITE side. Getting this backwards silently reverses every
    diode in a build - it cost 21 points of oracle agreement before it was caught.
    """
    if repeater_locked(grid, field, states, pos, cell):
        prev = states.get(pos)
        return prev if prev is not None else truthy(prop(cell, "powered"))
    facing = prop(cell, "facing", "north")
    return input_from(grid, field, states, pos, facing) > 0


# -- comparator -------------------------------------------------------------

def eval_comparator(grid, field, states, pos, cell):
    """
    Output level 0-15 at steady state.

        compare  : out = rear if (left <= rear and right <= rear) else 0
        subtract : out = max(0, rear - max(left, right))
    """
    facing = prop(cell, "facing", "north")
    rear = input_from(grid, field, states, pos, facing)
    left = input_from(grid, field, states, pos, LEFT[facing], sides_only=True)
    right = input_from(grid, field, states, pos, RIGHT[facing], sides_only=True)
    side = max(left, right)

    if prop(cell, "mode", "compare") == "subtract":
        return max(0, rear - side)
    return rear if side <= rear else 0


# -- lamp -------------------------------------------------------------------

def dust_activates(grid, dust_pos, target_pos):
    """
    Does this dust actually drive the mechanism next to it?

    Dust only activates a component it POINTS at, or one directly beneath it. Dust
    merely running past a lamp leaves it dark - treating any adjacent dust as an
    activator lights lamps all along a bus that are dark in the game.
    """
    from .grid import DIRS
    if step(dust_pos, DOWN) == target_pos:
        return True                       # dust sitting on top of it
    cell = grid.get(dust_pos)
    dirs = {d: prop(cell, d, "none") for d in DIRS}
    if all(v == "none" for v in dirs.values()):
        return True                       # a dot powers everything around it
    for d, v in dirs.items():
        if v != "none" and neighbour(dust_pos, d) == target_pos:
            return True
    return False


def eval_lamp(grid, field, states, pos, cell):
    """
    Lit if any neighbour powers it: dust pointing in, a point source, a diode, or a
    powered block.

    A weakly powered block DOES light an adjacent lamp - weak vs strong only decides
    whether a block can start a new dust run, so `block_power` is the right test here.
    """
    from .grid import DIRS
    for delta in list(DIRS.values()) + [UP, DOWN]:
        n = step(pos, delta)
        c = grid.get(n)
        if c.id == DUST and field.dust.get(n, 0) > 0 and dust_activates(grid, n, pos):
            return True
        if c.id == REDSTONE_BLOCK:
            return True
        # torch, lever, button, pressure plate - a lever mounted straight onto a lamp
        # is common and used to read as nothing at all
        if source_signal(grid, states, n, pos):
            return True
        if c.id in (REPEATER, COMPARATOR):
            if neighbour(n, OPPOSITE[prop(c, "facing", "north")]) == pos:
                if _diode_output(grid, field, states, n, c) > 0:
                    return True
        if is_conductive(c.id) and field.block_power(n) > 0:
            return True
    return False


# -- driver -----------------------------------------------------------------

def evaluate_all(grid, field, states):
    """One evaluation pass: what every component should be, given this field."""
    nxt = {}
    for pos, cell in grid.cells.items():
        bid = cell.id
        if bid in TORCHES:
            nxt[pos] = eval_torch(grid, field, states, pos, cell)
        elif bid == REPEATER:
            nxt[pos] = eval_repeater(grid, field, states, pos, cell)
        elif bid == COMPARATOR:
            nxt[pos] = eval_comparator(grid, field, states, pos, cell)
    return nxt


def saved_states(grid):
    """Component outputs as recorded in the schematic - the oracle's starting point."""
    s = {}
    for pos, cell in grid.cells.items():
        if cell.id in TORCHES:
            s[pos] = truthy(prop(cell, "lit", "true"))
        elif cell.id == REPEATER:
            s[pos] = truthy(prop(cell, "powered"))
        elif cell.id == COMPARATOR:
            # the schematic records only powered/not, so recover the level by
            # evaluating it later; seed with 15 or 0 as a starting guess
            s[pos] = 15 if truthy(prop(cell, "powered")) else 0
    return s
