from tkinter import *
from tkinter import filedialog, messagebox

import os
import tempfile
import matplotlib.pyplot as plt

from beam import Beam
from supports import PinSupport, RollerSupport
from loads import PointLoad, DistributedLoad
from solver import solve_reactions
from materials import materials
from sections import Rectangle, IBeam, TBeam
from shear import calculate_shear
from moment import calculate_moment
from max_values import find_max_moment
from stress import calculate_bending_stress
from deflection import calculate_deflection
from plotting import plot_beam, plot_shear, plot_moment
from report import generate_beam_report


# =========================================================
# GLOBAL DATA
# =========================================================

loads = []
last_analysis = None


# =========================================================
# WINDOW
# =========================================================

window = Tk()

window.title("Beam Solver")
window.geometry("800x850")


# =========================================================
# SCROLLABLE MAIN AREA
# =========================================================

canvas = Canvas(window)

scrollbar = Scrollbar(
    window,
    orient=VERTICAL,
    command=canvas.yview
)

main_frame = Frame(canvas)

main_frame.bind(
    "<Configure>",
    lambda event: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

frame_window = canvas.create_window(
    (0, 0),
    window=main_frame,
    anchor="nw"
)

canvas.bind(
    "<Configure>",
    lambda event: canvas.itemconfigure(
        frame_window,
        width=event.width
    )
)

canvas.configure(
    yscrollcommand=scrollbar.set
)

canvas.pack(
    side=LEFT,
    fill=BOTH,
    expand=True
)

scrollbar.pack(
    side=RIGHT,
    fill=Y
)



# =========================================================
# MOUSE WHEEL SCROLLING
# =========================================================

def _on_mousewheel(event):
    if event.delta:
        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )


def _on_linux_scroll_up(event):
    canvas.yview_scroll(-1, "units")


def _on_linux_scroll_down(event):
    canvas.yview_scroll(1, "units")


canvas.bind_all("<MouseWheel>", _on_mousewheel)
canvas.bind_all("<Button-4>", _on_linux_scroll_up)
canvas.bind_all("<Button-5>", _on_linux_scroll_down)

# =========================================================
# TKINTER VARIABLES
# =========================================================

material_var = StringVar(window)
material_var.set("A36 Steel")

section_var = StringVar(window)
section_var.set("Rectangle")


# =========================================================
# WIDGET REFERENCES
# =========================================================

length_entry = None
pin_entry = None
roller_entry = None

load_force_entry = None
load_position_entry = None

udl_force_entry = None
udl_start_entry = None
udl_end_entry = None

load_display = None
reaction_label = None

section_frame = None

width_entry = None
height_entry = None

flange_width_entry = None
flange_thickness_entry = None
web_thickness_entry = None
i_height_entry = None

t_flange_width_entry = None
t_flange_thickness_entry = None
t_web_thickness_entry = None
t_height_entry = None


# =========================================================
# LOAD FUNCTIONS
# =========================================================

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


# =========================================================
# CROSS SECTION FUNCTION
# =========================================================

