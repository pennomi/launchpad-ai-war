import math
from game.bot import Bot, Actions
from panda3d.core import Vec3, NodePath

__author__ = 'Davin'


def getEnemies(bot):
     for v in bot.visible_objects:
         if  not v in bot.team:
             return v



class Davinator(Bot):
    WAIT = (Actions.MoveForward, Actions.TurnAround)
    in_danger = False
    DoneAlready = False
    x = -1

    def update(self, tick_number, visible_objects):

        for v in visible_objects:
            # Punch anyone directly in front of you

            if v.get_position() == self.get_position() + self.get_direction():
                print("HIYAH")
                self.in_danger = False

                self.x = -1
                return Actions.Punch

            # Move to the side and punch the robot when he passes
            elif self.in_danger:
                    print("hahaYay")
                    if self.x >= len(self.WAIT)-1:
                        if self.x > 1:
                            self.DoneAlready = True
                            self.in_danger = False
                            self.x = -1
                        else:
                            print("Ready")
                            self.x += 1
                            return Actions.DoNothing
                    else:
                        print("Getting Ready")
                        self.x += 1
                        print("++++++++++++++++++++++++++++++++++++++++++")
                        print(self.x)
                        print("++++++++++++++++++++++++++++++++++++++++++")
                        return self.WAIT[self.x]


            #  ELSE, IF I"M FACING IN THE X DIRECTION
            elif self.get_direction().x != 0:  # I'm facing in the x direction

                #  Handle if approaching the same square as another bot
                if self.get_position() + self.get_direction() == v.get_position()+v.get_direction():

                    # if the robot is directly ahead, tell the robot to get ready
                    if self.get_position().y == v.get_position().y:
                        print("********************")
                        print("Facing X")
                        print("********************")
                        self.in_danger = True
                        self.x = -1

                    #  if the robot is coming from the side, wait
                    else:
                        if self.x < 0:
                            self.x += 1
                            return Actions.DoNothing
                        else:
                            self.x = -1
                            return Actions.TurnLeft
                # HUNT
                    # check y to see if its lined up
                            # if they are coming towards you get self.ready
                            # else Track robots down and punch them
                    # if not lined up get lined up

            # ELSE, IF I"M FACING IN THE Y DIRECTION
            elif self.get_direction().y != 0:  # I'm facing in the y direction

                #  Handle if approaching the same square as another bot. WORKING!
                if self.get_position() + self.get_direction() == v.get_position()+v.get_direction():

                    #  If the robot is directly ahead, get ready
                    if self.get_position().x == v.get_position().x:
                        print("********************")
                        print("Facing Y")
                        print("********************")
                        self.in_danger = True
                        self.x = -1
                        return Actions.TurnLeft

                    # if the robot is coming from the side, wait
                    else:
                        if self.x < 0:
                            self.x += 1
                            return Actions.DoNothing
                        else:
                            self.x = -1
                            return Actions.TurnLeft

                # HUNT
                    # check x to see if lined up
                        # if someone is coming towards you go to the side and wait for them to pass to punch them.
                        # else Track down robots and punch them
                    # if not lined up get lined up


        #  If nothing is returned from the for loop,
        if visible_objects and not self.DoneAlready:
            print("super Califragilistic stupidcalidocious")
            return Actions.MoveForward
        elif not self.in_danger:
            self.DoneAlready = False
            return Actions.TurnLeft
        else:
            self.DoneAlready = False
            return Actions.DoNothing







































# class TrackerHalelujiaBossBot1(Bot):
#     wait = False
#     turned = False
#     """Walk in a square and do nothing."""
#     def update(self, tick_number, visible_objects):
#
#         for v in visible_objects:
#             distance = (v.get_direction() - self.get_direction()).length()
#
#             if v.get_position() == self.get_position() + self.get_direction():
#                 return Actions.Punch
#
#             # Check if he's facing me
#             if v.get_direction() == -self.get_direction() and distance < 3:
#                 return Actions.TurnLeft
#
#
#             # hunt
#             if self.get_direction().x != 0:  # I'm facing in the x direction
#                 if v.get_position().y == self.get_position().y:
#                     # I'm lined up
#                     # wait and kill
#                     if v.get_direction == -self.get_direction():
#                         pass
#
#                 else:
#                     pass  # TODO: Turn right or left, depending
#             else:  # I'm facing in the y direction
#                 pass
#
#             # Target HunterBot
#             if v.get_name() == "HunterBot":
#                 distance
#
#
#                 # return Actions.TurnAround
#
#         if visible_objects:
#             return Actions.MoveForward
#
#         return Actions.TurnLeft
#

# class HuntBot3(Bot):
#     wait = False
#     turned = False
#     ready = False
#     """Ten successive moves"""
#     def update(self, tick_number, visible_objects):
#         for v in visible_objects:
#             if v.get_position() == self.get_position() + self.get_direction():
#                 self.wait = False
#                 self.turned = False
#                 self.ready = False
#                 return Actions.Punch
#
#             else:
#
#                 # hunt
#                 if self.get_direction().x != 0:  # I'm facing in the x direction
#                     if v.get_position().y == self.get_position().y:
#
#                         # I'm lined up
#                         # wait and kill
#                         if v.get_direction == self.get_direction()-180:
#                             self.turned = True
#                             return Actions.TurnLeft
#                         elif self.turned == True:
#                             self.ready = True
#                             return Actions.TurnAround
#                         elif self.ready == True:
#                             return Actions.DoNothing
#                     # elif v.get_position().y == self.get_position().y+3:
#
#                 elif self.get_direction().y != 0:  # I'm facing in the x direction
#                     if v.get_position().x == self.get_position().x:
#
#                         # I'm lined up
#                         # wait and kill
#                         if v.get_direction == self.get_direction()-180:
#                             self.turned = True
#                             return Actions.TurnLeft
#                         elif self.turned == True and tick_number % 2:
#                             self.ready = True
#                             self.turned = False
#                             return Actions.Punch
#                         elif self.ready == True:
#                             return Actions.DoNothing
#
#
#         if visible_objects:
#
#             return Actions.MoveForward
#         elif tick_number % 4:
#             return Actions.TurnLeft
#         else:
#             return Actions.DoNothing


