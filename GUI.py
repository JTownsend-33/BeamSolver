
from tkinter import *
from beam import Beam
from supports import PinSupport, RollerSupport
from loads import PointLoad, DistributedLoad
from solver import solve_reactions


# Stores all loads before solving
loads = []


window = Tk()

window.title("Beam Solver")
window.geometry("700x700")


# ---------------- FUNCTIONS ----------------

def show_loads():

    text = "Current Loads:\n"

    for load in loads:

        if isinstance(load, PointLoad):

            text += (
                f"Point Load: {load.magnitude} N "
                f"at {load.position} m\n"
            )

        elif isinstance(load, DistributedLoad):

            text += (
                f"UDL: {load.intensity} N/m "
                f"from {load.start} to {load.end} m\n"
            )

    load_display.config(text=text)


def add_point_load():

    force = float(load_force_entry.get())
    position = float(load_position_entry.get())

    load = PointLoad(force, position)

    loads.append(load)

    print("Added:", force, "N at", position, "m")

    show_loads()


def add_distributed_load():

    magnitude = float(udl_force_entry.get())
    start = float(udl_start_entry.get())
    end = float(udl_end_entry.get())

    load = DistributedLoad(
        magnitude,
        start,
        end
    )

    loads.append(load)

    print(
        "Added UDL:",
        magnitude,
        "N/m from",
        start,
        "to",
        end
    )

    show_loads()


def remove_last_load():

    if len(loads) > 0:

        loads.pop()

        show_loads()


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


    result_text = "Reactions:\n"

    for support in beam.supports:

        result_text += (
            type(support).__name__
            + ": "
            + str(round(support.reaction, 2))
            + " N\n"
        )

    reaction_label.config(text=result_text)



# ---------------- BEAM INPUT ----------------


length_label = Label(
    window,
    text="Beam Length (m):",
    font=("Arial",14)
)

length_label.grid(row=0,column=0,padx=10,pady=10)


length_entry = Entry(
    window,
    font=("Arial",14)
)

length_entry.grid(row=0,column=1)



pin_label = Label(
    window,
    text="Pin Location (m):",
    font=("Arial",14)
)

pin_label.grid(row=1,column=0,padx=10,pady=10)


pin_entry = Entry(
    window,
    font=("Arial",14)
)

pin_entry.grid(row=1,column=1)



roller_label = Label(
    window,
    text="Roller Location (m):",
    font=("Arial",14)
)

roller_label.grid(row=2,column=0,padx=10,pady=10)


roller_entry = Entry(
    window,
    font=("Arial",14)
)

roller_entry.grid(row=2,column=1)



# ---------------- POINT LOAD ----------------


load_force_label = Label(
    window,
    text="Load Force (N):",
    font=("Arial",14)
)

load_force_label.grid(row=3,column=0,padx=10,pady=10)


load_force_entry = Entry(
    window,
    font=("Arial",14)
)

load_force_entry.grid(row=3,column=1)



load_position_label = Label(
    window,
    text="Load Position (m):",
    font=("Arial",14)
)

load_position_label.grid(row=4,column=0,padx=10,pady=10)


load_position_entry = Entry(
    window,
    font=("Arial",14)
)

load_position_entry.grid(row=4,column=1)



add_load_button = Button(
    window,
    text="Add Point Load",
    font=("Arial",14),
    command=add_point_load
)

add_load_button.grid(row=5,column=1)



# ---------------- DISTRIBUTED LOAD ----------------


udl_force_label = Label(
    window,
    text="UDL Force (N/m):",
    font=("Arial",14)
)

udl_force_label.grid(row=6,column=0,padx=10,pady=10)



udl_force_entry = Entry(
    window,
    font=("Arial",14)
)

udl_force_entry.grid(row=6,column=1)



udl_start_label = Label(
    window,
    text="UDL Start (m):",
    font=("Arial",14)
)

udl_start_label.grid(row=7,column=0,padx=10,pady=10)



udl_start_entry = Entry(
    window,
    font=("Arial",14)
)

udl_start_entry.grid(row=7,column=1)



udl_end_label = Label(
    window,
    text="UDL End (m):",
    font=("Arial",14)
)

udl_end_label.grid(row=8,column=0,padx=10,pady=10)



udl_end_entry = Entry(
    window,
    font=("Arial",14)
)

udl_end_entry.grid(row=8,column=1)



udl_button = Button(
    window,
    text="Add Distributed Load",
    font=("Arial",14),
    command=add_distributed_load
)

udl_button.grid(row=9,column=1)



# ---------------- LOAD DISPLAY ----------------


load_display = Label(
    window,
    text="Current Loads:",
    font=("Arial",14)
)

load_display.grid(row=10,column=1)



remove_button = Button(
    window,
    text="Remove Last Load",
    font=("Arial",14),
    command=remove_last_load
)

remove_button.grid(row=11,column=1)



# ---------------- SOLVE ----------------


solve_button = Button(
    window,
    text="Solve Beam",
    font=("Arial",14),
    command=solve_beam
)

solve_button.grid(row=12,column=1)



reaction_label = Label(
    window,
    text="Reactions will appear here",
    font=("Arial",14)
)

reaction_label.grid(row=13,column=1,padx=10,pady=10)



window.mainloop()