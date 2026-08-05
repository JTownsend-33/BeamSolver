
def calculate_moment(x_values, shear_values):

    moment_values = []

    moment = 0

    moment_values.append(moment)

    for i in range(len(x_values)-1):

        dx = x_values[i+1] - x_values[i]

        average_shear = (
            shear_values[i] + shear_values[i+1]
        ) / 2

        moment += average_shear * dx

        moment_values.append(moment)

    return x_values, moment_values