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


def repeater_input_on(grid, field, states, pos, cell):
    """Whether a repeater's rear currently carries a signal, ignoring any lock."""
    return input_from(grid, field, states, pos, prop(cell, "facing", "north")) > 0


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

def comparator_rear(grid, field, states, pos, facing):
    """
    A comparator's rear input, which is not the same as a repeater's.

    On top of the ordinary rear read, a comparator measures containers, and it will
    read one THROUGH a solid block: if the block immediately behind is a full
    conductor and the reading so far is below 15, it looks one step further for a
    container and takes that instead. Reading a barrel through a block is a standard
    way to keep a signal-strength source out of the wiring, so missing it made those
    comparators read whatever the block happened to carry.

    Item frames also count in the game. They are entities, not blocks, so they are not
    in the extraction and are out of scope here.
    """
    base = input_from(grid, field, states, pos, facing)
    back = neighbour(pos, facing)
    if grid.is_container(back):
        return grid.containers.get(back, 0)      # a container behind it wins outright
    if base < 15 and is_conductive(grid.get(back).id):
        beyond = neighbour(back, facing)
        if grid.is_container(beyond):
            return grid.containers.get(beyond, 0)
    return base


def eval_comparator(grid, field, states, pos, cell):
    """
    Output level 0-15 at steady state.

        compare  : out = rear if (left <= rear and right <= rear) else 0
        subtract : out = max(0, rear - max(left, right))
    """
    facing = prop(cell, "facing", "north")
    rear = comparator_rear(grid, field, states, pos, facing)
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

STATEFUL = (REPEATER, COMPARATOR) + TORCHES


def eval_one(grid, field, states, pos, cell=None):
    """
    What a single stateful component should be outputting. None if it has no state.

    Bool for a torch or repeater, 0-15 for a comparator.
    """
    cell = cell or grid.get(pos)
    if cell.id in TORCHES:
        return eval_torch(grid, field, states, pos, cell)
    if cell.id == REPEATER:
        return eval_repeater(grid, field, states, pos, cell)
    if cell.id == COMPARATOR:
        return eval_comparator(grid, field, states, pos, cell)
    return None


def component_delay(cell):
    """
    How long this component waits before its output changes, in GAME ticks.

    One redstone tick is two game ticks, so a repeater set to "1" is 2 here. A
    comparator is always 2, and so is a torch.
    """
    if cell.id == REPEATER:
        return max(1, as_int(prop(cell, "delay", "1"), 1)) * 2
    return 2


def component_priority(grid, pos, cell, powered):
    """
    Which of several components due on the same tick goes first. Lower runs earlier.

    The interesting case is the first one: if the block this diode outputs INTO is
    another diode that is not pointing back at us - one facing across our output
    rather than into it - we go first. That is the rule that makes two repeaters
    feeding each other's sides resolve deterministically instead of by update order.
    """
    from .ticks import EXTREMELY_HIGH, VERY_HIGH, HIGH, NORMAL

    if cell.id in TORCHES:
        return NORMAL

    out_dir = OPPOSITE[prop(cell, "facing", "north")]
    front = grid.get(neighbour(pos, out_dir))
    if front.id in (REPEATER, COMPARATOR) and prop(front, "facing", "north") != out_dir:
        return EXTREMELY_HIGH
    return VERY_HIGH if powered else HIGH


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
