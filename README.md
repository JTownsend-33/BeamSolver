# Beam Solver

Beam Solver is a Python application for analyzing statically determinate beams. 
The goal of this project is to provide an intuitive tool for calculating support reactions, generating shear force and bending moment diagrams, 
and performing common beam analysis calculations used in mechanical and civil engineering.

This project is being developed from the ground up as a portfolio project while learning larger-scale Python software development practices. 
Rather than relying on existing engineering libraries for the calculations, 
the core statics and mechanics algorithms are implemented manually to demonstrate both programming and engineering knowledge.

## Current Features

* Create beam objects with configurable lengths
* Add pin and roller supports
* Add point loads
* Calculate support reactions using static equilibrium equations
* Modular, object-oriented project structure

## Planned Features

* Multiple point loads
* Uniform, triangular, and trapezoidal distributed loads
* Shear force diagram generation
* Bending moment diagram generation
* Bending stress calculations
* Beam deflection calculations
* Interactive graphical user interface (GUI)
* Material property database
* PDF report generation
* Save and load beam configurations

## Technologies

* Python
* Object-Oriented Programming (OOP)
* Git
* GitHub

Future versions will also utilize libraries such as NumPy and Matplotlib for numerical calculations and visualization.

## Project Structure

```
BeamSolver/
│
├── main.py          # Entry point
├── beam.py          # Beam class
├── loads.py         # Load classes
├── supports.py      # Support classes
├── solver.py        # Engineering calculations
├── plotting.py      # Diagram generation (future)
└── utils.py         # Helper functions
```

## Future Development Roadmap

* [x] Project setup
* [x] Beam object model
* [x] Point load implementation
* [x] Support reaction solver
* [x] Multiple point loads
* [ ] Distributed loads
* [ ] Shear force diagrams
* [ ] Bending moment diagrams
* [ ] Stress analysis
* [ ] Deflection analysis
* [ ] Graphical user interface
* [ ] Documentation and examples

## License

This project is currently under development and intended for educational and portfolio purposes.