def update_section_fields(*args):
    global width_entry
    global height_entry

    global flange_width_entry
    global flange_thickness_entry
    global web_thickness_entry
    global i_height_entry

    global t_flange_width_entry
    global t_flange_thickness_entry
    global t_web_thickness_entry
    global t_height_entry

    for widget in section_frame.winfo_children():
        widget.destroy()

    section_type = section_var.get()

    if section_type == "Rectangle":
        Label(
            section_frame,
            text="Width (m):",
            font=("Arial", 14)
        ).grid(row=0, column=0, padx=10, pady=5)

        width_entry = Entry(
            section_frame,
            font=("Arial", 14)
        )

        width_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(
            section_frame,
            text="Height (m):",
            font=("Arial", 14)
        ).grid(row=1, column=0, padx=10, pady=5)

        height_entry = Entry(
            section_frame,
            font=("Arial", 14)
        )

        height_entry.grid(row=1, column=1, padx=10, pady=5)

    elif section_type == "I-Beam":
        Label(
            section_frame,
            text="Flange Width (m):",
            font=("Arial", 14)
        ).grid(row=0, column=0, padx=10, pady=5)

        flange_width_entry = Entry(
            section_frame,
            font=("Arial", 14)
        )

        flange_width_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(
            section_frame,
            text="Flange Thickness (m):",
            font=("Arial", 14)
        ).grid(row=1, column=0, padx=10, pady=5)

        flange_thickness_entry = Entry(
            section_frame,
            font=("Arial", 14)
        )

        flange_thickness_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(
            section_frame,
            text="Web Thickness (m):",
            font=("Arial", 14)
        ).grid(row=2, column=0, padx=10, pady=5)

        web_thickness_entry = Entry(
            section_frame,
            font=("Arial", 14)
        )

        web_thickness_entry.grid(row=2, column=1, padx=10, pady=5)

        Label(
            section_frame,
            text="Height (m):",
            font=("Arial", 14)
        ).grid(row=3, column=0, padx=10, pady=5)

        i_height_entry = Entry(
            section_frame,
            font=("Arial", 14)
        )

        i_height_entry.grid(row=3, column=1, padx=10, pady=5)

    elif section_type == "T-Beam":
        Label(
            section_frame,
            text="Flange Width (m):",
            font=("Arial", 14)
        ).grid(row=0, column=0, padx=10, pady=5)

        t_flange_width_entry = Entry(
            section_frame,
            font=("Arial", 14)
        )

        t_flange_width_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(
            section_frame,
            text="Flange Thickness (m):",
            font=("Arial", 14)
        ).grid(row=1, column=0, padx=10, pady=5)

        t_flange_thickness_entry = Entry(
            section_frame,
            font=("Arial", 14)
        )

        t_flange_thickness_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(
            section_frame,
            text="Web Thickness (m):",
            font=("Arial", 14)
        ).grid(row=2, column=0, padx=10, pady=5)

        t_web_thickness_entry = Entry(
            section_frame,
            font=("Arial", 14)
        )

        t_web_thickness_entry.grid(row=2, column=1, padx=10, pady=5)

        Label(
            section_frame,
            text="Height (m):",
            font=("Arial", 14)
        ).grid(row=3, column=0, padx=10, pady=5)

        t_height_entry = Entry(
            section_frame,
            font=("Arial", 14)
        )

        t_height_entry.grid(row=3, column=1, padx=10, pady=5)


# =========================================================
# SOLVE FUNCTION
# =========================================================

