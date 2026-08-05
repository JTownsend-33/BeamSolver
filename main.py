
from beam import Beam                               # imports definitions from other .py programs
from loads import PointLoad
from loads import DistributedLoad
from supports import PinSupport, RollerSupport
from solver import solve_reactions
from shear import calculate_shear
from plotting import plot_shear

beam = Beam(10)

beam.add_support(PinSupport(0))
beam.add_support(RollerSupport(10))

beam.add_load(PointLoad(100, 2))
beam.add_load(PointLoad(50, 4))
beam.add_load(DistributedLoad(100, 6, 10))

solve_reactions(beam)
x_values, shear_values = calculate_shear(beam)

print("Beam length:", beam.length)

print("\nSupports")
for support in beam.supports:
    print(type(support).__name__, support.position)

print("\nLoads")

for load in beam.loads:

    if isinstance(load, PointLoad):
        print(load.magnitude, "N at", load.position, "m")

    elif isinstance(load, DistributedLoad):
        print(
            load.intensity,
            "N/m from",
            load.start,
            "m to",
            load.end,
            "m"
        )

print("\nReaction Forces")
for support in beam.supports:
    print(type(support).__name__, "=", support.reaction, "N")

for x, shear in zip(x_values, shear_values):
    print(f"x = {x:.1f} m     Shear = {shear:.1f} N")

plot_shear(x_values, shear_values)