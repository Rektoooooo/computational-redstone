# 2026-08-25 — Computational redstone skill library

## What was done

### 1. Fixed the YouTube transcript extension
`~/Downloads/yt-transcript-md`, bumped to v1.0.1.

**Bug:** every saved transcript contained the video twice.
**Root cause:** `pageScrapeTranscriptPanel` queried
`document.querySelectorAll('ytd-transcript-segment-renderer')` document-wide.
YouTube keeps **two** transcript panels in the DOM on a watch page (verified live via
Playwright: `ytd-transcript-renderer: 2`), so the scrape returned panel A's segments
followed by panel B's.

**Second bug that hid the first:** `groupSegments` computed
`isTooOld = segment.start - current.start > CHUNK_MAX_SECONDS`. When time runs
backwards that subtraction goes negative, so the seam was glued into one chunk.

**Fixes:** scoped the DOM query to a single visible panel; added `dropRepeatedPass()`
(truncates at a backward time jump > 5 s, with tolerance so late captions don't
truncate a good file); added an out-of-order guard to the chunker; deduped once in
`saveTranscript` so the file and the popup count agree.

**Tests:** `scratchpad/test-dedupe.mjs` loads the real `background.js` in a Node VM
with a `chrome` stub. 11 checks, all passing.

### 2. Built the transcript corpus — 32 files, all verified clean
The extension could not be driven from automation (Playwright uses its own isolated
Chromium; `chrome.commands` shortcuts are browser-process, not page-level — tested,
no file produced). YouTube also returns an empty caption body and refuses the panel
for unauthenticated sessions.

Used **yt-dlp** instead, in a throwaway venv in the session scratchpad. Wrote
`scratchpad/build_transcripts.py`, which mirrors `background.js` exactly (same
chunking, header, filename sanitising, dedupe) so output is indistinguishable.

Corpus: LRR #1–10, LMRC #1–11, Calculator #1–8, 3 standalone. ~504k chars.
The original 10 doubled files were **re-fetched clean and overwritten**; originals
backed up in `scratchpad/backup-original-10/`.

Dropped two videos: the "Fastest Multiplier" Short (captions are `[Music]` only) and
the "INSANE ideas" showcase reel.

### 3. Built the skill library
`~/Downloads/redstone-skills/` — 8 skills, 21 files, ~2550 lines.

Split by abstraction layer (user's explicit choice over the recommended task-based
split, made knowing the trigger-overlap tradeoff). Mitigated by writing every
description around a distinct task verb plus an explicit DO NOT TRIGGER clause
naming the sibling skill.

## Current status

Complete and validated. Frontmatter checks pass; all `name:` values match their
directory names.

## What's next

- **Not yet installed.** Symlink into `~/.claude/skills/` to activate:
  `for d in redstone-*/; do ln -s "$PWD/$d" ~/.claude/skills/; done`
- Skills are untested against real prompts — worth exercising the seven overlapping
  trigger terms (`decoder`, `register`, `comparator`, `counter`, `binary`, `shift`,
  `two's complement`) to see whether the right skill fires.
- `test-dedupe.mjs` lives in the scratchpad and will vanish with the session; move it
  into the extension folder if it should persist.

## Blockers / risks

- Opcodes 4 and 5 (`NOR`, `AND`) are inferred from the published BatPU-2 ISA, not
  stated on camera. Flagged in `redstone-cpu/references/isa-and-assembly.md`.
- "comparator" is genuinely ambiguous (component vs magnitude comparator) and is the
  most likely mis-trigger.

## Key files

| Path | What |
|---|---|
| `~/Downloads/yt-transcript-md/background.js` | fixed extension |
| `~/Downloads/YouTube Transcripts/` | 32 clean transcripts |
| `~/Downloads/redstone-skills/` | the skill library |
| `~/Downloads/redstone-skills/README.md` | index, install, gaps |
| `~/Downloads/redstone-skills/TRANSCRIPTS-TODO.md` | corpus + fetch method |
| `<scratchpad>/build_transcripts.py` | reusable fetch script |

---

# Session 2 — build pipeline + primitive extraction

## Done

**Researched how to give Claude build capability.** Wrote `BUILD-PIPELINE-RESEARCH.md`.
Key conclusion: three problems, not one — delivery (solved: litemapy/mcschematic),
generation (**composition, not synthesis** — synthesis via Yosys/V2MC exists but maps
to naive gates, losing the hand-optimised designs), and verification (the crux;
static linting first, behavioural sim second).

**Proof of concept working.** `pipeline/poc_litematic.py` — assembly → `.litematic`
with round-trip self-check. Assembles BatPU-2 subset with labels, emits repeaters per
bit, reloads from disk and reconstructs machine code from block positions. PASS.

