from ..HeatmapCalc.getPlayDirection import *
from ..HeatmapCalc.convertCoordinates import *
from ..HeatmapCalc.geometricCalculations import *
from ..HeatmapCalc.heatmapDataCalculation import *


def distanceToGoal(event: Event) -> float:
    if event.team == "Home":
        trackingData = getGameDataSet(getSelectedGameData()).trackingHome
    else:
        trackingData = getGameDataSet(getSelectedGameData()).trackingAway

    ballPosition = getBallPositionEvent(event, trackingData)
    if ballPosition.x is None and ballPosition.y is None:
        ballPosition = getKickerCoordinates(event)

    direction = getDirectionOfPlay(trackingData, event.period)

    if direction == 0:
        goalCenter = rightGoalPositions()[0]
    elif direction == 1:
        goalCenter = leftGoalPositions()[0]
    else:
        return -1

    ballPosition = coordinatesToMeter(ballPosition)
    goalCenter = coordinatesToMeter(goalCenter)

    vectorToGoal = makeVector(ballPosition, goalCenter)
    distance = calculateVectorLength(vectorToGoal)
    return distance


def leftGoalPositions():
    center = Coordinates(0.0, 0.5)
    post1 = coordinatesToMetrica(Coordinates(0, 30.34))
    post2 = coordinatesToMetrica(Coordinates(0, 37.66))
    return center, post1, post2


def rightGoalPositions():
    center = Coordinates(1.0, 0.5)
    post1 = coordinatesToMetrica(Coordinates(105, 30.34))
    post2 = coordinatesToMetrica(Coordinates(105, 37.66))
    return center, post1, post2
