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
from .ticks import TickQueue
from . import components as C


class Sim:
    def __init__(self, grid, states=None):
        self.grid = grid
        self.states = dict(states) if states else C.saved_states(grid)
        self.field = None
        self.converged = False
        self.iterations = 0
        self.queue = TickQueue()
        self.time = 0          # game ticks; one redstone tick is two of these
        # Lamp state, tracked only once the tick loop is running. Kept apart from
        # `states` so that `settle()` and the oracle behave exactly as they always have.
        self.lamps = {}

    @classmethod
    def from_file(cls, path):
        return cls(Grid.from_file(path))

    # -- inputs --------------------------------------------------------------

    def levers(self):
        return self.grid.of_type(LEVER)

    def _set_lever(self, pos, on):
        cell = self.grid.get(pos)
        if cell.id != LEVER:
            raise ValueError(f"no lever at {pos} (found {cell.id})")
        props = dict(cell.props)
        props["powered"] = "true" if on else "false"
        self.grid.cells[pos] = cell._replace(props=props)

    def set_lever(self, pos, on):
        """
        Flip a lever. If the simulation is already running, this re-solves and queues
        whatever the change affects straight away - flipping a lever in the game
        updates its neighbours immediately, and only then does anything wait its delay.
        """
        self._set_lever(pos, on)
        if self.field is not None:
            self.prime()

    def set_levers(self, mapping):
        """Flip several at once, settling the consequences only after all of them."""
        for pos, on in mapping.items():
            self._set_lever(pos, on)
        if self.field is not None:
            self.prime()

    def set_port(self, positions, value, lsb_first=True):
        """Drive an ordered list of lever positions as a binary number."""
        order = list(positions) if lsb_first else list(reversed(positions))
        for i, pos in enumerate(order):
            self._set_lever(tuple(pos), bool((value >> i) & 1))
        if self.field is not None:
            self.prime()

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

    # -- time ----------------------------------------------------------------

    def _reschedule(self):
        """Queue every component whose output is now out of date with the field."""
        for pos, cell in self.grid.cells.items():
            if cell.id not in C.STATEFUL:
                continue
            if self.queue.is_pending(pos):
                continue                      # already waiting; do not double-schedule
            target = C.eval_one(self.grid, self.field, self.states, pos, cell)
            if target != self.states.get(pos):
                self.queue.schedule(pos,
                                    self.time + C.component_delay(cell),
                                    C.component_priority(self.grid, pos, cell,
                                                         bool(self.states.get(pos))))

    LAMP_OFF_DELAY = 4      # game ticks; turning ON has no delay at all

    def _update_lamps(self):
        """
        Apply the lamp's own asymmetric timing.

        A lamp lights the instant it is powered, but when its power goes away it waits
        4 game ticks and only then goes dark - re-checking on arrival, so a signal that
        returns inside that window leaves it lit. That is deliberate anti-flicker
        behaviour in the game, and measuring it in-game is the only way it shows up:
        the steady state is identical either way.
        """
        changed = False
        for pos in self.grid.of_type(LAMP):
            target = C.eval_lamp(self.grid, self.field, self.states, pos,
                                 self.grid.get(pos))
            now = self.lamps.get(pos, False)
            if target and not now:
                self.lamps[pos] = True          # on is immediate
                changed = True
            elif not target and now and not self.queue.is_pending(pos):
                self.queue.schedule(pos, self.time + self.LAMP_OFF_DELAY)
        return changed

    def _fire_repeater(self, pos, cell):
        """
        A repeater's scheduled tick, with the pulse-stretch rule.

        The subtle part: when the tick arrives and the repeater is currently OFF, it
        turns ON **unconditionally** - even if the input that scheduled it has already
        gone away. It then schedules its own turn-off one delay later. That is what
        makes a repeater STRETCH a pulse shorter than its own delay, and why a 1-tick
        pulse through a 4-tick repeater comes out 4 ticks wide.

        Re-checking the input here instead, which is the obvious implementation, loses
        short pulses entirely - they schedule a turn-on, the input vanishes, and the
        repeater declines to fire. Every clock and edge detector depends on this.
        """
        if C.repeater_locked(self.grid, self.field, self.states, pos, cell):
            return False
        powered = bool(self.states.get(pos))
        should_on = C.repeater_input_on(self.grid, self.field, self.states, pos, cell)

        if powered and not should_on:
            self.states[pos] = False
            return True
        if not powered:
            self.states[pos] = True
            if not should_on:
                # input already gone: hold the pulse open for one full delay
                self.queue.schedule(pos, self.time + C.component_delay(cell),
                                    C.component_priority(self.grid, pos, cell, True))
            return True
        return False

    def tick(self):
        """
        Advance one GAME tick. Returns True if anything changed.

        The field is re-solved before each due component rather than once for the
        whole batch, because dust carries instantly: a component firing early in a
        drain can change what a later one at the same tick reads, and that ordering
        is exactly what priority exists to pin down.
        """
        self.time += 1
        changed = False

        for pos in self.queue.drain_due(self.time):
            self.field = solve(self.grid, self.states)
            if self.grid.get(pos).id == LAMP:
                # Only go dark if it is STILL unpowered - the signal may have come
                # back inside the 4-tick window, which is the whole point of the wait.
                if not C.eval_lamp(self.grid, self.field, self.states, pos,
                                   self.grid.get(pos)):
                    if self.lamps.get(pos):
                        self.lamps[pos] = False
                        changed = True
                continue
            cell = self.grid.get(pos)
            if cell.id == REPEATER:
                if self._fire_repeater(pos, cell):
                    changed = True
                continue
            target = C.eval_one(self.grid, self.field, self.states, pos)
            if target is not None and target != self.states.get(pos):
                self.states[pos] = target
                changed = True

        self.field = solve(self.grid, self.states)
        self._reschedule()
        if self._update_lamps():
            changed = True
        return changed

    def run(self, game_ticks):
        """Advance a fixed number of game ticks."""
        for _ in range(game_ticks):
            self.tick()
        return self

    def run_until_stable(self, max_ticks=200):
        """
        Run until nothing is scheduled, or give up.

        Returns True if the circuit came to rest. False means it is still switching -
        a clock, which has no resting state and is not a failure.
        """
        if self.field is None:
            self.field = solve(self.grid, self.states)
            self._reschedule()
        for _ in range(max_ticks):
            if not len(self.queue):
                return True
            self.tick()
        return not len(self.queue)

    def prime(self):
        """Solve once and queue whatever is already out of date, without advancing."""
        self.field = solve(self.grid, self.states)
        self._reschedule()
        # Seed lamps at whatever they are right now, so the first tick measures a
        # change from the real starting point rather than from "everything off".
        #
        # ONCE only. `set_lever` re-primes so an input change propagates immediately,
        # and re-seeding here would overwrite a lamp that is mid-way through its
        # 4-tick wait - which silently turned the delay back off.
        if not self.lamps:
            self.lamps = {p: C.eval_lamp(self.grid, self.field, self.states, p,
                                         self.grid.get(p))
                          for p in self.grid.of_type(LAMP)}
        else:
            # An input change reaches lamps at once - it lights them immediately, or
            # starts their 4-tick wait from HERE. Leaving it until the first tick put
            # everything one tick late.
            self._update_lamps()
        return self

    # -- outputs -------------------------------------------------------------

    def dust_power(self, pos):
        return self.field.dust.get(pos, 0) if self.field else 0

    def lamp_states(self):
        """
        What every lamp is showing.

        Once the tick loop is running these come from tracked state, because a lamp
        that has just lost power is still LIT for another 4 game ticks. Under
        `settle()` there is no time, so the instantaneous answer is the right one -
        and it is what the oracle has always compared against.
        """
        if self.lamps:
            return dict(self.lamps)
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
