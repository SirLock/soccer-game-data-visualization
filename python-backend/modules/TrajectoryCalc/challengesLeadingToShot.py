from models.events import *

from models.situation import Situation, CHALLENGE_LEADING_TO_SHOT

def challengesLeadingToShot(eventData: Events(), timespan) -> List[Situation]:
    challengeList = []
    shots = eventData.shots
    challenges = eventData.challenges
    for shot in shots:
        shotTime = shot.startTime
        for challenge in challenges:
            challengeTime = challenge.startTime
            if challengeTime > shotTime:
                break
            isChallengeBeforeShot = challengeTime >= shotTime - timespan
            if isChallengeBeforeShot:
                challengeList.append(Situation(startFrame=challenge.startFrame, endFrame=shot.endFrame,
                                               period=challenge.period, team=shot.team,
                                               kind=CHALLENGE_LEADING_TO_SHOT))
    return challengeList