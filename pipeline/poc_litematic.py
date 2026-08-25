#!/usr/bin/env python3
"""
Proof of concept: assembly -> .litematic, with a round-trip self-check.

Demonstrates the "composition, not synthesis" thesis on the highest-value case:
instruction memory. Each address is a row; a repeater sits wherever the
instruction has a 1 bit. That is 16 placement decisions per instruction, and
1024 addresses in a full build - exactly the mechanical work humans get wrong.
"""
from litemapy import Region, BlockState

OPCODES = {
    "NOP": 0, "HLT": 1, "ADD": 2, "SUB": 3, "NOR": 4, "AND": 5, "XOR": 6, "RSH": 7,
    "LDI": 8, "ADI": 9, "JMP": 10, "BRH": 11, "CAL": 12, "RET": 13, "LOD": 14, "STR": 15,
}
THREE_REG = {"ADD", "SUB", "NOR", "AND", "XOR"}
REG_IMM = {"LDI", "ADI"}
ADDR_ONLY = {"JMP", "CAL"}


def assemble(source):
    """Tiny subset assembler -> list of 16-bit words. Labels resolved in two passes."""
    lines, labels, pc = [], {}, 0
    for raw in source.strip().splitlines():
        line = raw.split("//")[0].strip()
        if not line:
            continue
        while line.startswith("."):
            label, _, rest = line.partition(" ")
            labels[label] = pc
            line = rest.strip()
            if not line:
                break
        if line:
            lines.append(line)
            pc += 1

    def val(tok):
        if tok.startswith("."):
            return labels[tok]
        if tok.lower().startswith("r"):
            return int(tok[1:])
        return int(tok, 0)

    words = []
    for line in lines:
        parts = line.split()
        op = parts[0].upper()
        if op not in OPCODES:
            raise ValueError(f"unknown opcode: {op}")
        code, args = OPCODES[op], [val(p) for p in parts[1:]]

        if op in THREE_REG:
            a, b, c = (args + [0, 0, 0])[:3]
            word = (code << 12) | (a << 8) | (b << 4) | c
        elif op in REG_IMM:
            a, imm = args[0], args[1] & 0xFF
            word = (code << 12) | (a << 8) | imm
        elif op in ADDR_ONLY:
            word = (code << 12) | (args[0] & 0x3FF)
        elif op == "RSH":
            a, c = args[0], args[1]
            word = (code << 12) | (a << 8) | c
        else:  # NOP, HLT, RET
            word = code << 12
        words.append(word & 0xFFFF)
    return words


# Bit 15 is the leftmost bit; we lay bit 0 at the bottom of the column.
REPEATER = BlockState("minecraft:repeater", facing="east", delay="1", locked="false", powered="false")
GLASS = BlockState("minecraft:glass")
AIR = BlockState("minecraft:air")


def build_region(words):
    """x=0 glass tower (the OR bus), x=1 the repeater column. z = address, y = bit."""
    reg = Region(0, 0, 0, 2, 16, max(1, len(words)))
    for addr, word in enumerate(words):
        for bit in range(16):
            reg[0, bit, addr] = GLASS
            reg[1, bit, addr] = REPEATER if (word >> bit) & 1 else AIR
    return reg


def read_back(reg, count):
    """Reconstruct the words from block data - the self-check."""
    out = []
    for addr in range(count):
        word = 0
        for bit in range(16):
            if reg[1, bit, addr].id == "minecraft:repeater":
                word |= 1 << bit
        out.append(word)
    return out


PROGRAM = """
// Fibonacci, from LMRC #6
LDI r1 1
LDI r2 1
.loop
ADD r1 r2 r3
ADD r2 r3 r4
ADD r3 r4 r5
JMP .done
.done HLT
"""

if __name__ == "__main__":
    words = assemble(PROGRAM)
    print(f"Assembled {len(words)} instructions:\n")
    for i, w in enumerate(words):
        print(f"  {i:3}  {w:016b}  0x{w:04X}")

    reg = build_region(words)
    schem = reg.as_schematic(
        name="instruction-memory",
        author="claude",
        description="Fibonacci program, generated from assembly",
    )
    out = "poc_instruction_memory.litematic"
    schem.save(out)

    # Round-trip verification: reload from disk and reconstruct
    from litemapy import Schematic
    loaded = Schematic.load(out)
    lreg = list(loaded.regions.values())[0]
    recovered = read_back(lreg, len(words))

    print(f"\nSaved {out}")
    print(f"Region: {reg.width}x{reg.height}x{reg.length}, "
          f"{sum(1 for _ in reg.block_positions())} positions")
    print(f"\nRound-trip: {'PASS - blocks match assembly' if recovered == words else 'FAIL'}")
    if recovered != words:
        for i, (a, b) in enumerate(zip(words, recovered)):
            if a != b:
                print(f"  addr {i}: expected {a:016b}, got {b:016b}")
