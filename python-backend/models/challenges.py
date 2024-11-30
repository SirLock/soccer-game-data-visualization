from models.coordinates import Coordinates

class Challenge:
    def __init__(self):
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
        self.fault: bool
        self.challengeType: str