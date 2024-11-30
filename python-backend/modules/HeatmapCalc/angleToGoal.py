from ..HeatmapCalc.distanceToGoal import *
from ..HeatmapCalc.getPlayDirection import *
from ..HeatmapCalc.geometricCalculations import *
from ..HeatmapCalc.heatmapDataCalculation import *


def angleToGoal(trackingData, event: Event):
    direction = getDirectionOfPlay(trackingData, event.period)

    if direction == -1:
        return -1
    elif direction == 0:
        goalCenter, post1, post2 = rightGoalPositions()
    else:
        goalCenter, post1, post2 = leftGoalPositions()

    goalVector = makeVector(post1, post2)

    if event.start.x is None and event.start.y is None:
        ballCoordinatesInMetrica = getBallPositionEvent(event, trackingData)
        eventStart = coordinatesToMeters(ballCoordinatesInMetrica)
    else:
        eventStart = coordinatesToMeters(event.start)

    goalCenter = coordinatesToMeters(goalCenter)
    shotVector = makeVector(eventStart, goalCenter)
    return (90 - calculateAngleBetweenVectors(shotVector, goalVector))
