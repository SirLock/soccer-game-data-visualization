from ..HeatmapCalc.heatmapDataCalculation import *


def detectPitchHalf(event: Event, tracking_data: List[FrameElement]):
    if math.isnan(event.start.x):
        coordinates = getBallPositionEvent(event, tracking_data)
    else:
        coordinates = event.start
    if coordinates.x <= 0.5:
        return 0
    else:
        return 1
