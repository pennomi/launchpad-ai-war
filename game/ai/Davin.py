import math
from game.bot import Bot, Actions
import random
from panda3d.core import Vec3, NodePath

__author__ = 'Davin'


def getEnemies(bot):
     for v in bot.visible_objects:
         if  not v in bot.team:
             return v


class DemonBot5(Bot):
    WAIT = (Actions.TurnRight, Actions.Punch)
    Smart_bots = ("ScoobsterHailHydra", "Hayden", "Bob")
    in_danger = False
    DoneAlready = False

    x = -1

    def update(self, tick_number, visible_objects):
        # self._hp += 600
        for v in visible_objects:
            # Punch anyone directly in front of you
            if v.team != self.team:
                if v.get_position() == self.get_position() + self.get_direction():
                    print("HIYAH")
                    self.in_danger = False
                    self.x = -1
                    return Actions.Punch


                # Move to the side and punch the robot when he passes
                elif self.in_danger:
                        print("hahaYay")
                        # if self.x >= 0:
                        #     if self.x > 0:
                        #         self.DoneAlready = True
                        #         self.in_danger = False
                        #         self.x = -1
                        #     else:
                        #         print("Ready")
                        #         self.x += 1
                        #         return Actions.DoNothing
                        # else:
                        #     print("Getting Ready")
                        #     self.x += 1
                        #     print("++++++++++++++++++++++++++++++++++++++++++")
                        #     print(self.x)
                        #     print("++++++++++++++++++++++++++++++++++++++++++")
                        #     return Actions.TurnRight


                        if self.x >= 1:
                            self.DoneAlready = True
                            self.in_danger = False
                            self.x = -1
                            return Actions.Punch

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
                            return Actions.StrafeLeft

                        #  if the robot is coming from the side, wait
                        else:
                            if v.get_name()in self.Smart_bots or v.get_name()[:-1] == "Thomas":
                                self.x = -1
                                print("Facing X")
                                print("enemy Position: "+ str(v.get_position()))
                                print("enemy direction: "+str(v.get_direction()))
                                print("self Position: "+str(self.get_position()))
                                print("self direction: "+ str(self.get_direction()))

                                if v.get_position().x > self.get_position().x:
                                    if v.get_position().y == self.get_position().y-1:
                                        return Actions.StrafeRight
                                    else:
                                        return Actions.StrafeLeft
                                else:
                                    if v.get_position().y == self.get_position().y-1:
                                        return Actions.StrafeLeft
                                    else:
                                        return Actions.StrafeRight

                            else:
                                self.x += 1
                                if self.x > 2:
                                    self.x = -1
                                    if v.get_position().x > self.get_position().x:
                                        if v.get_position().y == self.get_position().y-1:
                                            return Actions.StrafeRight
                                        else:
                                            return Actions.StrafeLeft
                                    else:
                                        if v.get_position().y == self.get_position().y-1:
                                            return Actions.StrafeLeft
                                        else:
                                            return Actions.StrafeRight
                                    # return Actions.TurnLeft
                                else:
                                    return Actions.DoNothing
                            # if self.x < 0:
                            #     self.x += 1
                            #     return Actions.DoNothing
                            # else:
                            #     self.x = -1
                            #     print("Facing X")
                            #     if v.get_position().y == self.get_position().y-1:
                            #         return Actions.StrafeRight
                            #     else:
                            #         return Actions.StrafeLeft
                    elif self.get_position() + self.get_direction() == v.get_position() + (v.get_direction()+1):
                        return Actions.MoveBackward

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
                            return Actions.StrafeLeft

                        # if the robot is coming from the side, wait
                        else:
                            if v.get_name()in self.Smart_bots or v.get_name()[:-1] == "Thomas":
                                self.x = -1
                                print("Facing Y")
                                print("enemy Position: "+ str(v.get_position()))
                                print("enemy direction: "+str(v.get_direction()))
                                print("self Position: "+str(self.get_position()))
                                print("self direction: "+ str(self.get_direction()))

                                if v.get_position().y < self.get_position().y:
                                    if v.get_position().x == self.get_position().x-1:
                                        return Actions.StrafeRight
                                    else:
                                        return Actions.StrafeLeft
                                else:
                                    if v.get_position().x == self.get_position().x-1:
                                        return Actions.StrafeLeft
                                    else:
                                        return Actions.StrafeRight

                            else:
                                self.x += 1
                                if self.x > 2:
                                    self.x = -1
                                    if v.get_position().y < self.get_position().y:
                                        if v.get_position().x == self.get_position().x-1:
                                            return Actions.StrafeRight
                                        else:
                                            return Actions.StrafeLeft
                                    else:
                                        if v.get_position().x == self.get_position().x-1:
                                            return Actions.StrafeLeft
                                        else:
                                            return Actions.StrafeRight
                                    # return Actions.TurnLeft
                                else:
                                    return Actions.DoNothing
                            # if self.x < 0:
                            #     self.x += 1
                            #     return Actions.DoNothing
                            # else:
                            #     self.x = -1
                            #     print("Facing Y")
                            #     if v.get_position().x == self.get_position().x-1:
                            #         return Actions.StrafeLeft
                            #     else:
                            #         return Actions.StrafeRight

                    elif self.get_position() + self.get_direction() == v.get_position() + (v.get_direction()+1):
                        return Actions.MoveBackward
                else:
                    # Try to move towards the nearest golem
                    nearest_dist = 9999
                    nearest_bot = None
                    for v in visible_objects:
                        distance = (v.get_position() - self.get_position()).length()
                        if distance < nearest_dist and distance != 0:
                            nearest_bot = v
                            nearest_dist = distance
                            self.target = nearest_bot

                    if self.target:
                        nearest_pos = self.target.get_position()
                    else:
                        nearest_pos = None
                    if not nearest_pos:
                        return Actions.TurnLeft

                    x, y = nearest_pos.x, nearest_pos.y

                    my_x, my_y = self.get_position().x, self.get_position().y
                    print(x, y, my_x, my_y)

                    dir_x = self.get_direction().x
                    dir_y = self.get_direction().y

                    dx = x - my_x
                    dy = y - my_y
                    if dx != 0 and dir_x != 0:
                        if math.copysign(1, dx) == math.copysign(1, dir_x):
                            return Actions.MoveForward
                        else:
                            return Actions.TurnAround
                    if dy != 0 and dir_y != 0:
                        if math.copysign(1, dy) == math.copysign(1, dir_y):
                            return Actions.MoveForward
                        else:
                            return Actions.TurnAround
                    # HUNT
                        # check x to see if lined up
                            # if someone is coming towards you go to the side and wait for them to pass to punch them.
                            # else Track down robots and punch them
                        # if not lined up get lined up

            # If the robot is on the same team
            elif v.team == self.team:
                if v.get_position() == self.get_position() + self.get_direction():
                    print("HIYAH")
                    self.in_danger = False
                    self.x = -1
                    return Actions.TurnLeft
                elif self.get_direction().x != 0:  # I'm facing in the x direction

                    #  Handle if approaching the same square as another bot
                    if self.get_position() + self.get_direction() == v.get_position()+v.get_direction():
                        return Actions.TurnLeft

                # ELSE, IF I"M FACING IN THE Y DIRECTION
                elif self.get_direction().y != 0:  # I'm facing in the y direction

                    #  Handle if approaching the same square as another bot. WORKING!
                    if self.get_position() + self.get_direction() == v.get_position()+v.get_direction():

                        return Actions.TurnLeft

        #  If nothing is returned from the for loop, probably utilize memory here
        if visible_objects and not self.DoneAlready:
            print("super Califragilistic stupidcalidocious")
            return Actions.MoveForward
        elif not self.in_danger:
            self.DoneAlready = False
            return Actions.TurnLeft
        else:

            self.DoneAlready = False
            print("Doing nothing")
            return Actions.DoNothing

