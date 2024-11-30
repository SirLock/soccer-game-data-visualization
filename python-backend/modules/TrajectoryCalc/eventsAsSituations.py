from models.events import *
from constants.columnAndFieldNames import *
from models.situation import Situation, GOAL, CORNER, FREE_KICK, FAULT, SHOT, OFFSIDE


def goalsToSituations(eventData: Events(), timespanBeforeStart, timespanAfterStart) -> List[Situation]:
    goalList = []
    shots = eventData.shots
    for shot in shots:
        if shot.subtype.find("ON TARGET-GOAL") >= 0:
            goalList.append(
                Situation(startFrame=shot.startFrame - timespanBeforeStart, endFrame=shot.endFrame + timespanAfterStart,
                          period=shot.period, team=shot.team,
                          kind=GOAL))
    return goalList


def shotsToSituations(eventData: Events(), timespanBeforeStart, timespanAfterStart) -> List[Situation]:
    shotList = []
    shots = eventData.shots
    for shot in shots:
        shotList.append(
            Situation(startFrame=shot.startFrame - timespanBeforeStart, endFrame=shot.endFrame + timespanAfterStart,
                      period=shot.period, team=shot.team,
                      kind=SHOT))
    return shotList


def cornersToSituations(eventData: Events(), timespanBeforeStart, timespanAfterStart) -> List[Situation]:
    cornerList = []
    corners = eventData.corners
    for corner in corners:
        cornerList.append(
            Situation(startFrame=corner.startFrame - timespanBeforeStart, endFrame=corner.endFrame + timespanAfterStart,
                      period=corner.period, team=corner.team,
                      kind=CORNER))
    return cornerList


def freeKicksToSituations(eventData: Events(), timespanBeforeStart, timespanAfterStart) -> List[Situation]:
    freeKickList = []
    freeKicks = eventData.freekicks
    for freeKick in freeKicks:
        freeKickList.append(Situation(startFrame=freeKick.startFrame - timespanBeforeStart,
                                      endFrame=freeKick.endFrame + timespanAfterStart,
                                      period=freeKick.period, team=freeKick.team,
                                      kind=FREE_KICK))
    return freeKickList


def faultsToSituations(eventData: Events(), timespanBeforeStart, timespanAfterStart) -> List[Situation]:
    faultList = []
    challenges = eventData.challenges
    for challenge in challenges:
        if challenge.fault:
            faultList.append(Situation(startFrame=challenge.startFrame - timespanBeforeStart,
                                       endFrame=challenge.endFrame + timespanAfterStart,
                                       period=challenge.period, team=challenge.team,
                                       kind=FAULT))
    return faultList


def offsidesToSituations(eventData: Events(), timespanBeforeStart, timespanAfterStart) -> List[Situation]:
    offsideList = []
    events = eventData.events
    for event in events:
        if event.subtype.find("OFFSIDE") >= 0:
            offsideList.append(Situation(startFrame=event.startFrame - timespanBeforeStart,
                                         endFrame=event.endFrame + timespanAfterStart,
                                         period=event.period, team=event.team,
                                         kind=OFFSIDE))
    return offsideList
