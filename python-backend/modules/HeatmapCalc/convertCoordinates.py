from models.coordinates import *


# X and Y dimensions of the field in meters
fieldX = 105    # 105 meters long
fieldY = 68  # 68 meters wide


# Function takes coordinates in internal format (0,1) and returns coordinates in meters
# returns -1 if coordinates are not in internal format
def coordinatesToMeters(metricaCoordinates: Coordinates):
    meterCoordinates = Coordinates(0, 0)
    if (metricaCoordinates.x >= 0 and metricaCoordinates.x <= 1) and (metricaCoordinates.y >= 0 and metricaCoordinates.y <= 1):
        meterCoordinates.x = fieldX * metricaCoordinates.x
        meterCoordinates.y = fieldY * metricaCoordinates.y
        return meterCoordinates
    return -1


def coordinatesToMetrica(meterCoordinates: Coordinates):
    metricaCoordinates = Coordinates(0, 0)
    metricaCoordinates.x = meterCoordinates.x / fieldX
    metricaCoordinates.y = meterCoordinates.y / fieldY
    return metricaCoordinates