def solve_beam():
    global last_analysis

    length = float(length_entry.get())
    pin_location = float(pin_entry.get())
    roller_location = float(roller_entry.get())

    beam = Beam(length)

    beam.add_support(PinSupport(pin_location))
    beam.add_support(RollerSupport(roller_location))

    for load in loads:
        beam.add_load(load)

    selected_material = materials[
        material_var.get()
    ]

    E = selected_material.E
    yield_strength = selected_material.yield_strength

    section_type = section_var.get()

    if section_type == "Rectangle":
        width = float(width_entry.get())
        height = float(height_entry.get())

        section = Rectangle(
            width,
            height
        )

    elif section_type == "I-Beam":
        flange_width = float(flange_width_entry.get())
        flange_thickness = float(flange_thickness_entry.get())
        web_thickness = float(web_thickness_entry.get())
        height = float(i_height_entry.get())

        section = IBeam(
            flange_width,
            flange_thickness,
            web_thickness,
            height
        )

    elif section_type == "T-Beam":
        flange_width = float(t_flange_width_entry.get())
        flange_thickness = float(t_flange_thickness_entry.get())
        web_thickness = float(t_web_thickness_entry.get())
        height = float(t_height_entry.get())

        section = TBeam(
            flange_width,
            flange_thickness,
            web_thickness,
            height
        )

    solve_reactions(beam)

    x_values, shear_values = calculate_shear(
        beam
    )

    x_values, moment_values = calculate_moment(
        x_values,
        shear_values
    )

    max_moment, max_moment_location = find_max_moment(
        x_values,
        moment_values
    )

    bending_stress = calculate_bending_stress(
        max_moment,
        section
    )

    I = section.moment_of_inertia()

    x_deflection, deflection_values = calculate_deflection(
        beam,
        x_values,
        moment_values,
        E,
        I
    )

    max_deflection = min(deflection_values)

    max_deflection_index = deflection_values.index(
        max_deflection
    )

    max_deflection_location = x_deflection[
        max_deflection_index
    ]

    safety_factor = (
        yield_strength /
        abs(bending_stress)
    )

    result_text = "Beam Analysis Results:\n\n"
    result_text += "Reactions:\n"

    for support in beam.supports:
        result_text += (
            type(support).__name__
            + ": "
            + str(round(support.reaction, 2))
            + " N\n"
        )

    result_text += (
        "\nMaximum Moment: "
        + str(round(max_moment, 2))
        + " Nm"
    )

    result_text += (
        "\nMoment Location: "
        + str(round(max_moment_location, 2))
        + " m"
    )

    result_text += (
        "\nMaximum Bending Stress: "
        + str(round(bending_stress / 1e6, 2))
        + " MPa"
    )

    result_text += (
        "\nMaximum Deflection: "
        + str(round(max_deflection * 1000, 2))
        + " mm"
    )

    result_text += (
        "\nDeflection Location: "
        + str(round(max_deflection_location, 2))
        + " m"
    )

    result_text += (
        "\nSafety Factor: "
        + str(round(safety_factor, 2))
    )

    reaction_label.config(
        text=result_text
    )

    # Save the completed analysis so the PDF generator can use
    # exactly the same results shown on screen.
    last_analysis = {
        "beam": beam,
        "section": section,
        "section_type": section_type,
        "material": selected_material,
        "E": E,
        "yield_strength": yield_strength,
        "x_values": x_values,
        "shear_values": shear_values,
        "moment_values": moment_values,
        "x_deflection": x_deflection,
        "deflection_values": deflection_values,
        "max_moment": max_moment,
        "max_moment_location": max_moment_location,
        "bending_stress": bending_stress,
        "max_deflection": max_deflection,
        "max_deflection_location": max_deflection_location,
        "safety_factor": safety_factor
    }


    # ---------------- PLOTS ----------------

    plot_beam(beam)

    plot_shear(
        x_values,
        shear_values
    )

    plot_moment(
        x_values,
        moment_values
    )

    print("\nMaterial:", selected_material.name)
    print("E =", E)
    print("Yield Strength =", yield_strength)

    print("\nSection:", section_type)
    print("Area =", section.area())
    print("Centroid =", section.centroid())
    print("Moment of Inertia =", I)

    print("\nMaximum Moment =", max_moment)
    print("Moment Location =", max_moment_location)

    print("Bending Stress =", bending_stress)
    print("Safety Factor =", safety_factor)

    print("Maximum Deflection =", max_deflection)
    print(
        "Deflection Location =",
        max_deflection_location
    )



# =========================================================
# PDF REPORT
# =========================================================

