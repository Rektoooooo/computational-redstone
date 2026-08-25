#!/bin/bash
# Opens each world download in your default browser, a few seconds apart.
# Downloads land wherever your browser puts them - move the .zip files here.
#
# Uses YOUR browser session deliberately: PlanetMinecraft is behind Cloudflare
# bot protection, and that should be respected rather than worked around.

SLUGS=(
  redstone-logic-gates-lrr-episode-3
  redstone-binary-addition-lrr-episode-4
  redstone-binary-subtraction
  combinational-redstone-devices
  pulses-clocks-latches-amp-flip-flops
  sequential-redstone-devices-lrr-8
  redstone-displays-lrr-9
  game-design-lrr-10
  redstone-alus-from-let-s-make-a-computer
  redstone-registers-from-let-s-make-a-computer
  redstone-control-rom-from-let-s-make-a-redstone-computer
  redstone-instruction-memory-from-let-s-make-a-redstone-computer
  redstone-program-counter-from-let-s-make-a-redstone-computer
  redstone-jumping-branching-from-let-s-make-a-redstone-computer
  the-call-stack-from-let-s-make-a-redstone-computer
  data-memory-from-let-s-make-a-redstone-computer
  input-and-output-from-let-s-make-a-redstone-computer
  5hz-8-bit-multiplier
  user-interfaces-from-video
  new-redstone-computer
)

# Just the four highest-value ones:  ./fetch.sh core
if [ "$1" = "core" ]; then
  SLUGS=(
    redstone-binary-addition-lrr-episode-4
    combinational-redstone-devices
    sequential-redstone-devices-lrr-8
    new-redstone-computer
  )
fi

# Everything except the core four, roughly in order of primitive value:
#   ./fetch.sh rest
if [ "$1" = "rest" ]; then
  SLUGS=(
    # CPU components - highest value, each isolated and labelled
    redstone-alus-from-let-s-make-a-computer                       # all 3 ALU designs
    redstone-registers-from-let-s-make-a-computer                  # register file, dual read
    # Core sequential + gate primitives
    pulses-clocks-latches-amp-flip-flops                           # SR/D latch, T flip-flop, clocks
    redstone-logic-gates-lrr-episode-3                             # the atomic gates
    redstone-displays-lrr-9                                        # matrix decoder, 7-segment
    redstone-binary-subtraction                                    # conditional inverters
    # Remaining CPU components
    redstone-control-rom-from-let-s-make-a-redstone-computer
    redstone-instruction-memory-from-let-s-make-a-redstone-computer
    redstone-program-counter-from-let-s-make-a-redstone-computer
    redstone-jumping-branching-from-let-s-make-a-redstone-computer
    the-call-stack-from-let-s-make-a-redstone-computer
    data-memory-from-let-s-make-a-redstone-computer
    input-and-output-from-let-s-make-a-redstone-computer
    # Extras
    5hz-8-bit-multiplier
    user-interfaces-from-video
    game-design-lrr-10
  )
fi

DELAY="${DELAY:-4}"
echo "Opening ${#SLUGS[@]} downloads, ${DELAY}s apart..."
for s in "${SLUGS[@]}"; do
  echo "  -> $s"
  open "https://www.planetminecraft.com/project/$s/download/worldmap/"
  sleep "$DELAY"
done
echo
echo "Done. Move the .zip files into this folder, then:  unzip '*.zip'"
