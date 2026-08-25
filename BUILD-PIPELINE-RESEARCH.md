# Giving Claude the ability to build redstone — research and design

**Date:** 2026-08-25
**Status:** research complete, proof of concept working, not yet built

---

## The reframe

"Give Claude the ability to build redstone" is really **three separate problems**, and
only the first is about file formats. Litematica solves the first one. It does not
touch the other two, and the third is what decides whether this works at all.

| # | Problem | Status |
|---|---|---|
| 1 | **Delivery** — get blocks into the world | **Solved.** Several mature options. |
| 2 | **Generation** — decide where each block goes | The real design decision. |
| 3 | **Verification** — know it works *before* you paste | **The crux.** Without it, blind blueprints. |

Litematica is a good instinct and a fine answer to (1). But if I generate a
schematic I cannot test, I am producing confident-looking garbage — and redstone is
unusually punishing here, because a build can be visually perfect and still fail on
timing or signal strength.

---

## Problem 1 — Delivery

All of these work. Ranked by fit.

| Option | How | Verdict |
|---|---|---|
| **litemapy** → `.litematic` | Python lib, writes Litematica's format directly | **Recommended.** Matches your proposal; Litematica handles paste, material list, and a hologram overlay for survival builds. |
| **mcschematic** → `.schem` | Python lib by Sloimay, Sponge format, WorldEdit `//paste` | **Also recommended.** This is what mattbatwings' own `schematic.py` uses. Proven in exactly this domain. |
| minecraft-mcp | MCP server, Claude Code → WebSocket → Paper plugin / Fabric mod | Direct live control, incl. `get_block_at`. **Targets MC 1.26.1.2 / Java 25** — mismatched with our 1.18.2 target. |
| MCHPRS | Redstone-optimised Rust server with WorldEdit built in | Great *runtime*, poor *interface* — see below. |
| RCON / `/setblock` | Vanilla server commands | Works, but slow and clumsy at scale. |

**Recommendation: emit both formats from one generator.** They are trivially
interchangeable at the data level, and it costs almost nothing to support both.

### Litematica specifics worth knowing

- Schematics go in `.minecraft/schematics` of the active instance
- **Paste is creative-only**; the `executeOperation` hotkey **ships unbound** — you
  must assign it before paste/fill/delete do anything
- **Printer** (auto-build) is off by default: Config → Generic → Tool Enabled, then
  Rendering / Printer → Print Enabled. Creative only.
- **Easy Place mode can get you banned on servers** — it clicks the target's air
  block, which anti-cheat detects. Fine in singleplayer.
- On servers/Realms, lower `commandLimitPerTick` to 5–10 to avoid a packet-spam kick

---

## Problem 2 — Generation: synthesis vs composition

Two fundamentally different approaches, and the choice matters more than the file format.

### Synthesis — compile logic to redstone from scratch

Real prior art exists:

- **V2MC** — full Verilog synthesis to redstone via Yosys, combinational *and*
  sequential, outputs a structure file
- **MinecraftHDL** — Verilog synthesis flow, McGill undergrad project
- **minecraft-hdl** — simpler, combinational only, sum-of-products input, `.schematic` out
- **RedHDL** — the *reverse*: reads redstone out of a world into SystemVerilog

**Why this is the wrong fit for us.** These tools technology-map to naive gate
primitives. The skill library I just built is a catalogue of *specific, hand-optimised
designs* — the carry-cancel adder, the "torches on 1s, repeaters on 0s" decoder, the
staggered two-wide register file. A synthesised 8-bit adder would be a ripple-carry
sprawl: bigger, slower, asynchronous, and nothing like what the library teaches.

Synthesis also produces output nobody can debug. When it fails you have no purchase on it.

### Composition — place and tile known-good components

Keep a library of verified component schematics, then compute placements, offsets,
tiling and wiring programmatically.

**This is what the experts already do by hand.** mattbatwings `//copy`s a CCA and
pastes it eight times, then wires the carries. His `schematic.py` takes machine code
and emits repeaters at computed coordinates. The whole workflow is composition.

