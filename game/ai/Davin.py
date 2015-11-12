import random
from game.bot import Bot, Actions
from panda3d.core import Vec3, NodePath

__author__ = 'Davin'


# class SentryBot1(Bot):
#     """Walk in a square and do nothing."""
#     def update(self, tick_number, visible_objects):
#         print(visible_objects)
#         if tick_number % 3:
#             return Actions.MoveForward
#
#         return Actions.TurnAround
#
#
class SentryBot2(Bot):
    """Walk in a square and do nothing."""
    def update(self, tick_number, visible_objects):
        print(visible_objects)
        if tick_number % 3:
            return Actions.MoveForward

        return Actions.TurnAround


class Trackbot1(Bot):
    """Walk in a square and do nothing."""
    def update(self, tick_number, visible_objects):
        Trackbot2._model = NodePath('bot')
        Trackbot2.__model.getPos()

        print(visible_objects)
        if tick_number % 3:
            return Actions.MoveForward

        return Actions.TurnLeft


class Trackbot2():
    """Walk in a square and do nothing."""
    def update(self, tick_number, visible_objects):
        Trackbot1._model = NodePath('bot')
        Trackbot1.__model.getPos()

        print(visible_objects)
        if tick_number % 3:
            return Actions.MoveForward

        return Actions.TurnLeft


class GimickBot(Bot):
    MOVES = (Actions.TurnLeft, Actions.MoveBackward, Actions.TurnAround, Actions.Punch, Actions.MoveForward, Actions.TurnRight, Actions.MoveBackward, Actions.TurnLeft, Actions.TurnAround, Actions.Punch)
    x = -1
    """Ten successive moves"""
    def update(self, tick_number, visible_objects):
        self.x += 1
        self.x %= len(self.MOVES) - 1
        print(self.x)
        return self.MOVES[self.x]





# class ScanBot1(Bot):
#     """Walk in a square and do nothing."""
#     def update(self, tick_number, visible_objects):
#         print(visible_objects)
#         if tick_number % 3:


# class SpinBot(Bot):
#     """Walk in a square and do nothing."""
#     def update(self, tick_number, visible_objects):
#         print(visible_objects)
#         if tick_number % 1:
#             return Actions.MoveForward
#
#         return Actions.TurnLeft


# class FastBot(Bot):
#
#     """Walk in a square and do nothing."""
#     def update(self, tick_number, visible_objects):
#         new_dir = ScanBot1._model.getHpr()
#         print(visible_objects)
#         if tick_number % 1:
#             return Actions.MoveForward
#
#         new_dir -= 30
#
# class LazyBot(Bot):
#     """Walk in a square and do nothing."""
#     def update(self, tick_number, visible_objects):
#         return Actions.DoNothing
