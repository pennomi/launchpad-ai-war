import random

from game.bot import Bot, Actions


class Bob(Bot):
    """Move toward enemies and punch them."""
    next_action = None
    next_action2 = None
    def update(self, tick_number, visible_objects):
        if self.next_action:
            a = self.next_action
            self.next_action = None
            return a
        if self.next_action2:
            b = self.next_action2
            self.next_action2 = None
            return b
        for v in visible_objects:
            if v.position == self.position + self.direction and v.team != self.team:
                return Actions.Punch
            if v.position == self.position + self.direction and v.team == self.team:
                return Actions.TurnLeft

            # If someone is going to walk into the same space as me
            if v.position + v.direction == self.position + self.direction:
                self.next_action = Actions.StrafeLeft
                self.next_action2 = Actions.TurnRight
                return Actions.DoNothing
        # don't kill team


        if visible_objects:
            return Actions.MoveForward

        if random.randint(0, 1):
            return Actions.TurnRight
        else:
            return Actions.TurnLeft