def _save_report_plots(analysis, folder):
    beam = analysis["beam"]
    x_values = analysis["x_values"]
    shear_values = analysis["shear_values"]
    moment_values = analysis["moment_values"]
    x_deflection = analysis["x_deflection"]
    deflection_values = analysis["deflection_values"]

    beam_path = os.path.join(folder, "beam.png")
    shear_path = os.path.join(folder, "shear.png")
    moment_path = os.path.join(folder, "moment.png")
    deflection_path = os.path.join(folder, "deflection.png")

    # ---------------- BEAM / LOAD DIAGRAM ----------------

    plt.figure(figsize=(8, 2.5))

    plt.plot(
        [0, beam.length],
        [0, 0],
        linewidth=4
    )

    for support in beam.supports:
        plt.scatter(
            support.position,
            0,
            s=80
        )

        plt.annotate(
            type(support).__name__,
            (support.position, 0),
            xytext=(0, -25),
            textcoords="offset points",
            ha="center"
        )

    for load in beam.loads:

        if isinstance(load, PointLoad):
            plt.annotate(
                f"{load.magnitude:g} N",
                xy=(load.position, 0),
                xytext=(load.position, 1.0),
                ha="center",
                arrowprops=dict(
                    arrowstyle="->"
                )
            )

        elif isinstance(load, DistributedLoad):
            plt.plot(
                [load.start, load.end],
                [0.65, 0.65],
                linewidth=3
            )

            plt.annotate(
                f"{load.intensity:g} N/m",
                (
                    (load.start + load.end) / 2,
                    0.65
                ),
                xytext=(0, 10),
                textcoords="offset points",
                ha="center"
            )

    plt.xlim(
        -0.05 * beam.length,
        1.05 * beam.length
    )

    plt.ylim(-0.8, 1.5)

    plt.xlabel("Position (m)")
    plt.yticks([])
    plt.title("Beam and Loading")
    plt.tight_layout()

    plt.savefig(
        beam_path,
        dpi=180
    )

    plt.close()


    # ---------------- SHEAR ----------------

    plt.figure(figsize=(8, 3))

    plt.plot(
        x_values,
        shear_values
    )

    plt.axhline(
        0,
        linewidth=0.8
    )

    plt.xlabel("Position (m)")
    plt.ylabel("Shear (N)")
    plt.title("Shear Force Diagram")
    plt.grid()

    plt.tight_layout()

    plt.savefig(
        shear_path,
        dpi=180
    )

    plt.close()


    # ---------------- MOMENT ----------------

    plt.figure(figsize=(8, 3))

    plt.plot(
        x_values,
        moment_values
    )

    plt.axhline(
        0,
        linewidth=0.8
    )

    plt.xlabel("Position (m)")
    plt.ylabel("Moment (N m)")
    plt.title("Bending Moment Diagram")
    plt.grid()

    plt.tight_layout()

    plt.savefig(
        moment_path,
        dpi=180
    )

    plt.close()


    # ---------------- DEFLECTION ----------------

    plt.figure(figsize=(8, 3))

    deflection_mm = [
        value * 1000
        for value in deflection_values
    ]

    plt.plot(
        x_deflection,
        deflection_mm
    )

    plt.axhline(
        0,
        linewidth=0.8
    )

    plt.xlabel("Position (m)")
    plt.ylabel("Deflection (mm)")
    plt.title("Deflection Diagram")
    plt.grid()

    plt.tight_layout()

    plt.savefig(
        deflection_path,
        dpi=180
    )

    plt.close()

    return (
        beam_path,
        shear_path,
        moment_path,
        deflection_path
    )


