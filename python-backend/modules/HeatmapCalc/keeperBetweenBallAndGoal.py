from ..HeatmapCalc.angleToGoal import *
from ..HeatmapCalc.distanceToGoal import *
from ..HeatmapCalc.getPlayDirection import *
from ..HeatmapCalc.convertCoordinates import *


def isKeeperBetweenBallAndGoal(event: Event):
    
    dataId = getSelectedGameData()
    data = getGameDataSet(dataId)
    if event.team == "Home":
        trackingData = data.trackingAway
    else:
        trackingData = data.trackingHome
    
    keeperId = getGoalKeeperId(trackingData)
    eventFrame = event.startFrame
    ballPosition = trackingData[eventFrame].coordinates.get("Ball")
    
    direction = getDirectionOfPlay(trackingData, event.period)
    if direction == 1:
        goalCenter, goalPost1, goalPost2 = rightGoalPositions()
    elif direction == 0:
        goalCenter, goalPost1, goalPost2 = leftGoalPositions()
    else:
        return -1
    vectorToGoal = makeVector(ballPosition, goalCenter)
    distanceToGoal = calculateVectorLength(vectorToGoal)

    goalWidth = calculateVectorLength(makeVector(goalPost1, goalPost2))

    xAxisDistance = abs(goalCenter.x - ballPosition.x)
    trapezoidWidthBall = 0.2 * distanceToGoal
    trapezoidWidthFarSide = 1.25 * (0.4 * distanceToGoal + goalWidth)
    point0 = Coordinates(0, 0 - trapezoidWidthBall / 2)
    point1 = Coordinates(0, 0 + trapezoidWidthBall / 2)
    point2 = Coordinates(1.5 * xAxisDistance, 0 + trapezoidWidthFarSide / 2)
    point3 = Coordinates(1.5 * xAxisDistance, 0 - trapezoidWidthFarSide / 2)
    trapezoid = Trapezoid(point0, point1, point2, point3)

    rotationAngle = 90 - angleToGoal(trackingData, event)
    if ballPosition.y <= 0.5:
        rotationAngle = -1 * rotationAngle

    if goalCenter.x == 0.0:
        trapezoid = transformTrapezoid(trapezoid, 180, Vector(0, 0))

    translationVector = makeVector(Coordinates(0, 0), ballPosition)

    transformedTrapezoid = transformTrapezoid(
        trapezoid, rotationAngle, translationVector)
    result = isPlayerInTrapezoid(
        trackingData, keeperId, eventFrame, transformedTrapezoid)
    return result


def getGoalKeeperId(trackingData):
    keeperId = None
    startCoordinates = trackingData[0].coordinates
    startDirection = getDirectionOfPlay(trackingData, 1)
    if startDirection == 0:
        smallestX = 1.0
        for playerId in startCoordinates.keys():
            currentX = startCoordinates.get(playerId).x
            if currentX is not None and currentX < smallestX:
                smallestX = currentX
                keeperId = playerId
    elif startDirection == 1:
        biggestX = 0.0
        for playerId in startCoordinates.keys():
            currentX = startCoordinates.get(playerId).x
            if currentX is not None and currentX > biggestX:
                biggestX = currentX
                keeperId = playerId
    return keeperId
