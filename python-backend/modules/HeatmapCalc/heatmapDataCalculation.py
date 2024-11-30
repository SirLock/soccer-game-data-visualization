from modules.gameDataManager import *
from models.gameData import *
from models.frameElement import *
from models.coordinates import *


def shotsOnTarget(eventData: Events()):
    shotsOnTargetList = []
    shots = eventData.shots
    for shot in shots:
        shotIsOnTarget = shot.subtype.find("ON") >= 0
        if shotIsOnTarget:
            shotsOnTargetList.append({
                "on": shot
            })
    print(shotsOnTargetList)  # TODO remove after testing / debugging
    return shotsOnTargetList

def getBallPositionEvent(event : Event, tracking_data : List[FrameElement]):
    frame = event.startFrame - 1 
    coordinates = tracking_data[frame].coordinates.get("Ball")
    return coordinates  


def getKickerCoordinates(event : Event):
    dataSetId = getSelectedGameData()
    data = getGameDataSet(dataSetId)
    frame = event.startFrame - 1 
    team = event.team
    kickerId = event.origin
    kickerCoordinates = Coordinates(0,0)

    if team == "Home":
        trackingData = data.trackingHome
    else:
        trackingData = data.trackingAway
  
    coordinates = trackingData[frame].coordinates
    playerCoordinates = {key: value for key, value in coordinates.items() if not key.startswith('Ball')}

    for player in list(playerCoordinates.keys()):
        if player == kickerId:
            kickerCoordinates = Coordinates(playerCoordinates.get(player).x,
                                 playerCoordinates.get(player).y)                             
    return kickerCoordinates