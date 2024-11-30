from models.challenges import *
from math import dist

from models.constants import FIELD_WIDTH_IN_METERS, FIELD_HEIGHT_IN_METERS


def coordinatesToMeter(coordinates: Coordinates):
    return Coordinates(
        coordinates.x * FIELD_WIDTH_IN_METERS,
        coordinates.y * FIELD_HEIGHT_IN_METERS
    )


###

def filterWithin(events, startFrame, endFrame):
    filteredEvents = []
    for event in events:
        eventStartFrame = event.startFrame
        if startFrame <= eventStartFrame <= endFrame:
            filteredEvents.append(event)
    return filteredEvents


def filterForRelevantPlayersByDistance(trackingData, startFrame, endFrame, relevantDistance):
    partialTrackingData = cropTrackingData(trackingData, startFrame, endFrame)
    relevantPlayers = []
    remainingPlayers = list(partialTrackingData[0].coordinates.keys())
    remainingPlayers.remove('Ball')
    for frame in partialTrackingData:
        ballCoordinates = frame.coordinates.get('Ball')
        relevantPlayersCurrentFrame = []

        for player in remainingPlayers:
            playerCoordinates = frame.coordinates.get(player)
            if pointHasValidCoordinates(ballCoordinates) and pointHasValidCoordinates(playerCoordinates):
                distance = calculateDistance(coordinatesToMeter(ballCoordinates), coordinatesToMeter(playerCoordinates))
                if distance <= relevantDistance:
                    relevantPlayersCurrentFrame.append(player)

        for player in relevantPlayersCurrentFrame:
            remainingPlayers.remove(player)
            relevantPlayers.append(player)

        if not remainingPlayers:
            break
    return relevantPlayers


def filterForRelevantPlayersByPassParticipation(eventData, startFrame, endFrame):
    passes = filterWithin(eventData.passes, startFrame, endFrame)
    relevantPlayers = []
    for p in passes:
        if p.origin not in relevantPlayers:
            relevantPlayers.append(p.origin)
        if p.target not in relevantPlayers:
            relevantPlayers.append(p.target)
    return relevantPlayers


def cropTrackingData(trackingData, startFrame, endFrame):
    partialTrackingData = []
    for frame in range(startFrame, endFrame + 1):
        partialTrackingData.append(trackingData[frame])
    return partialTrackingData


def calculateDistance(pointA, pointB):
    return dist([pointA.x, pointA.y], [pointB.x, pointB.y])


def pointHasValidCoordinates(point):
    return point.x is not None and point.y is not None
