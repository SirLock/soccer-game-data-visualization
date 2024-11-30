class ShotAttributes:
    def __init__(self, frame, time, angle, distance, teammates, opponents, leadsToGoal, keeper, direction):
        self.frame = frame
        self.time = time
        self.angle = angle
        self.distance = distance
        self.teammates = teammates
        self.opponents = opponents
        self.leadsToGoal = leadsToGoal
        self.keeper = keeper
        self.direction = direction


class FreekickAttributes:
    def __init__(self, frame, time, angle, distance, teammates, opponents, leadsToGoal, direction):
        self.frame = frame
        self.time = time
        self.angle = angle
        self.distance = distance
        self.teammates = teammates
        self.opponents = opponents
        self.leadsToGoal = leadsToGoal
        self.direction = direction


class CornerkickAttributes:
    def __init__(self, frame, time, players, leadsToGoal, direction):
        self.frame = frame
        self.time = time
        self.players = players
        self.leadsToGoal = leadsToGoal
        self.direction = direction


class ThrowinAttributes:
    def __init__(self, frame, time, distance, leadsToGoal, direction):
        self.frame = frame
        self.time = time
        self.distance = distance
        self.leadsToGoal = leadsToGoal
        self.direction = direction


class KickoffAttributes:
    def __init__(self, frame, time, direction):
        self.frame = frame
        self.time = time
        self.direction = direction
