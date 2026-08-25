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

## Verify it works

```bash
cd worlds
../.venv/bin/python -m sim.tests.test_units      # expect 13/13
../.venv/bin/python -m sim.oracle primitives     # expect ~88%, takes ~5 min
```

## Current state

| | |
|---|---|
| Transcripts | 32, verified clean |
| Skill library | 8 skills, ~2,500 lines, audited against real blocks |
| Extracted builds | 195, of which 43 named from in-world signs |
| Simulator | steady state, **88.09%** per-block agreement, 68/173 builds exact |
| Tick loop | **not built** |

## What to do next

In order. The handoff has fuller detail.

1. **Lamps sit at 65% agreement library-wide** — the biggest single gap, concentrated
   in the display worlds. A pointing-direction fix lifted them to 92% on arithmetic
   builds but moved nothing overall, so the cause is something else and unfound.
2. **Then the tick loop** — delays, scheduling, sequential behaviour. Steady state is
   the foundation and is proven.
3. **Then the behavioural tests**: drive `alus/build-17` through an AND truth table,
   and `addition/3-ticks-8-bit-cca-by-don` with real numbers via its port map. The
   adder is the headline — computing 37+91 from nothing but extracted blocks would
   validate the whole model.
4. **Compare against real Minecraft.** The game outranks the oracle, which is only a
   saved snapshot.

## Debugging technique that works

All three simulator bugs were found this way, and staring at single coordinates found
none of them:

- categorise mismatches as **under-** vs **over-powered** — that separates a missing
  source from a spurious one
- **correlate mismatches against adjacent block types** to identify the culprit component
- **print a 2D slice** showing `saved/computed` per cell to see the structure

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

## House rules for this project

- **Verify, don't assert.** Every documented claim here has been checked against real
  blocks where possible, and three were wrong. If you state a redstone rule, test it.
- **Mark inference as inference.** Sign labels are ground truth; structural guesses are
  not. A structural classifier was benchmarked at 50% useful and 6% actively
  misleading, and was deliberately not shipped as a labeller.
- **Ask before pushing.** Commit freely; confirm before `git push`.
