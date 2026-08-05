
from beam import Beam                               # imports definitions from other .py programs
from loads import PointLoad
from supports import PinSupport, RollerSupport
from solver import solve_reactions

beam = Beam(15)

beam.add_support(PinSupport(0))
beam.add_support(RollerSupport(15))

beam.add_load(PointLoad(100, 6))
beam.add_load(PointLoad(200, 8))
beam.add_load(PointLoad(50, 12))

solve_reactions(beam)

print("Beam length:", beam.length)

print("\nSupports")
for support in beam.supports:
    print(type(support).__name__, support.position)

print("\nLoads")
for load in beam.loads:
    print(load.magnitude, "N at", load.position, "m")

print("\nReaction Forces")
for support in beam.supports:
    print(type(support).__name__, "=", support.reaction, "N")