**Network diagnosis.** PlanetMinecraft was double-blocked: the user's Wi-Fi content
filter *and* PMC's own Cloudflare. Hotspot beat the first; Cloudflare needs a real
browser and shouldn't be worked around. Found the direct URL pattern instead:
`planetminecraft.com/project/<slug>/download/worldmap/`.

**Built `worlds/extract.py`** — reads Minecraft world files directly, no Minecraft
needed. Three modes: `survey` (find builds + Y range + sign labels), `probe`
(per-layer breakdown, `--verify` cross-checks the block stream against get_block),
`extract` (bounding box → .litematic + manifest).

**Extracted 5 adder primitives** from the LRR Addition world into `worlds/primitives/`.

**Validated the skill library against ground truth.** ICA pistons, CCA pistonlessness,
CLE torch-only logic, ICA horizontal orientation — all confirmed by block census.
One correction applied to `redstone-arithmetic/references/adders.md`: "torchless" CCA
has 1 torch, not 0.

## Key technical findings

- `stream_chunk()` yields 384 layers × 256, y-major, from y=−64. Verified.
- Block **properties survive extraction** (repeater facing/delay/locked, comparator
  mode, wire connections) — tested with save/reload round trip.
- 1.18 stores block entities under `block_entities`, not `TileEntities`.
- **mattbatwings labels builds with in-world signs** — the single most reliable way to
  identify a component. It corrected a wrong structural guess (comparator array read
  as a mux; the sign said magnitude comparator).
- Survey timing: ~80s for 9 regions, ~5min for 27.

## Next

1. Extract the magnitude comparator (located, signed, at (-16,60,-48) in Combinational)
2. Survey `LRR Sequential Blocks` for registers/counters
3. **Record I/O port maps** per primitive — the blocker for programmatic wiring. The
   `[1][2][4]...[128]` bit signs give bit ordering.
4. Phase 1 of the pipeline (full assembler) — independent of all this
5. Trim bounding boxes; they currently include wool/signs/air

## Blockers

- No primitive has been pasted back into Minecraft and tested. Block-level fidelity
  verified; in-world behaviour unconfirmed.
- Minecraft still not launched on this machine (no `.minecraft` dir).

---

# Session 3 — full harvest (autonomous)

## Done

**All 20 worlds downloaded and harvested. 195 builds extracted, 43 sign-named.**
Output in `worlds/primitives/`, indexed by `MASTER-INDEX.json` and `PROFILES.md`.

**Built `worlds/harvest.py`** — bulk extraction. Clusters components by spatial
proximity (voxel flood-fill at CELL=4), not chunk adjacency, which roughly doubled
yield and tightened bounds ~3x. Names builds from signs inside their bounding box.

**Built `worlds/profile.py`** — adds measured structural features to every manifest.

**Two more skill-library corrections from Computer v2's 113 signs:**
- Control ROM at z=-24 lists opcodes in order, confirming **NOR=4, AND=5** (was
  flagged as inferred). Caveat removed from `isa-and-assembly.md`.
- ALU has **six** control signals, not five — `right shift` is a control bit, not
  separate hardware. Corrected in `alu.md` and `redstone-cpu/SKILL.md`.
- Recorded the full 22-line control map; revealed three-way destination select
  (`dest A/B/C`) and three-way write-back source, both simplified in the videos.

## Judgement calls made without input

- **Did not ship the structural classifier as a labeller.** Benchmarked it against the
  18 known builds: 50% useful, 44% no answer, **6% actively misleading** (it called the
  CLE adder a "26-output decoder"). Removed the offending lamp-count rule and marked
  all candidates as weak inferences in PROFILES.md. A wrong label would propagate.
- **Moved only the 16 world zips by explicit name**, leaving the user's 5 unrelated
  zips in ~/Downloads — deliberately not repeating the earlier `*.zip` mistake.
- **Re-ran 4 worlds at `--min 4`** after noticing implausibly low yields.

## Key finding: threshold matters

First pass at `--min 20` badly under-harvested small builds: Logic Gates found 3,
Latches 3. Re-run at `--min 4` gave **12 and 8**, and latches gained 10 sign labels
missed entirely the first time. Small builds (a gate is ~10 components) fall under a
per-chunk threshold. If a world looks sparse, lower the threshold first.

## Blockers / open

- **`alus/` has ZERO signs** — 18 unlabelled builds, and it is the most valuable world
  for CPU work. Needs identifying in-game; the classifier is not good enough.
- **152 of 195 builds unlabelled.** Best resolved by opening worlds in Minecraft.
- **I/O port maps still missing** — the real blocker for programmatic wiring.
- **Nothing pasted back into Minecraft and tested.** Block fidelity verified only.

## Next

1. Identify `alus/` builds in-game (highest value, 18 builds)
2. Record I/O port maps — use the `[1][2][4]...[128]` bit signs for ordering
3. Phase 1 of the pipeline (full assembler) — independent of all the above

---

# Session 4 — the redstone simulator

## Why

