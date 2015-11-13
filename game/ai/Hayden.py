import random
from game.bot import Bot,  Actions


class Haydenbot (Bot):
def update(self, tick_number, visible_objects):
        for v in visible_objects:
            if v.get_position() == self.get_position() + self.get_direction():
                return Actions.Punch

        if visible_objects:
            return Actions.MoveForward
			
        else:
            return Actions.TurnAround
		
        return Actions.TurnLeft

