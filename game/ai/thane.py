import random
import math
from game.bot import Bot, Actions


class BoringBot(Bot):
    """Walk in a square and do nothing."""
    def update(self, tick_number, visible_objects):
        if tick_number % 3:
            return Actions.MoveForward
        return Actions.TurnLeft


class LazyBot(Bot):
    """Walk in a square and do nothing."""
    def update(self, tick_number, visible_objects):
        return Actions.Punch


class ZeroBot(Bot):
    """Do everything except Suicide."""
    def update(self, tick_number, visible_objects):
        p = self.get_position()
        v = self.get_direction()
        if p.x != 0:
            if math.copysign(1, p.x) != -math.copysign(1, v.x):
                return
        elif p
        return random.choice(list(Actions)[:-1])