The project had knowledge, data and rendering but **no feedback loop** — no way to
determine whether a circuit works, and no way to check my own reading of one. That had
already produced two wrong calls. Everything downstream (verifying primitives,
composing them, generating builds) was blocked on it.

## What was built

`worlds/sim/` — a simulator for the computational subset (dust, repeater, comparator,
torch, lever, redstone block, lamp). Pistons, observers, 0-tick and quasi-connectivity
are deliberately out of scope.

**Design:** a three-pass steady-state SOLVE, not an event-driven tick simulation.
Exploits the fact that strong power comes only from components and weak only from dust,
so dust power and block power are not mutually recursive. Dust connection shape is read
from the saved blockstate rather than reimplementing Minecraft's connection logic.

**The oracle** is the key asset: extracted `.litematic` files preserve LIVE circuit
state (dust power levels, powered/lit flags), so every build is a snapshot of a real
settled circuit — ~170,000 blocks of free ground truth. Test framed as a fixed-point
check (seed from saved, settle, verify it stays) rather than reproduce-from-scratch,
because bistable circuits have more than one valid resting state.

## Results

```
python -m sim.tests.test_units     ->  13/13 pass
python -m sim.oracle primitives    ->  88.09% over 173 builds, 68 at exactly 100%

  dust 89.67% | repeater 89.95% | torch 88.88% | comparator 82.33% | lamp 65.42%
```

## Three bugs the oracle caught

1. **`facing` on a diode points at the INPUT, not the output.** Minecraft's DiodeBlock
   reads from `pos.relative(facing)`. Having it backwards reversed every repeater and
   comparator in the library. 72.7% -> 94.1% on the sample.
   **The unit tests did not catch this** - the fixtures encoded the same wrong
   assumption as the code, so they agreed with each other. Only real data disagreed.
2. **Extraction dropped container contents.** `region.tile_entities` was empty, so every
   signal-strength barrel read as empty; 3737 comparators read a barrel and 87% were
   wrong. Fixed by `worlds/containers.py`, which recovers levels from the source worlds
   into the manifests. Comparators 39.6% -> 82.3%.
3. **Dust only activates a mechanism it points at.** Fixed; helped arithmetic builds
   but NOT library-wide (see below).

## Skill library correction

`redstone-fundamentals` claimed a weakly powered block leaves an attached torch lit.
That is **Bedrock** behaviour. In Java a torch is off whenever its support carries any
power, weak or strong; weak vs strong only decides whether a block can start new dust.
Corrected in the SKILL.md with a note explaining how it was found.

## Next session — start here

1. **Lamps are 65% library-wide** and that is the biggest single gap. The
   pointing-direction fix lifted them to 92% on arithmetic builds but did nothing
   overall, so the display worlds fail for a different, unfound reason. Diagnose with
   the same technique that worked before: correlate mismatches against adjacent block
   types, then print a slice.
2. **Then the tick loop** — delays, scheduling, sequential behaviour. Steady state is
   the foundation and is now proven.
3. **Then the behavioural tests** from the plan: drive `alus/build-17` through an AND
   truth table, and drive `addition/3-ticks-8-bit-cca-by-don` with real numbers using
   the port maps. The adder test is the headline: if it computes 37+91 correctly from
   nothing but extracted blocks, the model is validated.
4. **Compare against real Minecraft.** The user is home now. Any divergence in-game
   outranks the oracle, since the oracle is a saved snapshot and the game is the
   authority.

## Useful debugging technique discovered

When agreement drops, do NOT stare at one coordinate. Instead:
  - categorise mismatches (under-powered vs over-powered) to tell missing-source from
    spurious-source
  - correlate mismatches against adjacent block types to find the culprit component
  - print a 2D slice showing `saved/computed` per cell to see the structure
Each of the three bugs was found this way within a couple of iterations.

---

# Session 5 — steady state to 92%, and a reference for the rules

## Why

The roadmap's first item was lamps at 65% library-wide. It turned out not to be a lamp
bug at all.

## Done

**Lamps 69.7% → 95.0%, overall 88.7% → 92.2%.** Three fixes, all validated against the
oracle and locked in with 10 new unit tests (23/23 pass).

**1. Nothing fed a diode or a lamp from a point source.** `input_from` handled dust,
redstone blocks and diodes, then fell through to `return 0` — so a repeater sitting
directly against a torch read as unpowered, and 1799 diodes in the library sit against
one. On a lamp screen that leaves the driver torch lit and every lamp on: `displays`
agreed on 28% of its lamps, and `build-14` lit all 256. `eval_lamp` had the same hole
for levers, which are mounted straight onto lamps 1311 times. Added `source_signal()`
— torch / lever / button / pressure plate, respecting the rule that a torch never
powers its own support — below the `sides_only` gate so comparator sides are unaffected.
Lamps **69.7 → 95.0**, torches **92.6 → 98.0**, repeaters **92.1 → 95.9**.

