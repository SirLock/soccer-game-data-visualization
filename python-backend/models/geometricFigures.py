from models.coordinates import *


class Trapezoid:
    def __init__(self, point0: Coordinates, point1: Coordinates, point2: Coordinates, point3: Coordinates):
        self.point0 = point0
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3

class Triangle:
    def __init__(self, point0: Coordinates, point1: Coordinates, point2: Coordinates):
        self.point0 = point0
        self.point1 = point1
        self.point2 = point2

class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        
class Rectangle:
    def __init__(self, point0: Coordinates, point1: Coordinates, point2: Coordinates, point3: Coordinates):
        self.point0 = point0
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3