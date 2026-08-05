
import matplotlib.pyplot as plt


def plot_shear(x_values, shear_values):

    plt.figure(figsize=(10, 5))

    plt.plot(x_values, shear_values)

    plt.xlabel("Position along beam (m)")
    plt.ylabel("Shear Force (N)")
    plt.title("Shear Force Diagram")

    plt.grid(True)

    plt.axhline(0)

    plt.show()