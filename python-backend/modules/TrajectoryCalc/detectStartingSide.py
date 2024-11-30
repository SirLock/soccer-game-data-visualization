def isStartingSideLeft(trackingData):
    firstRowCoordinates = trackingData[0].coordinates
    for key in firstRowCoordinates.keys():
        x = firstRowCoordinates.get(key).x
        if not x:
            continue
        if x <= 0.35:
            return True
        if x >= 0.65:
            return False


def isStartingSideRight(trackingData):
    return not isStartingSideLeft(trackingData)