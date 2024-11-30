from models.challenges import *
from constants.columnAndFieldNames import *


def isWonChallenge(challenge):
    result = challenge.subtype.find("WON") >= 0
    return result


def isLostChallenge(challenge):
    result = challenge.subtype.find("LOST") >= 0
    return result


def findChallengeSubtype(challenge):
    subtype = None
    if challenge.subtype.find("GROUND") >= 0:
        subtype = "GROUND"
    elif challenge.subtype.find("AERIAL") >= 0:
        subtype = "AERIAL"
    elif challenge.subtype.find("TACKLE") >= 0:
        subtype = "TACKLE"
    elif challenge.subtype.find("DRIBBLE") >= 0:
        subtype = "DRIBBLE"
    return subtype


def determineFaultState(rawChallenge):
    fault = False
    if rawChallenge.subtype.find("FAULT") >= 0:
        fault = True
    return fault

def challengeBundleCondition(challenge1, challenge2):
    isBundle = False
    if challenge1.type == CHALLENGE and challenge2.type == CHALLENGE:
        challenge1Won = isWonChallenge(challenge1)
        challenge2Lost = isLostChallenge(challenge2)
        challenge1Lost = isLostChallenge(challenge1)
        challenge2Won = isWonChallenge(challenge2)
        if challenge1Won and challenge2Lost:
            isBundle = True
        elif challenge1Lost and challenge2Won:
            isBundle = True
    return isBundle


def bundleChallengeEvents(index, rawEvents):
    challengeObject = Challenge()
    challenge = rawEvents[index]
    nextChallenge = None

    nextChallengeFound = False
    searchMargin = 25
    i = index + 1
    while not nextChallengeFound and (
            rawEvents[i].startFrame < challenge.startFrame + searchMargin
            or challengeBundleCondition(challenge, rawEvents[i])
    ):
        if rawEvents[i].type == CHALLENGE:
            nextChallenge = rawEvents[i]
            rawEvents[i] = None
            nextChallengeFound = True
        else:
            i += 1

    challengeObject.team = challenge.team
    challengeObject.period = challenge.period
    challengeObject.startFrame = challenge.startFrame
    challengeObject.endFrame = challengeObject.startFrame
    challengeObject.startTime = challenge.startTime
    challengeObject.endTime = challengeObject.startTime
    challengeObject.start = challenge.start
    challengeObject.end = challengeObject.start
    challengeObject.type = CHALLENGE
    challengeObject.subtype = challenge.subtype
    challengeObject.challengeType = findChallengeSubtype(challenge)
    challengeObject.fault = determineFaultState(challenge)

    if nextChallenge is not None:
        if isWonChallenge(challenge):
            challengeObject.origin = challenge.origin
            if isLostChallenge(nextChallenge):
                challengeObject.target = nextChallenge.origin
        elif isLostChallenge(challenge):
            challengeObject.target = challenge.origin
            if isWonChallenge(nextChallenge):
                challengeObject.origin = nextChallenge.origin
    else:
        if isWonChallenge(challenge):
            challengeObject.origin = challenge.origin
            challengeObject.target = None
        elif isLostChallenge(challenge):
            challengeObject.target = challenge.origin
            challengeObject.origin = None

    return challengeObject