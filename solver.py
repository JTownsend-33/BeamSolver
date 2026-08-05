
def solve_reactions(beam):

    pin = beam.supports[0]
    roller = beam.supports[1]

    A = pin.position
    B = roller.position

    total_force = 0
    total_moment = 0

    for load in beam.loads:

        magnitude, position = load.equivalent_load()

        total_force += magnitude
        total_moment += magnitude * (position - A)

    By = total_moment / (B - A)
    Ay = total_force - By

    pin.reaction = Ay
    roller.reaction = By
