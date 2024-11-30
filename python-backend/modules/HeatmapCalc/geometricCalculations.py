import numpy as np
from models.geometricFigures import *
from modules.gameDataManager import *

# Shapes

def splitTrapezoid(trapezoid: Trapezoid):
    triangle1 = Triangle(trapezoid.point0, trapezoid.point1, trapezoid.point2)
    triangle2 = Triangle(trapezoid.point2, trapezoid.point3, trapezoid.point0)
    return triangle1, triangle2


def splitRectangle(rectangle: Rectangle):
    triangle1 = Triangle(rectangle.point0, rectangle.point1, rectangle.point2)
    triangle2 = Triangle(rectangle.point2, rectangle.point3, rectangle.point0)
    return triangle1, triangle2


# Function calculates barycentric coordinates of a point in relation to a triangle
# Formula from "Einführung in die Computergrafik SS2021" p. 121
def barycentricCoordinatesTriangle(point: Coordinates, triangle: Triangle):
    q = point
    p0 = triangle.point0
    p1 = triangle.point1
    p2 = triangle.point2
    x1 = (((q.x - p0.x) * (p2.y - p0.y) - (q.y - p0.y) * (p2.x - p0.x)) /
          ((p1.x - p0.x) * (p2.y - p0.y) - (p1.y - p0.y) * (p2.x - p0.x)))
    x2 = (((p1.x - p0.x) * (q.y - p0.y) - (q.x - p0.x) * (p1.y - p0.y)) /
          ((p1.x - p0.x) * (p2.y - p0.y) - (p1.y - p0.y) * (p2.x - p0.x)))
    x0 = 1 - x1 - x2
    return x0, x1, x2


def isPlayerInTrapezoid(trackingData, playerId, frame, trapezoid: Trapezoid) -> bool:
    result = None
    triangle1, triangle2 = splitTrapezoid(trapezoid)
    result = (isPlayerInTriangle(trackingData, playerId, frame, triangle1)
              or isPlayerInTriangle(trackingData, playerId, frame, triangle2))
    return result


def isPlayerInTriangle(trackingData, playerId, frame: int, triangle: Triangle) -> bool:
    coordinates = trackingData[frame].coordinates
    noCoordinatesForPlayer = coordinates.get(playerId) is None
    if noCoordinatesForPlayer or coordinates.get(playerId).x is None or coordinates.get(playerId).y is None:
        return False
    playerPosition = Coordinates(coordinates.get(playerId).x,
                                 coordinates.get(playerId).y)
def isPlayerInRectangle(trackingData, playerId, frame: int, rectangle: Rectangle) -> bool:
    result = None
    triangle1, triangle2 = splitRectangle(rectangle)
    result = isPlayerInTriangle(trackingData, playerId, frame, triangle1) or isPlayerInTriangle(trackingData, playerId, frame, triangle2)
    return result


def isPlayerInTriangle(trackingData, playerId, frame: int, triangle: Triangle) -> bool:
    coordinates = trackingData[frame].coordinates
    noCoordinatesForPlayer = coordinates.get(playerId) is None
    if noCoordinatesForPlayer or coordinates.get(playerId).x is None or coordinates.get(playerId).y is None:
        return False
    playerPosition = Coordinates(coordinates.get(playerId).x,
                                 coordinates.get(playerId).y)
    x0, x1, x2 = barycentricCoordinatesTriangle(playerPosition, triangle)
    result = (0 <= x0 <= 1) and (0 <= x1 <= 1) and (0 <= x2 <= 1)
    return result


def transformTrapezoid(trapezoid: Trapezoid, rotationAngle: float, translationVector: Vector):
    rotationMatrix = createRotationMatrix(rotationAngle)
    transformationMatrix = createTransformationMatrix(
        rotationMatrix, translationVector)

    p0 = np.array([[trapezoid.point0.x],
                   [trapezoid.point0.y],
                   [1]])

    p1 = np.array([[trapezoid.point1.x],
                   [trapezoid.point1.y],
                   [1]])

    p2 = np.array([[trapezoid.point2.x],
                   [trapezoid.point2.y],
                   [1]])

    p3 = np.array([[trapezoid.point3.x],
                   [trapezoid.point3.y],
                   [1]])

    p0Transformed = transformationMatrix.dot(p0)
    p1Transformed = transformationMatrix.dot(p1)
    p2Transformed = transformationMatrix.dot(p2)
    p3Transformed = transformationMatrix.dot(p3)

    p0 = Coordinates(float(p0Transformed[0]), float(p0Transformed[1]))
    p1 = Coordinates(float(p1Transformed[0]), float(p1Transformed[1]))
    p2 = Coordinates(float(p2Transformed[0]), float(p2Transformed[1]))
    p3 = Coordinates(float(p3Transformed[0]), float(p3Transformed[1]))

    transformedTrapezoid = Trapezoid(p0, p1, p2, p3)
    return transformedTrapezoid


# Vectors


def makeVector(point1: Coordinates, point2: Coordinates):
    vectorX = point2.x - point1.x
    vectorY = point2.y - point1.y
    vector = Vector(vectorX, vectorY)
    return vector


def calculateAngleBetweenVectors(vector1: Vector, vector2: Vector):
    return math.degrees(math.acos(
        vectorMultiplication(vector1, vector2) / (calculateVectorLength(vector1) * calculateVectorLength(vector2))))


def vectorMultiplication(vector1: Vector, vector2: Vector):
    return vector1.x * vector2.x + vector1.y * vector2.y


def calculateVectorLength(vector: Vector):
    return math.sqrt(pow(vector.x, 2) + pow(vector.y, 2))


# Matrices

def createRotationMatrix(angle: float):
    cos = round(math.cos(math.radians(angle)), 10)
    sin = round(math.sin(math.radians(angle)), 10)
    rotationMatrix = np.array([[cos, -1 * sin], [sin, cos]])
    return rotationMatrix


def createTransformationMatrix(rotation, vector: Vector):
    transformationMatrix = np.array([[rotation[0][0], rotation[0][1], vector.x],
                                     [rotation[1][0], rotation[1][1], vector.y],
                                     [0, 0, 1]])
    return transformationMatrix
