
def calculate_bending_stress(max_moment, section):

    I = section.moment_of_inertia()

    c = section.c()

    stress = max_moment * c / I

    return stress
