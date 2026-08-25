# Structural profiles

Measured features for every harvested build.

## How much to trust this

**`measured` values are facts** — read directly off the blocks. Lever and lamp
counts describe the *test harness* width, ratios and stack period describe the
build itself.

**`candidate` values are weak inferences.** Benchmarked against the 18 builds
whose identity is known from in-world signs, the heuristic produced a useful
candidate **50%** of the time, nothing at all 44%, and something actively
misleading 6%. Treat candidates as leads to check, never as labels.

A sign always beats a guess. Structural inference has already been wrong twice:
a comparator array that looked like a mux was the magnitude comparator, and the
CLE adder was briefly mislabelled a decoder by a lamp-count rule that has since
been removed.


## addition

### `3-ticks-8-bit-cca-by-don` — **labelled**
Signs: 2, 8, 32, 128, 64, 4, 16, 1
258 components, 13×22×10, 17 levers, 25 lamps
Ratios — comparator 0.151, repeater 0.066, torch 0.093, wire 0.523
- tall and narrow — vertical, bit-per-layer construction
- 17 levers — likely two 8-bit inputs
- repeating vertical module every 2 blocks — stacked per-bit design

### `3-ticks-torchless-fearless-8-bit-cca-by` — **labelled**
Signs: 64, 4, 128, 8, 3 ticks, torchless Fearless 8-bit CCA by, 32, 2, 16
299 components, 13×22×12, 17 levers, 25 lamps
Ratios — comparator 0.217, repeater 0.033, torch 0.003, wire 0.512
- tall and narrow — vertical, bit-per-layer construction
- 17 levers — likely two 8-bit inputs
- *candidate:* comparator logic (mux, cancel-tower, or CCA) — comparator-dominant — cancelling is the usual mechanism

### `4-ticks-8-bit-cle` — **labelled**
Signs: 128, 64, 32, 8, 4, 2, 16, 1
646 components, 16×24×24, 17 levers, 26 lamps
Ratios — comparator 0.0, repeater 0.05, torch 0.223, wire 0.633
- tall and narrow — vertical, bit-per-layer construction
- 17 levers — likely two 8-bit inputs
- repeating vertical module every 2 blocks — stacked per-bit design

### `5-ticks-8-bit-cca` — **labelled**
Signs: 1, COUT, CIN, 5 ticks 8-bit CCA, 128, 32, 8, 2
358 components, 21×23×8, 17 levers, 26 lamps
Ratios — comparator 0.115, repeater 0.115, torch 0.05, wire 0.601
- 17 levers — likely two 8-bit inputs

### `build-02` — inferred
Signs: 1, 2, 64, 128, 16, 32, 4, 8
309 components, 18×10×25, 17 levers, 17 lamps
Ratios — comparator 0.0, repeater 0.11, torch 0.233, wire 0.495
- flat and wide — horizontal construction
- 17 levers — likely two 8-bit inputs
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-06` — inferred
172 components, 20×7×23, 9 levers, 13 lamps
Ratios — comparator 0.0, repeater 0.0, torch 0.279, wire 0.593
- flat and wide — horizontal construction
- 9 levers — likely one 8-bit input
- *candidate:* decoder / encoder — torch-dominant with no comparators — matches 'torches on 1s, repeaters on 0s, OR into a torch'

### `build-07` — inferred
146 components, 47×7×17, 2 levers, 3 lamps
Ratios — comparator 0.027, repeater 0.089, torch 0.041, wire 0.808
- flat and wide — horizontal construction
- 2 levers — small input, around 2 bits

### `build-08` — inferred
53 components, 18×7×12, 2 levers, 4 lamps
Ratios — comparator 0.038, repeater 0.113, torch 0.057, wire 0.679
- 2 levers — small input, around 2 bits

### `build-09` — inferred
41 components, 17×7×10, 2 levers, 4 lamps
Ratios — comparator 0.0, repeater 0.0, torch 0.317, wire 0.537
- 2 levers — small input, around 2 bits
- *candidate:* decoder / encoder — torch-dominant with no comparators — matches 'torches on 1s, repeaters on 0s, OR into a torch'

### `yellowbunny-4-digit-hexcca-by` — **labelled**
Signs: YellowBunny 4-digit HexCCA by
262 components, 18×22×9, 0 levers, 5 lamps
Ratios — comparator 0.336, repeater 0.076, torch 0.065, wire 0.42
- *candidate:* comparator logic (mux, cancel-tower, or CCA) — comparator-dominant — cancelling is the usual mechanism


## alus

### `build-00` — inferred
2986 components, 41×24×27, 26 levers, 34 lamps
Ratios — comparator 0.06, repeater 0.159, torch 0.036, wire 0.725
- 26 levers — likely two 8-bit inputs
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-01` — inferred
1100 components, 37×24×26, 27 levers, 35 lamps
Ratios — comparator 0.088, repeater 0.115, torch 0.055, wire 0.685
- 27 levers — likely two 8-bit inputs
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-02` — inferred
853 components, 35×24×23, 26 levers, 34 lamps
Ratios — comparator 0.095, repeater 0.118, torch 0.057, wire 0.659
- 26 levers — likely two 8-bit inputs
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-03` — inferred
776 components, 34×19×15, 96 levers, 144 lamps
Ratios — comparator 0.041, repeater 0.124, torch 0.072, wire 0.454
- 96 levers — likely two 8-bit inputs
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-04` — inferred
638 components, 45×12×27, 18 levers, 22 lamps
Ratios — comparator 0.025, repeater 0.049, torch 0.146, wire 0.718
- 18 levers — likely two 8-bit inputs
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-05` — inferred
576 components, 14×23×23, 21 levers, 29 lamps
Ratios — comparator 0.141, repeater 0.153, torch 0.033, wire 0.587
- tall and narrow — vertical, bit-per-layer construction
- 21 levers — likely two 8-bit inputs
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-06` — inferred
534 components, 13×23×23, 20 levers, 28 lamps
Ratios — comparator 0.137, repeater 0.15, torch 0.034, wire 0.59
- tall and narrow — vertical, bit-per-layer construction
- 20 levers — likely two 8-bit inputs
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-07` — inferred
509 components, 13×23×23, 19 levers, 27 lamps
Ratios — comparator 0.143, repeater 0.141, torch 0.035, wire 0.589
- tall and narrow — vertical, bit-per-layer construction
- 19 levers — likely two 8-bit inputs
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-08` — inferred
481 components, 13×23×25, 17 levers, 25 lamps
Ratios — comparator 0.119, repeater 0.135, torch 0.037, wire 0.622
- tall and narrow — vertical, bit-per-layer construction
- 17 levers — likely two 8-bit inputs
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-09` — inferred
380 components, 22×12×27, 13 levers, 17 lamps
Ratios — comparator 0.042, repeater 0.053, torch 0.166, wire 0.661
- 13 levers — likely one 8-bit input

