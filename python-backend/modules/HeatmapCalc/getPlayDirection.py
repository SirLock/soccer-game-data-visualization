# Function takes tracking Data for a given team and the period of play
# Takes the starting position from the players' positions at the beginning
# of the game and inverts it if period is 2 
def getDirectionOfPlay(trackingData, period: int):
    startCoordinates = trackingData[0].coordinates
    dir = -1
    for key in startCoordinates.keys():
        x = startCoordinates.get(key).x
        if not x:
            continue
        elif float(x) <= 0.35:
            dir = 0
            break
        elif float(x) >= 0.65:
            dir = 1
            break

    if period == 2 and not dir == -1:
        return 1 - dir
    return dir
