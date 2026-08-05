
class PointLoad:
    def __init__(self, magnitude, position):
        self.magnitude = magnitude
        self.position = position

    def equivalent_load(self):
        return self.magnitude, self.position


class DistributedLoad:

    def __init__(self, intensity, start, end):
        self.intensity = intensity
        self.start = start
        self.end = end

    def equivalent_load(self):
        length = self.end - self.start
        magnitude = self.intensity * length
        position = (self.start + self.end) / 2

        return magnitude, position


class TriangularLoad:

    def __init__(self, max_intensity, start, end):
        self.max_intensity = max_intensity
        self.start = start
        self.end = end

    def equivalent_load(self):
        length = self.end - self.start
        magnitude = 0.5 * length * self.max_intensity
        position = self.start + (2/3)*length

        return magnitude, position