### `build-10` — inferred
359 components, 22×12×27, 12 levers, 16 lamps
Ratios — comparator 0.045, repeater 0.045, torch 0.175, wire 0.657
- 12 levers — likely one 8-bit input

### `build-11` — inferred
357 components, 8×23×22, 17 levers, 25 lamps
Ratios — comparator 0.115, repeater 0.137, torch 0.073, wire 0.557
- tall and narrow — vertical, bit-per-layer construction
- 17 levers — likely two 8-bit inputs

### `build-12` — inferred
341 components, 8×23×21, 17 levers, 25 lamps
Ratios — comparator 0.12, repeater 0.12, torch 0.053, wire 0.584
- tall and narrow — vertical, bit-per-layer construction
- 17 levers — likely two 8-bit inputs

### `build-13` — inferred
334 components, 22×12×27, 11 levers, 15 lamps
Ratios — comparator 0.048, repeater 0.048, torch 0.174, wire 0.653
- 11 levers — likely one 8-bit input

### `build-14` — inferred
307 components, 9×23×18, 17 levers, 25 lamps
Ratios — comparator 0.134, repeater 0.13, torch 0.059, wire 0.541
- tall and narrow — vertical, bit-per-layer construction
- 17 levers — likely two 8-bit inputs
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-15` — inferred
280 components, 22×11×27, 10 levers, 14 lamps
Ratios — comparator 0.029, repeater 0.043, torch 0.189, wire 0.654
- 10 levers — likely one 8-bit input

### `build-16` — inferred
180 components, 23×10×19, 9 levers, 14 lamps
Ratios — comparator 0.0, repeater 0.0, torch 0.267, wire 0.606
- flat and wide — horizontal construction
- 9 levers — likely one 8-bit input
- *candidate:* decoder / encoder — torch-dominant with no comparators — matches 'torches on 1s, repeaters on 0s, OR into a torch'

### `build-17` — inferred
44 components, 9×8×18, 3 levers, 4 lamps
Ratios — comparator 0.0, repeater 0.0, torch 0.273, wire 0.568
- 3 levers — small input, around 3 bits
- *candidate:* decoder / encoder — torch-dominant with no comparators — matches 'torches on 1s, repeaters on 0s, OR into a torch'


## callstack

### `build-00` — inferred
99782 components, 141×63×119, 0 levers, 0 lamps
Ratios — comparator 0.012, repeater 0.08, torch 0.07, wire 0.832
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-01` — inferred
3464 components, 59×27×22, 11 levers, 21 lamps
Ratios — comparator 0.09, repeater 0.293, torch 0.054, wire 0.551
- 11 levers — likely one 8-bit input
- repeating vertical module every 2 blocks — stacked per-bit design
- *candidate:* register / counter / shift register — repeater-dominant — repeater locks are the memory primitive

### `build-02` — inferred
132 components, 21×9×15, 1 levers, 2 lamps
Ratios — comparator 0.061, repeater 0.144, torch 0.068, wire 0.697
- flat and wide — horizontal construction
- 1 levers — small input, around 1 bits

### `build-03` — inferred
112 components, 19×11×13, 1 levers, 3 lamps
Ratios — comparator 0.107, repeater 0.143, torch 0.134, wire 0.5
- 1 levers — small input, around 1 bits
- repeating vertical module every 3 blocks — stacked per-bit design


## combinational

### `a-gt-b` — **labelled**
Signs: A > B, A == B, A < B
168 components, 15×21×11, 16 levers, 19 lamps
Ratios — comparator 0.143, repeater 0.119, torch 0.012, wire 0.458
- tall and narrow — vertical, bit-per-layer construction
- 16 levers — likely two 8-bit inputs

### `build-00` — inferred
661 components, 40×9×24, 3 levers, 7 lamps
Ratios — comparator 0.0, repeater 0.08, torch 0.097, wire 0.808
- flat and wide — horizontal construction
- 3 levers — small input, around 3 bits

### `build-01` — inferred
300 components, 17×8×50, 7 levers, 13 lamps
Ratios — comparator 0.0, repeater 0.04, torch 0.113, wire 0.78
- flat and wide — horizontal construction
- 7 levers — likely one 8-bit input

### `build-02` — inferred
293 components, 11×14×21, 4 levers, 4 lamps
Ratios — comparator 0.0, repeater 0.096, torch 0.16, wire 0.717
- 4 levers — small input, around 4 bits

