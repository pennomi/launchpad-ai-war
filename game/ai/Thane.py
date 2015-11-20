from collections import deque
import random
import math
from game.bot import Bot, Actions


class HunterBot(Bot):
    """Move toward enemies and punch them."""
    def update(self, tick_number, visible_objects):
        for v in visible_objects:
            if v.get_position() == self.get_position() + self.get_direction():
                if v.team != self.team:
                    return Actions.Punch
                else:
                    return Actions.TurnLeft

        if visible_objects:
            return Actions.MoveForward

        return Actions.TurnLeft


class BigUglyRockPerson(Bot):
    """
    Win. Every. Time.
    """
    suggested_next_moves = deque()
    suggested_direction = None

    def update(self, tick, bots):
        possible_moves = {
            Actions.MoveForward,
            Actions.MoveBackward,
            Actions.StrafeLeft,
            Actions.StrafeRight,
            Actions.TurnLeft,
            Actions.TurnRight,
            Actions.TurnAround,
            Actions.Punch,
            Actions.DoNothing,
        }
        good_moves = set()
        forward = self.get_position() + self.get_direction()
        enemies = [b for b in bots if b.team != self.team]

        # Find the nearest enemy
        nearest_enemy, distance = self.get_nearest_bot(enemies)
        if nearest_enemy:
            self.suggested_direction = self.get_direction_to_bot(nearest_enemy)

        # If an enemy is diagonal, turn towards it THEN make a decision
        if round(distance, 1) == round(math.sqrt(2), 1):
            good_moves.add(self.suggested_direction)

        if self.suggested_next_moves:
            good_moves.add(self.suggested_next_moves.pop())

        for b in bots:
            # Calculate some stuff
            b_forward = b.get_position() + b.get_direction()
            b_forward2 = b.get_position() + b.get_direction() + b.get_direction()

            # TODO: Never move forward onto a square next to an enemy!
            # First turn, then strafe

            # If the square I'm about to move into is occupied by anyone
            if b.get_position() == forward:
                if b in enemies:
                    # TODO: But if he's looking at me, can I dodge?
                    good_moves.add(Actions.Punch)
                else:
                    # Don't walk forward! We might collide
                    possible_moves.discard(Actions.MoveForward)
                    # If my ally is about to walk into me, don't just sit there
                    if b_forward == self.get_position():
                        possible_moves.discard(Actions.DoNothing)
                        possible_moves.discard(Actions.TurnLeft)
                        possible_moves.discard(Actions.TurnRight)
                        possible_moves.discard(Actions.TurnAround)
                        possible_moves.discard(Actions.Punch)

            # If the bot is about to move into the same square as I am
            if b_forward == forward:
                if b in enemies:
                    # Hopefully he'll move in and die.
                    good_moves.add(Actions.DoNothing)
                else:
                    possible_moves.discard(Actions.MoveForward)

            # If we both move forward, lead to a mutual kill. Avoid.
            if b_forward2 == forward and b in enemies:
                possible_moves.discard(Actions.MoveForward)
                if self.suggested_direction:
                    self.suggested_next_moves.append(self.suggested_direction)
                self.suggested_next_moves.append(Actions.DoNothing)
                self.suggested_next_moves.append(Actions.StrafeLeft)
                self.suggested_next_moves.append(Actions.StrafeRight)

            # TODO: If I just passed the bot, turn towards it

        # If there's something ahead to kill, hunt it down
        if enemies:
            good_moves.add(Actions.MoveForward)
        # Otherwise look for something new
        else:
            if self.suggested_direction:
                good_moves.add(self.suggested_direction)
                self.suggested_direction = None
            else:
                good_moves.add(Actions.TurnAround)
                good_moves.add(Actions.TurnRight)
                good_moves.add(Actions.TurnLeft)

        return self.choose_move(good_moves, possible_moves)

    def choose_move(self, good_moves, possible_moves):
        # Filter out any good moves that we also decided were bad
        good_moves = good_moves.intersection(possible_moves)

        # Prioritize punching
        if Actions.Punch in good_moves:
            return Actions.Punch

        # Pick one of the good moves, if possible, otherwise pick an OK move.
        if good_moves:
            choices = good_moves
        elif possible_moves:
            choices = possible_moves
        else:
            choices = {Actions.Suicide}  # Well, been nice knowin' ya.

        # Only punch deliberately
        choices.discard(Actions.Punch)
        return random.choice(list(choices))

    def get_nearest_bot(self, bots):
        nearest_bot = None
        nearest_dist = 999
        for b in bots:
            distance = (b.get_position() - self.get_position()).length()
            if distance < nearest_dist and distance != 0:
                nearest_dist = distance
                nearest_bot = b
        return nearest_bot, nearest_dist

    def get_direction_to_bot(self, bot):
        v = bot.get_position() - self.get_position()
        v.normalize()

        # Get the angle between the two vectors
        facing = self.get_direction()
        relative_angle = facing.relativeAngleDeg(v)

        # Check if it's small enough
        return Actions.TurnRight if relative_angle < 0 else Actions.TurnLeft
