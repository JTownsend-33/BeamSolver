
from beam import Beam                               # imports definitions from other .py programs
from loads import PointLoad
from loads import DistributedLoad
from loads import TriangularLoad
from supports import PinSupport, RollerSupport
from solver import solve_reactions
from shear import calculate_shear
from plotting import plot_shear
from moment import calculate_moment
from plotting import plot_moment

beam = Beam(12)

beam.add_support(PinSupport(0))
beam.add_support(RollerSupport(12))

beam.add_load(PointLoad(100, 3))
beam.add_load(DistributedLoad(20, 5, 10))
beam.add_load(TriangularLoad(50, 7, 12))


solve_reactions(beam)

x_values, shear_values = calculate_shear(beam)

x_values, moment_values = calculate_moment(
    x_values,
    shear_values
)

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

for x, moment in zip(x_values, moment_values):
    print(f"x = {x:.1f} m   Moment = {moment:.2f} Nm")

plot_shear(x_values, shear_values)
plot_moment(x_values, moment_values)
