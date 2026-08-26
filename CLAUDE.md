# Working on this repo

Orientation for a fresh session. Read this first, then `.handoffs/` for the latest
state.

## What this is

Tooling and a knowledge library for **computational redstone** — digital logic and CPUs
built inside Minecraft. Three parts:

1. **9 agent skills** (`redstone-*/`) covering components through CPU architecture,
   wiring included
2. **A toolchain** (`worlds/`) that reads Minecraft world files directly, with no
   Minecraft installed, and extracts redstone builds as reusable `.litematic` components
3. **A simulator** (`worlds/sim/`) that solves those circuits and checks them against
   the real saved state

Scope is Java Edition, 1.18.2 conventions, and *computational* redstone specifically —
pistons, observers, 0-tick tricks and quasi-connectivity are deliberately excluded
throughout. That restriction is what makes the subset deterministic enough to simulate.

## Setup

```bash
python3 -m venv .venv
./.venv/bin/pip install anvil-parser2 litemapy mcschematic Pillow cairosvg
```

That is enough for the simulator and the renderer — 195 extracted builds, their
manifests and the block textures are all committed.

Only needed if you are re-extracting from source worlds:
```bash
cd worlds && unzip '*.zip'      # 115 MB of committed zips -> 925 MB of worlds
```

## Current state

| | |
|---|---|
| Transcripts | 32, verified clean |
| Skill library | 9 skills, ~2,700 lines, audited against real blocks |
| Extracted builds | 195, of which 43 named from in-world signs |
| Simulator | steady state, **97.59%** per-block agreement, **153/175 builds exact** (dust 97.7, repeater 97.8, torch 98.5, comparator 94.4, lamp 96.7) |
| Tick loop | **built and verified against the game** — delays, priority, lamp on/off asymmetry, repeater pulse stretching; 20 timing tests |
| In-game checks | **10 passed**, incl. the CCA adder computing 37+155=192, two corrected labels, and the tick model measured with `/tick step` |
| Composition | **M1–M4 done.** M4 is a working **decimal adder**: two digits in on levers, the sum on a seven-segment screen |
| Skill library | plus **`redstone-wiring`**, written from a world download rather than a video — 49 builds harvested and driven |
| ALU builds driven | **6 of 18** — they are one ALU built up in stages, ending at `build-09` with all six bitwise ops |

## Verify it works

```bash
cd worlds
../.venv/bin/python -m sim.tests.test_units      # expect 34/34
../.venv/bin/python -m sim.tests.test_ticks      # expect 20/20
../.venv/bin/python -m sim.oracle primitives     # expect 97.59%, takes ~5 min
```

## What we are working on: improving M4

**M4 is built and works.** `pipeline/digit_adder.py` → `pipeline/m4-decimal-adder-v2.litematic`.
Two numbers 1–9 on eighteen levers, the sum shown as a decimal number 0–18 on two
seven-segment digits. 100/100 over every input pair, checked straight off the file
against the real glyphs, nothing floating, and pasted and tested in game.

```bash
./.venv/bin/python pipeline/digit_adder.py           # sweep all 100 pairs
./.venv/bin/python pipeline/digit_adder.py --emit    # write the next -vN .litematic
./.venv/bin/python pipeline/analog.py                # the primitives' own self-test
```

The arithmetic is **signal strength, not binary** — seven comparators, because
`15 - ((15 - x) - y)` is `min(15, x + y)` and dust cannot add any other way. The
converter and both digits are lifted whole out of the library.

**What to improve, in order:**

1. **Speed.** 7 to 10.5 seconds to settle. The core still moves values by comparator
   relay at two ticks per hop; `hex_wire()` does the same job in two ticks total and
   already exists. This is the biggest single win and the least risky.
2. **The zero-tick crossover.** `primitives/wiring/build-14` fails in our simulator —
   four of sixteen lamps light regardless of input. It is pure diagonal dust behaviour,
   so a rule we have wrong there is a rule we have wrong everywhere.
3. **Drive the remaining 12 ALU builds.** `verify/alu_probe.py` splits wide builds into
   operands and controls by behaviour. A component whose behaviour is unknown cannot be
   chosen for a task, and `high` confidence has already been wrong twice.
4. **Repeater locking as a bus latch.** See `docs/timing.md`. It solves what padding
   cannot — data-dependent skew — and is the natural way to feed a register.

Lower priority: comparators are the weakest category at 94.4%; four builds oscillate
rather than settling (some are genuine clocks, not failures); the worst builds are
`displays/blank`, `displays/build-02` and `cpu-ep07-branching/build-07`. `docs/roadmap.md`
has the analysis of what getting to 175/175 would actually take, and why it may be the
wrong target.

## The tooling, and what each thing is for

| tool | what it does |
|---|---|
| `worlds/sim/` | the simulator — `settle()` for steady state, `tick()`/`run_until_stable()` for time |
| `worlds/sim/oracle.py` | per-block diff against 175 real builds; the regression that must not move |
| `worlds/signs.py` | recover sign text **and position** from source worlds, and write it back into the `.litematic` |
| `worlds/containers.py` | recover barrel fill levels the same way |
| `verify/make_test_schematic.py` | build a small test case: `decay`, `steps`, `comparator`, `timing` |
| `verify/predict.py` | what the simulator expects a schematic to do |
| `verify/to_commands.py` | `.litematic` → `/setblock` lines; better than pasting under ~50 blocks |
| `verify/drive.py` | drive a build through its inputs and name what each output computes |
| `verify/alu_probe.py` | for wide builds — split levers into operands/controls **by behaviour**, then name the arithmetic per control setting |
| `pipeline/compose.py` | placement, port conversion, routing, `align()`, and both the collision and structural checks |
| `pipeline/analog.py` | signal-strength arithmetic and every wiring primitive, each with its own self-test |
| `pipeline/digit_adder.py` | M4 itself — the decimal adder, and the sweep that checks it |

