import json
from typing import List
from models.frameElement import *
from models.events import Events
from models.player import Player


class GameData:
    def __init__(self):
        self.id: str
        self.basicInformation: dict[str, any]
        self.trackingHome: List[FrameElement] = []
        self.trackingAway: List[FrameElement] = []
        self.traveledDistancesHome: dict[str, dict]
        self.traveledDistancesAway: dict[str, dict]
        self.playersHome: dict[str, Player]
        self.playersAway: dict[str, Player]
        self.events: Events
        self.asJson: str = None

    def toJSON(self):
        if self.asJson:
            return self.asJson
        self.asJson = json.dumps(self, default=lambda o: o.__dict__)
        return self.asJson