# class SentryBot2(Bot):
#     """pace back and forth and kill anything found."""
#     def update(self, tick_number, visible_objects):
#         for v in visible_objects:
#             if v.get_position() == self.get_position() + self.get_direction():
#
#                 return Actions.Punch
#
#         if tick_number % 6:
#             return Actions.MoveForward
#
#         return Actions.TurnAround
#
#
# class GimickBot(Bot):
#     MOVES = (Actions.TurnLeft, Actions.MoveBackward, Actions.TurnAround, Actions.Punch, Actions.MoveForward, Actions.TurnRight, Actions.MoveBackward, Actions.TurnLeft, Actions.TurnAround, Actions.Punch)
#     x = -1
#     """Ten successive moves"""
#     def update(self, tick_number, visible_objects):
#         for v in visible_objects:
#             if v.get_position() == self.get_position() + self.get_direction():
#                 return Actions.Punch
#
#         if tick_number % 5:
#             self.x += 1
#             self.x %= len(self.MOVES) - 1
#
#             return self.MOVES[self.x]
#
#         return Actions.TurnLeft


# class SpinBot(Bot):
#
#     def update(self, tick_number, visible_objects):
#         for v in visible_objects:
#             if v.get_position() == self.get_position() + self.get_direction():
#                 return Actions.Punch
#
#
#         return Actions.TurnLeft

# class SpinBot1(Bot):
#
#     def update(self, tick_number, visible_objects):
#         for v in visible_objects:
#             if v.get_position() == self.get_position() + self.get_direction():
#                 return Actions.Punch
#
#
#         return Actions.TurnLeft
#
# class SpinBot2(Bot):
#
#     def update(self, tick_number, visible_objects):
#         for v in visible_objects:
#             if v.get_position() == self.get_position() + self.get_direction():
#                 return Actions.Punch
#
#
#         return Actions.TurnLeft
#
# class SpinBot3(Bot):
#
#     def update(self, tick_number, visible_objects):
#         for v in visible_objects:
#             if v.get_position() == self.get_position() + self.get_direction():
#                 return Actions.Punch
#
#
#         return Actions.TurnLeft
#
# class SpinBot4(Bot):
#
#     def update(self, tick_number, visible_objects):
#         for v in visible_objects:
#             if v.get_position() == self.get_position() + self.get_direction():
#                 return Actions.Punch
#
#
#         return Actions.TurnLeft
#
# class SpinBot5(Bot):
#
#     def update(self, tick_number, visible_objects):
#         for v in visible_objects:
#             if v.get_position() == self.get_position() + self.get_direction():
#                 return Actions.Punch
#
#
#         return Actions.TurnLeft
#
# class SpinBot6(Bot):
#
#     def update(self, tick_number, visible_objects):
#         for v in visible_objects:
#             if v.get_position() == self.get_position() + self.get_direction():
#                 return Actions.Punch
#
#
#         return Actions.TurnLeft
#
# class SpinBot7(Bot):
#
#     def update(self, tick_number, visible_objects):
#         for v in visible_objects:
#             if v.get_position() == self.get_position() + self.get_direction():
#                 return Actions.Punch
#
#
#         return Actions.TurnLeft
#
# class SpinBot8(Bot):
#
#     def update(self, tick_number, visible_objects):
#         for v in visible_objects:
#             if v.get_position() == self.get_position() + self.get_direction():
#                 return Actions.Punch
#
#
#         return Actions.TurnLeft
#
# class SpinBot9(Bot):
#
#     def update(self, tick_number, visible_objects):
#         for v in visible_objects:
#             if v.get_position() == self.get_position() + self.get_direction():
#                 return Actions.Punch
#
#
#         return Actions.TurnLeft
#
# class SpinBot10(Bot):
#
#     def update(self, tick_number, visible_objects):
#         for v in visible_objects:
#             if v.get_position() == self.get_position() + self.get_direction():
#                 return Actions.Punch
#
#
#         return Actions.TurnLeft
#
# class SpinBot11(Bot):
#
#     def update(self, tick_number, visible_objects):
#         for v in visible_objects:
#             if v.get_position() == self.get_position() + self.get_direction():
#                 return Actions.Punch
#
#
#         return Actions.TurnLeft

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
class Thomas1(Bot):
    """walk around and throw other bots in the air"""

class Thomas2(Bot):
    """walk around and throw other bots in the air"""

class Thomas3(Bot):
    """walk around and throw other bots in the air"""

class Thomas4(Bot):
    """walk around and throw other bots in the air"""

class Thomas5(Bot):
    """walk around and throw other bots in the air"""

class Thomas6(Bot):
    """walk around and throw other bots in the air"""

class Thomas7(Bot):
    """walk around and throw other bots in the air"""

class Thomas8(Bot):
    """walk around and throw other bots in the air"""

class Thomas9(Bot):
    """walk around and throw other bots in the air"""

class Thomas10(Bot):
    """walk around and throw other bots in the air"""

class Thomas11(Bot):
    """walk around and throw other bots in the air"""

class Thomas12(Bot):
    """walk around and throw other bots in the air"""