**2. A lever strongly powers only the block it is mounted on**, not all six neighbours.
The old behaviour let a lever start a dust run from a block it merely touched.

**3. A comparator reads a container THROUGH a solid block.** If the block behind is a
full conductor and the reading is under 15, it looks one further for a container and
takes that instead. Keeping a signal-strength barrel one block back is a normal build,
and those comparators were reading whatever the intervening block carried.
Comparators **83.5 → 93.4**.

## Method note — the diagnosis, not the fix, was the work

The documented technique found it in about three steps, and none of them involved
looking at a lamp:

1. split lamp mismatches by direction — **2321 over-lit against 280 under-lit**, so a
   spurious source, not a missing one
2. correlate against neighbouring block types — 97% of the over-lighting sat in two
   worlds, both screens
3. print a slice — and the wrongness was two blocks upstream, at a repeater reading a
   torch, not at the lamp at all

Shipped as `sim/lampdiag.py` (steps 1–2) and `sim/probe_lamp.py` (step 3). Worth
re-pointing at whatever category is currently worst.

## A reference for the rules

Bugs 2 and 3 were found by reading what the game actually does. Pulled the 1.18.2
client and its official mappings, converted ProGuard → TSRG, remapped with
SpecialSource and decompiled the ten redstone classes with Vineflower.

It lives at **`../.mc-reference`, outside the repo on purpose** — Mojang's code is not
ours to redistribute. Nothing from it is committed and nothing should be; only rules in
our own words. `pg2tsrg.py` is there if it needs rebuilding.

It confirmed the solver's core architecture is right, which was worth knowing: the
strong/weak split models the game's actual mechanism, where dust switches off all wire
signalling while computing its own strength. That is exactly why a weakly powered block
cannot start a new dust run but *can* light a lamp.

It also corrected a reason, not just a result: comparator side inputs are **not**
restricted to diodes, as a comment claimed. A side reads any signal source but takes
its DIRECT signal — and a torch emits direct signal only upward, a lever only into its
support, so neither reaches a comparator sideways. Same outcome, different rule; the
wrong reason would have misled the next change.

## Next — start here

1. **Dust, at 89.91%, is now the gap** — 15,252 of the 18,047 wrong blocks, because
   dust is two thirds of the library. Errors run **4:1 over-powered** (12,158 / 3,094),
   so hunt a spurious connection. The commonest neighbour of a wrong dust is stained
   glass by a wide margin — the glass towers. Prime suspect: `dust_links` follows a
   connection one level DOWN for any side that is not `none`, while vanilla only steps
   down when the block in between does not occlude. **Unconfirmed — verify first.**
   Worst worlds: `subtraction` 66%, `multiplier` 73%, `callstack` 78%.
2. Then the tick loop. Repeater delay is `delay * 2` game ticks, comparator always 2,
   and both schedule at a priority that depends on whether they are turning off — that
   is what makes diode ordering deterministic. Read it in the reference before building.
3. Then the behavioural tests (AND truth table, then 37+91 through the adder).
4. Then real Minecraft. **It is installed on this machine now** — but as 26.2 and a
   26.3 snapshot, and this project targets 1.18.2, so add 1.18.2 before comparing.

## Blockers

- Nothing has still been pasted back into Minecraft and tested.
- 20 of 195 builds skipped as too large for the oracle.

---

# Session 5b — dust, and steady state is essentially done

## Done

**Dust 88.8% → 97.7%. Overall 92.2% → 97.6%. 153 of 175 builds now exact, up from 68.**

One bug, the one flagged as the prime suspect at the end of 5a — and it was the
suspect, but for a slightly different reason than predicted.

`dust_links` decided power flow by reading the wire's saved
`north/east/south/west` shape, following a step DOWN for any side that was not `none`.
Those properties describe how the wire is *drawn* and which mechanisms it feeds. The
game works out neighbour-to-neighbour power **separately, from block occupancy**, and
never consults the shape for it. The extra downward steps carried power across gaps
that do not conduct, which is why the errors ran 4:1 over-powered and clustered around
the glass towers.

Rewritten to the real rule. Per horizontal direction, from the reader's side, the
deciding block is the one beside the reader, in between the two:

| source | condition on the block between |
|---|---|
| same level | none |
| one level UP | must **be** a conductor, and nothing solid may cap the reader |
| one level DOWN | must **not** be a conductor |

The two diagonal cases demand the opposite thing of that block, so the relation is
**asymmetric** — a diagonal step legal one way need not be legal back. Five unit tests
pin both directions and both failure modes (28/28 pass).

Dust is two thirds of every build, so fixing it carried every other category with it:
comparators +1.1, lamps +1.6, repeaters +1.0 without touching any of them.

## Worth remembering

