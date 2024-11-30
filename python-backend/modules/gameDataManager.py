from modules.dataImport import *

GAME_DATA_SETS: dict[str, GameData] = dict()

game_data_sets_config = [
    {
        "setId": "sample_game_1",
        "trackingDataHome": "../gameData/Sample_Game_1/Sample_Game_1_RawTrackingData_Home_Team.csv",
        "trackingDataAway": "../gameData/Sample_Game_1/Sample_Game_1_RawTrackingData_Away_Team.csv",
        "events": "../gameData/Sample_Game_1/Sample_Game_1_RawEventsData.csv"
    },
    {
       "setId": "sample_game_2",
       "trackingDataHome": "../gameData/Sample_Game_2/Sample_Game_2_RawTrackingData_Home_Team.csv",
       "trackingDataAway": "../gameData/Sample_Game_2/Sample_Game_2_RawTrackingData_Away_Team.csv",
       "events": "../gameData/Sample_Game_2/Sample_Game_2_RawEventsData.csv"
    }
]

selectedGameDataSet = ""


def getGameDataSet(dataSetId):
    setSelectedGameData(dataSetId)
    return GAME_DATA_SETS.get(dataSetId)


def initGameDataManager():
    delimiter = ','
    for config in game_data_sets_config:
        setId = config.get("setId")
        gameData = importGameData(
            setId,
            config.get("trackingDataHome"),
            config.get("trackingDataAway"),
            config.get("events"),
            delimiter
        )
        basicInfo = getBasicInformation(gameData.events.allEvents)
        gameData.basicInformation = basicInfo
        GAME_DATA_SETS.update({
            setId: gameData
        })


def getBasicInformation(allEvents: List[Event]) -> dict:
    basicInfo = dict()
    basicInfo.update(getHalfEndAndNextStartFrame(allEvents))
    return basicInfo


def getHalfEndAndNextStartFrame(allEvents):
    index = 0
    length = len(allEvents)
    indexSearchOffset = 20
    while allEvents[index].period == 1 and index < length - 1:
        index += 1
    if index == len(allEvents):
        print("getHalfEndAndNextStartFrame: No second period found in event data!")
        return None
    while (allEvents[index].subtype.find('END HALF') > -1) and (index > index - indexSearchOffset):
        index -= 1
    if allEvents[index].subtype.find('END HALF') > -1:
        print("getHalfEndAndNextStartFrame: END HALF not found in event data!")
        return None
    firstPeriodEnd = allEvents[index].startFrame
    while allEvents[index].type != 'SET PIECE' and index < length:
        index += 1
    secondPeriodStart = allEvents[index].startFrame
    return {'firstPeriodEnd': firstPeriodEnd, 'secondPeriodStart': secondPeriodStart}


def getSelectedGameData():
    return selectedGameDataSet


def setSelectedGameData(dataSetId):
    global selectedGameDataSet
    selectedGameDataSet = dataSetId
