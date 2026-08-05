
class Rectangle:

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def centroid(self):
        return self.height / 2

    def moment_of_inertia(self):
        return (
            self.width * self.height**3
        ) / 12

    def c(self):
        return self.height / 2


class IBeam:

    def __init__(
        self,
        flange_width,
        flange_thickness,
        web_thickness,
        height
    ):

        self.flange_width = flange_width
        self.flange_thickness = flange_thickness
        self.web_thickness = web_thickness
        self.height = height

    def area(self):
        flange_area = (
                self.flange_width *
                self.flange_thickness
        )

        web_area = (
                self.web_thickness *
                (
                        self.height -
                        2 * self.flange_thickness
                )
        )

        return (
                2 * flange_area +
                web_area
        )

    def centroid(self):
        return self.height / 2

    def c(self):
        return self.height / 2

    def moment_of_inertia(self):
        # Top and bottom flange
        flange_I = (
                           self.flange_width *
                           self.flange_thickness ** 3
                   ) / 12

        flange_area = (
                self.flange_width *
                self.flange_thickness
        )

        d = (
                self.height / 2
                - self.flange_thickness / 2
        )

        I_top = flange_I + flange_area * d ** 2
        I_bottom = flange_I + flange_area * d ** 2

        # Web
        web_height = (
                self.height -
                2 * self.flange_thickness
        )

        I_web = (
                        self.web_thickness *
                        web_height ** 3
                ) / 12

        return (
                I_top +
                I_bottom +
                I_web
        )


class TBeam:

    def __init__(
        self,
        flange_width,
        flange_thickness,
        web_thickness,
        height
    ):

        self.flange_width = flange_width
        self.flange_thickness = flange_thickness
        self.web_thickness = web_thickness
        self.height = height

    def area(self):
        flange_area = (
                self.flange_width *
                self.flange_thickness
        )

        web_height = (
                self.height -
                self.flange_thickness
        )

        web_area = (
                self.web_thickness *
                web_height
        )

        return flange_area + web_area

    def centroid(self):
        flange_area = (
                self.flange_width *
                self.flange_thickness
        )

        flange_y = (
                self.height -
                self.flange_thickness / 2
        )

        web_height = (
                self.height -
                self.flange_thickness
        )

        web_area = (
                self.web_thickness *
                web_height
        )

        web_y = web_height / 2

        return (
                flange_area * flange_y +
                web_area * web_y
        ) / (
                flange_area +
                web_area
        )

    def c(self):
        return max(
            self.centroid(),
            self.height - self.centroid()
        )

    def moment_of_inertia(self):
        y_bar = self.centroid()

        flange_area = (
                self.flange_width *
                self.flange_thickness
        )

        flange_I = (
                           self.flange_width *
                           self.flange_thickness ** 3
                   ) / 12

        flange_y = (
                self.height -
                self.flange_thickness / 2
        )

        d_flange = abs(flange_y - y_bar)

        web_height = (
                self.height -
                self.flange_thickness
        )

        web_area = (
                self.web_thickness *
                web_height
        )

        web_I = (
                        self.web_thickness *
                        web_height ** 3
                ) / 12

        web_y = web_height / 2

        d_web = abs(web_y - y_bar)

        return (
                flange_I +
                flange_area * d_flange ** 2 +
                web_I +
                web_area * d_web ** 2
        )
