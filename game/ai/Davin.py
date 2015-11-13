import math
from game.bot import Bot, Actions
from panda3d.core import Vec3, NodePath

__author__ = 'Davin'


def getEnemies(bot):
     for v in bot.visible_objects:
         if  not v in bot.team:
             return v


class TrackerHalelujiaBossBot1(Bot):
    """Walk in a square and do nothing."""
    def update(self, tick_number, visible_objects):
        for v in visible_objects:
            if v.get_position() == self.get_position() + self.get_direction():
                return Actions.Punch
            if v.get_position() == self.get_position() + 3 and v.get_direction() == self.get_direction()-180:
                return Actions.TurnAround
            if v.get_position() == self.get_position()+3:
                distance = v.get_direction() - self.get_direction()

                return Actions.TurnAround

        if visible_objects:
            return Actions.MoveForward

        return Actions.TurnLeft




class SentryBot2(Bot):
    """pace back and forth and kill anything found."""
    def update(self, tick_number, visible_objects):
        for v in visible_objects:
            if v.get_position() == self.get_position() + self.get_direction():

                return Actions.Punch

        if visible_objects:
            return Actions.MoveForward

        return Actions.TurnAround


class GimickBot(Bot):
    MOVES = (Actions.TurnLeft, Actions.MoveBackward, Actions.TurnAround, Actions.Punch, Actions.MoveForward, Actions.TurnRight, Actions.MoveBackward, Actions.TurnLeft, Actions.TurnAround, Actions.Punch)
    x = -1
    """Ten successive moves"""
    def update(self, tick_number, visible_objects):
        for v in visible_objects:
            if v.get_position() == self.get_position() + self.get_direction():
                return Actions.Punch

        if visible_objects:
            self.x += 1
            self.x %= len(self.MOVES) - 1

            return self.MOVES[self.x]

        return Actions.TurnLeft


class SpinBot(Bot):

    """Ten successive moves"""
    def update(self, tick_number, visible_objects):
        for v in visible_objects:
            v._death_played()
            if v.get_position() == self.get_position() + self.get_direction():
                return Actions.Punch

        return Actions.TurnLeft


# class SpinBot2(Bot):
#
#     """Ten successive moves"""
#     def update(self, tick_number, visible_objects):
#         for v in visible_objects:
#             if v.get_position() == self.get_position() + self.get_direction():
#                 return Actions.Punch
#
#         return Actions.TurnLeft
#
#
#
# class SpinBot3(Bot):
#
#     """Ten successive moves"""
#     def update(self, tick_number, visible_objects):
#         for v in visible_objects:
#             if v.get_position() == self.get_position() + self.get_direction():
#                 return Actions.Punch
#
#         return Actions.TurnLeft
