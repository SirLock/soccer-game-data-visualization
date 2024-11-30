import math


def normalizeCoordinate(coordinate: float):
    if math.isnan(coordinate):
        return None
    return coordinate


class Coordinates:
    def __init__(self, x: float, y: float):
        self.x: float = normalizeCoordinate(x)
        self.y: float = normalizeCoordinate(y)
