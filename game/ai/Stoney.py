import random
from game.bot import Bot, Actions

__author__ = 'Stoney'

class CheeseBot(Bot):
    #moves = [Actions.MoveBackward, Actions.MoveForward, Actions.StrafeLeft, Actions.StrafeRight]
    target = None
    closest = None

    def update(self, tick_number, visible_objects):
        if self.closest == None:
            self.getClosest(visible_objects)
        else:
            return self.attackClosest()
        return Actions.DoNothing

    def getClosest(self, visible_objects):
        if visible_objects:
            for v in visible_objects:
                if v.get_position() - self.get_direction() < self.closest:
                    self.closest = v
        else:
            return Actions.TurnLeft

    def attackClosest(self):
        p = self.closest.get_position()
        d = self.closest.get_direction()
        mep = self.get_position()
        med = self.get_direction()
        if mep - p < 2 and d == p - med:
            return Actions.DoNothing

        return Actions.Punch
