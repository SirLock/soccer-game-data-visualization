from models.situation import Situation, ATTACKS_THROUGH_TOP, ATTACKS_THROUGH_CENTER, ATTACKS_THROUGH_BOTTOM
from models.fieldPart import FieldPart

fieldParts = {
    "top": FieldPart(0, 1, 0, 0.33),
    "center": FieldPart(0, 1, 0.25, 0.75),
    "bottom": FieldPart(0, 1, 0.66, 1)
}


def attackThroughFieldPart(gameData, fieldPartName):
    fieldPart = fieldParts[fieldPartName]
    xLowerLimit = fieldPart.minX
    xUpperLimit = fieldPart.maxX
    yLowerLimit = fieldPart.minY
    yUpperLimit = fieldPart.maxY
    situationKind = ""
    if fieldPartName == "top":
        situationKind = ATTACKS_THROUGH_TOP
    elif fieldPartName == "center":
        situationKind = ATTACKS_THROUGH_CENTER
    elif fieldPartName == "bottom":
        situationKind = ATTACKS_THROUGH_BOTTOM

    attackList = []
    timespan = 10
    accuracyWithinFieldPart = 0.75
    events = gameData.events
    trackingHome = gameData.trackingHome

    shots = []
    for shot in events.shots:
        shots.append(shot)
    for shot in shots:
        withinFieldPart = 0
        shotFrame = shot.startFrame
        if (shot.start.x > xLowerLimit) and (shot.start.x < xUpperLimit):
            for i in range(shotFrame - 25 * timespan, shotFrame):
                ballY = trackingHome[i].coordinates.get("Ball").y
                if ballY is not None and (yLowerLimit <= ballY <= yUpperLimit):
                    withinFieldPart += 1
            if withinFieldPart / (timespan * 25) >= accuracyWithinFieldPart:
                startFrame = shotFrame - timespan * 25
                attackList.append(Situation(startFrame=startFrame, endFrame=shot.endFrame,
                                            period=shot.period, team=shot.team,
                                            kind=situationKind))
                shots.remove(shot)
    return attackList
