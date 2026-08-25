# How this was built, step by step

A working log of the project, written for a talk. Each step has what we did, what went
wrong, and what the lesson was. The failures are more interesting than the successes,
so they are kept in.

---

## Step 0 — The question

> "Research Minecraft redstone so you know how it works."

The first useful discovery was that **redstone is two separate disciplines**, and
almost every guide conflates them:

| | Survival redstone | Computational redstone |
|---|---|---|
| Goal | farms, doors, contraptions | digital logic, CPUs |
| Components | pistons, hoppers, observers, dust | **dust, repeater, comparator, torch only** |
| Exploits | quasi-connectivity, 0-tick, BUD | deliberately avoided |
| Edition | Java and Bedrock differ hugely | Java only |

Computational redstone *deliberately restricts itself* to four components, precisely
to avoid the timing chaos of pistons and observers. That restriction is what makes the
whole field tractable — and, much later, what makes simulating it plausible.

**Lesson:** scope the domain before researching it. "Redstone" was two questions.

---

## Step 1 — A bug hiding a bug

The source material was 10 YouTube transcripts saved by a Chrome extension. Every one
contained the video **twice**.

Rather than assume, we measured. All ten had exactly one point where the timestamp
jumped backwards, at almost precisely the midpoint:

```
The Basics of Redstone - LRR #1.md      96 chunks, backward jump at 48
Redstone Displays - LRR #9.md          136 chunks, backward jump at 68
```

**Root cause:** the extension queried `document.querySelectorAll('ytd-transcript-segment-renderer')`
document-wide. YouTube leaves the *previous* video's panel in the DOM after in-page
navigation, so a watch page holds **two** transcript panels. Confirmed live:

```
ytd-transcript-renderer:              2
ytd-transcript-segment-list-renderer: 2
```

**The second bug is the interesting one.** The duplicate should have obviously restarted
at `[0:00]`. It didn't — it restarted mid-sentence at `[0:08]`. Because the chunker did:

```js
const isTooOld = segment.start - current.start > CHUNK_MAX_SECONDS;
```

When time runs backwards that subtraction goes **negative**, so the guard never fired.
The chunker glued the end of the video onto the beginning of the repeat and kept going.
One bug concealed the other.

**Lesson worth stating in a talk:** *a subtraction used as a comparison silently inverts
its meaning when the inputs go out of order.* Any `a - b > limit` guard needs an answer
for "what if `b > a`?"

Fixed with three changes, plus a test that loads the real `background.js` in a Node VM
so it cannot drift from the shipped code. 11 checks, all passing.

---

## Step 2 — Building a corpus properly

We needed the rest of the series. The obvious route — drive the fixed extension with
browser automation — **does not work**, for two independent reasons worth knowing:

1. Playwright runs its own isolated Chromium, not your Chrome. It hit a fresh consent
   wall and was never signed in, so the installed extension was simply absent.
2. Even if it were present, `chrome.commands` shortcuts are handled by the **browser
   process**. Playwright injects keystrokes into the **page renderer**. Extension
   shortcuts never see them.

Tested rather than assumed: counted files, pressed `Alt+Shift+Y`, counted again. No change.

Moot anyway — YouTube now returns an **empty body** for the caption endpoint and refuses
to populate the transcript panel for unauthenticated automated sessions. Both of the
extension's strategies fail in that browser regardless.

`yt-dlp` sidesteps all of it. We wrote a converter mirroring the extension exactly (same
chunking, header, filename sanitising, dedupe) so output is indistinguishable.

**Result: 32 transcripts, ~504,000 characters, all verified clean.** The original 10 were
re-fetched rather than patched.

Reading the raw `json3` also settled an open question: ASR captions contain `aAppend: 1`
events holding only `'\n'` — roll-up newline markers, not duplicated text.

**Lesson:** when automation fights a system, check whether a purpose-built tool already
solved it. Also: prove a fix on one item before running it on twenty.

---

## Step 3 — Eight skills from 32 transcripts

Read all 32 in full, then built a library split by abstraction layer:

```
fundamentals -> number-systems -> logic-gates -> arithmetic
                                              -> combinational -> sequential
                                                               -> displays -> cpu
```

A known weakness of splitting by *layer* rather than by *task* is that descriptions
compete at trigger time. We measured it: **7 terms genuinely overlap** (`decoder`,
`register`, `comparator`, `counter`, `binary`, `shift`, `two's complement`). Mitigated
by writing every description around a distinct task verb plus an explicit
`DO NOT TRIGGER` clause naming the sibling skill.

