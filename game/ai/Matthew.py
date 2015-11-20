from game.bot import Bot, Actions


class MattBot(Bot):
    going = False

    def update(self, tick_number, visible_objects):
        enemies = self.get_enemies(visible_objects)
        if enemies == False:
            return Actions.TurnLeft
        for v in visible_objects:
            Enemy = v.get_position()
            Self = self.get_position()
            distance_to_enemy = (Enemy - Self).length()

            if distance_to_enemy < 2:
                return Actions.Punch
            elif distance_to_enemy == 2:
                self.going = True
                return Actions.StrafeLeft
            # elif self.going:
            #     self.going = False
            #     return Actions.TurnRight
            else:
                return Actions.DoNothing



    def get_enemies(self, visible_objects):
        enemies = []
        for v in visible_objects:
            if v.team != self.team:
                enemies.append(v)
        return enemies

