# Transcript corpus — computational redstone skill library

**Status: COMPLETE — 32 transcripts, all verified clean.** ✅

Fetched with `yt-dlp` (not the extension — see note below), converted to the same
Markdown shape the extension produces. Every file passed a duplication check:
no backward timestamp jumps anywhere. Total ~504,000 characters.

## What we have

### Logical Redstone Reloaded (10/10) — re-fetched clean
Components · number systems · boolean algebra · adders · subtraction ·
combinational devices · latches & flip-flops · sequential devices · displays · games

> These were the originally doubled files. Regenerated from source rather than
> patched. Originals backed up in the session scratchpad under
> `backup-original-10/`.

### Let's Make a Redstone Computer! (11/11)
Introduction · ALU · register file · machine code & assembly · instruction memory ·
program counter · jumping/branching/flags · call stack · data memory · I/O ·
assembly programming

### Redstone Calculator Tutorial (8/8)
Requirements · inputting to display · BCD→binary · addition & subtraction ·
**multiplication** · **division** · logistics · binary→BCD

### Standalone (3/3)
Redstone user interfaces · best redstone world & tips · sorting algorithms

### Dropped
- `I Made the Fastest Redstone Multiplier!` — 1:08 Short, no narration, captions
  are `[Music]` only. Multiplication is covered by Calculator Part 5.
- `Building your INSANE Redstone ideas!` — showcase reel, not instructional.

## Note on acquisition method

The extension could not be driven from automation, for two reasons:

1. Playwright runs its own isolated Chromium profile, not your Chrome — it hit a
   fresh consent wall and was never signed in, so your installed extension was
   not present.
2. `chrome.commands` shortcuts are handled by the browser process; Playwright
   injects keystrokes into the page renderer, so extension shortcuts never fire.
   Tested and confirmed: pressing Alt+Shift+Y produced no file.

YouTube also now returns an empty body for the caption endpoint and refuses to
populate the transcript panel for unauthenticated automated sessions — so the
extension's own two strategies both fail in that browser regardless.

`yt-dlp` sidesteps all of it. Installed in a throwaway venv in the session
scratchpad; nothing was installed system-wide.

Reusable for future videos:
```
cd <scratchpad>
./ytvenv/bin/python build_transcripts.py <videoId> [<videoId> ...]
```

## Next: build the skill library

Eight skills, one per abstraction layer, descriptions written to be mutually
exclusive so the right one triggers.

| Skill | Fires when | Sources |
|---|---|---|
| `redstone-fundamentals` | components, power, timing, world setup | LRR #1, best-world |
| `redstone-number-systems` | binary, hex, two's complement, BCD | LRR #2, #5, Calc #3, #8 |
| `redstone-logic-gates` | truth tables, boolean algebra, gates | LRR #3 |
| `redstone-arithmetic` | adders, subtractors, multipliers, dividers | LRR #4, #5, Calc #4, #5, #6 |
| `redstone-combinational` | decoders, encoders, mux, comparators | LRR #6 |
| `redstone-sequential` | latches, registers, counters, memory | LRR #7, #8 |
| `redstone-displays` | pixel screens, seven-segment, matrix decoders | LRR #9, Calc #2, UIs |
| `redstone-cpu` | ALU, ISA, program counter, branching, call stack | LMRC #1-11, sorting |
