from modules.TrajectoryCalc.filters import *

from models.constants import FIELD_WIDTH_IN_METERS, FIELD_HEIGHT_IN_METERS


def calculateDistanceTraveled(trackingData, player, startFrame, endFrame):
    partialTrackingData = cropTrackingData(trackingData, startFrame, endFrame)
    totalDistance = 0
    for index in range(len(partialTrackingData)):
        if index + 1 >= len(partialTrackingData):
            break
        currentPosition = partialTrackingData[index].coordinates.get(player)
        nextPosition = partialTrackingData[index + 1].coordinates.get(player)
        if not (pointHasValidCoordinates(currentPosition) and pointHasValidCoordinates(nextPosition)):
            continue
        distance = calculateDistance(coordinatesToMeter(currentPosition), coordinatesToMeter(nextPosition))
        totalDistance += distance
    return totalDistance


def calculateTraveledDistancesIntervals(trackingData, players):
    allPlayersIntervals = dict()
    for player in players:
        allPlayersIntervals.update({player: 0})

    lengthOfGameInFrames = len(trackingData)
    numberOfOneMinuteIntervals = int((lengthOfGameInFrames / 25) / 60)
    framePerMinute = int(lengthOfGameInFrames / numberOfOneMinuteIntervals)

    for player in players:
        playerIntervals = []
        for interval in range(numberOfOneMinuteIntervals):
            startFrame = interval * framePerMinute
            endFrame = (interval + 1) * framePerMinute - 1
            playerIntervals.append(calculateDistanceTraveled(trackingData, player, startFrame, endFrame))

        totalDistance = 0
        for interval in range(0, numberOfOneMinuteIntervals):
            totalDistance += playerIntervals[interval]
        playerIntervals.append(totalDistance)

        allPlayersIntervals[player] = playerIntervals
    return allPlayersIntervals


def calculateTotalDistanceTraveledForAllPlayers(trackingData, players):
    playersToDistances = dict()
    for player in players:
        playersToDistances.update({player: 0})

    for index in range(len(trackingData)):
        if index + 1 >= len(trackingData):
            break
        currentFrame = trackingData[index]
        nextFrame = trackingData[index + 1]

        for player in players:
            currentCoordinate = currentFrame.coordinates.get(player)
            nextCoordinate = nextFrame.coordinates.get(player)
            if not (pointHasValidCoordinates(currentCoordinate)
                    and pointHasValidCoordinates(nextCoordinate)):
                continue
            currentCoordinatesInMeter = coordinatesToMeter(currentCoordinate)
            nextCoordinatesInMeter = coordinatesToMeter(nextCoordinate)
            distance = calculateDistance(currentCoordinatesInMeter, nextCoordinatesInMeter)
            playersToDistances[player] += distance
    return playersToDistances


def coordinatesToMeter(coordinates: Coordinates):
    return Coordinates(
        coordinates.x * FIELD_WIDTH_IN_METERS,
        coordinates.y * FIELD_HEIGHT_IN_METERS
    )
