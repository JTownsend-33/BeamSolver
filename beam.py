
class Beam:
    def __init__(self, length):
        self.length = length
        self.loads = []
        self.supports = []

    def add_load(self, load):
        self.loads.append(load)

    def add_support(self, support):
        self.supports.append(support)
