import random
from game.bot import Bot, Actions

class Hayden(Bot):
    def update(self, tick_number, visible_objects):
        for v in visible_objects:
            if v.position == self.position + self.direction:
                if self.team != v.team:
                    return Actions.Punch

        for v in visible_objects:
            if self.position + self.direction == v.position + v.direction:
                if self.team != v.team:
                    return Actions.DoNothing
                elif self.team == v.team:
                    return Actions.TurnAround


        if visible_objects:
            return Actions.MoveForward

        return random.choice([Actions.TurnLeft, Actions.TurnRight])
