from game.bot import Bot, Actions

__author__ = 'Davin'


class DemonBot5(Bot):
    WAIT = (Actions.TurnRight, Actions.Punch)
    Tactic1 = (Actions.StrafeLeft, Actions.DoNothing, Actions.TurnRight)
    Tactic2 = (Actions.MoveBackward, Actions.MoveForward)
    Tactic3 = (Actions.TurnLeft, Actions.MoveForward, Actions.TurnAround)
    Tactic4 = (Actions.MoveForward, Actions.StrafeLeft, Actions.TurnAround)
    Smart_bots = ("Hayden", "Bob")
    prev_PositionX = 0
    prev_PositionY = 0
    distance = 0
    in_danger = False
    DoneAlready = False
    j = 0
    x = -1
    using_tactic = False
    selected_tactic = Tactic1

    def use_tactic(self, tactic):
        # x = -1
        if self.j < len(tactic)-1:
            self.j += 1
            return tactic[self.j]
        else:
            i = self.j
            self.j = 0
            self.using_tactic = False
            return tactic[i]

    def update(self, tick_number, visible_objects):
        # self._hp += 600
        for v in visible_objects:

            # save positions for memory
            self.prev_PositionX = v.position.x
            self.prev_PositionY = v.position.y
            self.distance = (v.position - self.position).length()

            if v.team != self.team:  # or v.name in self.annoying:
                # Punch anyone directly in front of you
                if v.position == self.position + self.direction:
                    self.in_danger = False
                    self.x = -1
                    return Actions.Punch

                # Move to the side and punch the robot when he passes
                elif self.in_danger:
                        self.DoneAlready = True
                        self.in_danger = False
                        return Actions.TurnRight

                elif self.using_tactic:
                    return self.use_tactic(self.selected_tactic)

                    # return self.use_tactic(self.selected_tactic)

                #  ELSE, IF I"M FACING IN THE X DIRECTION
                elif self.direction.x != 0:  # I'm facing in the x direction
                    #  Handle if approaching the same square as another bot
                    if self.position + self.direction == v.position+v.direction:
                        # if the robot is directly ahead, tell the robot to get ready
                        if self.position.y == v.position.y and v.name != "SpinBot":
                            if v.name == "ScoobYaUp" and self.distance == 2:
                                    self.selected_tactic = self.Tactic2
                                    self.using_tactic = True
                                    return self.selected_tactic[0]
                                    # self.use_tactic(self.Tactic2)
                            else:
                                self.in_danger = True
                                self.x = -1
                                return Actions.StrafeLeft

                        #  if the robot is coming from the side, wait
                        else:
                            if v.name in self.Smart_bots or v.name[:-1] == "Thomas":
                                self.x = -1

                                if v.position.x > self.position.x:
                                    if v.position.y == self.position.y-1:
                                        return Actions.StrafeRight
                                    else:
                                        return Actions.StrafeLeft
                                else:
                                    if v.position.y == self.position.y-1:
                                        return Actions.StrafeLeft
                                    else:
                                        return Actions.StrafeRight
                            elif v.name == "ScoobYaUp":
                                self.selected_tactic = self.Tactic2
                                self.using_tactic = True
                                return self.selected_tactic[0]
                            else:
                                self.x += 1
                                if self.x > 2:
                                    self.x = -1
                                    if v.position.x > self.position.x:
                                        if v.position.y == self.position.y-1:
                                            return Actions.StrafeRight
                                        else:
                                            return Actions.StrafeLeft
                                    else:
                                        if v.position.y == self.position.y-1:
                                            return Actions.StrafeLeft
                                        else:
                                            return Actions.StrafeRight
                                    # return Actions.TurnLeft
                                else:
                                    return Actions.DoNothing
                    # Look for bots two spaces ahead
                    elif self.position.x + 3 == v.position.x and self.position.y == v.position.y and v.direction == -(self.direction):
                        self.selected_tactic = self.Tactic3
                        self.using_tactic = True
                        self.j = 0
                        return self.selected_tactic[0]

                        # return Actions.StrafeLeft
                    # # return something so that you don't get stuck doing nog
                    # else:
                    #     return Actions.MoveForward

                # ELSE, IF I"M FACING IN THE Y DIRECTION
                elif self.direction.y != 0:  # I'm facing in the y direction
                    #  Handle if approaching the same square as another bot. WORKING!
                    if self.position + self.direction == v.position+v.direction:

                        #  If the robot is directly ahead, get ready
                        if self.position.x == v.position.x and v.name != "SpinBot":
                            self.in_danger = True
                            self.x = -1
                            return Actions.StrafeLeft

                        # if the robot is coming from the side, wait
                        else:
                            if v.name in self.Smart_bots or v.name[:-1] == "Thomas":
                                self.x = -1
                                if v.position.y < self.position.y:
                                    if v.position.x == self.position.x-1:
                                        return Actions.StrafeRight
                                    else:
                                        return Actions.StrafeLeft
                                else:
                                    if v.position.x == self.position.x-1:
                                        return Actions.StrafeLeft
                                    else:
                                        return Actions.StrafeRight
                            elif v.name == "ScoobYaUp":
                                self.selected_tactic = self.Tactic2
                                self.using_tactic = True
                                return self.selected_tactic[0]
                                # self.use_tactic(self.Tactic2)
                            else:
                                self.x += 1
                                if self.x > 2:
                                    self.x = -1
                                    if v.position.y < self.position.y:
                                        if v.position.x == self.position.x-1:
                                            return Actions.StrafeRight
                                        else:
                                            return Actions.StrafeLeft
                                    else:
                                        if v.position.x == self.position.x-1:
                                            return Actions.StrafeLeft
                                        else:
                                            return Actions.StrafeRight
                                    # return Actions.TurnLeft
                                else:
                                    return Actions.DoNothing

                    elif self.position.y + 3 == v.position.y and self.position.x == v.position.x and v.direction == -(self.direction):
                        self.selected_tactic = self.Tactic3
                        self.using_tactic = True
                        self.j = 0
                        return self.selected_tactic[0]

            # If the robot is on the same team
            elif v.team == self.team:
                if v.position == self.position + self.direction:
                    self.in_danger = False
                    self.x = -1
                    return Actions.TurnLeft
                elif self.direction.x != 0:  # I'm facing in the x direction

                    #  Handle if approaching the same square as another bot
                    if self.position + self.direction == v.position+v.direction:
                        return Actions.TurnLeft

                # ELSE, IF I"M FACING IN THE Y DIRECTION
                elif self.direction.y != 0:  # I'm facing in the y direction
                    # Handle if approaching the same square as another bot. WORKING!
                    if self.position + self.direction == v.position+v.direction:
                        return Actions.TurnLeft

        # If nothing is returned from the for loop, probably utilize memory here
        if visible_objects and not self.DoneAlready:
            return Actions.MoveForward
        elif not self.in_danger and not self.using_tactic:
            self.DoneAlready = False
            return Actions.TurnLeft
        elif self.using_tactic:
            return self.use_tactic(self.selected_tactic)
        else:
            self.DoneAlready = False
            return Actions.DoNothing
