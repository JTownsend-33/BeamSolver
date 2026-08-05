
from tkinter import *
from beam import Beam
from supports import PinSupport, RollerSupport
from loads import PointLoad
from solver import solve_reactions

loads = []

window = Tk()

window.title("Beam Solver")
window.geometry("500x500")

def add_point_load():

    force = float(load_force_entry.get())
    position = float(load_position_entry.get())

    load = PointLoad(force, position)

    loads.append(load)

    print("Added:", force, "N at", position, "m")

def solve_beam():

    length = float(length_entry.get())
    pin_location = float(pin_entry.get())
    roller_location = float(roller_entry.get())

    beam = Beam(length)

    beam.add_support(PinSupport(pin_location))
    beam.add_support(RollerSupport(roller_location))

    for load in loads:
        beam.add_load(load)

    solve_reactions(beam)

    result_text = ""

    for support in beam.supports:
        result_text += (
            type(support).__name__
            + ": "
            + str(round(support.reaction, 2))
            + " N\n"
        )

    reaction_label.config(text=result_text)


# Beam Length
length_label = Label(
    window,
    text="Beam Length (m):",
    font=("Arial", 14)
)
length_label.grid(row=0, column=0, padx=10, pady=10)


length_entry = Entry(
    window,
    font=("Arial", 14)
)
length_entry.grid(row=0, column=1)


# Pin Support
pin_label = Label(
    window,
    text="Pin Location (m):",
    font=("Arial", 14)
)
pin_label.grid(row=1, column=0, padx=10, pady=10)


pin_entry = Entry(
    window,
    font=("Arial", 14)
)
pin_entry.grid(row=1, column=1)


# Roller Support
roller_label = Label(
    window,
    text="Roller Location (m):",
    font=("Arial", 14)
)
roller_label.grid(row=2, column=0, padx=10, pady=10)


roller_entry = Entry(
    window,
    font=("Arial", 14)
)
roller_entry.grid(row=2, column=1)

# load force
load_force_label = Label(
    window,
    text="Load Force (N):",
    font=("Arial",14)
)

load_force_label.grid(row=3, column=0, padx=10, pady=10)


load_force_entry = Entry(
    window,
    font=("Arial",14)
)

load_force_entry.grid(row=3, column=1)


load_position_label = Label(
    window,
    text="Load Position (m):",
    font=("Arial",14)
)

load_position_label.grid(row=4, column=0, padx=10, pady=10)


load_position_entry = Entry(
    window,
    font=("Arial",14)
)

load_position_entry.grid(row=4, column=1)

# Add Load Button
add_load_button = Button(
    window,
    text="Add Point Load",
    font=("Arial",14),
    command=add_point_load
)

add_load_button.grid(row=5, column=1)

# Solve Button
solve_button = Button(
    window,
    text="Solve Beam",
    font=("Arial", 14),
    command=solve_beam
)

solve_button.grid(row=6, column=1)


# Results
reaction_label = Label(
    window,
    text="Reactions will appear here",
    font=("Arial", 14)
)

reaction_label.grid(row=7, column=1, padx=10, pady=10)


window.mainloop()