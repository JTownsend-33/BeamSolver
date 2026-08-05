
from loads import PointLoad, DistributedLoad, TriangularLoad


def calculate_shear(beam):

    x_values = []
    shear_values = []

    step = 0.01
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

        # Triangular load
        for load in beam.loads:

            if isinstance(load, TriangularLoad):

                if x < load.start:

                    pass

                elif x <= load.end:

                    length = x - load.start

                    height = load.max_intensity * (
                            length / (load.end - load.start)
                    )

                    shear -= 0.5 * length * height

                else:

                    length = load.end - load.start

                    shear -= 0.5 * length * load.max_intensity

        x_values.append(x)
        shear_values.append(shear)

    return x_values, shear_values
