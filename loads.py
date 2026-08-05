
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