def generate_pdf_report():
    if last_analysis is None:
        messagebox.showwarning(
            "No Analysis",
            "Please solve the beam before generating a report."
        )

        return

    filename = filedialog.asksaveasfilename(
        title="Save BeamSolver Report",
        defaultextension=".pdf",
        filetypes=[
            ("PDF files", "*.pdf")
        ],
        initialfile="BeamSolver_Report.pdf"
    )

    if not filename:
        return

    analysis = last_analysis

    beam = analysis["beam"]
    section = analysis["section"]
    material = analysis["material"]


    # ---------------- SUPPORT DATA ----------------

    support_data = []

    reaction_data = []

    for support in beam.supports:

        support_data.append(
            {
                "type": type(support).__name__,
                "position": support.position
            }
        )

        reaction_data.append(
            {
                "support": type(support).__name__,
                "reaction": support.reaction
            }
        )


    # ---------------- LOAD DATA ----------------

    load_data = []

    for load in beam.loads:

        if isinstance(load, PointLoad):

            load_data.append(
                {
                    "type": "Point Load",
                    "magnitude": f"{load.magnitude:g} N",
                    "location": f"{load.position:g} m"
                }
            )

        elif isinstance(load, DistributedLoad):

            load_data.append(
                {
                    "type": "Uniform Distributed Load",
                    "magnitude": f"{load.intensity:g} N/m",
                    "location": (
                        f"{load.start:g} m to "
                        f"{load.end:g} m"
                    )
                }
            )


    # ---------------- SECTION DATA ----------------

    section_properties = {
        "Area": f"{section.area():.6g} m^2",
        "Centroid": f"{section.centroid():.6g} m",
        "Moment of Inertia": (
            f"{section.moment_of_inertia():.6e} m^4"
        )
    }


    # For the simple bending model, max stress occurs
    # where the maximum bending moment occurs.
    max_stress_location = (
        analysis["max_moment_location"]
    )


    # ---------------- CREATE REPORT ----------------

    try:
        with tempfile.TemporaryDirectory() as temp_folder:

            (
                beam_plot,
                shear_plot,
                moment_plot,
                deflection_plot
            ) = _save_report_plots(
                analysis,
                temp_folder
            )


            generate_beam_report(
                filename=filename,

                beam_length=beam.length,

                supports=support_data,

                loads=load_data,

                material_name=material.name,

                E=analysis["E"],

                yield_strength=analysis[
                    "yield_strength"
                ],

                section_type=analysis[
                    "section_type"
                ],

                section_properties=section_properties,

                reactions=reaction_data,

                max_moment=analysis[
                    "max_moment"
                ],

                max_moment_location=analysis[
                    "max_moment_location"
                ],

                max_stress=analysis[
                    "bending_stress"
                ],

                max_stress_location=(
                    max_stress_location
                ),

                max_deflection=analysis[
                    "max_deflection"
                ],

                max_deflection_location=analysis[
                    "max_deflection_location"
                ],

                safety_factor=analysis[
                    "safety_factor"
                ],

                beam_plot=beam_plot,

                shear_plot=shear_plot,

                moment_plot=moment_plot,

                deflection_plot=deflection_plot
            )


        messagebox.showinfo(
            "Report Generated",
            "BeamSolver PDF report generated successfully."
        )

    except Exception as error:

        messagebox.showerror(
            "Report Error",
            str(error)
        )



# =========================================================
# GUI — BEAM INPUT
# =========================================================

length_label = Label(
    main_frame,
    text="Beam Length (m):",
    font=("Arial", 14)
)

length_label.grid(
    row=0,
    column=0,
    padx=10,
    pady=10
)

length_entry = Entry(
    main_frame,
    font=("Arial", 14)
)

length_entry.grid(
    row=0,
    column=1
)

pin_label = Label(
    main_frame,
    text="Pin Location (m):",
    font=("Arial", 14)
)

pin_label.grid(
    row=1,
    column=0,
    padx=10,
    pady=10
)

pin_entry = Entry(
    main_frame,
    font=("Arial", 14)
)

pin_entry.grid(
    row=1,
    column=1
)

roller_label = Label(
    main_frame,
    text="Roller Location (m):",
    font=("Arial", 14)
)

roller_label.grid(
    row=2,
    column=0,
    padx=10,
    pady=10
)

roller_entry = Entry(
    main_frame,
    font=("Arial", 14)
)

roller_entry.grid(
    row=2,
    column=1
)


# =========================================================
# GUI — MATERIAL
# =========================================================

material_label = Label(
    main_frame,
    text="Material:",
    font=("Arial", 14)
)

material_label.grid(
    row=3,
    column=0,
    padx=10,
    pady=10
)

material_menu = OptionMenu(
    main_frame,
    material_var,
    *materials.keys()
)

material_menu.config(
    font=("Arial", 14)
)

material_menu.grid(
    row=3,
    column=1,
    padx=10,
    pady=10
)


# =========================================================
# GUI — POINT LOAD
# =========================================================

load_force_label = Label(
    main_frame,
    text="Load Force (N):",
    font=("Arial", 14)
)

load_force_label.grid(
    row=4,
    column=0,
    padx=10,
    pady=10
)

load_force_entry = Entry(
    main_frame,
    font=("Arial", 14)
)

load_force_entry.grid(
    row=4,
    column=1
)

load_position_label = Label(
    main_frame,
    text="Load Position (m):",
    font=("Arial", 14)
)

