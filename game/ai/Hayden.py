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


        if visible_objects:
            return Actions.MoveForward

        return random.choice([Actions.TurnLeft, Actions.TurnRight])
