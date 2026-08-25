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
