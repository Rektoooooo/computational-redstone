# The tick loop

Steady state is done — 97.59% per-block, 153/175 builds exact. Everything sequential
is blocked on time: latches, counters, shift registers, clocks, and every behavioural
test worth running.

## The rules, read from the game rather than guessed

Checked against decompiled 1.18.2 in `../.mc-reference`, not the wiki.

**Time.** One redstone tick is two game ticks. All delays below are in GAME ticks.

**Delays.** Repeater `delay × 2` (so 2–8). Comparator always 2. Torch 2.

**Scheduling.** A component schedules itself when its target output differs from its
current one, and only if it has no tick already pending — that guard is what stops a
diode being scheduled twice by two neighbours changing in the same tick.

**Priority.** Draining is ordered by trigger tick, then priority, then insertion
order. Lower value runs first:

| | value | when a diode uses it |
|---|---|---|
| EXTREMELY_HIGH | -3 | the block in front is a diode NOT pointing back at us |
| VERY_HIGH | -2 | otherwise, when currently powered (turning off) |
| HIGH | -1 | otherwise (turning on) |
| NORMAL | 0 | torches |

That first case is the "repeater facing into another's side" rule, and it is what makes
diode ordering deterministic rather than dependent on update order.

**Dust is instantaneous.** It never schedules. It re-solves the moment anything
changes, which is why the existing steady-state solver stays exactly as it is.

**Torch burnout.** At most 8 toggles tracked in a 60-game-tick window; exceeding that
burns the torch out and reschedules it 160 ticks later. Reachable only once time
exists. Deferred — noted below.

## Design

Keep the proven steady-state solver as the "settle the dust field" step and add a
scheduled-tick queue over the stateful components only (torch, repeater, comparator).
That reuses what is already validated instead of rewriting it.

Per game tick:

1. drain every tick due now, in (priority, insertion) order; before each one, re-solve
   the field, because dust is instantaneous and an earlier tick in the same drain can
   change what a later one reads
2. re-solve
3. schedule any component whose target now differs from its state, unless it already
   has one pending

## Tasks

- [x] read the scheduling rules from the decompiled source
- [x] correct the repeater/comparator side-input comment — the two use different rules
- [x] `sim/ticks.py` — the queue: trigger tick, priority, insertion order, pending guard
- [x] `sim/components.py` — per-component delay and priority
- [x] `sim/engine.py` — `tick()`, `run(n)`, `run_until_stable()`, `prime()`
- [x] unit tests: repeater delay, comparator delay, priority ordering, pending guard
- [x] a torch clock oscillates with the right period instead of hanging
- [x] check the 4 builds that currently oscillate — expect some to be genuine clocks
- [x] confirm the steady-state oracle is unchanged (97.59%, 153/175)

## Then, unblocked by this

- [ ] behavioural test: `alus/build-17` through an AND truth table
- [ ] behavioural test: 37+91 through `addition/3-ticks-8-bit-cca-by-don`
- [ ] paste a build into 1.18.2 via Litematica and compare against the real game
- [ ] torch burnout

## Review

Done. 14 timing tests, and the steady-state oracle is byte-identical at 97.59% —
the tick loop sits alongside `settle()` rather than replacing it.

**Reusing the solver was the right call.** Dust is instantaneous in the game, so the
proven three-pass solve became the "settle the field" step unchanged, and only the
three stateful components needed scheduling. No part of the validated work was
disturbed to get here.

**The design decision worth recording** is re-solving the field before *each* due
component rather than once per tick. Components due on the same tick are ordered by
priority precisely because an earlier one can change what a later one reads; solving
once per batch would have made that ordering meaningless and quietly wasted the
priority rules.

**Unexpected result: the tick loop resolved three builds steady state could not.**
Of the four builds where `settle()` never converges, three — all latches — simply come
to rest once time exists. Their bistability was never really a failure of the solver;
a latch's state is history, and history is what steady state does not have. Only
`displays/convert` genuinely clocks, at 13 repeaters and 10 torches, which is what an
animation driver should do.

**Reading the rules first paid for itself.** Priority is the part that would have been
invented wrongly: the rule that a diode outputting into another diode *not* pointing
back at it goes first is not something that falls out of thinking about it, and every
diode-ordering result would have been subtly wrong without it. Same for delays being
counted in game ticks rather than redstone ticks — a factor of two hiding under
plausible-looking behaviour.

**A correction it forced.** Checking the side-input rules showed repeaters and
comparators do *not* share one: a repeater's lock is restricted to diodes outright,
while a comparator's side accepts any signal source and takes its direct signal. An
earlier comment here had applied the comparator's rule to both. Same outcome in this
subset, different rule — and the wrong reason would have misled the next change.

Not done: torch burnout, and nothing has been driven through a whole real build yet.
Both are recorded above.
