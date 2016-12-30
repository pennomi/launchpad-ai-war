import random

from game.bot import Bot, Actions


class OptionsBot(Bot):
    """Calculate which actions are most likely to maximize points.
    """
    visible_objects = None

    def bot_at(self, position):
        for b in self.visible_objects:
            if b.position == position:
                return b
        return None

    def bot_threatens(self, position):
        for b in self.visible_objects:
            if b.position + b.direction == position:
                return b
        return None

    def update(self, tick_number, visible_objects):
        self.visible_objects = visible_objects

        options = {
            Actions.MoveForward: 0,
            Actions.TurnLeft: 0,
            Actions.TurnRight: 0,
            Actions.TurnAround: 0,
            Actions.Punch: 0,
            Actions.DoNothing: 0,

            # Strafing is slightly risky because someone behind us could move
            # into that space without us knowing
            Actions.StrafeLeft: -.1,
            Actions.StrafeRight: -.1,

            # Moving backward is risky because I don't know what is behind me.
            # Only pick this option if I think there's no other escape.
            Actions.MoveBackward: -0.25,

            # By default this is a bad option because it results in death.
            # However! Suicide is preferable to getting killed because it
            # denies the opponent's point. :D
            Actions.Suicide: -0.5,
        }

        # TODO: Here are some thoughts
        # * Check if surrounding squares are threatened
        # * Pay attention to other bots' directions
        # * Move toward the action when safe

        ###################################################################
        # If someone is in front of me...
        ###################################################################
        bot = self.bot_at(self.position + self.direction)
        if bot:
            # Don't move forward in case they're staying put
            options[Actions.MoveForward] -= 1

            # If it's an enemy
            if bot.team != self.team:
                # Attacking is a good plan
                # TODO: but is it more important than survival?
                options[Actions.Punch] += 1
            # If it's an ally, don't attack
            else:
                options[Actions.Punch] -= 1

            # TODO: If they're looking at me, better move!

        ###################################################################
        # If someone threatens the square in front of me...
        ###################################################################
        bot = self.bot_threatens(self.position + self.direction)
        if bot:
            # Don't move there
            options[Actions.MoveForward] -= 1

            # If it's an enemy, consider pausing to see if they move in
            if bot.team != self.team:
                options[Actions.DoNothing] += 0.5

        ###################################################################
        # If someone threatens my square...
        ###################################################################
        bot = self.bot_threatens(self.position)
        if bot:
            # Better get out of the way so we don't get trampled or punched
            options[Actions.MoveForward] += 1
            options[Actions.MoveBackward] += 1
            options[Actions.StrafeLeft] += 1
            options[Actions.StrafeRight] += 1

        ###################################################################
        # If someone is to my right...
        ###################################################################
        bot = self.bot_at(self.position + self.right_direction)
        if bot:
            # Better get out of the way so we don't get trampled or punched
            options[Actions.MoveForward] += 1
            options[Actions.MoveBackward] += 1
            options[Actions.StrafeLeft] += 1

            # But don't go right
            options[Actions.StrafeRight] += 1

        ###################################################################
        # If someone is to my left...
        ###################################################################
        bot = self.bot_at(self.position + self.left_direction)
        if bot:
            # Better get out of the way so we don't get trampled or punched
            options[Actions.MoveForward] += 1
            options[Actions.MoveBackward] += 1
            options[Actions.StrafeRight] += 1

            # But don't go left
            options[Actions.StrafeLeft] -= 1

        ###################################################################
        # If I see an enemy in the distance...
        ###################################################################
        for bot in visible_objects:
            if bot.team != self.team:
                # Let's tentatively move forward
                options[Actions.MoveForward] += 0.25
                break

        # Extract the best action from the options and return it
        option_tuples = list(options.items())
        random.shuffle(option_tuples)  # randomize to break ties
        option_tuples = sorted(option_tuples, key=lambda x: -x[1])

        #
        print(option_tuples[0:3])
        return option_tuples[0][0]
