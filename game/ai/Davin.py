import math
from game.bot import Bot, Actions
from panda3d.core import Vec3, NodePath

__author__ = 'Davin'


def getEnemies(bot):
     for v in bot.visible_objects:
         if  not v in bot.team:
             return v


class TrackerHalelujiaBossBot1(Bot):
    wait = False
    turned = False
    """Walk in a square and do nothing."""
    def update(self, tick_number, visible_objects):

        for v in visible_objects:
            distance = (v.get_direction() - self.get_direction()).length()

            if v.get_position() == self.get_position() + self.get_direction():
                return Actions.Punch

            # Check if he's facing me
            if v.get_direction() == -self.get_direction() and distance < 3:
                return Actions.TurnLeft


            # hunt
            if self.get_direction().x != 0:  # I'm facing in the x direction
                if v.get_position().y == self.get_position().y:
                    # I'm lined up
                    # wait and kill
                    if v.get_direction == -self.get_direction():
                        pass

                else:
                    pass  # TODO: Turn right or left, depending
            else:  # I'm facing in the y direction
                pass

            # Target HunterBot
            if v.get_name() == "HunterBot":
                distance


                # return Actions.TurnAround

        if visible_objects:
            return Actions.MoveForward

        return Actions.TurnLeft


class HuntBot3(Bot):
    wait = False
    turned = False
    ready = False
    """Ten successive moves"""
    def update(self, tick_number, visible_objects):
        for v in visible_objects:
            if v.get_position() == self.get_position() + self.get_direction():
                self.wait = False
                self.turned = False
                self.ready = False
                return Actions.Punch

            else:

                # hunt
                if self.get_direction().x != 0:  # I'm facing in the x direction
                    if v.get_position().y == self.get_position().y:

                        # I'm lined up
                        # wait and kill
                        if v.get_direction == self.get_direction()-180:
                            self.turned = True
                            return Actions.TurnLeft
                        elif self.turned == True:
                            self.ready = True
                            return Actions.TurnAround
                        elif self.ready == True:
                            return Actions.DoNothing

                elif self.get_direction().y != 0:  # I'm facing in the x direction
                    if v.get_position().x == self.get_position().y:

                        # I'm lined up
                        # wait and kill
                        if v.get_direction == self.get_direction()-180:
                            self.turned = True
                            return Actions.TurnLeft
                        elif self.turned == True and tick_number % 2:
                            self.ready = True
                            self.turned = False
                            return Actions.Punch
                        elif self.ready == True:
                            return Actions.DoNothing


        if visible_objects:

            return Actions.MoveForward
        elif tick_number % 4:
            return Actions.TurnLeft
        else:
            return Actions.DoNothing


class SentryBot2(Bot):
    """pace back and forth and kill anything found."""
    def update(self, tick_number, visible_objects):
        for v in visible_objects:
            if v.get_position() == self.get_position() + self.get_direction():

                return Actions.Punch

        if tick_number % 6:
            return Actions.MoveForward

        return Actions.TurnAround


class GimickBot(Bot):
    MOVES = (Actions.TurnLeft, Actions.MoveBackward, Actions.TurnAround, Actions.Punch, Actions.MoveForward, Actions.TurnRight, Actions.MoveBackward, Actions.TurnLeft, Actions.TurnAround, Actions.Punch)
    x = -1
    """Ten successive moves"""
    def update(self, tick_number, visible_objects):
        for v in visible_objects:
            if v.get_position() == self.get_position() + self.get_direction():
                return Actions.Punch

        if tick_number % 5:
            self.x += 1
            self.x %= len(self.MOVES) - 1

            return self.MOVES[self.x]

        return Actions.TurnLeft


class SpinBot(Bot):

    """Ten successive moves"""
    def update(self, tick_number, visible_objects):
        for v in visible_objects:
            v._death_played()
            if v.get_position() == self.get_position() + self.get_direction():
                return Actions.Punch

        return Actions.TurnLeft


# class SpinBot2(Bot):
#
#     """Ten successive moves"""
#     def update(self, tick_number, visible_objects):
#         for v in visible_objects:
#             if v.get_position() == self.get_position() + self.get_direction():
#                 return Actions.Punch
#
#         return Actions.jump
#
#
#