The saved blockstate is a good oracle for *what the game rendered*, and a bad one for
*why*. Shape and power flow are computed by different code from different inputs, and
reading one to infer the other worked well enough to hide for four sessions. Where the
schematic records an outcome, prefer re-deriving the cause from the blocks.

## Next — start here

1. **The tick loop.** Steady state is done enough to build on and everything sequential
   is blocked on it. Repeater delay is `delay * 2` game ticks, comparator always 2, and
   both schedule at a priority that depends on whether they are turning off — that is
   what makes diode ordering deterministic. Read it in `../.mc-reference` first; this is
   the area where guessing costs most.
2. Then the behavioural tests: AND truth table through `alus/build-17`, then 37+91
   through `addition/3-ticks-8-bit-cca-by-don` using its port map.
3. Then real Minecraft, once 1.18.2 is installed.

Lower priority, only if the residue starts mattering: comparators are the weakest
category at 94.4%; four builds oscillate instead of settling, and some of those are
probably genuine clocks, which have no steady state and are not failures; the worst
builds are `displays/blank`, `displays/build-02`, `cpu-ep07-branching/build-07`.

---

# Session 5c — the tick loop

## Done

**Built the tick loop.** Steady state answers "where does this rest"; this answers
"what does it do", which is what anything sequential needs. 14 timing tests, and the
steady-state oracle is byte-identical at 97.59% — the tick loop sits alongside
`settle()` rather than replacing it.

Rules read from decompiled 1.18.2 before writing any of it, not guessed:

- one redstone tick is **two game ticks**; everything counts in game ticks
- repeater `delay x 2`, comparator always 2, torch 2
- draining is ordered by trigger tick, then **priority**, then insertion order
- a diode goes first when the block it outputs into is another diode NOT pointing back
  at it — the "repeater facing into another's side" case. Otherwise one turning off
  outranks one turning on
- a component with a tick already pending does not get another, so two neighbours
  changing at once cannot make one repeater fire twice

New: `sim/ticks.py` (the queue), `component_delay`/`component_priority`/`eval_one` in
components, and `tick`/`run`/`run_until_stable`/`prime` on `Sim`. `set_lever` now
re-solves immediately, because flipping a lever updates its neighbours at once in the
game and only then does anything wait its delay.

## Judgement calls

**Reused the solver rather than rewriting.** Dust is instantaneous in the game, so the
proven three-pass solve became the "settle the field" step unchanged and only the three
stateful components needed scheduling. Nothing already validated was disturbed.

**Re-solve before each due component, not once per tick.** Components due on the same
tick are ordered by priority precisely because an earlier one can change what a later
one reads. Solving once per batch would have made the ordering meaningless and quietly
wasted the priority rules.

## Unexpected result

**The tick loop resolved three builds steady state could not.** Of the four where
`settle()` never converges, three — all latches — come to rest once time exists. Their
bistability was never a failure of the solver: a latch's state is history, and history
is what steady state does not have. Only `displays/convert` genuinely clocks, at 13
repeaters and 10 torches, which is right for an animation driver.

## A correction

Repeaters and comparators do **not** share a side-input rule. A repeater's lock is
restricted to diodes outright; a comparator's side accepts any signal source and takes
its DIRECT signal. A comment added in 5a had applied the comparator's rule to both.
Same outcome in this subset — a torch emits direct signal only upward and a lever only
into its support, so neither reaches a comparator sideways — but a different rule, and
the wrong reason would have misled the next change. Fixed.

## Next — start here

1. **Behavioural tests.** This is the gap now: the timing rules are checked against the
   game's own and the micro-circuits pass, but nothing has been driven through a whole
   extracted build. AND truth table through `alus/build-17`, then 37+91 through
   `addition/3-ticks-8-bit-cca-by-don` using its port map. Use `prime()`, `set_port()`,
   `run_until_stable()`.
2. **Real Minecraft.** 1.18.2 is installed with a flat world, and Litematica pastes a
   `.litematic` straight in. Nothing has ever been pasted back and tested — the oldest
   open item in the project, open since session 2. The game outranks the oracle.
3. **Torch burnout**, if a fast clock misbehaves: 8 toggles in a 60-tick window burns a
   torch out for 160 ticks. Only reachable now that time exists.

---

# Session 5d — checked against the real game at last

## Done

**Two circuits built in Minecraft 1.18.2 and compared against the simulator. Both
matched exactly.** This closes the item open since session 2: nothing from this project
had ever been pasted back and run.

`verify/` holds the tooling — `make_test_schematic.py` builds a case, `predict.py`
prints what the simulator expects, `to_commands.py` emits `/setblock` lines. The
prediction is written down before looking at the game, because a model consulted
afterwards always seems to agree.

**Test 1, `decay`** — redstone block, six dust, lamp. Predicted 15/14/13/12/11/10 and a
lit lamp. Exact. The lamp is less trivial than it looks: dust does not connect to a
lamp, since a lamp is not a signal source, and only reaches it because a wire with
nothing north or south straightens itself into a line.

