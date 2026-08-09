
class Material:
    def __init__(self, name, E, yield_strength):
        self.name = name
        self.E = E
        self.yield_strength = yield_strength


materials = {

    "A36 Steel": Material(
        "A36 Steel",
        200e9,
        250e6
    ),

    "A992 Steel": Material(
        "A992 Steel",
        200e9,
        345e6
    ),

    "1018 Steel": Material(
        "1018 Steel",
        205e9,
        370e6
    ),

    "6061-T6 Aluminum": Material(
        "6061-T6 Aluminum",
        69e9,
        276e6
    ),

    "7075-T6 Aluminum": Material(
        "7075-T6 Aluminum",
        71.7e9,
        503e6
    ),

    "Douglas Fir": Material(
        "Douglas Fir",
        12e9,
        40e6
    ),

    "Southern Pine": Material(
        "Southern Pine",
        11e9,
        35e6
    ),

    "Oak": Material(
        "Oak",
        11e9,
        50e6
    )
}