class TrackerHalelujiaBossBot1(Bot):
    wait = False
    turned = False
    """Walk in a square and do nothing."""
    def update(self, tick_number, visible_objects):

        for v in visible_objects:
            distance = (v.get_direction() - self.get_direction()).length()

            if v.get_position() == self.get_position() + self.get_direction():
                if v.team != self.team:
                    return Actions.Punch
                else:
                    return Actions.TurnLeft

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
                if v.team != self.team:
                    return Actions.Punch
                else:
                    return Actions.TurnLeft

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
                    # elif v.get_position().y == self.get_position().y+3:

                elif self.get_direction().y != 0:  # I'm facing in the x direction
                    if v.get_position().x == self.get_position().x:

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

                if v.team != self.team and v.get_name() != "DemonBot5":
                    return Actions.Punch
                else:
                    return Actions.TurnLeft

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
                if v.team != self.team and v.get_name() != "DemonBot5":
                    return Actions.Punch
                else:
                    return Actions.TurnLeft

        if tick_number % 5:
            self.x += 1
            self.x %= len(self.MOVES) - 1

            return self.MOVES[self.x]

        return Actions.TurnLeft


class SpinBot(Bot):

    def update(self, tick_number, visible_objects):
        for v in visible_objects:
            if v.get_position() == self.get_position() + self.get_direction():
                if v.team != self.team and v.get_name() != "DemonBot5":
                    return Actions.Punch
                else:
                    return Actions.TurnLeft


        return Actions.TurnLeft






# class Thomas2(Bot):
#     """walk around and throw other bots in the air"""
#
# class Thomas3(Bot):
#     """walk around and throw other bots in the air"""
#
# class Thomas4(Bot):
#     """walk around and throw other bots in the air"""
#
# class Thomas5(Bot):
#     """walk around and throw other bots in the air"""
#
# class Thomas6(Bot):
#     """walk around and throw other bots in the air"""
#
# class Thomas7(Bot):
#     """walk around and throw other bots in the air"""
#
# class Thomas8(Bot):
#     """walk around and throw other bots in the air"""
#
# class Thomas9(Bot):
#     """walk around and throw other bots in the air"""
#
# class ThomasA(Bot):
#     """walk around and throw other bots in the air"""
#
# class ThomasB(Bot):
#     """walk around and throw other bots in the air"""
#
# class ThomasC(Bot):
#     """walk around and throw other bots in the air"""
#
# class ThomasD(Bot):
#     """walk around and throw other bots in the air"""
#
# class ThomasE(Bot):
#     """walk around and throw other bots in the air"""
#
# class ThomasF(Bot):
#     """walk around and throw other bots in the air"""
#
# class ThomasG(Bot):
#     """walk around and throw other bots in the air"""
#
# class ThomasH(Bot):
#     """walk around and throw other bots in the air"""
#
# class ThomasI(Bot):
#     """walk around and throw other bots in the air"""
#
# class ThomasJ(Bot):
#     """walk around and throw other bots in the air"""
#
# class ThomasK(Bot):
#     """walk around and throw other bots in the air"""
#
# class ThomasL(Bot):
#     """walk around and throw other bots in the air"""
#
# class ThomasM(Bot):
#     """walk around and throw other bots in the air"""
#
# class ThomasN(Bot):
#     """walk around and throw other bots in the air"""
#
# class ThomasO(Bot):
#     """walk around and throw other bots in the air"""
#
# class ThomasP(Bot):
#     """walk around and throw other bots in the air"""