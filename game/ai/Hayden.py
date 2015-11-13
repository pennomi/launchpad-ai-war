import random
from game.bot import Bot, Actions
__author__ = 'Davin'

class BoringBot(Bot):
    """Walk in a square and do nothing."""
    def update(self, tick_number, visible_objects):
        print(visible_objects)
        if tick_number % 3:
            return Actions.MoveForward
        return Actions.TurnLeft


class LazyBot(Bot):
    """Walk in a square and do nothing."""
    def update(self, tick_number, visible_objects):
        return Actions.DoNothing
