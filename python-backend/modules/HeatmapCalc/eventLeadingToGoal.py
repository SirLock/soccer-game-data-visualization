from modules.gameDataManager import *


def doesEventLeadToGoal(event: Event) -> float:
    timeFrameSeconds = 120
    timeToNextGoal = -1
    dataSetId = getSelectedGameData()
    data = getGameDataSet(dataSetId)

    if eventIsGoal(event):
        return 0.0
    followingEvents = getFollowingEvents(event, data.events.allEvents, timeFrameSeconds * 25)

    for fEvent in followingEvents:
        if eventIsGoal(fEvent):
            timeToNextGoal = fEvent.startTime - event.startTime
            break
    return timeToNextGoal


def getFollowingEvents(event: Event, events: List[Event], searchRange: int) -> List[Event]:
    eventFrame = event.startFrame
    eventIndex = 0
    for tmpEvent in events:
        if tmpEvent == event:
            break
        eventIndex += 1

    followingEvents = []
    while eventIndex + 2 <= len(events) and events[eventIndex + 1].startFrame <= (eventFrame + searchRange):
        eventIndex += 1
        followingEvents.append(events[eventIndex])

    return followingEvents


def eventIsGoal(event: Event) -> bool:
    if event.type == SHOT and event.subtype.find("GOAL") >= 0:
        return True
    return False