### `build-04` — inferred
147 components, 9×12×21, 0 levers, 4 lamps
Ratios — comparator 0.109, repeater 0.177, torch 0.0, wire 0.68
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-05` — inferred
144 components, 15×14×11, 4 levers, 8 lamps
Ratios — comparator 0.0, repeater 0.056, torch 0.083, wire 0.75
- 4 levers — small input, around 4 bits
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-06` — inferred
126 components, 10×13×17, 4 levers, 8 lamps
Ratios — comparator 0.0, repeater 0.159, torch 0.0, wire 0.746
- 4 levers — small input, around 4 bits
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-07` — inferred
116 components, 12×9×16, 4 levers, 8 lamps
Ratios — comparator 0.0, repeater 0.0, torch 0.172, wire 0.724
- 4 levers — small input, around 4 bits
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-08` — inferred
112 components, 18×8×15, 0 levers, 8 lamps
Ratios — comparator 0.0, repeater 0.071, torch 0.107, wire 0.75
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-09` — inferred
98 components, 18×7×8, 0 levers, 14 lamps
Ratios — comparator 0.0, repeater 0.143, torch 0.286, wire 0.286
- *candidate:* decoder / encoder — torch-dominant with no comparators — matches 'torches on 1s, repeaters on 0s, OR into a torch'

### `build-10` — inferred
96 components, 14×12×11, 4 levers, 8 lamps
Ratios — comparator 0.0, repeater 0.083, torch 0.125, wire 0.667
- 4 levers — small input, around 4 bits
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-11` — inferred
92 components, 10×12×13, 4 levers, 8 lamps
Ratios — comparator 0.0, repeater 0.174, torch 0.0, wire 0.696
- 4 levers — small input, around 4 bits
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-12` — inferred
90 components, 16×8×15, 3 levers, 6 lamps
Ratios — comparator 0.0, repeater 0.078, torch 0.111, wire 0.711
- 3 levers — small input, around 3 bits
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-13` — inferred
89 components, 14×10×14, 6 levers, 7 lamps
Ratios — comparator 0.045, repeater 0.09, torch 0.045, wire 0.674
- 6 levers — small input, around 6 bits
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-14` — inferred
88 components, 15×7×14, 4 levers, 5 lamps
Ratios — comparator 0.0, repeater 0.0, torch 0.193, wire 0.705
- 4 levers — small input, around 4 bits

### `build-15` — inferred
81 components, 10×20×6, 0 levers, 16 lamps
Ratios — comparator 0.012, repeater 0.0, torch 0.383, wire 0.198
- tall and narrow — vertical, bit-per-layer construction
- *candidate:* decoder / encoder — torch-dominant with no comparators — matches 'torches on 1s, repeaters on 0s, OR into a torch'

### `build-16` — inferred
74 components, 9×12×14, 3 levers, 7 lamps
Ratios — comparator 0.0, repeater 0.095, torch 0.122, wire 0.649
- 3 levers — small input, around 3 bits

### `build-17` — inferred
73 components, 16×7×12, 4 levers, 7 lamps
Ratios — comparator 0.0, repeater 0.0, torch 0.123, wire 0.726
- 4 levers — small input, around 4 bits

### `build-18` — inferred
51 components, 10×10×12, 0 levers, 4 lamps
Ratios — comparator 0.078, repeater 0.078, torch 0.0, wire 0.765

### `build-19` — inferred
45 components, 14×6×11, 4 levers, 8 lamps
Ratios — comparator 0.067, repeater 0.156, torch 0.0, wire 0.511
- 4 levers — small input, around 4 bits

### `build-20` — inferred
28 components, 12×13×17, 3 levers, 5 lamps
Ratios — comparator 0.071, repeater 0.036, torch 0.107, wire 0.5
- 3 levers — small input, around 3 bits

### `build-21` — inferred
26 components, 12×8×12, 3 levers, 4 lamps
Ratios — comparator 0.077, repeater 0.038, torch 0.115, wire 0.5
- 3 levers — small input, around 3 bits


## cpu-ep04-controlrom

### `build-00` — inferred
7824 components, 64×42×64, 4 levers, 24 lamps
Ratios — comparator 0.075, repeater 0.152, torch 0.057, wire 0.647
- 4 levers — small input, around 4 bits

### `build-01` — inferred
6492 components, 29×38×64, 7 levers, 19 lamps
Ratios — comparator 0.091, repeater 0.168, torch 0.061, wire 0.598
- 7 levers — likely one 8-bit input
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-02` — inferred
4996 components, 27×36×45, 21 levers, 37 lamps
Ratios — comparator 0.099, repeater 0.182, torch 0.074, wire 0.532
- 21 levers — likely two 8-bit inputs

### `build-03` — inferred
829 components, 16×24×26, 16 levers, 30 lamps
Ratios — comparator 0.117, repeater 0.146, torch 0.034, wire 0.648
- tall and narrow — vertical, bit-per-layer construction
- 16 levers — likely two 8-bit inputs
- repeating vertical module every 2 blocks — stacked per-bit design


## cpu-ep05-instrmem

### `build-00` — inferred
92633 components, 135×65×143, 10 levers, 10 lamps
Ratios — comparator 0.008, repeater 0.069, torch 0.072, wire 0.843
- 10 levers — likely one 8-bit input
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-01` — inferred
91995 components, 135×65×143, 10 levers, 10 lamps
Ratios — comparator 0.007, repeater 0.069, torch 0.072, wire 0.843
- 10 levers — likely one 8-bit input
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-02` — inferred
82999 components, 119×61×75, 10 levers, 26 lamps
Ratios — comparator 0.001, repeater 0.061, torch 0.074, wire 0.86
- 10 levers — likely one 8-bit input
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-03` — inferred
31800 components, 116×29×75, 10 levers, 1034 lamps
Ratios — comparator 0.003, repeater 0.122, torch 0.13, wire 0.712
- 10 levers — likely one 8-bit input

### `build-04` — inferred
30829 components, 117×61×75, 10 levers, 26 lamps
Ratios — comparator 0.003, repeater 0.126, torch 0.134, wire 0.735
- 10 levers — likely one 8-bit input

### `build-05` — inferred
7827 components, 64×42×65, 16 levers, 16 lamps
Ratios — comparator 0.075, repeater 0.152, torch 0.057, wire 0.647
- 16 levers — likely two 8-bit inputs

### `build-06` — inferred
7060 components, 262×26×10, 10 levers, 138 lamps
Ratios — comparator 0.0, repeater 0.136, torch 0.082, wire 0.761
- 10 levers — likely one 8-bit input
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-07` — inferred
360 components, 38×14×9, 4 levers, 20 lamps
Ratios — comparator 0.0, repeater 0.111, torch 0.133, wire 0.689
- 4 levers — small input, around 4 bits


## cpu-ep06-progcounter

