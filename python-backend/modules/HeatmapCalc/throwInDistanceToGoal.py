from ..HeatmapCalc.getPlayDirection import *
from ..HeatmapCalc.heatmapDataCalculation import *

def throwInDistanceToGoal(event : Event, tracking_data : List[FrameElement]):
    playDirection = getDirectionOfPlay(tracking_data, event.period)
    ballPosition = getBallPositionEvent(event, tracking_data)
    distance = -1
    if ballPosition.x is None:
       ballPosition = getKickerCoordinates(event)
    
    ballPosition = coordinatesToMeter(ballPosition)

    if playDirection == 0:
        distance = 105 - ballPosition.x
    elif playDirection == 1:
        distance = ballPosition.x
    return distance
