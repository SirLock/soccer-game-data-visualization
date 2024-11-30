CHALLENGE_LEADING_TO_SHOT = 'challenge_leading_to_shot'
ATTACKS_FROM_RIGHT_HALF_RIGHT_SIDE = 'attack_from_right_half_right_side'
ATTACKS_FROM_RIGHT_HALF_CENTER = 'attack_from_right_half_center'
ATTACKS_THROUGH_TOP = 'attacks_through_top'
ATTACKS_THROUGH_CENTER = 'attacks_through_center'
ATTACKS_THROUGH_BOTTOM = 'attacks_through_bottom'
COUNTERS_RIGHT_TO_LEFT = 'counters_right_to_left'
COUNTERS_LEFT_TO_RIGHT = 'counters_left_to_right'
COUNTERS = 'counters'
GOAL = 'goal'
CORNER = 'corner'
FREE_KICK = 'free_kick'
SHOT = 'shot'
FAULT = 'fault'
OFFSIDE = 'offside'


class Situation:
    def __init__(self, startFrame: int, endFrame: int, period: int, team: str, kind: str):
        self.startFrame = startFrame
        self.endFrame = endFrame
        self.period = period
        self.team = team
        self.kind = kind

