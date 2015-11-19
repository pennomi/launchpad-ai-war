from game.bot import Bot, Actions

class Hayden(Bot):
    def update(self, tick_number, visible_objects):
        for v in visible_objects:
            if v.get_position() == self.get_position() + self.get_direction():
                return Actions.Punch

        for v in visible_objects:
            if self.get_position() + self.get_direction() == v.get_position() + v.get_direction():
                if self.team == v.team:
                    return Actions.TurnRight
                else:
                    return Actions.DoNothing

        # near bot
        nearest_dist = 20
        nearest_bot = None
        for v in visible_objects:
            distance = (v.get_position() - self.get_position()).length()
            if distance < nearest_dist:
                nearest_bot = v
                nearest_dist = distance
            print("Hayden " + "is near " + nearest_bot.__class__.__name__ + " who is " + str(nearest_dist) + " away.")

        if visible_objects:
            return Actions.MoveForward

        return Actions.TurnLeft