### `build-00` — inferred
93461 components, 147×65×143, 0 levers, 11 lamps
Ratios — comparator 0.008, repeater 0.07, torch 0.071, wire 0.843
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-01` — inferred
93244 components, 134×65×143, 0 levers, 10 lamps
Ratios — comparator 0.008, repeater 0.069, torch 0.071, wire 0.843
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-02` — inferred
92626 components, 135×65×143, 10 levers, 10 lamps
Ratios — comparator 0.008, repeater 0.069, torch 0.072, wire 0.843
- 10 levers — likely one 8-bit input
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-03` — inferred
614 components, 18×26×19, 0 levers, 10 lamps
Ratios — comparator 0.086, repeater 0.148, torch 0.039, wire 0.708
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-04` — inferred
98 components, 13×23×10, 10 levers, 20 lamps
Ratios — comparator 0.01, repeater 0.214, torch 0.01, wire 0.449
- tall and narrow — vertical, bit-per-layer construction
- 10 levers — likely one 8-bit input
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-05` — inferred
71 components, 9×21×7, 0 levers, 8 lamps
Ratios — comparator 0.014, repeater 0.352, torch 0.113, wire 0.296
- tall and narrow — vertical, bit-per-layer construction
- repeating vertical module every 2 blocks — stacked per-bit design
- *candidate:* register / counter / shift register — repeater-dominant — repeater locks are the memory primitive

### `build-06` — inferred
25 components, 16×6×7, 0 levers, 2 lamps
Ratios — comparator 0.04, repeater 0.48, torch 0.08, wire 0.24
- *candidate:* register / counter / shift register — repeater-dominant — repeater locks are the memory primitive


## cpu-ep07-branching

### `build-00` — inferred
95271 components, 148×67×149, 0 levers, 11 lamps
Ratios — comparator 0.008, repeater 0.07, torch 0.07, wire 0.843
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-01` — inferred
94513 components, 148×66×143, 0 levers, 11 lamps
Ratios — comparator 0.008, repeater 0.07, torch 0.071, wire 0.843
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-02` — inferred
93971 components, 146×65×143, 0 levers, 10 lamps
Ratios — comparator 0.008, repeater 0.07, torch 0.071, wire 0.843
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-03` — inferred
972 components, 27×25×30, 24 levers, 25 lamps
Ratios — comparator 0.105, repeater 0.145, torch 0.046, wire 0.651
- 24 levers — likely two 8-bit inputs
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-04` — inferred
891 components, 22×25×30, 20 levers, 24 lamps
Ratios — comparator 0.11, repeater 0.152, torch 0.037, wire 0.65
- 20 levers — likely two 8-bit inputs

### `build-05` — inferred
889 components, 19×25×30, 22 levers, 24 lamps
Ratios — comparator 0.11, repeater 0.152, torch 0.035, wire 0.649
- 22 levers — likely two 8-bit inputs

### `build-06` — inferred
866 components, 18×24×26, 22 levers, 24 lamps
Ratios — comparator 0.112, repeater 0.15, torch 0.033, wire 0.65
- 22 levers — likely two 8-bit inputs

### `build-07` — inferred
847 components, 18×24×26, 20 levers, 22 lamps
Ratios — comparator 0.115, repeater 0.15, torch 0.034, wire 0.651
- 20 levers — likely two 8-bit inputs

### `build-08` — inferred
42 components, 7×19×9, 8 levers, 9 lamps
Ratios — comparator 0.0, repeater 0.19, torch 0.024, wire 0.357
- tall and narrow — vertical, bit-per-layer construction
- 8 levers — likely one 8-bit input
- repeating vertical module every 2 blocks — stacked per-bit design


## cpu-ep09-datamem

### `build-00` — inferred
143224 components, 141×63×119, 0 levers, 0 lamps
Ratios — comparator 0.037, repeater 0.112, torch 0.075, wire 0.741
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-01` — inferred
99782 components, 141×63×119, 0 levers, 0 lamps
Ratios — comparator 0.012, repeater 0.08, torch 0.07, wire 0.832
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-02` — inferred
42117 components, 73×40×74, 17 levers, 17 lamps
Ratios — comparator 0.098, repeater 0.189, torch 0.091, wire 0.518
- 17 levers — likely two 8-bit inputs

### `build-03` — inferred
12824 components, 69×24×72, 9 levers, 519 lamps
Ratios — comparator 0.0, repeater 0.116, torch 0.12, wire 0.703
- 9 levers — likely one 8-bit input

### `build-04` — inferred
9953 components, 69×22×69, 8 levers, 264 lamps
Ratios — comparator 0.0, repeater 0.145, torch 0.129, wire 0.699
- 8 levers — likely one 8-bit input

### `build-05` — inferred
9186 components, 64×35×23, 8 levers, 20 lamps
Ratios — comparator 0.101, repeater 0.18, torch 0.075, wire 0.537
- 8 levers — likely one 8-bit input

### `build-06` — inferred
4906 components, 41×35×23, 21 levers, 37 lamps
Ratios — comparator 0.1, repeater 0.18, torch 0.075, wire 0.528
- 21 levers — likely two 8-bit inputs


## cpu-ep10-io

### `build-03` — inferred
147291 components, 187×63×141, 0 levers, 0 lamps
Ratios — comparator 0.036, repeater 0.124, torch 0.073, wire 0.732
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-04` — inferred
146484 components, 187×63×141, 0 levers, 0 lamps
Ratios — comparator 0.036, repeater 0.123, torch 0.074, wire 0.733
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-05` — inferred
146321 components, 187×63×141, 0 levers, 0 lamps
Ratios — comparator 0.036, repeater 0.123, torch 0.074, wire 0.732
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-06` — inferred
144093 components, 153×63×154, 0 levers, 41 lamps
Ratios — comparator 0.038, repeater 0.112, torch 0.075, wire 0.738
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-07` — inferred
143844 components, 119×63×145, 0 levers, 256 lamps
Ratios — comparator 0.036, repeater 0.112, torch 0.077, wire 0.738
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-08` — inferred
143224 components, 141×63×119, 0 levers, 0 lamps
Ratios — comparator 0.037, repeater 0.112, torch 0.075, wire 0.741
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-09` — inferred
68599 components, 96×83×45, 10 levers, 4111 lamps
Ratios — comparator 0.091, repeater 0.342, torch 0.087, wire 0.34
- 10 levers — likely one 8-bit input
- *candidate:* register / counter / shift register — repeater-dominant — repeater locks are the memory primitive

### `build-10` — inferred
9531 components, 72×31×47, 5 levers, 158 lamps
Ratios — comparator 0.044, repeater 0.377, torch 0.034, wire 0.483
- 5 levers — small input, around 5 bits
- *candidate:* register / counter / shift register — repeater-dominant — repeater locks are the memory primitive

### `build-11` — inferred
899 components, 23×13×40, 10 levers, 51 lamps
Ratios — comparator 0.334, repeater 0.073, torch 0.019, wire 0.349
- 10 levers — likely one 8-bit input
- *candidate:* comparator logic (mux, cancel-tower, or CCA) — comparator-dominant — cancelling is the usual mechanism

### `build-12` — inferred
832 components, 20×20×13, 64 levers, 256 lamps
Ratios — comparator 0.0, repeater 0.154, torch 0.308, wire 0.154
- 64 levers — likely two 8-bit inputs
- repeating vertical module every 2 blocks — stacked per-bit design
- *candidate:* decoder / encoder — torch-dominant with no comparators — matches 'torches on 1s, repeaters on 0s, OR into a torch'

### `build-13` — inferred
801 components, 20×11×38, 0 levers, 33 lamps
Ratios — comparator 0.375, repeater 0.074, torch 0.014, wire 0.321
- *candidate:* comparator logic (mux, cancel-tower, or CCA) — comparator-dominant — cancelling is the usual mechanism

### `build-14` — inferred
733 components, 16×20×27, 0 levers, 8 lamps
Ratios — comparator 0.067, repeater 0.274, torch 0.011, wire 0.636
- tall and narrow — vertical, bit-per-layer construction
- repeating vertical module every 2 blocks — stacked per-bit design
- *candidate:* register / counter / shift register — repeater-dominant — repeater locks are the memory primitive

### `build-15` — inferred
164 components, 20×22×13, 0 levers, 8 lamps
Ratios — comparator 0.024, repeater 0.104, torch 0.0, wire 0.78
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-16` — inferred
72 components, 8×20×13, 0 levers, 8 lamps
Ratios — comparator 0.111, repeater 0.222, torch 0.0, wire 0.486
- tall and narrow — vertical, bit-per-layer construction
- repeating vertical module every 2 blocks — stacked per-bit design
- *candidate:* register / counter / shift register — repeater-dominant — repeater locks are the memory primitive


