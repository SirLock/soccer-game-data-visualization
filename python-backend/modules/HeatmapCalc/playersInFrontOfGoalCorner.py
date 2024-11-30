from ..HeatmapCalc.convertCoordinates import *
from ..HeatmapCalc.geometricCalculations import *
from ..HeatmapCalc.heatmapDataCalculation import *


def playersInFrontOfGoal(event: Event) -> int:
    corner = getEventCorner(event)
    extendedPenaltyArea = getExtendedPenaltyArea(corner)
    trackingData = getOpponentData(event)
    frame = event.startFrame - 1
    playerIDs = trackingData[frame].coordinates.keys()
    playerCount = 0
    for player in playerIDs:
        if player != "Ball" and isPlayerInRectangle(
            trackingData, player, frame, extendedPenaltyArea
        ):
            playerCount += 1

    return playerCount


# Function returns the corner of the field where a corner kick happened
# from. 0 = top left, anti-clockwise
def getEventCorner(event: Event) -> int:
    dataSetId = getSelectedGameData()
    data = getGameDataSet(dataSetId)
    if event.team == "Home":
        trackingData = data.trackingAway
    else:
        trackingData = data.trackingHome

    ballPos = getBallPositionEvent(event, trackingData)
    if ballPos.x is None:
        ballPos = getKickerCoordinates(event)
    if not event.subtype == "CORNER KICK":
        print("Event is not a Corner Kick!")
        return -1
    elif ballPos.x <= 0.25 and ballPos.y <= 0.25:
        corner = 0
    elif ballPos.x <= 0.25 and ballPos.y >= 0.75:
        corner = 1
    elif ballPos.x >= 0.75 and ballPos.y >= 0.75:
        corner = 2
    elif ballPos.x >= 0.75 and ballPos.y <= 0.25:
        corner = 3
    return corner


# Function takes a corner (0 - 3) and returns the Penalty Area extended to the Edge
# of the field on the side of the corner as a rectangle.
def getExtendedPenaltyArea(corner: int) -> Rectangle:
    if corner == 0:
        p0 = Coordinates(0.0, 0.0)
        p1 = coordinatesToMetrica(Coordinates(0.0, 54.16))
        p2 = coordinatesToMetrica(Coordinates(16.5, 54.16))
        p3 = coordinatesToMetrica(Coordinates(16.5, 0.0))
    elif corner == 1:
        p0 = coordinatesToMetrica(Coordinates(0.0, 13.84))
        p1 = Coordinates(0.0, 1.0)
        p2 = coordinatesToMetrica(Coordinates(16.5, 68))
        p3 = coordinatesToMetrica(Coordinates(16.5, 13.84))
    elif corner == 2:
        p0 = coordinatesToMetrica(Coordinates(88.5, 13.84))
        p1 = coordinatesToMetrica(Coordinates(88.5, 68))
        p2 = Coordinates(1.0, 1.0)
        p3 = coordinatesToMetrica(Coordinates(105, 13.84))
    elif corner == 3:
        p0 = coordinatesToMetrica(Coordinates(88.5, 0.0))
        p1 = coordinatesToMetrica(Coordinates(88.5, 54.16))
        p2 = coordinatesToMetrica(Coordinates(105, 54.16))
        p3 = Coordinates(1.0, 0.0)

    return Rectangle(p0, p1, p2, p3)


def getOpponentData(event: Event) -> List[FrameElement]:
    dataSetId = getSelectedGameData()
    data = getGameDataSet(dataSetId)
    if event.team == "Home":
        trackingData = data.trackingAway
    else:
        trackingData = data.trackingHome
    return trackingData