load_position_label.grid(
    row=5,
    column=0,
    padx=10,
    pady=10
)

load_position_entry = Entry(
    main_frame,
    font=("Arial", 14)
)

load_position_entry.grid(
    row=5,
    column=1
)

add_load_button = Button(
    main_frame,
    text="Add Point Load",
    font=("Arial", 14),
    command=add_point_load
)

add_load_button.grid(
    row=6,
    column=1,
    padx=10,
    pady=5
)


# =========================================================
# GUI — DISTRIBUTED LOAD
# =========================================================

udl_force_label = Label(
    main_frame,
    text="UDL Force (N/m):",
    font=("Arial", 14)
)

udl_force_label.grid(
    row=7,
    column=0,
    padx=10,
    pady=10
)

udl_force_entry = Entry(
    main_frame,
    font=("Arial", 14)
)

udl_force_entry.grid(
    row=7,
    column=1
)

udl_start_label = Label(
    main_frame,
    text="UDL Start (m):",
    font=("Arial", 14)
)

udl_start_label.grid(
    row=8,
    column=0,
    padx=10,
    pady=10
)

udl_start_entry = Entry(
    main_frame,
    font=("Arial", 14)
)

udl_start_entry.grid(
    row=8,
    column=1
)

udl_end_label = Label(
    main_frame,
    text="UDL End (m):",
    font=("Arial", 14)
)

udl_end_label.grid(
    row=9,
    column=0,
    padx=10,
    pady=10
)

udl_end_entry = Entry(
    main_frame,
    font=("Arial", 14)
)

udl_end_entry.grid(
    row=9,
    column=1
)

udl_button = Button(
    main_frame,
    text="Add Distributed Load",
    font=("Arial", 14),
    command=add_distributed_load
)

udl_button.grid(
    row=10,
    column=1,
    padx=10,
    pady=5
)


# =========================================================
# GUI — LOAD DISPLAY
# =========================================================

load_display = Label(
    main_frame,
    text="Current Loads:",
    font=("Arial", 14)
)

load_display.grid(
    row=11,
    column=0,
    columnspan=2,
    padx=10,
    pady=10
)

remove_button = Button(
    main_frame,
    text="Remove Last Load",
    font=("Arial", 14),
    command=remove_last_load
)

remove_button.grid(
    row=12,
    column=1,
    padx=10,
    pady=5
)


# =========================================================
# GUI — CROSS SECTION
# =========================================================

section_label = Label(
    main_frame,
    text="Cross Section:",
    font=("Arial", 14)
)

section_label.grid(
    row=13,
    column=0,
    padx=10,
    pady=10
)

section_menu = OptionMenu(
    main_frame,
    section_var,
    "Rectangle",
    "I-Beam",
    "T-Beam",
    command=update_section_fields
)

section_menu.config(
    font=("Arial", 14)
)

section_menu.grid(
    row=13,
    column=1,
    padx=10,
    pady=10
)

section_frame = Frame(
    main_frame
)

section_frame.grid(
    row=14,
    column=0,
    columnspan=2,
    padx=10,
    pady=10
)

update_section_fields()


# =========================================================
# GUI — SOLVE
# =========================================================

solve_button = Button(
    main_frame,
    text="Solve Beam",
    font=("Arial", 14),
    command=solve_beam
)

solve_button.grid(
    row=15,
    column=1,
    padx=10,
    pady=10
)


generate_report_button = Button(
    main_frame,
    text="Generate PDF Report",
    font=("Arial", 14),
    command=generate_pdf_report
)

generate_report_button.grid(
    row=16,
    column=1,
    padx=10,
    pady=10
)


# =========================================================
# GUI — RESULTS
# =========================================================

reaction_label = Label(
    main_frame,
    text="Results will appear here",
    font=("Arial", 14),
    justify=LEFT
)

reaction_label.grid(
    row=17,
    column=0,
    columnspan=2,
    padx=10,
    pady=10
)


# =========================================================
# START PROGRAM
# =========================================================

window.mainloop()