The worst offender is `comparator` — the *redstone comparator* (a component) and a
*magnitude comparator* (a circuit) are different things with the same name.

---

## Step 4 — "Can you actually build it?"

The proposal was Litematica. The useful reframe: **that is three problems, and Litematica
solves one.**

| | Problem | Status |
|---|---|---|
| 1 | Delivery — get blocks into the world | solved, many options |
| 2 | Generation — decide where each block goes | the design decision |
| 3 | Verification — know it works *before* pasting | the crux |

### The central decision: composition, not synthesis

Synthesis (compile logic → redstone) has real prior art — V2MC does full Verilog via
Yosys. **It is the wrong fit**, because it technology-maps to naive gate primitives. A
synthesised 8-bit adder is a ripple-carry sprawl; the community's carry-cancel adder is
smaller, faster, synchronous, and completely different in structure. Synthesis also
produces output nobody can debug.

**Composition** — placing and tiling known-good components — is what experts already do
by hand. Correctness of each primitive is established *once*. The tedious part, offset
arithmetic and tiling, is exactly where humans err and computers do not.

The clinching case: instruction memory is 1024 addresses × 16 bits = **16,384 placement
decisions**. Nobody should do that by hand.

### Proof of concept

Assembly → `.litematic`, with a round-trip self-check:

```
    0  1000000100000001  0x8101     LDI r1 1
    2  0010000100100011  0x2123     ADD r1 r2 r3
    5  1010000000000110  0xA006     JMP .done

Round-trip: PASS - blocks match assembly
```

It emits a repeater wherever a bit is 1, then **reloads the file from disk and
reconstructs the machine code from block positions**. Verification without Minecraft.

---

## Step 5 — A network detective story

The primitives had to come from mattbatwings' published world downloads. PlanetMinecraft
was blocked. Switching to a phone hotspot appeared to fail — but the responses were
**byte-identical** (69,740 b, same title) across two different networks, which ruled out
the connection entirely.

Forcing traffic over each interface separately told the real story:

| Route | Result |
|---|---|
| Wi-Fi (`en0`) | 403, 69,740 b — **"Blocked site"** = network content filter |
| Hotspot (`en19`) | 403, 5,778 b — **"Cloudflare"** = PlanetMinecraft's own bot protection |
| Control (github via `en19`) | **HTTP 200** |

Two different blockers. The hotspot beat the first; the second is a control the site
deliberately deployed, so we stopped rather than engineered around it.

The useful output was the **direct download URL pattern**, which turns twenty downloads
into a two-minute job in a normal browser:

```
planetminecraft.com/project/<slug>/download/worldmap/
```

**Lesson:** identical failures across different networks means the failure is not the
network. And when you hit deliberate protection, the answer is usually a different
route, not a harder push.

---

## Step 6 — Reading Minecraft worlds directly

`anvil-parser2` reads `.mca` region files with **no Minecraft required**. Three tools:

- `survey` — locate builds, y-ranges, sign labels
- `probe` — per-layer breakdown of one chunk
- `harvest` — bulk-extract every build

Two details that mattered:

**Block properties survive.** Verified by save/reload round trip — repeater `facing`,
`delay`, `locked`; comparator `mode`; wire connection shapes. Without those a primitive
looks right and does nothing.

**Coordinates were verified, not assumed.** `stream_chunk()` yields 384 layers × 256,
y-major, from y=−64. `probe --verify` cross-checks against `get_block`. It passes.

### The best discovery: the builds are signed

mattbatwings labels his builds in-world, and the signs are readable from the NBT (under
`block_entities` in 1.18, not `TileEntities`).

That immediately **corrected us**. A build with three comparators across six stacked
layers looked like a multiplexer. The sign said:

```
[A > B]  [A == B]  [A < B]
```

A magnitude comparator. Structural inference is a decent heuristic; the author's own
label is ground truth.

---

## Step 7 — Clustering, and getting it wrong first

The first harvest clustered **adjacent chunks**. It merged everything, because these
worlds lay builds out in tightly-spaced rows — one "build" came out 301 blocks long
containing a dozen devices.

Fix: cluster on **spatial proximity** instead — voxelise to 4-block cells and flood-fill.
Builds separated by a real gap split apart.

| | Chunk clustering | Spatial clustering |
|---|---|---|
| Addition | 6 builds | **10** |
| Combinational | 9 builds | **22** |
| Bounding box | 32×20×16 | **13×22×12** |

