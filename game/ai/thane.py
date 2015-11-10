import random
from game.bot import Bot, Actions


class BoringBot(Bot):
    """Walk in a square and do nothing."""
    def update(self, tick_number):
        if tick_number % 2:
            return Actions.MoveForward
        return Actions.TurnLeft


class RandomBot(Bot):
    """Walk in a square and do nothing."""
    def update(self, tick_number):
        return random.choice(list(Actions)[:-1])
