from pathlib import Path
from models.gameData import GameData
from models.player import Player
from models.frameElement import *
from modules.TrajectoryCalc.bundleChallenges import *
from modules.TrajectoryCalc.statisticalDataCalculation import *
from modules.TrajectoryCalc.findSetPieceCoordinates import *


def importGameData(dataSetId, homeTeamTrackingDataPath, awayTeamTrackingDataPath, eventDataPath, delimiter):
    trackingHome, playersHome = parseTrackingData(homeTeamTrackingDataPath, delimiter)
    trackingAway, playersAway = parseTrackingData(awayTeamTrackingDataPath, delimiter)
    traveledDistancesHome = calculateTraveledDistancesIntervals(trackingHome, playersHome.keys())
    traveledDistancesAway = calculateTraveledDistancesIntervals(trackingAway, playersAway.keys())
    allEvents = parseEventData(eventDataPath, delimiter)
    gameData = GameData()
    gameData.id = dataSetId
    gameData.trackingHome = trackingHome
    gameData.trackingAway = trackingAway
    gameData.traveledDistancesHome = traveledDistancesHome
    gameData.traveledDistancesAway = traveledDistancesAway
    gameData.playersHome = playersHome
    gameData.playersAway = playersAway
    gameData.events = categorizeEvents(allEvents)
    return gameData


def preparseHeader(rawDataFile, delimiter):
    team = rawDataFile.readline().rstrip("\n").split(delimiter)
    playerNumbers = rawDataFile.readline().rstrip("\n").split(delimiter)
    header = rawDataFile.readline().rstrip("\n").split(delimiter)
    return team, playerNumbers, header


def initPlayerObjects(team, playerNumbers, header):
    players: dict[str, Player] = dict()
    for i in range(0, len(playerNumbers)):
        if playerNumbers[i]:
            player = Player()
            player.id = playerNumbers[i]
            player.name = header[i]
            player.team = team[i]
            players.update({player.name: player})
    return players


def stripUntilHeaderAndReturnColumnNames(rawDataFile, headerKeyword) -> str:
    for row in rawDataFile:
        isHeader = row.find(headerKeyword) > -1
        if isHeader:
            return row
        rawDataFile.readline()


def parseTrackingData(dataFilePath, delimiter):
    trackingFrames = []
    base_path = Path(__file__).parent
    file_path = (base_path / dataFilePath).resolve()
    with open(file_path, newline='', mode='r') as rawDataFile:
        teamAndPlayerNumbersAndHeader = preparseHeader(rawDataFile, delimiter)
        team = teamAndPlayerNumbersAndHeader[0]
        playerNumbers = teamAndPlayerNumbersAndHeader[1]
        columnNames = teamAndPlayerNumbersAndHeader[2]
        players = initPlayerObjects(team, playerNumbers, columnNames)
        for row in rawDataFile:
            columnValues = row.rstrip("\n").split(delimiter)
            trackingFrames.append(
                convertToFrameElement(columnValues, columnNames))
    return trackingFrames, players


def convertToFrameElement(columnValues: List[str], columnNames: List[str]) -> FrameElement:
    frameElement = FrameElement()
    frameElement.period = int(columnValues[0])
    frameElement.frame = int(columnValues[1])
    frameElement.time = float(columnValues[2])
    i = 3
    frameElement.coordinates = dict()
    while i < len(columnValues):
        columnName = columnNames[i]
        x = float(columnValues[i])
        y = float(columnValues[i + 1])
        coordinates = Coordinates(x, y)
        frameElement.coordinates.update({
            columnName: coordinates
        })
        i += 2
    return frameElement


def parseEventData(dataFilePath, delimiter):
    base_path = Path(__file__).parent
    file_path = (base_path / dataFilePath).resolve()
    events = []
    with open(file_path, newline='', mode='r') as rawDataFile:
        columnNames = stripUntilHeaderAndReturnColumnNames(
            rawDataFile, "Frame").rstrip("\n").split(delimiter)
        for index, row in enumerate(rawDataFile):
            columnValues = row.rstrip("\n").split(delimiter)
            events.append(convertToEvent(columnValues, rowIndex=index))
    return events


def convertToEvent(columnValues: List[str], rowIndex: int) -> Event:
    event = Event()
    event.id = rowIndex
    event.team = columnValues[0]
    event.type = columnValues[1]
    event.subtype = columnValues[2]
    event.period = int(columnValues[3])
    event.startFrame = int(columnValues[4])
    event.startTime = float(columnValues[5])
    event.endFrame = int(columnValues[6])
    event.endTime = float(columnValues[7])
    event.origin = columnValues[8]
    event.target = columnValues[9]
    event.start = Coordinates(float(columnValues[10]), float(columnValues[11]))
    event.end = Coordinates(float(columnValues[12]), float(columnValues[13]))
    return event


def categorizeEvents(allEventData):
    events = Events()
    for index, event in enumerate(allEventData):
        if event is not None and event.type != CHALLENGE:
            events.allEvents.append(event)
        elif event is not None and event.type == CHALLENGE:
            challengeObject = bundleChallengeEvents(index, allEventData)
            events.challenges.append(challengeObject)
            events.allEvents.append(challengeObject)
            if challengeObject.fault:
                events.faults.append(challengeObject)
        else:
            continue
        if event.type == SHOT:
            events.shots.append(event)
        elif event.type == PASS:
            events.passes.append(event)
        elif event.subtype == FREE_KICK:
            event.start = findSetPieceCoordinates(event, allEventData)
            events.freekicks.append(event)
        elif event.subtype == THROW_IN:
            event.start = findSetPieceCoordinates(event, allEventData)
            events.throwins.append(event)
        elif event.subtype == KICK_OFF:
            event.start = findSetPieceCoordinates(event, allEventData)
            events.kickoffs.append(event)
        elif event.subtype == CORNER_KICK:
            event.start = findSetPieceCoordinates(event, allEventData)
            events.corners.append(event)
        elif event.type == BALL_OUT:
            events.ballouts.append(event)
        elif event.type == CARD:
            events.cards.append(event)
        elif event.type == BALL_LOST:
            events.ballLostEvents.append(event)
        elif event.type == RECOVERY:
            events.recovery.append(event)
    return events
