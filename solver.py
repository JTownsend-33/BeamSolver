
def solve_reactions(beam):
    pin = beam.supports[0]
    roller = beam.supports[1]

    load = beam.loads[0]

    A = pin.position
    B = roller.position

    P = load.magnitude
    x = load.position

    By = P * (x - A) / (B - A)
    Ay = P - By

    pin.reaction = Ay
    roller.reaction = By
