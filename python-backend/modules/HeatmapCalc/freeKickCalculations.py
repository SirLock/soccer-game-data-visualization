from ..HeatmapCalc.angleToGoal import *
from ..HeatmapCalc.distanceToGoal import *


def calculateRelevantAreaOfEvent(trackingData, event: Event):
    eventFrame = event.startFrame - 1
    ballPosition = trackingData[eventFrame].coordinates.get("Ball")

    if ballPosition.x is None and ballPosition.y is None:
        ballPosition = getKickerCoordinates(event)

    direction = getDirectionOfPlay(trackingData, event.period)

    if direction == 1:
        goalCenter, goalPost1, goalPost2 = rightGoalPositions()
    elif direction == 0:
        goalCenter, goalPost1, goalPost2 = leftGoalPositions()
    else:
        return -1

    vectorToGoal = makeVector(ballPosition, goalCenter)
    distanceToGoal_ = calculateVectorLength(vectorToGoal)

    goalWidth = calculateVectorLength(makeVector(goalPost1, goalPost2))

    xAxisDistance = abs(goalCenter.x - ballPosition.x)
    trapezoidWidthBall = 0.2 * distanceToGoal_
    trapezoidWidthFarSide = 1.25 * (0.8 * distanceToGoal_ + goalWidth)
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

    return transformedTrapezoid


def getPlayerQuantityBetweenBallAndGoal(trackingData, event: Event):
    playerQuantity = 0
    relevantArea = calculateRelevantAreaOfEvent(trackingData, event)
    eventFrame = event.startFrame - 1

    startCoordinates = trackingData[eventFrame].coordinates

    for playerId in list(startCoordinates.keys()):
        if isPlayerInTrapezoid(trackingData, playerId, eventFrame, relevantArea):
            playerQuantity += 1
    return playerQuantity


def getRelevantPlayersOfEvent(trackingData, event: Event):
    relevantPlayers = []
    relevantArea = calculateRelevantAreaOfEvent(trackingData, event)
    eventFrame = event.startFrame - 1
    trackingDataInExactFrame = trackingData[event.startFrame]

    # playerCoordinates = trackingDataInExactFrame.coordinates
    # playerCoordinates.pop('Ball', None)  # playerCoords is not a copy it is a reference on the object. Pop will delete the value in the original source.
    coordinates = trackingDataInExactFrame.coordinates
    playerCoordinates = {key: value for key, value in coordinates.items() if not key.startswith('Ball')}

    for player in list(playerCoordinates.keys()):
        if player not in relevantPlayers:
            if isPlayerInTrapezoid(trackingData, player, eventFrame, relevantArea):
                relevantPlayers.append(player)
                playerCoordinates.pop(player, None)
    return relevantPlayers