## displays

### `blank` — **labelled**
Signs: blank, 1, 7
137 components, 20×11×13, 3 levers, 13 lamps
Ratios — comparator 0.263, repeater 0.036, torch 0.0, wire 0.307
- 3 levers — small input, around 3 bits
- *candidate:* comparator logic (mux, cancel-tower, or CCA) — comparator-dominant — cancelling is the usual mechanism

### `buffer` — **labelled**
Signs: Buffer
1618 components, 20×23×21, 0 levers, 0 lamps
Ratios — comparator 0.04, repeater 0.238, torch 0.243, wire 0.274
- repeating vertical module every 2 blocks — stacked per-bit design
- *candidate:* register / counter / shift register — repeater-dominant — repeater locks are the memory primitive

### `build-02` — inferred
2932 components, 26×28×29, 12 levers, 268 lamps
Ratios — comparator 0.087, repeater 0.155, torch 0.119, wire 0.473
- 12 levers — likely one 8-bit input
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-03` — inferred
Signs: 4, 2, 1, 8
2568 components, 45×13×27, 12 levers, 201 lamps
Ratios — comparator 0.0, repeater 0.055, torch 0.183, wire 0.668
- 12 levers — likely one 8-bit input
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-09` — inferred
1458 components, 18×27×26, 6 levers, 262 lamps
Ratios — comparator 0.0, repeater 0.112, torch 0.251, wire 0.453
- 6 levers — small input, around 6 bits
- repeating vertical module every 2 blocks — stacked per-bit design
- *candidate:* decoder / encoder — torch-dominant with no comparators — matches 'torches on 1s, repeaters on 0s, OR into a torch'

### `build-11` — inferred
Signs: 4, 8, 1, 2
989 components, 46×26×9, 4 levers, 49 lamps
Ratios — comparator 0.0, repeater 0.131, torch 0.065, wire 0.741
- 4 levers — small input, around 4 bits
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-12` — inferred
Signs: 1, 8, 4, 2
838 components, 45×13×11, 4 levers, 49 lamps
Ratios — comparator 0.0, repeater 0.056, torch 0.187, wire 0.683
- 4 levers — small input, around 4 bits
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-14` — inferred
768 components, 11×20×20, 0 levers, 256 lamps
Ratios — comparator 0.0, repeater 0.167, torch 0.333, wire 0.167
- tall and narrow — vertical, bit-per-layer construction
- repeating vertical module every 2 blocks — stacked per-bit design
- *candidate:* decoder / encoder — torch-dominant with no comparators — matches 'torches on 1s, repeaters on 0s, OR into a torch'

### `build-15` — inferred
Signs: 8, 4, 2, 1
647 components, 34×26×9, 4 levers, 49 lamps
Ratios — comparator 0.0, repeater 0.134, torch 0.063, wire 0.706
- 4 levers — small input, around 4 bits
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-16` — inferred
Signs: 1, 2, 4, 8
552 components, 32×13×11, 4 levers, 49 lamps
Ratios — comparator 0.0, repeater 0.058, torch 0.179, wire 0.65
- 4 levers — small input, around 4 bits
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-17` — inferred
Signs: F, E, D, C, B, A, 9, 8
383 components, 36×12×17, 11 levers, 35 lamps
Ratios — comparator 0.305, repeater 0.026, torch 0.042, wire 0.183
- 11 levers — likely one 8-bit input
- *candidate:* comparator logic (mux, cancel-tower, or CCA) — comparator-dominant — cancelling is the usual mechanism

### `build-19` — inferred
205 components, 18×13×8, 0 levers, 13 lamps
Ratios — comparator 0.122, repeater 0.063, torch 0.205, wire 0.395

### `build-21` — inferred
103 components, 6×27×19, 2 levers, 24 lamps
Ratios — comparator 0.0, repeater 0.243, torch 0.039, wire 0.466
- tall and narrow — vertical, bit-per-layer construction
- 2 levers — small input, around 2 bits
- repeating vertical module every 2 blocks — stacked per-bit design
- *candidate:* register / counter / shift register — repeater-dominant — repeater locks are the memory primitive

### `build-22` — inferred
64 components, 13×12×12, 8 levers, 0 lamps
Ratios — comparator 0.125, repeater 0.125, torch 0.062, wire 0.438
- 8 levers — likely one 8-bit input
- repeating vertical module every 2 blocks — stacked per-bit design

### `convert` — **labelled**
Signs: 16, Convert, 32, 64, 128, 4, 8, 1
3156 components, 69×16×37, 8 levers, 198 lamps
Ratios — comparator 0.004, repeater 0.071, torch 0.146, wire 0.704
- 8 levers — likely one 8-bit input

### `data` — **labelled**
Signs: Data, Plot Pixel, Plot All Pixels
2091 components, 24×28×28, 7 levers, 263 lamps
Ratios — comparator 0.037, repeater 0.15, torch 0.18, wire 0.467
- 7 levers — likely one 8-bit input

### `default-0` — **labelled**
Signs: 9, 8, 7, 6, 5, 4, 3, 2
255 components, 30×11×13, 10 levers, 35 lamps
Ratios — comparator 0.263, repeater 0.071, torch 0.027, wire 0.212
- 10 levers — likely one 8-bit input
- *candidate:* comparator logic (mux, cancel-tower, or CCA) — comparator-dominant — cancelling is the usual mechanism

### `play-animation` — **labelled**
Signs: Play Animation
3445 components, 48×23×22, 0 levers, 0 lamps
Ratios — comparator 0.0, repeater 0.264, torch 0.092, wire 0.505
- repeating vertical module every 2 blocks — stacked per-bit design
- *candidate:* register / counter / shift register — repeater-dominant — repeater locks are the memory primitive

### `plot-pixel-2` — **labelled**
Signs: Plot Pixel, Data
2038 components, 22×28×27, 7 levers, 263 lamps
Ratios — comparator 0.034, repeater 0.149, torch 0.184, wire 0.463
- 7 levers — likely one 8-bit input

### `plot-pixel` — **labelled**
Signs: Plot Pixel, Clear
2073 components, 24×28×26, 6 levers, 262 lamps
Ratios — comparator 0.003, repeater 0.146, torch 0.243, wire 0.478
- 6 levers — small input, around 6 bits
- repeating vertical module every 2 blocks — stacked per-bit design

### `reset` — **labelled**
Signs: Reset
817 components, 18×13×22, 0 levers, 52 lamps
Ratios — comparator 0.122, repeater 0.064, torch 0.206, wire 0.397

