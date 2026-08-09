
from beam import Beam                               # imports definitions from other .py programs
from loads import PointLoad
from loads import DistributedLoad
from loads import TriangularLoad
from supports import PinSupport, RollerSupport
from solver import solve_reactions
from shear import calculate_shear
from plotting import plot_shear
from plotting import plot_beam
from moment import calculate_moment
from plotting import plot_moment
from max_values import find_max_moment
from sections import Rectangle
from stress import calculate_bending_stress
from deflection import calculate_deflection

beam = Beam(10)

beam.add_support(PinSupport(0))
beam.add_support(RollerSupport(10))

beam.add_load(PointLoad(100, 2))

solve_reactions(beam)

x_values, shear_values = calculate_shear(beam)

x_values, moment_values = calculate_moment(
    x_values,
    shear_values

)

max_moment, location = find_max_moment(
    x_values,
    moment_values
)

section = Rectangle(
    width=0.0381,
    height=0.0889
)

print(
    "Maximum Moment:",
    round(max_moment, 2),
    "Nm"
)

print(
    "Location:",
    round(location, 2),
    "m"
)

stress = calculate_bending_stress(
    max_moment,
    section
)

print(
    "Maximum Bending Stress:",
    round(stress / 1e6, 2),
    "MPa"
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

E = 200e9          # Steel (Pa)

I = section.moment_of_inertia()

x_deflection, deflection = calculate_deflection(
    beam,
    x_values,
    moment_values,
    E,
    I
)
print("Start:", deflection[0])
print("End:", deflection[-1])
print("Minimum:", min(deflection))
print("Middle:", deflection[len(deflection)//2])
plot_beam(beam)
plot_shear(x_values, shear_values)
plot_moment(x_values, moment_values)