### And a threshold bug

Logic Gates returned 3 builds. Latches returned 3. Both implausible — LRR #3 covers
seven gate types.

The per-chunk minimum of 20 components was **eating the small builds**. A logic gate is
a torch and some dust, perhaps 10 components. Re-running at `--min 4`:

| | at `--min 20` | at `--min 4` |
|---|---|---|
| Logic Gates | 3 | **12** |
| Latches | 3 | **8**, and 10 sign labels that were missed entirely |

**Lesson:** if a scan returns implausibly little, suspect your filter before concluding
the data is sparse.

---

## Step 8 — Ground truth auditing the documentation

**195 builds harvested from 19 worlds, 43 named from signs.** With real blocks in hand,
the skill library could be checked against reality.

Most of it held:

| Claim | Evidence | Verdict |
|---|---|---|
| ICA "uses pistons to block carry propagation" | **7 sticky pistons**, one per carry boundary | correct |
| CCAs are "completely pistonless" | **0 pistons** in all three | correct |
| CLE "uses glass towers to combine carries" | 96 glass, 113 torches, 0 comparators | correct |
| ICA horizontal, CCA vertical | ICA is **8** tall, CCAs are 20–21 | correct |

Three things were wrong or incomplete:

1. **"Torchless" CCA has one torch, not zero.** Checked whether it was extraction
   overspill — it is not; the torch sits inside the build next to the comparator mass.
   The name is the community's, not a spec. (It does carry 65 comparators against 39,
   so the reliability trade is real.)
2. **The ALU has six control signals, not five.** *Computer v2*'s ALU is signed
   `Right Shift · Flood Carry · Carry In · OR · Invert A · Invert B`. Right shift is a
   control bit, not separate hardware.
3. **NOR=4 and AND=5 confirmed.** Previously flagged as inferred, because the videos
   never state it. The control ROM carries a sign per row in opcode order:
   `nop add sub nor and xor rsh ldi adi jmp brh cal ret lod str`.

The full 22-line control map also revealed two things the videos simplify: destination
select is *three*-way (`dest A/B/C`, because `LOD` writes to register B), and write-back
source is three-way too (`ir data mem / ir alu / ir imm`).

**Lesson:** documentation derived from a video is a claim. Documentation checked against
the artefact is a fact. The gap between them was three errors in ~2,500 lines.

---

## Step 9 — The classifier we deliberately did not ship

152 of 195 builds are unlabelled. The obvious move is to classify them by component
ratios. We built that — and then benchmarked it against the 18 builds whose identity was
already known from signs:

```
on 18 known builds:  9 useful, 8 no-candidate, 1 MISLEADING
right about 50% of the time, actively wrong 6%
```

It called the **CLE adder** a "26-output decoder", because a rule was reading the *test
rig's* output lamps as if they were decoder outputs.

A classifier that is confidently wrong 6% of the time is **worse than none** for
labelling primitives, because a bad label propagates into everything built on top of it.
So the rule was deleted, the remaining guesses were demoted to clearly-marked "weak
inferences", and the *measured* facts — size, census, ratios, stack period — were kept,
because those are read directly off the blocks and cannot be wrong.

**The lesson worth ending a talk on:** benchmark your heuristic against known answers
before you trust it. Fifty percent sounds useful until you notice the six percent that
is confidently wrong, and that a wrong label is worse than a missing one.

---

## Where it stands

| Built | Status |
|---|---|
| 32-transcript corpus | complete, verified clean |
| 8-skill library, ~2,500 lines | complete, audited against ground truth |
| Extension fix | complete, tested |
| World extraction toolchain | complete, verified |
| **195 primitives, 43 named** | extracted |
| Assembly → `.litematic` PoC | working, self-verifying |

**Open:**
- 152 builds unlabelled; the 18 ALU builds have **zero signs** and are the most valuable
- **I/O port maps** — the real blocker for programmatic wiring
- Nothing has been pasted back into Minecraft and tested; fidelity is verified at block
  level only

---

## Credit

Every world download, and all 32 transcripts, are the work of
**[mattbatwings](https://www.youtube.com/@mattbatwings)** — the *Logical Redstone
Reloaded*, *Let's Make a Redstone Computer* and *Redstone Calculator* series, plus the
[BatPU-2](https://github.com/mattbatwings/BatPU-2) computer. This project analyses and
indexes his published work; it does not replace it. Go and watch the series.
