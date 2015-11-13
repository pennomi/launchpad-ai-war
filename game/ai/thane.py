from game.bot import Bot, Actions


class HunterBot(Bot):
    """Move toward enemies and punch them."""
    def update(self, tick_number, visible_objects):
        for v in visible_objects:
            if v.get_position() == self.get_position() + self.get_direction():
                return Actions.Punch

        if visible_objects:
            return Actions.MoveForward

        return Actions.TurnLeft
