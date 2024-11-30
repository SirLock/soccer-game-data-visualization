from flask import Flask, json, Response
from flask_cors import CORS

from models.requestExceptions import InvalidRequest, invalidRequest
from modules.HeatmapCalc.calculateEventAttributes import *
from modules.TrajectoryCalc.challengesLeadingToShot import *
from modules.TrajectoryCalc.attackThroughFieldPart import *
from modules.TrajectoryCalc.detectCounters import *
from modules.TrajectoryCalc.filters import *
from modules.TrajectoryCalc.eventsAsSituations import *

SOCCER_SERVER = Flask(__name__)
CORS(SOCCER_SERVER)

initGameDataManager()


def toJson(dataStructure) -> str:
    return json.dumps(dataStructure, default=lambda o: o.__dict__)


@SOCCER_SERVER.errorhandler(InvalidRequest)
def triggerInvalidRequest(exception):
    return invalidRequest(exception)


#################
# REST interfaces


@SOCCER_SERVER.route("/get-basic-game-information/<dataSetId>")
def getBasicGameInformation(dataSetId: str):
    return toJson(getGameDataSet(dataSetId).basicInformation)


@SOCCER_SERVER.route("/get-events-of/<dataSetId>")
def getEventsOf(dataSetId: str):
    return toJson(getGameDataSet(dataSetId).events)


@SOCCER_SERVER.route("/get-players-of/<params>")
def getPlayersOf(params: str):
    parameters = params.split('$')
    dataSetId = parameters[0]
    team = parameters[1]
    gameData = getGameDataSet(dataSetId)
    if team == "away":
        return toJson(gameData.playersAway)
    elif team == "home":
        return toJson(gameData.playersHome)
    else:
        errorString = f"No players found for data set: {dataSetId} and team: {team}."
        raise InvalidRequest(errorString)


@SOCCER_SERVER.route("/get-tracking-data-of/<params>")
def getTrackingDataOf(params: str):
    parameters = params.split('$')
    dataSetId = parameters[0]
    team = parameters[1]
    gameData = getGameDataSet(dataSetId)
    if team == "away":
        return toJson(gameData.trackingAway)
    elif team == "home":
        return toJson(gameData.trackingHome)
    else:
        errorString = f"No tracking data found for data set: {dataSetId} and team: {team}."
        raise InvalidRequest(errorString)


@SOCCER_SERVER.route("/get-basic-game-data/<dataSetId>")
def gameDataSetRequest(dataSetId: str):
    data = getGameDataSet(dataSetId)
    return data.toJSON()


@SOCCER_SERVER.route("/get-challenges-leading-to-shot/<dataSetId>")
def getChallengesToShotRequest(dataSetId: str):
    data = getGameDataSet(dataSetId)
    events = data.events
    challenges = challengesLeadingToShot(events, 15)
    return json.dumps(challenges, default=lambda o: o.__dict__)


@SOCCER_SERVER.route("/get-counters/<dataSetId>")
def getCountersRequest(dataSetId: str):
    data = getGameDataSet(dataSetId)
    events = data.events
    counters = detectCounters(events, 25 * 20)
    return json.dumps(counters, default=lambda o: o.__dict__)


@SOCCER_SERVER.route("/get-goals/<dataSetId>")
def getGoals(dataSetId: str):
    data = getGameDataSet(dataSetId)
    events = data.events
    goals = goalsToSituations(events, 25 * 15, 0)
    return json.dumps(goals, default=lambda o: o.__dict__)


@SOCCER_SERVER.route("/get-shots/<dataSetId>")
def getShots(dataSetId: str):
    data = getGameDataSet(dataSetId)
    events = data.events
    shots = shotsToSituations(events, 25 * 15, 0)
    return json.dumps(shots, default=lambda o: o.__dict__)


@SOCCER_SERVER.route("/get-faults/<dataSetId>")
def getFaults(dataSetId: str):
    data = getGameDataSet(dataSetId)
    events = data.events
    faults = faultsToSituations(events, 25 * 15, 0)
    return json.dumps(faults, default=lambda o: o.__dict__)


@SOCCER_SERVER.route("/get-corners/<dataSetId>")
def getCorners(dataSetId: str):
    data = getGameDataSet(dataSetId)
    events = data.events
    corners = cornersToSituations(events, 0, 25 * 10)
    return json.dumps(corners, default=lambda o: o.__dict__)


