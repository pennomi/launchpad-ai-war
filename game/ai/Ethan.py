import math
import random

from game.bot import Bot, Actions


class ScoobsterHailHydra(Bot):
    """Move toward enemies and punch them."""
    target = None

    def update(self, tick_number, visible_objects):
        # Check if something needs killed
        for v in visible_objects:
            if v.get_position() == self.get_position() + self.get_direction():
                return Actions.Punch
            if v.get_position() + v.get_direction() == self.get_position() + self.get_direction():
                return random.choice([Actions.MoveBackward, Actions.StrafeRight])

        # Try to move towards the nearest golem
        nearest_dist = 9999
        nearest_bot = None
        for v in visible_objects:
            distance = (v.get_position() - self.get_position()).length()
            if distance < nearest_dist and distance != 0:
                nearest_bot = v
                nearest_dist = distance
                self.target = nearest_bot

        if self.target:
            nearest_pos = self.target.get_position()
        else:
            nearest_pos = None
        if not nearest_pos:
            return Actions.TurnLeft

        x, y = nearest_pos.x, nearest_pos.y

        my_x, my_y = self.get_position().x, self.get_position().y
        print(x, y, my_x, my_y)

        dir_x = self.get_direction().x
        dir_y = self.get_direction().y

        dx = x - my_x
        dy = y - my_y
        if dx != 0 and dir_x != 0:
            if math.copysign(1, dx) == math.copysign(1, dir_x):
                return Actions.MoveForward
            else:
                return Actions.TurnAround
        if dy != 0 and dir_y != 0:
            if math.copysign(1, dy) == math.copysign(1, dir_y):
                return Actions.MoveForward
            else:
                return Actions.TurnAround

        return Actions.TurnRight