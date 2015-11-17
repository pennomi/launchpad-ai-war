from game.bot import Bot, Actions


class ScoobyMaiBoi(Bot):
    """Move toward enemies and punch them."""
    def update(self, tick_number, visible_objects):
        # Check if something needs killed
        for v in visible_objects:
            if v.get_position() == self.get_position() + self.get_direction():
                return Actions.Punch

        # Try to move towards the nearest golem
        nearest_dist = 9999
        nearest_bot = None
        for v in visible_objects:
            distance = (v.get_position() - self.get_position()).length()
            if distance < nearest_dist:
                nearest_bot = v
                nearest_dist = distance

        print("Near", nearest_bot.__class__.__name__)


        if visible_objects:
            return Actions.MoveForward


        return Actions.TurnRight