@SOCCER_SERVER.route("/get-free-kicks/<dataSetId>")
def getFreeKicks(dataSetId: str):
    data = getGameDataSet(dataSetId)
    events = data.events
    freeKicks = freeKicksToSituations(events, 0, 25 * 10)
    return json.dumps(freeKicks, default=lambda o: o.__dict__)


@SOCCER_SERVER.route("/get-attack-through-field-part/<dataSetId>/<fieldPartName>")
def getAttacksThroughFieldPartRequest(dataSetId: str, fieldPartName: str):
    data = getGameDataSet(dataSetId)
    result = attackThroughFieldPart(data, fieldPartName)
    return Response(json.dumps(result, default=lambda o: o.__dict__), mimetype="application/json")


@SOCCER_SERVER.route("/get-passes-within/<params>")
def getPassesWithinRequest(params: str):
    parameters = params.split('$')
    dataSetId = parameters[0]
    startFrame = int(parameters[1])
    endFrame = int(parameters[2])
    events = getGameDataSet(dataSetId).events
    passes = filterWithin(events.passes, startFrame, endFrame)
    return json.dumps(passes, default=lambda o: o.__dict__)


@SOCCER_SERVER.route("/get-events-within/<params>")
def getEventsWithinRequest(params: str):
    parameters = params.split('$')
    dataSetId = parameters[0]
    startFrame = int(parameters[1])
    endFrame = int(parameters[2])
    events = getGameDataSet(dataSetId).events.allEvents
    eventsWithin = filterWithin(events, startFrame, endFrame)
    return json.dumps(eventsWithin, default=lambda o: o.__dict__)


@SOCCER_SERVER.route("/get-shots-on-target/<dataSetId>")
def getShotsOnTargetRequest(dataSetId: str):
    data = getGameDataSet(dataSetId)
    events = data.events
    shots = shotsOnTarget(events)
    return json.dumps(shots, default=lambda o: o.__dict__)


@SOCCER_SERVER.route(
    "/get-relevant-players-by-distance/<dataSetId>/<teamId>/<startFrame>/<endFrame>/<relevantDistance>")
def getRelevantPlayersByDistance(dataSetId: str, teamId: str, startFrame: int, endFrame: int, relevantDistance: float):
    gameData = getGameDataSet(dataSetId)
    if teamId == 'away':
        trackingData = gameData.trackingAway
    elif teamId == 'home':
        trackingData = gameData.trackingHome
    else:
        return json.dumps([], default=lambda o: o.__dict__)
    relevantPlayers = filterForRelevantPlayersByDistance(trackingData, int(startFrame),
                                                         int(endFrame), float(relevantDistance))
    return json.dumps(relevantPlayers, default=lambda o: o.__dict__)


@SOCCER_SERVER.route("/get-relevant-players-by-pass-participation/<params>")
def getRelevantPlayersByPassParticipation(params: str):
    parameters = params.split('$')
    dataSetID = parameters[0]
    startFrame = int(parameters[1])
    endFrame = int(parameters[2])
    trackingData = getattr(getGameDataSet(dataSetID), 'events')
    relevantPlayers = filterForRelevantPlayersByPassParticipation(trackingData, startFrame, endFrame)
    return json.dumps(relevantPlayers, default=lambda o: o.__dict__)


@SOCCER_SERVER.route("/get-event-attributes/<params>")
def getEventAttributes(params: str):
    parameters = params.split('$')
    dataSetId = parameters[0]
    eventType = parameters[1]
    team = parameters[2]
    setSelectedGameData(dataSetId)
    attributes = calculateEventAttributes(eventType, team)
    return json.dumps(attributes, default=lambda o: o.__dict__)


@SOCCER_SERVER.route("/get-position-data/<params>")
def getPositionData(params: str):
    parameters = params.split('$')
    dataSetId = parameters[0]
    frames = parameters[1].split(',')

    gameData = getGameDataSet(dataSetId)

    dataHome = []
    dataAway = []
    for frame in frames:
        frame = int(frame)
        dataHome.append(gameData.trackingHome[frame].coordinates)
        dataAway.append(gameData.trackingAway[frame].coordinates)

    positionData = [dataHome, dataAway]
    return json.dumps(positionData, default=lambda o: o.__dict__)


@SOCCER_SERVER.route("/get-traveled-distances/<dataSetId>")
def getTraveledDistances(dataSetId: str):
    gameData = getGameDataSet(dataSetId)

    traveledDistances = {'home': gameData.traveledDistancesHome, 'away': gameData.traveledDistancesAway}
    return json.dumps(traveledDistances, default=lambda o: o.__dict__)