**Test 2, `steps`** — the one that carried weight. Four lanes differing in only two
things: the block the dust steps over (stone or glass) and whether the source sits
below the step or above it.

| lane | step | source | reader | lamp |
|---|---|---|---|---|
| 1 | stone | below | 13 | lit |
| 2 | glass | below | 13 | lit |
| 3 | stone | above | 13 | lit |
| 4 | glass | above | **0** | **dark** |

All four exact. Lanes 2 and 4 are the same build with the source at opposite ends, and
the same glass block let power climb onto it while refusing to let it back down.

That asymmetry was **derived** in 5b by inverting reader-side logic, not read off
directly, and the dust fix resting on it moved agreement 88.79% -> 97.67% - the largest
single correction in the project. It could easily have been backwards. It is not.

## Practical findings, all of which cost time

- The game runs through **ModrinthApp**, not the vanilla launcher. Schematics belong in
  `~/Library/Application Support/ModrinthApp/profiles/Redstone/schematics/`.
- **Litematica's `executeOperation` hotkey ships UNBOUND**, which makes pasting look
  broken when nothing is wrong. Tool mode cycles with Left Ctrl + scroll while holding
  the tool item, and paste needs a placement *selected*, not just loaded.
- Those defaults are readable rather than guessable: `javap -c` on
  `fi/dy/masa/litematica/config/Hotkeys.class` in the mod jar pairs each hotkey with
  its default. Worth remembering as a technique - guessing at keybinds wasted several
  exchanges before that.
- **Under ~50 blocks, prefer `/setblock` over pasting.** Commands fire block updates;
  a paste does not always, and an un-updated redstone paste reads as all zeros and
  looks exactly like a broken model.

## Next

1. **Behavioural tests on extracted builds** - the real gap. AND truth table through
   `alus/build-17`, then 37+91 through `addition/3-ticks-8-bit-cca-by-don`. Predict
   first, then paste the same build in game and compare. The pipeline for doing that
   now exists and is proven on small cases.
2. Comparator reading a container through a solid block is the other big fix that has
   not been checked in game. It needs a barrel with a known fill level, so the schematic
   has to carry block entity data or the barrel gets filled by hand.
3. Torch burnout, still unmodelled.

---

# Session 5e — the first extracted build driven in game, and a label was wrong

## Done

**`alus/build-17` driven through its truth table in Minecraft. It is a 3-input XOR
(odd parity), NOT the "single AND gate" its label claimed at confidence `high`.**

The simulator predicted a 3-input XOR offline. The manifest said AND. The game settled
it: both inputs on gives output **off**, which an AND gate cannot do, and each single
input on gives output **on**. Five of eight rows observed directly - A and B read off
their own indicator lamps, C inferred from the output. **The simulator called every
observed row correctly.**

Odd parity across three inputs is the SUM output of a full adder, which is exactly what
belongs in an ALU world - a far more useful thing to have identified than a stray AND.

## Why the label was wrong, and what it says about the other 17

The reading came from visual structure: "torches on both inputs, merge into a dust
line, one final torch" - the De Morgan AND. Built that way, an AND and a XOR really do
look alike, so the shape was not crazy. Two things should have caught it:

- **it described *two* levers for a build with three.** The measured port map and census
  both said three. Where a reading contradicts a measurement, the measurement wins.
- **nobody had driven it.** It cost about two minutes once the tooling existed.

It was also marked `high`, so **`high` did not mean reliable**. Two other ALU builds
carry that same confidence and fifteen sit at `medium`; all seventeen are still guesses.
Marked as such in `alus/IDENTIFICATION.md` rather than quietly left alone.

This is the third time structural inference has been wrong in this project, which is
consistent with the earlier benchmark of 50% useful and 6% actively misleading. The
inference is still worth keeping as a lead. It is not worth trusting as a label.

## Method note

Screenshots were read straight out of the game directory
(`ModrinthApp/profiles/Redstone/screenshots/`) rather than pasted in. Downscaling them
and cropping the lamp and lever regions into a single montage made the states readable
at a fraction of the cost of reading ten 4112x2522 frames. Worth repeating: the levers'
own indicator lamps sit directly beneath them, so input state is visible in the same
frame as the output.

## Next

1. **37+91 through `addition/3-ticks-8-bit-cca-by-don`** - the headline test. Predict
   offline, paste the same build, compare. Watch for bit ordering: `portmap.py` measures
   port positions and widths but the `[1][2][4]...[128]` signs never reached the
   `.litematic`, so a garbled sum means wrong bit order before it means wrong physics.
2. Drive the other ALU builds now that it is cheap - `build-03` and `build-00` first,
   since they carry `high` confidence and have never been checked.
3. Torch burnout, still unmodelled.

---

# Session 5f — the adder works in the real game