**Composition wins here because:**

- Correctness of each primitive is established **once**, not re-derived per build
- The tedious part — offset arithmetic, tiling, bit-order bookkeeping — is exactly
  where humans err and computers excel
- Failures are *legible*: a wrong offset is visible and fixable
- It matches the library's structure directly, one generator per documented design

**The canonical case:** instruction memory is 1024 addresses × 16 bits = **16,384
placement decisions**. No human should do that by hand. It is a pure mechanical
transformation from a list of numbers. That is the sweet spot, and it is precisely
where the existing toolchain already automates.

> **Decision: composition, not synthesis.**

---

## Problem 3 — Verification: the crux

Ranked by value.

### (a) Static linting — cheap, catches most composition bugs

No simulation needed. Analyse the generated block data directly:

- **Signal strength exhaustion** — trace dust runs, flag any exceeding 15 without a
  repeater. This is the single most common redstone bug and it is statically detectable.
- **Glass tower length** — flag towers over 8 layers with no extender
- **Extender support** — flag a backwards-repeater or double-torch extender whose
  backing block is not solid (an error the source material calls out as constantly forgotten)
- **Timing sync** — where several paths must arrive together, compare accumulated
  tick counts and flag mismatches
- **Bit-order sanity** — confirm bit *n* lands on the row it should

Build this first. It is a few hundred lines and it catches the class of bug that
actually occurs when composing verified parts.

### (b) Behavioural simulation — component-level, not block-level

The insight that makes this tractable: **because components are known-good, I do not
need to simulate dust.** I need to simulate the *component graph* — this output feeds
that input, this component costs 3 ticks, does everything arrive on the same edge.

That is ordinary discrete-event simulation, a few hundred lines, and it verifies
composition without reimplementing Minecraft.

### (c) Block-level simulation — feasible, but a project

Worth noting *why* it is even plausible: computational redstone **deliberately
restricts itself** to dust/repeater/comparator/torch, explicitly to avoid the timing
chaos of pistons, observers and 0-tick tricks. That subset is far more deterministic
and position-independent than redstone at large, so a simulator for it is a real
possibility where a general one would not be.

Existing options are weak: **nodestone** (Sloimay, Kotlin) is a standalone redstone
simulator but sits at 1 star and looks early. MCHPRS's **redpiler** is a genuine
high-performance simulator but is welded into a server.

### (d) In-world acceptance test — the ground truth

Paste and run. Always the final word.

**MCHPRS is the ideal runtime for this** — it has `/radvance <ticks>` for
deterministic tick-stepping, `/rtps` for speed control, and WorldEdit `//load` /
`//paste` built in. That is precisely a test harness.

**But it has no RCON and no documented headless mode.** Driving it means a scripted
*client* connection. It has no player auth, so a mineflayer bot issuing chat commands
is plausible — but MCHPRS is a partial protocol implementation, so this needs a spike
before anyone depends on it.

---

## Recommended architecture

```
   component library            generator (Python)
   (verified .litematic    -->  compute offsets,          -->  linter  -->  emit
    primitives, one per          tile, wire, place              (static)     .litematic
    documented design)                                                       .schem
                                        |                                        |
                                        v                                        v
                              behavioural sim                            you paste + run
                              (component graph)                          (ground truth)
```

**Four layers, each independently useful:**

1. **Primitive library** — one verified schematic per design in the skill library.
   Sourced by copying proven community builds, not synthesised.
2. **Generator** — Python. Composes primitives; owns all offset and tiling arithmetic.
3. **Verifier** — linter first, behavioural sim second.
4. **Emitter** — litemapy and mcschematic, same data both ways.

This maps one-to-one onto the skill library: each documented design becomes a
parameterised generator.

---

## Proof of concept — working

Built and tested today. Assembly → `.litematic`, with a round-trip self-check.

```
Assembled 7 instructions:
    0  1000000100000001  0x8101     LDI r1 1
    2  0010000100100011  0x2123     ADD r1 r2 r3
    5  1010000000000110  0xA006     JMP .done
    6  0001000000000000  0x1000     HLT

Saved poc_instruction_memory.litematic
Region: 2x16x7, 224 positions
Round-trip: PASS - blocks match assembly
```