### `sad` — **labelled**
Signs: Sad, Smiley, Surprised
2055 components, 23×35×25, 3 levers, 259 lamps
Ratios — comparator 0.0, repeater 0.075, torch 0.141, wire 0.656
- 3 levers — small input, around 3 bits

### `surprised` — **labelled**
Signs: Surprised, Sad, Smiley
1373 components, 19×23×22, 3 levers, 259 lamps
Ratios — comparator 0.0, repeater 0.233, torch 0.197, wire 0.348
- 3 levers — small input, around 3 bits
- repeating vertical module every 2 blocks — stacked per-bit design
- *candidate:* register / counter / shift register — repeater-dominant — repeater locks are the memory primitive


## gamedesign

### `build-01` — inferred
1624 components, 32×12×33, 0 levers, 392 lamps
Ratios — comparator 0.0, repeater 0.091, torch 0.181, wire 0.306
- repeating vertical module every 4 blocks — stacked per-bit design

### `build-02` — inferred
835 components, 25×12×25, 0 levers, 200 lamps
Ratios — comparator 0.0, repeater 0.09, torch 0.18, wire 0.311
- repeating vertical module every 4 blocks — stacked per-bit design

### `build-03` — inferred
301 components, 17×12×17, 0 levers, 71 lamps
Ratios — comparator 0.0, repeater 0.09, torch 0.176, wire 0.319
- repeating vertical module every 4 blocks — stacked per-bit design

### `build-04` — inferred
32 components, 8×12×9, 0 levers, 8 lamps
Ratios — comparator 0.0, repeater 0.094, torch 0.156, wire 0.312
- repeating vertical module every 4 blocks — stacked per-bit design

### `reset` — **labelled**
Signs: Reset, X, O
2634 components, 34×36×21, 1 levers, 378 lamps
Ratios — comparator 0.045, repeater 0.123, torch 0.077, wire 0.577
- 1 levers — small input, around 1 bits


## gates

### `build-00` — inferred
117 components, 38×7×14, 12 levers, 18 lamps
Ratios — comparator 0.051, repeater 0.043, torch 0.154, wire 0.496
- flat and wide — horizontal construction
- 12 levers — likely one 8-bit input

### `build-01` — inferred
36 components, 16×6×14, 4 levers, 6 lamps
Ratios — comparator 0.111, repeater 0.028, torch 0.056, wire 0.528
- 4 levers — small input, around 4 bits

### `build-02` — inferred
32 components, 11×7×15, 4 levers, 6 lamps
Ratios — comparator 0.031, repeater 0.0, torch 0.156, wire 0.469
- 4 levers — small input, around 4 bits

### `build-03` — inferred
26 components, 14×7×14, 4 levers, 6 lamps
Ratios — comparator 0.0, repeater 0.038, torch 0.0, wire 0.577
- 4 levers — small input, around 4 bits

### `build-04` — inferred
18 components, 7×6×14, 2 levers, 3 lamps
Ratios — comparator 0.0, repeater 0.0, torch 0.167, wire 0.556
- 2 levers — small input, around 2 bits

### `build-05` — inferred
17 components, 7×6×14, 2 levers, 3 lamps
Ratios — comparator 0.059, repeater 0.0, torch 0.059, wire 0.588
- 2 levers — small input, around 2 bits

### `build-06` — inferred
16 components, 7×6×12, 2 levers, 2 lamps
Ratios — comparator 0.0, repeater 0.0, torch 0.125, wire 0.625
- 2 levers — small input, around 2 bits

### `build-07` — inferred
15 components, 7×6×13, 2 levers, 3 lamps
Ratios — comparator 0.0, repeater 0.133, torch 0.0, wire 0.533
- 2 levers — small input, around 2 bits

### `build-08` — inferred
14 components, 7×6×13, 2 levers, 3 lamps
Ratios — comparator 0.0, repeater 0.143, torch 0.071, wire 0.429
- 2 levers — small input, around 2 bits

### `build-09` — inferred
13 components, 6×6×14, 1 levers, 2 lamps
Ratios — comparator 0.077, repeater 0.077, torch 0.0, wire 0.538
- 1 levers — small input, around 1 bits

### `build-10` — inferred
13 components, 5×7×14, 2 levers, 3 lamps
Ratios — comparator 0.0, repeater 0.077, torch 0.0, wire 0.538
- 2 levers — small input, around 2 bits

### `build-11` — inferred
10 components, 5×6×14, 1 levers, 2 lamps
Ratios — comparator 0.0, repeater 0.0, torch 0.1, wire 0.6
- 1 levers — small input, around 1 bits


## latches

### `5t-output-pulse-10t-period` — **labelled**
Signs: 5t output pulse 10t period, 3t output pulse 10t period, 1t output pulse 2t period, On/Off
54 components, 14×5×22, 4 levers, 4 lamps
Ratios — comparator 0.111, repeater 0.148, torch 0.019, wire 0.574
- flat and wide — horizontal construction
- 4 levers — small input, around 4 bits

### `enable` — **labelled**
Signs: Enable, Data, NOT Output, Output
29 components, 13×7×13, 4 levers, 3 lamps
Ratios — comparator 0.069, repeater 0.069, torch 0.172, wire 0.448
- 4 levers — small input, around 4 bits

### `not-output-2` — **labelled**
Signs: NOT Output, Output, Reset, Set, Enable
31 components, 13×7×11, 1 levers, 4 lamps
Ratios — comparator 0.065, repeater 0.0, torch 0.161, wire 0.548
- 1 levers — small input, around 1 bits

### `not-output-3` — **labelled**
Signs: NOT Output, Output, Reset, Set
28 components, 12×7×10, 0 levers, 2 lamps
Ratios — comparator 0.071, repeater 0.143, torch 0.107, wire 0.607

### `not-output` — **labelled**
Signs: NOT Output, Output, Data, Enable
44 components, 19×7×13, 5 levers, 5 lamps
Ratios — comparator 0.045, repeater 0.045, torch 0.182, wire 0.5
- 5 levers — small input, around 5 bits

### `on-off` — **labelled**
Signs: On/Off
33 components, 11×5×20, 3 levers, 0 lamps
Ratios — comparator 0.152, repeater 0.121, torch 0.03, wire 0.606
- 3 levers — small input, around 3 bits

### `output-2` — **labelled**
Signs: Output, Data
13 components, 10×5×9, 1 levers, 1 lamps
Ratios — comparator 0.0, repeater 0.462, torch 0.077, wire 0.308
- 1 levers — small input, around 1 bits
- *candidate:* register / counter / shift register — repeater-dominant — repeater locks are the memory primitive

### `output` — **labelled**
Signs: Output, Output Toggle the
70 components, 33×7×16, 1 levers, 5 lamps
Ratios — comparator 0.071, repeater 0.186, torch 0.086, wire 0.486
- flat and wide — horizontal construction
- 1 levers — small input, around 1 bits

