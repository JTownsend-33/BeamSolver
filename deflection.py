
def calculate_deflection(
    beam,
    x_values,
    moment_values,
    E,
    I
):

    dx = x_values[1] - x_values[0]

    # Calculate curvature
    curvature = []

    for moment in moment_values:

        curvature.append(
            moment / (E * I)
        )

    # Integrate curvature -> slope
    slope = [0]

    for i in range(1, len(curvature)):
        average_curvature = (
                                    curvature[i - 1]
                                    +
                                    curvature[i]
                            ) / 2

        slope.append(
            slope[-1]
            +
            average_curvature * dx
        )

    # Integrate slope -> raw deflection
    raw_deflection = [0]

    for i in range(1, len(slope)):

        raw_deflection.append(
            raw_deflection[-1]
            +
            slope[i-1] * dx
        )

    # Calculate missing initial slope
    initial_slope = (
        -raw_deflection[-1]
        /
        beam.length
    )

    # Apply slope correction
    corrected_slope = []

    for i in range(len(slope)):

        corrected_slope.append(
            slope[i]
            +
            initial_slope
        )

    # Integrate corrected slope -> final deflection
    deflection = [0]

    for i in range(1, len(corrected_slope)):
        average_slope = (
                                corrected_slope[i - 1]
                                +
                                corrected_slope[i]
                        ) / 2

        deflection.append(
            deflection[-1]
            +
            average_slope * dx
        )

    end_error = deflection[-1]

    for i in range(len(deflection)):
        correction = (
                end_error *
                x_values[i] /
                beam.length
        )

        deflection[i] -= correction

    return x_values, deflection
