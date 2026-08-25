"""
Public API for the simulator.

    sim = Sim.from_file("primitives/alus/build-17.litematic")
    sim.set_lever(pos, True)
    sim.settle()
    sim.lamp_states()

`settle` alternates solving the power field and re-evaluating components until nothing
changes. Because a bistable circuit (an SR latch) has more than one valid resting
state, settle starts from whatever state the components are already in - seeded from
the schematic by default. That makes the resting state a property of history, as it is
in the game, rather than something invented from scratch.
"""
from .grid import Grid, DUST, LAMP, LEVER, TORCHES, REPEATER, COMPARATOR, prop, truthy
from .power import solve
from . import components as C


class Sim:
    def __init__(self, grid, states=None):
        self.grid = grid
        self.states = dict(states) if states else C.saved_states(grid)
        self.field = None
        self.converged = False
        self.iterations = 0

    @classmethod
    def from_file(cls, path):
        return cls(Grid.from_file(path))

    # -- inputs --------------------------------------------------------------

    def levers(self):
        return self.grid.of_type(LEVER)

    def set_lever(self, pos, on):
        cell = self.grid.get(pos)
        if cell.id != LEVER:
            raise ValueError(f"no lever at {pos} (found {cell.id})")
        props = dict(cell.props)
        props["powered"] = "true" if on else "false"
        self.grid.cells[pos] = cell._replace(props=props)

    def set_levers(self, mapping):
        for pos, on in mapping.items():
            self.set_lever(pos, on)

    def set_port(self, positions, value, lsb_first=True):
        """Drive an ordered list of lever positions as a binary number."""
        order = list(positions) if lsb_first else list(reversed(positions))
        for i, pos in enumerate(order):
            self.set_lever(tuple(pos), bool((value >> i) & 1))

    # -- solving -------------------------------------------------------------

    def step(self):
        """One solve+evaluate pass. Returns True if anything changed."""
        self.field = solve(self.grid, self.states)
        nxt = C.evaluate_all(self.grid, self.field, self.states)
        changed = nxt != self.states
        self.states = nxt
        return changed

    def settle(self, max_iterations=200):
        """
        Iterate to a fixed point.

        Returns True if it converged. A False return means the circuit is oscillating
        (a clock) or the model is unstable - both worth knowing, so it is reported
        rather than hidden.
        """
        for i in range(max_iterations):
            if not self.step():
                self.converged = True
                self.iterations = i + 1
                return True
        # one final solve so the field matches the last state
        self.field = solve(self.grid, self.states)
        self.converged = False
        self.iterations = max_iterations
        return False

    # -- outputs -------------------------------------------------------------

    def dust_power(self, pos):
        return self.field.dust.get(pos, 0) if self.field else 0

    def lamp_states(self):
        if self.field is None:
            self.settle()
        return {p: C.eval_lamp(self.grid, self.field, self.states, p, self.grid.get(p))
                for p in self.grid.of_type(LAMP)}

    def read_port(self, positions, lsb_first=True):
        """Read an ordered list of lamp positions back as a binary number."""
        lamps = self.lamp_states()
        order = list(positions) if lsb_first else list(reversed(positions))
        v = 0
        for i, pos in enumerate(order):
            if lamps.get(tuple(pos)):
                v |= 1 << i
        return v

    def __repr__(self):
        return (f"<Sim {self.grid!r} settled={self.converged} "
                f"iters={self.iterations}>")
