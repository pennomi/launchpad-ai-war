import math
from game.bot import Bot, Actions
from game.bot import Bot, Actions
from panda3d.core import Vec3, NodePath

class MarksBot(Bot):
    def update(self, tick_number, visible_objects):
        for v in visible_objects:
            #return Actions.MoveBackward

            if v.position == self.position + self.direction:
                return Actions.TurnRight #and Actions.MoveBackward
                #return Actions.MoveBackward
                return Actions.Punch

        #if visible_objects:
        while v.position == self.position + 10:
            return Actions.MoveBackward

        return Actions.TurnAround

