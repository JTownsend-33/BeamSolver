
import matplotlib.pyplot as plt
from loads import PointLoad, DistributedLoad, TriangularLoad


def plot_shear(x_values, shear_values):

    plt.figure(figsize=(10,5))

    plt.plot(x_values, shear_values)

    zero_points = find_zero_shear_points(
        x_values,
        shear_values
    )

    for point in zero_points:

        plt.scatter(
            point,
            0
        )

        plt.text(
            point,
            0,
            f" V=0 @ {round(point,2)}m"
        )

    plt.xlabel("Position along beam (m)")
    plt.ylabel("Shear Force (N)")
    plt.title("Shear Force Diagram")

    plt.grid(True)

    plt.axhline(0)

    plt.show()


def plot_moment(x_values, moment_values):

    plt.figure(figsize=(10,5))

    plt.plot(x_values, moment_values)

    max_moment = max(moment_values)

    max_index = moment_values.index(max_moment)

    max_x = x_values[max_index]

    plt.scatter(max_x, max_moment)

    plt.text(
        max_x,
        max_moment,
        f" Max Moment = {round(max_moment,2)} Nm"
    )

    plt.xlabel("Position along beam (m)")
    plt.ylabel("Moment (Nm)")
    plt.title("Bending Moment Diagram")

    plt.grid(True)

    plt.axhline(0)

    plt.show()


def find_zero_shear_points(x_values, shear_values):

    zero_points = []

    for i in range(len(shear_values)-1):

        if shear_values[i] * shear_values[i+1] < 0:

            zero_points.append(x_values[i])

    return zero_points


def plot_beam(beam):

    plt.figure(figsize=(10,3))

    # Draw beam
    plt.plot(
        [0, beam.length],
        [0,0],
        linewidth=3
    )

    # Supports
    for support in beam.supports:

        plt.scatter(
            support.position,
            0
        )

        plt.text(
            support.position,
            -0.3,
            type(support).__name__
        )

        plt.text(
            support.position,
            0.3,
            f"{round(support.reaction,1)} N"
        )

    # Point Loads
    for load in beam.loads:

        if isinstance(load, PointLoad):

            plt.arrow(
                load.position,
                1,
                0,
                -0.8,
                head_width=0.2,
                length_includes_head=True
            )

            plt.text(
                load.position,
                1.1,
                f"{load.magnitude} N"
            )

        elif isinstance(load, DistributedLoad):

            x = load.start

            while x <= load.end:
                plt.arrow(
                    x,
                    1,
                    0,
                    -0.7,
                    head_width=0.15,
                    length_includes_head=True
                )

                x += (load.end - load.start) / 10

            plt.text(
                (load.start + load.end) / 2,
                1.2,
                f"{load.intensity} N/m"
            )

        elif isinstance(load, TriangularLoad):

            x = load.start

            while x <= load.end:
                height = (
                        (x - load.start) /
                        (load.end - load.start)
                )

                plt.arrow(
                    x,
                    1,
                    0,
                    -height,
                    head_width=0.15,
                    length_includes_head=True
                )

                x += (load.end - load.start) / 10

    plt.xlim(
        -1,
        beam.length + 1
    )

    plt.ylim(
        -1.5,
        1.5
    )

    plt.axis("off")

    plt.title("Beam Loading Diagram")

    plt.show()