**The verification loop that works:** build → simulate → `floating()` → predict in writing
→ paste → compare. Every one of the ten in-game tests followed it, and three failures got
through everything except the paste.

## Read this before generating anything

`tasks/lessons.md`. Most entries came from things that passed every simulator check and
still failed — floating repeaters, a repeater facing the wrong way, wire shape wrong on
disk, and a build that pasted showing 7 with every lever off.

**The simulator models signal. Not physics, not appearance, and not the state a block is
saved in.** That last one is the newest and the sharpest: `settle()` recomputes from
scratch and reaches the same answer whatever it starts from, so a build can pass every
sweep and still be wrong the instant it is pasted. `Build.rest()` and `Build.stale()`
now run on every emit.

Anything generated needs a structural check and a state check as well as a behavioural
one, and then a human to look at it.

## Checking a rule against the game

Minecraft is installed on this machine (26.2 and a 26.3 snapshot, no saves yet), but
this project targets **1.18.2**, so do not verify against the installed version.

For reading the rules rather than playing them, there is a decompiled 1.18.2 reference
at `../.mc-reference`, **deliberately outside this repository** — Mojang's code is not
ours to redistribute, so none of it is committed and none of it should be. Only rules
expressed in our own words belong in here.

To rebuild it: take the 1.18.2 entry from Mojang's public version manifest, download
`client.jar` and `client_mappings`, convert the ProGuard mappings to TSRG
(`pg2tsrg.py` is there), remap with SpecialSource and decompile with Vineflower.

It has already settled three rules that had been argued rather than checked, and it
matters more for the tick loop, where scheduling and priority decide the answer.

## Debugging technique that works

All seven simulator bugs were found this way, and staring at single coordinates found
none of them:

- categorise mismatches as **under-** vs **over-powered** — that separates a missing
  source from a spurious one
- **correlate mismatches against adjacent block types** to identify the culprit component
- **print a 2D slice** showing `saved/computed` per cell to see the structure

`sim/lampdiag.py` does the first two for lamps and `sim/probe_lamp.py` does the third
for any cell. Both are worth copying for whatever category is currently worst.

## Things that will otherwise waste your time

- **`gh` flips between two accounts.** This repo is on `Rektoooooo`; pushes fail with a
  403 naming `SebkuceraRSM`. Fix: `gh auth switch --user Rektoooooo`. Commit as
  `Rektoooooo <sebastian.kucera@icloud.com>`, not the RSM work address.
- **PlanetMinecraft is double-blocked** — the user's Wi-Fi filter *and* Cloudflare bot
  protection. Downloads need their phone hotspot and their own browser. Do not try to
  automate it; `worlds/fetch.sh` opens the URLs for them.
- **`facing` on a repeater or comparator points at the INPUT**, not the output. This is
  the single most consequential convention in the simulator and getting it backwards
  costs ~21 points of agreement.
- **Never `mv ~/Downloads/*.zip`** — it sweeps up the user's unrelated files. Move world
  zips by explicit name.
- **The game runs through ModrinthApp, not the vanilla launcher.** Schematics go in
  `~/Library/Application Support/ModrinthApp/profiles/Redstone/schematics/`. Dropping
  them in `~/Library/Application Support/minecraft/` looks right and does nothing.
- **Litematica's paste needs setting up first**, and the defaults are actively
  unhelpful. `executeOperation` ships **unbound** — that alone makes pasting look
  broken. Tool mode cycles with **Left Ctrl + scroll** while holding the tool item (a
  stick), and the paste also needs a placement *selected*, not merely loaded. All of
  this is readable from the mod jar rather than guessable: the defaults live in
  `fi/dy/masa/litematica/config/Hotkeys.class`, and `javap -c` on it pairs each name
  with its default key.
- **For anything under ~50 blocks, skip Litematica and use `/setblock`.**
  `verify/to_commands.py` generates the list. Commands fire block updates, which a
  paste does not always do — and on a redstone test an un-updated paste reads as all
  zeros and looks exactly like a broken model.
- **Renders over ~400k cells are skipped**; one large build produced a 28 MB SVG that
  nothing could open.

## Where the documentation lives

| File | Contents |
|---|---|
| `.handoffs/` | session-by-session state — **read the latest before starting** |
| `README.md` | project overview and toolchain reference |
| `JOURNEY.md` | the step-by-step story, written for a talk, including what went wrong |
| `worlds/sim/README.md` | simulator design, the oracle, and the bugs it caught |
| `worlds/primitives/README.md` | the 195 extracted builds and how far to trust each label |
| `BUILD-PIPELINE-RESEARCH.md` | design work on generating builds — composition vs synthesis |
| `docs/plan-simulator.md` | the approved plan the simulator was built from |
| `docs/timing.md` | **tick delays for every component**, each cross-checked against the decompiled client and measured in game |
| `docs/roadmap.md` | the route to generating builds — M1–M3 done, M4 next |
| `verify/README.md` | the ten in-game tests and what each one pinned down |
| `tasks/lessons.md` | **read before generating anything** — every entry is a real failure |

## House rules for this project

- **Verify, don't assert.** Every documented claim here has been checked against real
  blocks where possible, and three were wrong. If you state a redstone rule, test it.
- **Mark inference as inference.** Sign labels are ground truth; structural guesses are
  not. A structural classifier was benchmarked at 50% useful and 6% actively
  misleading, and was deliberately not shipped as a labeller.
- **Ask before pushing.** Commit freely; confirm before `git push`.
