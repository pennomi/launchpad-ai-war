import math
from game.bot import Bot, Actions


class BoringBot(Bot):
    """Walk in a square and do nothing."""
    def update(self, tick_number, visible_objects):
        if tick_number % 3:
            return Actions.MoveForward
        return Actions.TurnLeft


class LazyBot(Bot):
    """Just punch stuff."""
    def update(self, tick_number, visible_objects):
        return Actions.Punch


class ZeroBot(Bot):
    """Try to get to the center of the board."""
    def update(self, tick_number, visible_objects):
        p = self.get_position()
        v = self.get_direction()
        if p.x != 0:
            if v.x != 0 and math.copysign(1, p.x) == -math.copysign(1, v.x):
                return Actions.MoveForward
            else:
                return Actions.TurnLeft
        elif p.y != 0:
            if v.y != 0 and math.copysign(1, p.y) == -math.copysign(1, v.y):
                return Actions.MoveForward
            else:
                return Actions.TurnLeft
        return Actions.Punch
