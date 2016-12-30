from game.bot import Bot, Actions


class MarksBot(Bot):
    def update(self, tick_number, visible_objects):
        for v in visible_objects:

            if v.position == self.position + self.direction:
                return Actions.TurnRight

            if v.position == self.position + 10:
                return Actions.MoveBackward

        return Actions.TurnAround