### `pulse-generator-4-tick-2` — **labelled**
Signs: Pulse Generator 4-Tick, Pulse Generator 2-Tick, Pulse Generator 3-Tick
35 components, 19×7×16, 0 levers, 5 lamps
Ratios — comparator 0.086, repeater 0.143, torch 0.114, wire 0.371

### `pulse-generator-4-tick` — **labelled**
Signs: Pulse Generator 4-Tick, Pulse Generator 3-Tick, Pulse Generator 1-Tick, Pulse Generator 2-Tick
36 components, 18×6×17, 4 levers, 8 lamps
Ratios — comparator 0.0, repeater 0.222, torch 0.0, wire 0.111
- 4 levers — small input, around 4 bits
- *candidate:* register / counter / shift register — repeater-dominant — repeater locks are the memory primitive


## multiplier

### `build-00` — inferred
6415 components, 72×39×41, 129 levers, 129 lamps
Ratios — comparator 0.164, repeater 0.177, torch 0.001, wire 0.504
- 129 levers — likely two 8-bit inputs


## registers

### `build-00` — inferred
4906 components, 23×35×41, 21 levers, 37 lamps
Ratios — comparator 0.1, repeater 0.18, torch 0.075, wire 0.528
- 21 levers — likely two 8-bit inputs

### `build-01` — inferred
4863 components, 23×33×40, 20 levers, 36 lamps
Ratios — comparator 0.1, repeater 0.18, torch 0.075, wire 0.528
- 20 levers — likely two 8-bit inputs

### `build-02` — inferred
2736 components, 16×33×40, 16 levers, 24 lamps
Ratios — comparator 0.09, repeater 0.168, torch 0.073, wire 0.561
- tall and narrow — vertical, bit-per-layer construction
- 16 levers — likely two 8-bit inputs

### `build-03` — inferred
1965 components, 13×26×36, 0 levers, 0 lamps
Ratios — comparator 0.122, repeater 0.183, torch 0.084, wire 0.477
- tall and narrow — vertical, bit-per-layer construction

### `build-04` — inferred
1314 components, 30×27×29, 14 levers, 30 lamps
Ratios — comparator 0.039, repeater 0.15, torch 0.024, wire 0.753
- 14 levers — likely one 8-bit input
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-05` — inferred
1238 components, 9×24×35, 0 levers, 120 lamps
Ratios — comparator 0.097, repeater 0.297, torch 0.024, wire 0.369
- tall and narrow — vertical, bit-per-layer construction
- *candidate:* register / counter / shift register — repeater-dominant — repeater locks are the memory primitive

### `build-06` — inferred
1070 components, 23×27×19, 14 levers, 30 lamps
Ratios — comparator 0.048, repeater 0.165, torch 0.032, wire 0.713
- 14 levers — likely one 8-bit input
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-07` — inferred
606 components, 23×27×18, 12 levers, 20 lamps
Ratios — comparator 0.045, repeater 0.157, torch 0.035, wire 0.71
- 12 levers — likely one 8-bit input
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-08` — inferred
443 components, 14×27×22, 10 levers, 42 lamps
Ratios — comparator 0.0, repeater 0.172, torch 0.027, wire 0.682
- tall and narrow — vertical, bit-per-layer construction
- 10 levers — likely one 8-bit input
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-09` — inferred
408 components, 11×22×22, 8 levers, 40 lamps
Ratios — comparator 0.01, repeater 0.186, torch 0.01, wire 0.667
- tall and narrow — vertical, bit-per-layer construction
- 8 levers — likely one 8-bit input
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-10` — inferred
349 components, 19×27×18, 10 levers, 34 lamps
Ratios — comparator 0.009, repeater 0.175, torch 0.032, wire 0.656
- 10 levers — likely one 8-bit input
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-11` — inferred
74 components, 12×23×8, 9 levers, 16 lamps
Ratios — comparator 0.108, repeater 0.108, torch 0.122, wire 0.216
- tall and narrow — vertical, bit-per-layer construction
- 9 levers — likely one 8-bit input
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-12` — inferred
72 components, 9×20×7, 1 levers, 8 lamps
Ratios — comparator 0.111, repeater 0.333, torch 0.0, wire 0.319
- tall and narrow — vertical, bit-per-layer construction
- 1 levers — small input, around 1 bits
- repeating vertical module every 2 blocks — stacked per-bit design
- *candidate:* register / counter / shift register — repeater-dominant — repeater locks are the memory primitive

### `build-13` — inferred
69 components, 15×8×20, 2 levers, 2 lamps
Ratios — comparator 0.043, repeater 0.101, torch 0.072, wire 0.71
- 2 levers — small input, around 2 bits

### `build-14` — inferred
62 components, 8×22×10, 8 levers, 16 lamps
Ratios — comparator 0.016, repeater 0.274, torch 0.016, wire 0.29
- tall and narrow — vertical, bit-per-layer construction
- 8 levers — likely one 8-bit input
- repeating vertical module every 2 blocks — stacked per-bit design
- *candidate:* register / counter / shift register — repeater-dominant — repeater locks are the memory primitive

### `build-15` — inferred
54 components, 16×8×16, 2 levers, 2 lamps
Ratios — comparator 0.056, repeater 0.093, torch 0.093, wire 0.667
- 2 levers — small input, around 2 bits

### `build-16` — inferred
54 components, 8×8×19, 2 levers, 2 lamps
Ratios — comparator 0.0, repeater 0.074, torch 0.074, wire 0.778
- 2 levers — small input, around 2 bits
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-17` — inferred
43 components, 7×9×22, 0 levers, 4 lamps
Ratios — comparator 0.023, repeater 0.209, torch 0.093, wire 0.558
- flat and wide — horizontal construction
- repeating vertical module every 2 blocks — stacked per-bit design


## sequential

### `add-to-total` — **labelled**
Signs: Add to total
383 components, 14×21×12, 9 levers, 16 lamps
Ratios — comparator 0.104, repeater 0.128, torch 0.06, wire 0.616
- tall and narrow — vertical, bit-per-layer construction
- 9 levers — likely one 8-bit input
- repeating vertical module every 2 blocks — stacked per-bit design

### `build-04` — inferred
238 components, 14×14×28, 2 levers, 8 lamps
Ratios — comparator 0.008, repeater 0.134, torch 0.05, wire 0.697
- 2 levers — small input, around 2 bits

### `build-08` — inferred
144 components, 25×9×15, 0 levers, 0 lamps
Ratios — comparator 0.007, repeater 0.118, torch 0.139, wire 0.736
- flat and wide — horizontal construction

