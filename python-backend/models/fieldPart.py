import math


def normalizeCoordinate(coordinate: float):
    if math.isnan(coordinate):
        return None
    return coordinate


class FieldPart:
    def __init__(self, minX: float, maxX: float, minY: float, maxY: float):
        self.minX: float = normalizeCoordinate(minX)
        self.maxX: float = normalizeCoordinate(maxX)
        self.minY: float = normalizeCoordinate(minY)
        self.maxY: float = normalizeCoordinate(maxY)
