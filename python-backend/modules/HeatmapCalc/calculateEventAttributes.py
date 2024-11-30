from modules.HeatmapCalc.eventLeadingToGoal import *
from modules.HeatmapCalc.keeperBetweenBallAndGoal import *
from modules.HeatmapCalc.freeKickCalculations import *
from modules.HeatmapCalc.playersInFrontOfGoalCorner import *
from modules.HeatmapCalc.throwInDistanceToGoal import *
from modules.HeatmapCalc.getPlayDirection import *


def calculateEventAttributes(eventType: str, team: str):
    attributes = []
    if eventType == "shot":
        attributes = calculateShotAttributes(team)
    if eventType == "freekick":
        attributes = calculateFreekickAttributes(team)
    if eventType == "corner":
        attributes = calculateCornerkickAttributes(team)
    if eventType == "throwin":
        attributes = calculateThrowinAttributes(team)
    if eventType == "kickoff":
        attributes = calculateKickoffAttributes(team)
    return attributes


def calculateShotAttributes(currentTeam):
    dataSetId = getSelectedGameData()
    data = getGameDataSet(dataSetId)
    shots = data.events.shots
    attributes = []
    for shot in shots:
        team = shot.team
        if team == currentTeam:
            if team == "Home":
                trackingDataTeam = data.trackingHome
                trackingDataOpponents = data.trackingAway
            else:
                trackingDataTeam = data.trackingAway
                trackingDataOpponents = data.trackingHome
            frame = shot.startFrame
            time = shot.startTime / 60
            angle = angleToGoal(trackingDataTeam, shot)
            distance = distanceToGoal(shot)
            teammates = getPlayerQuantityBetweenBallAndGoal(trackingDataTeam, shot)
            opponents = getPlayerQuantityBetweenBallAndGoal(trackingDataOpponents, shot)
            leadsToGoal = doesEventLeadToGoal(shot)
            keeper = isKeeperBetweenBallAndGoal(shot)
            period = shot.period
            direction = getDirectionOfPlay(trackingDataTeam, period)
            shotAttribute = ShotAttributes(frame, time, angle, distance, teammates, opponents, leadsToGoal, keeper,
                                           direction)
            attributes.append(shotAttribute)
    return attributes


def calculateFreekickAttributes(currentTeam):
    dataSetId = getSelectedGameData()
    data = getGameDataSet(dataSetId)
    freekicks = data.events.freekicks
    attributes = []
    for freekick in freekicks:
        team = freekick.team
        if team == currentTeam:
            if team == "Home":
                trackingDataTeam = data.trackingHome
                trackingDataOpponent = data.trackingAway
            else:
                trackingDataTeam = data.trackingAway
                trackingDataOpponent = data.trackingHome
            frame = freekick.startFrame
            time = freekick.startTime / 60
            angle = angleToGoal(trackingDataTeam, freekick)
            distance = distanceToGoal(freekick)
            teammates = getPlayerQuantityBetweenBallAndGoal(trackingDataTeam, freekick)
            opponents = getPlayerQuantityBetweenBallAndGoal(trackingDataOpponent, freekick)
            leadsToGoal = doesEventLeadToGoal(freekick)
            period = freekick.period
            direction = getDirectionOfPlay(trackingDataTeam, period)
            freekickAttribute = FreekickAttributes(frame, time, angle, distance, teammates, opponents, leadsToGoal,
                                                   direction)
            attributes.append(freekickAttribute)
    return attributes


def calculateCornerkickAttributes(currentTeam):
    dataSetId = getSelectedGameData()
    data = getGameDataSet(dataSetId)
    cornerkicks = data.events.corners
    attributes = []
    for cornerkick in cornerkicks:
        team = cornerkick.team
        if team == currentTeam:
            if currentTeam == "Home":
                trackingData = data.trackingHome
            else:
                trackingData = data.trackingAway

            frame = cornerkick.startFrame
            time = cornerkick.startTime / 60
            player = playersInFrontOfGoal(cornerkick)
            leadsToGoal = doesEventLeadToGoal(cornerkick)
            direction = getDirectionOfPlay(trackingData, cornerkick.period)
            cornerkickAttribute = CornerkickAttributes(frame, time, player, leadsToGoal, direction)
            attributes.append(cornerkickAttribute)
    return attributes


def calculateThrowinAttributes(currentTeam):
    dataSetId = getSelectedGameData()
    data = getGameDataSet(dataSetId)
    throwins = data.events.throwins
    attributes = []
    for throwin in throwins:
        team = throwin.team
        if team == currentTeam:
            if team == "Home":
                trackingData = data.trackingHome
            else:
                trackingData = data.trackingAway
            frame = throwin.startFrame
            time = throwin.startTime / 60
            distance = throwInDistanceToGoal(throwin, trackingData)
            leadsToGoal = doesEventLeadToGoal(throwin)
            period = throwin.period
            direction = getDirectionOfPlay(trackingData, period)
            throwinAttribute = ThrowinAttributes(frame, time, distance, leadsToGoal, direction)
            attributes.append(throwinAttribute)
    return attributes


def calculateKickoffAttributes(currentTeam):
    dataSetId = getSelectedGameData()
    data = getGameDataSet(dataSetId)
    kickoffs = data.events.kickoffs
    attributes = []
    for kickoff in kickoffs:
        team = kickoff.team
        if team == currentTeam:
            if team == "Home":
                trackingData = data.trackingHome
            else:
                trackingData = data.trackingAway
            frame = kickoff.startFrame
            time = kickoff.startTime / 60
            period = kickoff.period
            direction = getDirectionOfPlay(trackingData, period)
            kickoffAttribute = KickoffAttributes(frame, time, direction)
            attributes.append(kickoffAttribute)
    return attributes
