from ..HeatmapCalc.geometricCalculations import *

# Function takes two evetns and returns the distance between the starting positions
# returns -1 if the events' starting coordinates are not in the internal format
def calcEventDistance(event1: Event, event2: Event):
    startE1 = coordinatesToMeters(event1.start)
    startE2 = coordinatesToMeters(event2.start)
    if startE1 == -1 or startE2 == -1:
        return -1
    distance = calculateVectorLength(makeVector(startE1, startE2))
    return distance