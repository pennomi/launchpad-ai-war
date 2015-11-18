import random
from game.bot import Bot, Actions

__author__ = 'Stoney'

class CheeseBot(Bot):
    #moves = [Actions.MoveBackward, Actions.MoveForward, Actions.StrafeLeft, Actions.StrafeRight]
    target = None
    closest = None

    def update(self, tick_number, visible_objects):

        if visible_objects:
            return Actions.MoveForward

        return Actions.TurnLeft

    def scan(self, visible_objects):
        if visible_objects:
            for v in visible_objects:
                if v.getPosition() - self.get_direction() < self.closest:
                    self.closest = v;
        else:
            return Actions.TurnLeft




