
from loads import PointLoad, DistributedLoad


def calculate_shear(beam):

    x_values = []
    shear_values = []

    step = 0.1
    num_steps = int(beam.length / step)

    for i in range(num_steps + 1):

        x = i * step

        shear = 0

        # Support reactions
        for support in beam.supports:

            if support.position <= x:

                shear += support.reaction

        # Point loads
        for load in beam.loads:

            if isinstance(load, PointLoad):

                if load.position <= x:

                    shear -= load.magnitude

        # Distributed loads
        for load in beam.loads:

            if isinstance(load, DistributedLoad):

                # Before the load starts
                if x < load.start:
                    pass

                # Inside the load
                elif x <= load.end:

                    loaded_length = x - load.start

                    shear -= load.intensity * loaded_length

                # After the load ends
                else:

                    total_length = load.end - load.start

                    shear -= load.intensity * total_length

        x_values.append(x)
        shear_values.append(shear)

    return x_values, shear_values