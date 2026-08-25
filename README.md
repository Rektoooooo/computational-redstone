<img src="docs/logo.png" width="96" align="right" alt="">

# Computational Redstone

Tooling and an agent skill library for **computational redstone** — building digital
logic, arithmetic, memory and full CPUs inside Minecraft.

Three things live here:

1. **An 8-skill knowledge library** (~2,500 lines) covering components through to CPU
   architecture, built from 32 video transcripts and then **audited against the actual
   builds**
2. **A toolchain** that reads Minecraft world files directly — no Minecraft required —
   and extracts redstone builds as reusable `.litematic` components
3. **195 extracted components** from 19 published world downloads, 43 of them
   identified from the author's own in-world signs

Scope is *computational* redstone, not survival: pistons, hoppers and
quasi-connectivity are deliberately out. Java Edition, 1.18.2 conventions.

> **New here, or starting a fresh session? Read [CLAUDE.md](CLAUDE.md)** — setup,
> current state, what to do next, and the traps worth avoiding.

> **[JOURNEY.md](JOURNEY.md) is the step-by-step story** — including the bugs, the wrong
> turns, and the three documentation errors that only surfaced once we had real blocks
> to check against. Start there if you want the narrative rather than the reference.

---

## The skill library

Eight skills, one per abstraction layer.

| Skill | Covers |
|---|---|
| `redstone-fundamentals` | components, soft/hard power, glass towers, ticks, tooling |
| `redstone-number-systems` | binary, hex, two's complement, BCD, double dabble |
| `redstone-logic-gates` | boolean algebra, gate construction, bitwise ops |
| `redstone-arithmetic` | adders, carry-cancel adder, multipliers, dividers |
| `redstone-combinational` | decoders, encoders, mux/demux, comparators |
| `redstone-sequential` | latches, registers, counters, shift registers, clocks |
| `redstone-displays` | pixel screens, seven-segment, buffers, UI |
| `redstone-cpu` | ALU, ISA, program counter, flags, call stack, I/O, assembly |

Read bottom-up; `redstone-cpu` draws on all the others.

**Install** (Claude Code):
```bash
for d in redstone-*/; do ln -s "$PWD/$d" ~/.claude/skills/; done
```

---

## The toolchain

```bash
python3 -m venv .venv && ./.venv/bin/pip install anvil-parser2 litemapy mcschematic
cd worlds && unzip '*.zip'          # restore the worlds from the committed archives
```

| Tool | What it does |
|---|---|
| `worlds/extract.py survey <world>` | locate every build: coordinates, y-range, sign labels |
| `worlds/extract.py probe <world> <cx> <cz>` | per-layer breakdown of one chunk |
| `worlds/extract.py extract <world> x1 y1 z1 x2 y2 z2 <name>` | pull a bounding box |
| `worlds/harvest.py <world> <out>` | bulk-extract every build, auto-named from signs |
| `worlds/profile.py` | add measured structural features to every manifest |
| `worlds/portmap.py` | derive I/O port maps — levers/buttons are inputs, lamps/trapdoors outputs |
| `worlds/sim/` | **redstone simulator** — solves circuits without Minecraft; `python -m sim.oracle primitives` |
| `worlds/containers.py` | recover container fill levels from source worlds into manifests |
| `worlds/signs.py` | recover sign text **and position**, and write it back into the `.litematic` so pasted signs read |
| `worlds/render_png.py` | render a build as layer-by-layer plates using **real Minecraft textures** |
| `worlds/render.py` | the earlier SVG renderer (vector, but slow to display at scale) |
| `worlds/fetch.sh [core\|rest]` | open the source world downloads in your browser |
| `pipeline/poc_litematic.py` | assembly → `.litematic`, with round-trip verification |

Everything is read-only against the worlds. Nothing is written back.

---

## The extracted components

**195 builds** in `worlds/primitives/`, indexed by `MASTER-INDEX.json`, with structural
detail in `PROFILES.md`. Each has a `.litematic` and a `.manifest.json` recording origin,
size, sign labels and full block census.

