import random

from game.bot import Bot, Actions


class Bae(Bot):
    """Move toward enemies and punch them."""

    def update(self, tick_number, visible_objects):
        self._name_label.setScale(4, 4, 4)
        v = None
        for v in visible_objects:
            if v.get_position() == self.get_position() + self.get_direction() and v.team != self.team:
                return Actions.Punch

        if not v:
            return Actions.TurnLeft

        if v.get_position() + v.get_direction() == self.get_position() + self.get_direction():
            return random.choice([Actions.StrafeLeft, Actions.StrafeRight])

        if visible_objects:
            return Actions.MoveForward

        if random.randint(0, 1):
            return Actions.TurnRight
        else:
            return Actions.TurnLeft


class SideBae(Bot):
    """Move toward enemies and punch them."""

    def update(self, tick_number, visible_objects):
        self._name_label.setScale(4, 4, 4)
        v = None
        for v in visible_objects:
            if v.get_position() == self.get_position() + self.get_direction() and v.team != self.team:
                return Actions.Punch

        if not v:
            return Actions.TurnLeft

        if v.get_position() + v.get_direction() == self.get_position() + self.get_direction():
            return random.choice([Actions.StrafeLeft, Actions.StrafeRight])

        if visible_objects:
            return Actions.MoveForward

        if random.randint(0, 1):
            return Actions.TurnRight
        else:
            return Actions.TurnLeft

