from models.coordinates import Coordinates


class FrameElement:
    def __init__(self) -> None:
        self.period: int
        self.frame: int
        self.time: float
        self.coordinates: dict[str, Coordinates]
