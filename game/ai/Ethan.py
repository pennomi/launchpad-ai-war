import math
import random

from game.bot import Bot, Actions


class ScoobYaUp(Bot):
    """Move toward enemies and punch them."""
    target = None
    def update(self, tick_number, visible_objects):
        # Check if something needs killed
        for v in visible_objects:
            if v.position == self.position + self.direction and v.team != self.team:
                return Actions.Punch
            if v.position + v.direction == self.position + self.direction and v.team != self.team:
                return random.choice([Actions.StrafeRight, Actions.StrafeLeft, Actions.MoveBackward])
        # Try to move towards the nearest golem
        nearest_dist = 9999
        for v in visible_objects:
            distance = (v.position - self.position).length()
            if distance < nearest_dist and distance != 0:
                nearest_dist = distance
                self.target = v

        if self.target:
            nearest_pos = self.target.position
        else:
            nearest_pos = None
        if not nearest_pos:
            return Actions.TurnRight

        x, y = nearest_pos.x, nearest_pos.y

        my_x, my_y = self.position.x, self.position.y

        dir_x = self.direction.x
        dir_y = self.direction.y

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