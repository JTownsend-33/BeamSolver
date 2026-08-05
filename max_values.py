
def find_max_moment(x_values, moment_values):

    max_moment = max(moment_values, key=abs)

    index = moment_values.index(max_moment)

    location = x_values[index]

    return max_moment, location
