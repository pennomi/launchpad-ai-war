# import math
# from game.bot import Bot, Actions
# from game.bot import Bot, Actions
# from panda3d.core import Vec3, NodePath
#
# class MarksBot(Bot):
#     def update(self, tick_number, visible_objects):
#         for v in visible_objects:
#             if v.get_position() == self.get_position() + self.get_direction():
#                 return Actions.Punch
#
#
#         if visible_objects:
#             return Actions.MoveForward
#         return Actions.TurnLeft
#