It assembles a subset of the BatPU-2 ISA (with label resolution), emits a real
`.litematic` with a repeater wherever a bit is 1, then **reloads the file from disk
and reconstructs the machine code from block positions** to prove the placement is
correct.

Script: `<scratchpad>/poc_litematic.py`. Note the scratchpad is session-scoped —
move it into the project to keep it.

**What this proves:** delivery works, generation works for the mechanical case, and
self-verification is possible without Minecraft running.
**What it does not prove:** that a *circuit* I compose from primitives will function.
That needs layers 1 and 3.

---

## Environment findings

Checked on this machine:

| | Status |
|---|---|
| `Minecraft.app` | present in `/Applications` |
| `.minecraft` data dir | **does not exist** — Java Edition seemingly never launched here |
| Existing schematics | none found |
| Java | 17.0.18 |
| Node / npm | 23.10.0 / 11.6.0 |
| Rust / cargo | **not installed** — MCHPRS would need it, or a prebuilt binary |
| litemapy / mcschematic | installed and working in the session venv |

**Version tension worth deciding early:** the skill library, the reference designs and
the BatPU-2 computer all target **Java 1.18.2**. `minecraft-mcp` targets **1.26.1.2 /
Java 25**. You cannot have both without either porting the designs or giving up live
MCP control. 1.18.2 is the one the whole ecosystem is standardised on.

---

## Risks and open questions

1. **Primitive orientation and rotation.** Redstone components are directional.
   Composing rotated copies is the most likely source of subtle bugs. The generator
   needs a rigorous rotation model from day one — retrofitting it is painful.
2. **Signal strength across composition boundaries.** Each primitive is verified in
   isolation; connecting them can exhaust strength in the wiring between. The linter
   must model this, not just intra-component runs.
3. **MCHPRS drivability is unproven.** No RCON. The mineflayer-bot route needs a spike
   before committing to it as the test harness.
4. **Where do primitives come from?** Ideally copied from proven world downloads. That
   means an import path: read an existing `.litematic`/`.schem`, extract a region,
   register it as a named primitive. Worth building early.
5. **Nothing is verified in-world yet.** Everything above is file-level correctness.

---

## Suggested phasing

**Phase 1 — mechanical generation** *(smallest useful thing)*
Finish the assembler for the full 16-instruction ISA. Emit instruction memory as
`.litematic` and `.schem`. You paste it into an existing CPU build and confirm it
runs. This is genuinely useful on its own and needs no primitive library.

**Phase 2 — primitive import**
Build the reader: extract a region from an existing schematic and register it as a
named primitive with an anchor point, size and I/O port map.

**Phase 3 — composition + linter**
Generators for the library's designs (register file, decoder, CCA). Static linter for
signal strength, tower length and timing sync.

**Phase 4 — closing the loop**
Either the behavioural simulator, or the MCHPRS spike for in-world testing. Decide
based on what Phase 3 turns out to get wrong.

**Do Phase 1 first regardless.** It is small, immediately useful, and the proof of
concept already covers most of it.

---

## Sources

- [litemapy](https://github.com/SmylerMC/litemapy) · [docs](https://litemapy.readthedocs.io/)
- [mcschematic](https://github.com/Sloimayyy/mcschematic) · [nodestone](https://github.com/Sloimayyy) (redstone simulator, early)
- [MCHPRS](https://github.com/MCHPR/MCHPRS)
- [minecraft-mcp](https://github.com/InventivetalentDev/minecraft-mcp)
- [Litematica wiki — pasting](https://github.com/maruohon/litematica/wiki/Schematic-Pasting) · [reference guide](https://thejud.github.io/litematica-guide/)
- [V2MC](https://github.com/Kenny2github/V2MC) · [MinecraftHDL](https://github.com/itsfrank/MinecraftHDL) · [minecraft-hdl](https://github.com/cemulate/minecraft-hdl) · [RedHDL](https://github.com/ebby-s/RedHDL)
