from typing import List
from models.coordinates import Coordinates
from models.challenges import Challenge


class Event:
    def __init__(self):
        self.id: int
        self.team: str
        self.type: str
        self.subtype: str
        self.period: int
        self.startFrame: int
        self.startTime: float
        self.endFrame: int
        self.endTime: float
        self.origin: str
        self.target: str
        self.start: Coordinates
        self.end: Coordinates


class Events:
    def __init__(self):
        self.allEvents = []
        self.shots = []
        self.passes = []
        self.challenges: List[Challenge] = []
        self.freekicks = []
        self.throwins = []
        self.kickoffs = []
        self.corners = []
        self.ballouts = []
        self.faults: List[Challenge] = []
        self.cards = []
        self.ballLostEvents = []
        self.recovery = []
