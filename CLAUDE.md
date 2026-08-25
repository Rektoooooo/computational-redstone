# Working on this repo

Orientation for a fresh session. Read this first, then `.handoffs/` for the latest
state.

## What this is

Tooling and a knowledge library for **computational redstone** — digital logic and CPUs
built inside Minecraft. Three parts:

1. **8 agent skills** (`redstone-*/`) covering components through CPU architecture
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
| Skill library | 8 skills, ~2,500 lines, audited against real blocks |
| Extracted builds | 195, of which 43 named from in-world signs |
| Simulator | steady state, **97.59%** per-block agreement, **153/175 builds exact** (dust 97.7, repeater 97.8, torch 98.5, comparator 94.4, lamp 96.7) |
| Tick loop | **built** — delays, priority, scheduling; 14 timing tests |
| In-game checks | **9 passed**, incl. the CCA adder computing 37+155=192 and two corrected labels |
| Composition | **M1 + M2 done** — components join, and routes find their way round obstacles |

## Verify it works

```bash
cd worlds
../.venv/bin/python -m sim.tests.test_units      # expect 28/28
../.venv/bin/python -m sim.tests.test_ticks      # expect 14/14
../.venv/bin/python -m sim.oracle primitives     # expect 97.59%, takes ~5 min
```

## What to do next

Steady state, time, verification against the game, and composition are all in place.
`docs/roadmap.md` holds the full picture; the short version is that M1 (join two
components) and M2 (route around an obstacle) are done and confirmed in game.

1. **M3 — timing alignment.** The next real milestone. M2's eight routes were the same
   length, so their delays matched for free. They will not in general, and a bus whose
   bits land on different ticks feeds garbage to anything sequential. The tick loop
   already models delay; this turns that into repeater padding computed per bit.
2. **Drive the remaining ALU builds.** Six of eighteen done, and they turned out to be
   one ALU built up in stages, ending at `build-09` with all six bitwise operations.
   `build-03` (96 levers, needs port-driven handling) and `build-00` are the ones that
   matter most — both still carry `high` confidence, and `high` has already been wrong.
3. **Torch burnout**, if a fast clock ever misbehaves — 8 toggles in a 60-tick window
   burns a torch out for 160 ticks. Only reachable now that time exists.

Lower priority: comparators are the weakest category at 94.4%, four builds oscillate
rather than settling (some are genuine clocks, which have no steady state and are not
failures), and the worst builds are `displays/blank`, `displays/build-02` and
`cpu-ep07-branching/build-07`.

## Read this before generating anything

`tasks/lessons.md`. Four of the five entries came from things that passed every
simulator check and still failed — floating repeaters, a repeater facing the wrong way,
wire shape wrong on disk. **The simulator models signal, not physics, and not
appearance.** Anything generated needs a structural check as well as a behavioural one,
and then a human to look at it.

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

## House rules for this project

- **Verify, don't assert.** Every documented claim here has been checked against real
  blocks where possible, and three were wrong. If you state a redstone rule, test it.
- **Mark inference as inference.** Sign labels are ground truth; structural guesses are
  not. A structural classifier was benchmarked at 50% useful and 6% actively
  misleading, and was deliberately not shipped as a labeller.
- **Ask before pushing.** Commit freely; confirm before `git push`.
