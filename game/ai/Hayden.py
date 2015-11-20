import math
import random
from game.bot import Bot, Actions

class Hayden(Bot):
    def update(self, tick_number, visible_objects):
        for v in visible_objects:
            if v.get_position() == self.get_position() + self.get_direction():
                if self.team != v.team:
                    return Actions.Punch

        for v in visible_objects:
            if self.get_position() + self.get_direction() == v.get_position() + v.get_direction():
                if self.team != v.team:
                    return Actions.DoNothing
                elif self.team == v.team:
                    return Actions.TurnAround
        nearest_bot = None
        nearest_dist = 20
        for v in visible_objects:
            distance = (v.get_position() - self.get_position()).length()
            if distance < nearest_dist:
                nearest_bot = v
                nearest_dist = distance
                return nearest_bot

        if visible_objects:
            return Actions.MoveForward

        return random.choice[Actions.TurnRight, Actions.TurnLeft]

# class trackerjacker(Bot):
#     def update(self, tick_number, visible_objects):
#         self._name_label.setScale(4, 4, 4)
#         for v in visible_objects:
#             if v.get_position() == self.get_position() + self.get_direction():
#                 return Actions.Punch
#         for v in visible_objects:
#             if self.get_position() + self.get_direction() == v.get_position() + v.get_direction():
#                 if self.team == v.team:
#                     return Actions.TurnRight
#                 else:
#                     return Actions.DoNothing
#
#         nearest_dist = 999
#         nearest_bot = None
#         for v in visible_objects:
#             distance = (v.get_position() - self.get_position()).length()
#             if distance < nearest_dist and distance != 0:
#                 nearest_bot = v
#                 nearest_dist = distance
#                 self.target = nearest_bot
#             #print(nearest_bot.__class__.__name__)
#
#         if self.target:
#             nearest_pos = self.target.get_position()
#         else:
#             nearest_pos = None
#         if not nearest_pos:
#             return Actions.TurnRight
#
#         x, y = nearest_pos.x, nearest_pos.y
#
#         my_x, my_y = self.get_position().x, self.get_position().y
#
#         dir_x = self.get_direction().x
#         dir_y = self.get_direction().y
#
#         dx = x - my_x
#         dy = y - my_y
#         if dx != 0 and dir_x != 0:
#             if math.copysign(1, dx) == math.copysign(1, dir_x):
#                 return Actions.MoveForward
#             else:
#                 return Actions.TurnAround
#         if dy != 0 and dir_y != 0:
#             if math.copysign(1, dy) == math.copysign(1, dir_y):
#                 return Actions.MoveForward
#             else:
#                 return Actions.TurnAround
