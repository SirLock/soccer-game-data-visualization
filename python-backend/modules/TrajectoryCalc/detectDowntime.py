from models.events import *
from constants.columnAndFieldNames import *

def detectDowntimeBallOut(eventList, downTimeList, loopCounter, event):
    startTime = event.startTime
    if loopCounter + 1 >= len(eventList):
        return
    nextEvent = eventList[loopCounter + 1]
    endTime = nextEvent.endTime
    downTime = endTime - startTime
    downTimeList.append({
        "start": startTime,
        "end": endTime,
        "totalDowntime": downTime,
        "causedByPlayer": event.origin,
        "eventType": event.type,
        "eventSubtype": event.subtype,
        "nextEventType": nextEvent.type,
        "nextEventSubtype": nextEvent.subtype
    })


def detectDowntimeFaults(eventList, downTimeList, loopCounter, event):
    startTime = event.startTime
    searchMargin = 5
    j = loopCounter + 1
    while j <= loopCounter + searchMargin:
        if j < len(eventList):
            if eventList[j].type == SET_PIECE:
                nextEvent = eventList[j]
                endTime = nextEvent.endTime
                downTime = endTime - startTime
                downTimeList.append({
                    "start": startTime,
                    "end": endTime,
                    "totalDowntime": downTime,
                    "causedByPlayer": event.origin,
                    "eventType": event.type,
                    "eventSubtype": event.subtype,
                    "nextEventType": nextEvent.type,
                    "nextEventSubtype": nextEvent.subtype
                })
                break
            else:
                j += 1


def detectDowntimeGoals(eventList, downTimeList, loopCounter, event):
    startTime = event.startTime
    searchMargin = 3
    j = loopCounter + 1
    while j <= loopCounter + searchMargin:
        if j < len(eventList):
            if eventList[j].subtype == KICK_OFF:
                nextEvent = eventList[j]
                endTime = nextEvent.endTime
                downTime = endTime - startTime
                downTimeList.append({
                    "start": startTime,
                    "end": endTime,
                    "totalDowntime": downTime,
                    "causedByPlayer": event.origin,
                    "eventType": event.type,
                    "eventSubtype": event.subtype,
                    "nextEventType": nextEvent.type,
                    "nextEventSubtype": nextEvent.subtype
                })
                break
            else:
                j += 1


def detectDowntime(eventData: Events()):
    downTimeList = []
    eventList = eventData.allEvents
    for i in range(len(eventList)):
        event = eventList[i]
        if event.type == BALL_OUT:
            detectDowntimeBallOut(eventList, downTimeList, i, event)
        elif event.type == CHALLENGE:
            if event.fault:
                detectDowntimeFaults(eventList, downTimeList, i, event)
        elif event.subtype.find("GOAL") >= 0:
            detectDowntimeGoals(eventList, downTimeList, i, event)
    return downTimeList