import math
from game.bot import Bot, Actions
from game.bot import Bot, Actions
from panda3d.core import Vec3, NodePath

class MarksBot(Bot):
    def update(self, tick_number, visible_objects):
        for v in visible_objects:
            #return Actions.MoveBackward

            if v.get_position() == self.get_position() + self.get_direction():
                return Actions.TurnRight #and Actions.MoveBackward
                #return Actions.MoveBackward
                return Actions.Punch

        #if visible_objects:
        while v.get_position() == self.get_position() + 10:
            return Actions.MoveBackward

        return Actions.TurnAround