### `build-14` — inferred
32 components, 12×6×13, 1 levers, 5 lamps
Ratios — comparator 0.031, repeater 0.25, torch 0.031, wire 0.5
- 1 levers — small input, around 1 bits
- *candidate:* register / counter / shift register — repeater-dominant — repeater locks are the memory primitive

### `count-2` — **labelled**
Signs: Count
77 components, 13×19×8, 0 levers, 8 lamps
Ratios — comparator 0.013, repeater 0.325, torch 0.104, wire 0.429
- tall and narrow — vertical, bit-per-layer construction
- *candidate:* register / counter / shift register — repeater-dominant — repeater locks are the memory primitive

### `count-3` — **labelled**
Signs: Count
51 components, 14×6×19, 0 levers, 4 lamps
Ratios — comparator 0.02, repeater 0.255, torch 0.078, wire 0.549
- *candidate:* register / counter / shift register — repeater-dominant — repeater locks are the memory primitive

### `count-4` — **labelled**
Signs: Count
41 components, 13×11×8, 0 levers, 4 lamps
Ratios — comparator 0.024, repeater 0.317, torch 0.098, wire 0.439
- *candidate:* register / counter / shift register — repeater-dominant — repeater locks are the memory primitive

### `count` — **labelled**
Signs: Count, Load
169 components, 12×23×8, 8 levers, 16 lamps
Ratios — comparator 0.059, repeater 0.272, torch 0.053, wire 0.361
- tall and narrow — vertical, bit-per-layer construction
- 8 levers — likely one 8-bit input
- repeating vertical module every 2 blocks — stacked per-bit design
- *candidate:* register / counter / shift register — repeater-dominant — repeater locks are the memory primitive

### `load-2` — **labelled**
Signs: Load, Shift Up
178 components, 12×23×11, 8 levers, 16 lamps
Ratios — comparator 0.096, repeater 0.236, torch 0.017, wire 0.506
- tall and narrow — vertical, bit-per-layer construction
- 8 levers — likely one 8-bit input
- repeating vertical module every 2 blocks — stacked per-bit design
- *candidate:* register / counter / shift register — repeater-dominant — repeater locks are the memory primitive

### `load-3` — **labelled**
Signs: Load, Shift Down
178 components, 12×22×11, 8 levers, 16 lamps
Ratios — comparator 0.096, repeater 0.236, torch 0.017, wire 0.506
- tall and narrow — vertical, bit-per-layer construction
- 8 levers — likely one 8-bit input
- *candidate:* register / counter / shift register — repeater-dominant — repeater locks are the memory primitive

### `load` — **labelled**
Signs: Load, Read, Count
255 components, 11×27×52, 16 levers, 36 lamps
Ratios — comparator 0.059, repeater 0.231, torch 0.039, wire 0.451
- tall and narrow — vertical, bit-per-layer construction
- 16 levers — likely two 8-bit inputs
- *candidate:* register / counter / shift register — repeater-dominant — repeater locks are the memory primitive

### `read` — **labelled**
Signs: Read, Write
1296 components, 24×32×13, 11 levers, 21 lamps
Ratios — comparator 0.099, repeater 0.161, torch 0.079, wire 0.512
- 11 levers — likely one 8-bit input

### `shift-down-2` — **labelled**
Signs: Shift Down
89 components, 9×21×10, 1 levers, 9 lamps
Ratios — comparator 0.011, repeater 0.191, torch 0.011, wire 0.663
- tall and narrow — vertical, bit-per-layer construction
- 1 levers — small input, around 1 bits
- repeating vertical module every 2 blocks — stacked per-bit design

### `shift-down` — **labelled**
Signs: Shift Down, Shift Up, Load
345 components, 16×21×13, 8 levers, 16 lamps
Ratios — comparator 0.072, repeater 0.197, torch 0.012, wire 0.641
- tall and narrow — vertical, bit-per-layer construction
- 8 levers — likely one 8-bit input
- repeating vertical module every 2 blocks — stacked per-bit design

### `shift-up` — **labelled**
Signs: Shift Up
89 components, 9×22×10, 1 levers, 9 lamps
Ratios — comparator 0.011, repeater 0.191, torch 0.011, wire 0.663
- tall and narrow — vertical, bit-per-layer construction
- 1 levers — small input, around 1 bits
- repeating vertical module every 2 blocks — stacked per-bit design


## subtraction

### `on-a-b-off-a-plus-b` — **labelled**
Signs: A, B, ON = A - B OFF = A + B
268 components, 23×16×14, 9 levers, 13 lamps
Ratios — comparator 0.108, repeater 0.123, torch 0.037, wire 0.649
- 9 levers — likely one 8-bit input
- repeating vertical module every 2 blocks — stacked per-bit design


## uis

### `1` — **labelled**
Signs: Q, W, E, R, T, 1 !, 2 @, 3 #
2250 components, 38×25×31, 1 levers, 9 lamps
Ratios — comparator 0.01, repeater 0.051, torch 0.092, wire 0.841
- 1 levers — small input, around 1 bits
- repeating vertical module every 2 blocks — stacked per-bit design

### `backspace` — **labelled**
Signs: Backspace, Enter, 15, 14, 13, 12, 11, 10
102 components, 30×10×11, 0 levers, 2 lamps
Ratios — comparator 0.118, repeater 0.02, torch 0.0, wire 0.333
- flat and wide — horizontal construction

### `build-01` — inferred
160 components, 13×7×20, 0 levers, 0 lamps
Ratios — comparator 0.0, repeater 0.062, torch 0.0, wire 0.938

### `build-02` — inferred
116 components, 9×7×21, 0 levers, 0 lamps
Ratios — comparator 0.034, repeater 0.259, torch 0.0, wire 0.707
- flat and wide — horizontal construction
- *candidate:* register / counter / shift register — repeater-dominant — repeater locks are the memory primitive

### `build-04` — inferred
77 components, 17×7×13, 0 levers, 6 lamps
Ratios — comparator 0.0, repeater 0.156, torch 0.312, wire 0.377
- *candidate:* decoder / encoder — torch-dominant with no comparators — matches 'torches on 1s, repeaters on 0s, OR into a torch'

### `build-05` — inferred
38 components, 9×11×8, 0 levers, 0 lamps
Ratios — comparator 0.0, repeater 0.0, torch 0.263, wire 0.737
- repeating vertical module every 2 blocks — stacked per-bit design
- *candidate:* decoder / encoder — torch-dominant with no comparators — matches 'torches on 1s, repeaters on 0s, OR into a torch'

### `build-06` — inferred
37 components, 10×10×9, 0 levers, 7 lamps
Ratios — comparator 0.0, repeater 0.0, torch 0.216, wire 0.378