## Done

**`addition/3-ticks-8-bit-cca-by-don` computed 37 + 155 = 192 correctly in Minecraft,
and the simulator predicted it.** A real mattbatwings circuit, read out of a world
file, pasted back, and doing correct 8-bit arithmetic. That is the whole chain
validated end to end.

**Bit ordering is no longer inferred.** Added `worlds/signs.py`, which recovers sign
text AND POSITION from the source worlds. The harvest had kept the strings and thrown
the coordinates away, and the coordinates are the valuable half: mattbatwings labels a
port's bits with signs reading 1, 2, 4 ... 128, so without their positions `portmap.py`
could measure where the levers were but not which one was the low bit. 95 signs
recovered. For the adder they settle it outright - inputs and outputs both run bottom
up. The old inference happened to be right, but it is now measured.

Also identified the 17th lever, outside both input ports, as the **carry-in**: it adds
exactly 1 to every sum, which is what two's-complement subtraction needs.

## The two results worth keeping

**The timing matched the author's own labels.** Sums settle in 6 game ticks and
carry-out in 8 - 3 and 4 redstone ticks - against a build named "3 ticks 8-bit CCA by
Don" whose carry-out sign reads "COUT (4 ticks)". Those numbers were never given to the
model. A steady-state solver cannot produce that; only a tick loop can.

**The inputs were not the ones predicted, which made it a better test.** The prediction
was written for 37 + 91. One lever landed a row off, so the real inputs were 37 + 155.
The machine gave the right answer for what it actually had and the simulator matched,
which is worth more than reproducing a pre-computed expectation - nothing could have
been tuned to fit. A bit-ordering error would have lit some other pair of lamps.

## Note on reading results

Screenshots of a 22-block-tall tower at an angle were NOT readable enough to call the
lamp states, and saying so was better than guessing from ambiguous crops. The user read
the levers and lamps off directly and reported them in one line. For tall builds, ask
for the reading rather than trying to recover it from an isometric screenshot.

## Next

1. **Drive the remaining ALU builds.** 17 of 18 readings are still guesses and `high`
   confidence has already been wrong once. `build-03` and `build-00` first.
2. Unzip the remaining worlds and re-run `signs.py` - only LRR Addition was unpacked, so
   most builds still have no recovered sign positions and therefore no measured bit
   order.
3. Torch burnout, still unmodelled.

---

# Session 6 — the ALU family, and composition (M1 + M2)

## Done

**Six of eighteen ALU builds driven, and they are one device built up in stages.**
`verify/drive.py` enumerates small builds; `verify/alu_probe.py` handles the rest by
splitting levers into operands and controls from BEHAVIOUR and then naming the
arithmetic per control setting, since build-03 has 96 levers and 2^96 is not an option.

    build-16   carry-in          A+B, A+B+1
    build-15   + invert A        adds ~A+B, B-A
    build-13   + invert B        adds A+~B, A-B, ~A+~B
    build-10   + logic mode      adds bitwise XNOR, and XOR with either invert
    build-09   + one more        all six bitwise ops - the end of the progression

Two labels were outright wrong: `build-17` read as a single AND gate is a 3-input XOR,
and `build-16` read as "four independent gates" is a ripple-carry adder. Both failures
had the same shape - the visual read got the PARTS right and missed how they were
JOINED. A De Morgan AND and a XOR look alike; four adder stages look like four gates
until you notice the carry.

**All 20 worlds unpacked and signs recovered**: 355 signs across 52 manifests, 323
embedded into the .litematic files so pasted signs read again. The ALU world has zero
signs, exactly as session 3 recorded, which is why those builds had to be driven.

**M1 - two components joined.** `pipeline/compose.py`. Two adders chained into
(A+B)+C, verified over 512 bus + 517 arithmetic cases, confirmed in game.

**M2 - the output routed round to the front.** The adder was inside-out: inputs west,
sum lamps east, so you set the numbers and walked around 517 blocks to read the answer.
Now `(Input A) (Input B) (Output)` sit on one face. 517 cases, confirmed in game.

## The thing that made M2 tractable

Each bit routes inside its OWN horizontal plane, so the search is two-dimensional. Bits
sit 2 apart in y, and a support block over a live wire does not leak into the line above
- simulated before relying on it. In any one plane the adder occupies ~26 cells inside
x 4-9, z 2-7, leaving the whole x=12 column and z=8-10 rows free.

## Three failures the simulator could not see

Worth more than the milestones. All three passed every sweep:

1. **16 repeaters floating in mid-air.** M1 shipped with them, passed 1029 cases, and
   fell apart on paste. The swap looked like-for-like - an output lamp and a WALL lever
   both need no floor, but a repeater does. Now `Composition.floating()`.
2. **A drive repeater facing the wrong way.** Its facing was hardcoded east on the
   assumption the wire would arrive from the east; the router came from the north. The
   signal travelled the whole route and died at the last block. Fixed by routing to the
   cell east of the repeater, making the approach a fact rather than a hope.
