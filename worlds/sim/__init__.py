"""
A simulator for the computational subset of redstone.

Scope is deliberate: dust, repeater, comparator, torch, lever, button, redstone block
and lamp. Pistons, observers, 0-tick pulses and quasi-connectivity are out, because
computational redstone avoids them by construction - which is exactly what makes this
subset deterministic enough to simulate.

    from sim import Sim
    s = Sim.from_file("primitives/alus/build-17.litematic")
    s.settle()
    s.lamp_states()
"""
from .grid import Grid
from .engine import Sim

__all__ = ["Grid", "Sim"]
