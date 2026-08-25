"""
Scheduled ticks.

Redstone is not all instantaneous. Dust settles within the tick it changes in, which
is why the steady-state solver can ignore time entirely, but the stateful components -
torches, repeaters, comparators - schedule themselves to change LATER, and the order
they come back in is what gives sequential circuits their behaviour.

Three things decide that order, and all three matter:

    trigger tick    when it fires. One redstone tick is TWO game ticks; everything
                    here counts in game ticks.
    priority        which of several components due on the same tick goes first.
    insertion order the tie-break, so two components at the same priority resolve in
                    the order they were scheduled rather than arbitrarily.

The pending guard is the other load-bearing rule: a component that already has a tick
waiting does not get another. Without it, two neighbours changing in the same tick
would schedule the same repeater twice and it would fire twice.
"""
import heapq

# Lower runs first. Named for the game's own priorities so the mapping is obvious.
EXTREMELY_HIGH = -3
VERY_HIGH = -2
HIGH = -1
NORMAL = 0

PRIORITY_NAMES = {EXTREMELY_HIGH: "extremely_high", VERY_HIGH: "very_high",
                  HIGH: "high", NORMAL: "normal"}


class TickQueue:
    """Pending component updates, ordered by (trigger tick, priority, insertion)."""

    def __init__(self):
        self._heap = []
        self._pending = set()
        self._seq = 0

    def schedule(self, pos, when, priority=NORMAL):
        """
        Queue `pos` to fire at game tick `when`.

        Returns False and does nothing if that position already has a tick waiting -
        the game's own guard against being scheduled twice in one tick.
        """
        if pos in self._pending:
            return False
        heapq.heappush(self._heap, (when, priority, self._seq, pos))
        self._seq += 1
        self._pending.add(pos)
        return True

    def is_pending(self, pos):
        return pos in self._pending

    def drain_due(self, now):
        """Every position due at or before `now`, in the order the game would run them."""
        out = []
        while self._heap and self._heap[0][0] <= now:
            _when, _priority, _seq, pos = heapq.heappop(self._heap)
            self._pending.discard(pos)
            out.append(pos)
        return out

    def next_time(self):
        """The tick the next update falls on, or None if nothing is waiting."""
        return self._heap[0][0] if self._heap else None

    def clear(self):
        self._heap.clear()
        self._pending.clear()

    def __len__(self):
        return len(self._heap)

    def __repr__(self):
        return f"<TickQueue {len(self._heap)} pending, next={self.next_time()}>"