3. **Wire shape wrong on disk.** End cells were given connections only toward their
   PATH neighbours, so they drew as straight lines past the repeaters beside them. The
   game recomputes shape on update and it behaves correctly, so nothing failed - it just
   looked wrong to someone standing there.

The pattern: **the simulator models signal, not physics and not appearance.** Generated
builds need a structural check and a human eye as well as a behavioural sweep. All in
`tasks/lessons.md`, along with the user's conventions - build in wool with one colour
per line, and version schematics rather than overwriting them.

## Next

1. **M3, timing alignment.** M2's routes were all the same length so delays matched for
   free; they will not in general, and a skewed bus feeds garbage to anything
   sequential.
2. **The remaining 12 ALU builds** - `build-03` and `build-00` first, both still `high`
   confidence and never checked.
3. Torch burnout, still unmodelled.

Disk: the unpacked worlds are 936 MB and the disk was at 97%. They regenerate from the
committed zips, and both `signs.py` and `containers.py` have already run.

---

# Session 7 — M3, and the clock checked against the game

## Done

**M3.1 - verified the tick model in game.** It had never been compared to the real
thing; the 14 unit tests only proved it was self-consistent. `verify/timing.litematic`,
stepped with `/tick freeze` + `/tick step`:

    A0..A7    predicted 8,16,24..64   measured 9,17,25..65
    B d1..d4  predicted 16,32,48,64   measured 17,33,49,65

Delay setting N is 2N game ticks, delays add linearly, order strictly correct. Every
lane exactly one tick late - that is where tick-stepping starts counting, since the
lever is flipped while frozen, and it cancels in any difference.

Doing this BEFORE using the numbers was the user's call and it was right: M3.2 pads
using these very numbers, so a wrong ruler would have produced a wrong alignment that
then verified against itself.

**M3.2 - measure bus skew and pad it flat.** `arrival_ticks()`, `settle_profile()` and
`align()` in `pipeline/compose.py`. Skew 4 -> 0 at no block cost, by turning UP delay
settings on repeaters already in place. 512 cases still exact: alignment changes WHEN,
not WHAT. Confirmed in game repeater by repeater - the whole firing sequence matched,
not just the final lamps.

## Three rules the simulator was missing, all found by measuring

1. **A lamp is asymmetric.** Instant on, **4 game ticks** to go dark, re-checking on
   arrival so a signal returning inside the window leaves it lit. The oracle is blind to
   this by construction - the settled state is identical either way - so it survived 175
   builds and nine in-game tests. Found by the user stepping ticks and noticing a lamp
   still lit with every repeater behind it dark.

2. **A repeater STRETCHES a pulse shorter than its own delay.** When its scheduled tick
   arrives while it is off it turns on unconditionally, even if the input has gone, then
   schedules its own turn-off. The sim re-checked the input at fire time - the obvious
   implementation, and wrong: short pulses vanished completely. Every clock and edge
   detector depends on this. Found by cross-checking against community documentation at
   the user's suggestion.

3. **Two kinds of skew, and only one is paddable.** STRUCTURAL skew is fixed by the
   wiring and pads flat. DATA-DEPENDENT skew from a carry chain varies with the input -
   the ripple-carry adder settles in 8 ticks for 162 of 256 pairs and 22 for 8 of them -
   and no fixed padding flattens it. Wait for the worst case instead.

All three are in `docs/timing.md` with their evidence level.

## Known limitation of align()

It pads by raising delay settings, and **one 4-tick repeater is not equivalent to four
1-tick repeaters**. They delay a steady signal identically, but a single slow repeater
distorts any pulse narrower than itself. Fine for the level signals it was tested on;
wrong where pulse width has to survive. Recorded rather than silently carried.

**Repeater locking is the better tool** and is not implemented yet: lock every output
repeater from one control line, let the data settle at its own unequal speeds, then
unlock and all lines transition together. It works on data-dependent skew too, which
padding cannot touch - the obvious way to feed a register.

## Mistakes worth not repeating

- **Two builds that look alike need a visible difference.** M3's staggered and aligned
  builds differ by five block properties and nothing else. I said so, then handed both
  over with no way to tell them apart, and the aligned one got tested twice. The tell is
  the repeater behind the white lamp: torches far apart when aligned, close when not.
- **align() saved its output under the input's name**, so Litematica listed the aligned
  build calling itself the staggered one.
- **"Stagger the lamps to create skew" does not work.** Dust carries within the tick, so
  a longer route is not a slower one - only the repeaters it forces are.

## Next

**M4 - spec to build.** Everything under it exists and has been used in anger. See
`CLAUDE.md` for the two cheap things worth doing first: driving the remaining 12 ALU
builds, and trying repeater locking as a bus latch.