Highlights, all named from in-world signs:

- **Adders** — five designs with their authors' own tick counts: 3-tick CCA, 3-tick
  torchless, 5-tick CCA, 4-tick CLE, hex CCA
- **Sequential** — register file, accumulator, bidirectional shift register, four counters
- **Latches and timing** — SR latches, gated latch, 2/3/4-tick pulse generators, a clock
- **Displays** — frame buffer, plot-pixel, animation driver, the LRR #9 image display
- **Arithmetic** — the adder/subtractor toggle (`ON = A − B  OFF = A + B`)

### Reliability

| Source | Trust |
|---|---|
| Sign labels | reliable — the author's own words |
| Measured features | reliable — read off the blocks |
| `candidate` guesses in `PROFILES.md` | **weak** — benchmarked at 50% useful, 6% actively misleading |

Structural inference has been wrong twice. It is kept, clearly marked, because leads are
useful; it is not used for labelling.

---

## What this does not do yet

- **152 of 195 builds are unlabelled.** The 18 ALU builds — the most valuable for CPU
  work — have **zero** signs and need identifying in-game.
- **Bit ordering is now measured wherever the author labelled a port**, and pasted
  signs read again. `signs.py` recovers sign text *and position* from the source
  worlds and embeds it back into the `.litematic` as block entities, so the
  `[1][2][4]…[128]` labels give the real ordering instead of `portmap.py` guessing
  "ascending y", and they are legible in game instead of pasting blank. 95 recovered,
  86 embedded — **only for worlds that have been unzipped**, so most builds still have
  neither. Where a port has no signs, ordering is still inferred; check before wiring.
- **Only two circuits have been checked in the real game**, not whole builds. Both
  passed exactly — see [`verify/`](verify/) — and one of them confirmed the asymmetric
  dust-stepping rule that the largest simulator correction rests on. Block-level
  fidelity round-trips correctly, but no *extracted* build has been pasted back and
  driven yet.
- **The simulator solves steady state at 97.6% per-block agreement** across 175 real
  builds, with 153 of them reproducing exactly, and now has a **tick loop** — delays,
  priority and scheduling — so sequential circuits run in time. The timing rules are
  checked against the game's own, but nothing has yet been driven through a whole real
  build, which is the next step. See [`worlds/sim/`](worlds/sim/).

See [BUILD-PIPELINE-RESEARCH.md](BUILD-PIPELINE-RESEARCH.md) for the design work behind
generating builds programmatically — including why **composition beats synthesis** here,
and why verification is the hard part rather than file formats.

---

## Credit

All source material — 20 world downloads and 32 video transcripts — is the work of
**[mattbatwings](https://www.youtube.com/@mattbatwings)**:

- [Logical Redstone Reloaded](https://www.youtube.com/playlist?list=PL5LiOvrbVo8keeEWRZVaHfprU4zQTCsV4) — components through displays
- [Let's Make a Redstone Computer!](https://www.youtube.com/playlist?list=PL5LiOvrbVo8nPTtdXAdSmDWzu85zzdgRT) — the full CPU curriculum
- [Redstone Calculator Tutorial](https://www.youtube.com/playlist?list=PL5LiOvrbVo8kDJ-wJu7l-lIc97yaZo96n) — multiplication, division, BCD
- [BatPU-2](https://github.com/mattbatwings/BatPU-2) — the computer, assembler and ISA

Individual builds also credit their designers where the signs name them — Don, Fearless,
q2ck, YellowBunny.

This repository analyses and indexes published work. It is not a substitute for the
series — go and watch it.

Block textures in the rendered plates are from mattbatwings'
[MattPack](https://modrinth.com/resourcepack/mattpack) resource pack.

Tooling built on [anvil-parser2](https://github.com/0xTiger/anvil-parser2),
[litemapy](https://github.com/SmylerMC/litemapy),
[mcschematic](https://github.com/Sloimayyy/mcschematic) and
[yt-dlp](https://github.com/yt-dlp/yt-dlp).
