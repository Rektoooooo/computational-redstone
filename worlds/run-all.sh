#!/bin/bash
# Harvest every world, highest primitive value first so an interruption
# still leaves the important ones done.
cd "$(dirname "$0")"
P=../.venv/bin/python
LOG=harvest-all.log
: > "$LOG"

run () {  # run <world-dir> <out-name>
  echo "=================== $1 ===================" >> "$LOG"
  /usr/bin/time -p $P harvest.py "$1" "primitives/$2" >> "$LOG" 2>&1
  echo "[done $2 @ $(date +%H:%M:%S)]" >> "$LOG"
  echo "$2" >> harvest-done.txt
}

: > harvest-done.txt

run "ALUs by mattbatwings"        alus
run "Registers by mattbatwings"   registers
run "LRR Latches_Flipflops"       latches
run "LRR Logic Gates"             gates
run "LRR Displays"                displays
run "LRR Subtraction"             subtraction
run "Call Stack by mattbatwings"  callstack
run "5hz multiplier by mattbatwings" multiplier
run "CPU Episode 4"               cpu-ep04-controlrom
run "CPU Episode 5"               cpu-ep05-instrmem
run "CPU Episode 6"               cpu-ep06-progcounter
run "CPU Episode 7"               cpu-ep07-branching
run "CPU Episode 9"               cpu-ep09-datamem
run "CPU Episode 10"              cpu-ep10-io
run "UIs by mattbatwings"         uis
run "LRR Game Design"             gamedesign

echo "ALLDONE" >> harvest-done.txt
