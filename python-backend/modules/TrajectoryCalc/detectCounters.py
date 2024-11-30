from models.events import *
from models.situation import Situation, COUNTERS


def detectCounters(eventData: Events(), framespan) -> List[Situation]:
    counterList = []
    shots = []
    for shot in eventData.shots:
        shots.append(shot)
    ballLostEvents = eventData.ballLostEvents
    for ballLost in ballLostEvents:
        ballLostFrame = ballLost.endFrame
        ballLostX = ballLost.end.x
        if ballLostX is not None:
            for shot in shots:
                shotFrame = shot.startFrame
                shotX = shot.start.x
                if ballLostFrame > shotFrame:
                    continue
                isShotWithinFramespan = shotFrame <= ballLostFrame + framespan
                isCounterLeftToRight = ballLostX <= 0.6 and shotX > 0.5 and isShotWithinFramespan
                isCounterRightToLeft = ballLostX >= 0.4 and shotX <= 0.5 and isShotWithinFramespan
                if isCounterLeftToRight:
                    counterList.append(Situation(startFrame=ballLostFrame - 50, endFrame=shot.endFrame,
                                                 period=shot.period, team=shot.team,
                                                 kind=COUNTERS))
                    shots.remove(shot)
                elif isCounterRightToLeft:
                    counterList.append(Situation(startFrame=ballLostFrame - 50, endFrame=shot.endFrame,
                                                 period=shot.period, team=shot.team,
                                                 kind=COUNTERS))
                    shots.remove(shot)
    return counterList
