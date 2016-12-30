from __future__ import print_function, unicode_literals, division

import json
from enum import Enum

from direct.actor.Actor import Actor
from direct.interval.LerpInterval import LerpPosHprInterval
from panda3d.core import Vec3, NodePath, TextNode

from game.announcer import Announcement, Color


KILLSTREAK_MESSAGES = {
    2: ("{} is SICK with a double kill!", Announcement.DoubleKill),
    3: ("{} is ON FIRE with a triple kill!", Announcement.TripleKill),
    4: ("{} is DOMINATING with a 4x kill streak!", Announcement.Dominating),
}
MEGA_KILLSTREAK_MESSAGE = ("{} is GODLIKE with a {}x kill streak!",
                           Announcement.Godlike)


class Actions(Enum):
    # Movement
    MoveForward = 0
    MoveBackward = 1
    StrafeLeft = 2
    StrafeRight = 3

    # Rotation
    TurnLeft = 4
    TurnRight = 5
    TurnAround = 6

    # Attacking
    Punch = 7

    # Lame Stuff
    DoNothing = 8
    Suicide = 9


class Bot(object):
    """The base class for all bots. Just subclass and implement `update` to
    build your very own battle AI!
    """
    _orders = Actions.DoNothing
    _death_played = False
    _interval = None
    alive = True
    kills = 0
    _global_stats = None

    def __init__(self, team, position, direction):
        # Initialize some vars
        self.team = team
        self._load_global_stats()

        # Create an empty node to contain the actor, nametag, and FOV fan.
        self._model = NodePath('bot')
        self._model.reparentTo(render)
        self._model.setPos(position)
        self._model.setHpr(direction, 0, 0)
        self._model.setColorScale(*self.team)
        self._model.setScale(.2, .2, .2)

        # Load the animations
        self._actor = Actor("models/RockGolem", {
            'idle': 'models/RockGolem-idle',
            'walk': 'models/RockGolem-walk',
            'reverse-walk': 'models/RockGolem-walk',
            'punch': 'models/RockGolem-punch',
            'death': 'models/RockGolem-death',
            'throw': 'models/RockGolem-throw',
        })
        self._actor.setPlayRate(2.65, 'walk')
        self._actor.setPlayRate(-2.65, 'reverse-walk')
        self._actor.setPlayRate(4, 'punch')
        self._actor.setPlayRate(5.25, 'throw')
        self._actor.setBlend(frameBlend=True)
        self._actor.reparentTo(self._model)
        self._actor.loop('idle')
        self._actor.setH(180)

        # Floating Name Label
        text = TextNode('node name')
        text.setText(self.__class__.__name__)
        text.setAlign(TextNode.ACenter)
        self._name_label = self._model.attachNewNode(text)
        self._name_label.setBillboardPointEye()
        self._name_label.setPos(Vec3(0, 0, 6))
        self._name_label.setScale(3, 3, 3)

        # Increment the number of games played
        self.record_stat("games", 1)

    def __str__(self):
        return self.name

    def update(self, tick_number, visible_objects):
        """Subclass and implement this method to make your own bot!"""
        raise NotImplementedError()

    @property
    def _global_stats_filepath(self):
        """Return the filepath to the stats json file."""
        return "stats/{}.json".format(self.name)

    def _load_global_stats(self):
        try:
            with open(self._global_stats_filepath, 'r') as infile:
                self._global_stats = json.load(infile)
        except IOError:
            self._global_stats = {}

    def _write_global_stats(self):
        with open(self._global_stats_filepath, 'w') as outfile:
            json.dump(self._global_stats, outfile)

    def record_stat(self, key, value):
        """Add an integer to a stat safely."""
        assert type(value) == int
        old_val = self._global_stats.get(key, 0)
        self._global_stats[key] = old_val + value

    @property
    def position(self):
        """Return a rounded version of the position vector."""
        # TODO: Have both model and "game position" so low framerate is ok.
        p = self._model.getPos()
        return Vec3(round(p.x, 0), round(p.y, 0), round(p.z, 0))
        # return Vec3(self._position)

    @property
    def direction(self):
        """Return a rounded version of the direction vector."""
        # TODO: Have both model and "game position" so low framerate is ok.
        v = render.getRelativeVector(self._model, Vec3(0, 1, 0))
        v.normalize()
        return Vec3(round(v.x, 0), round(v.y, 0), round(v.z, 0))

    @property
    def right_direction(self):
        """Return a unit vector pointing to the bot's right."""
        return Vec3(self.direction.y, -self.direction.x, self.direction.z)

    @property
    def left_direction(self):
        """Return a unit vector pointing to the bot's right."""
        return Vec3(-self.direction.y, self.direction.x, self.direction.z)

    @property
    def name(self):
        return self.__class__.__name__

    def _get_orders(self, tick_number, visible_objects):
        # noinspection PyBroadException
        try:
            self._orders = self.update(tick_number, visible_objects)
        except Exception as e:
            print(self.__class__.__name__, e)
            self._orders = None

    def _execute_orders(self, tick_length, battle):
        # Pre-calculate some useful things
        new_pos = self.position
        new_dir = self._model.getHpr()  # TODO: Getting rounding errors here
        velocity = self.direction

        # If we're outside of the arena, take damage
        ARENA_SIZE = 13  # TODO: Move this to battle.py
        if new_pos.length() > ARENA_SIZE:
            battle.announcer.announce("{} fled the battle!".format(self.name))
            self.die()

        # Execute the order
        if self._orders == Actions.MoveForward:
            new_pos += velocity
            self.safe_loop('walk')

        elif self._orders == Actions.MoveBackward:
            new_pos -= velocity
            self.safe_loop('reverse-walk')

        elif self._orders == Actions.StrafeLeft:
            v = render.getRelativeVector(self._model, Vec3(-1, 0, 0))
            v.normalize()
            v = Vec3(round(v.x, 0), round(v.y, 0), round(v.z, 0))
            new_pos += v
            self.safe_loop('walk')

        elif self._orders == Actions.StrafeRight:
            v = render.getRelativeVector(self._model, Vec3(1, 0, 0))
            v.normalize()
            v = Vec3(round(v.x, 0), round(v.y, 0), round(v.z, 0))
            new_pos += v
            self.safe_loop('walk')

        elif self._orders == Actions.TurnLeft:
            new_dir.x += 90
            self.safe_loop('walk')

        elif self._orders == Actions.TurnAround:
            new_dir.x += 180
            self.safe_loop('walk')

        elif self._orders == Actions.TurnRight:
            new_dir.x -= 90
            self.safe_loop('walk')

        elif self._orders == Actions.Punch:
            self.punch(battle)

        elif self._orders == Actions.DoNothing:
            self.safe_loop('idle')

        elif self._orders == Actions.Suicide:
            battle.announcer.announce("{} killed itself.".format(self.name))
            self.die()
            self.record_stat("suicides", 1)
            # TODO: Can we track "denies" as well?

        else:  # Bad orders detected! Kill this bot.
            battle.announcer.announce("{} made an illegal move and died.".format(self.name))
            self.die()
            self.record_stat("exceptions", 1)

        # Animate the motion
        if not self.alive:
            return
        self._interval = LerpPosHprInterval(
            self._model, tick_length, new_pos, new_dir)
        self._interval.start()

    def safe_loop(self, animation):
        if self._death_played:
            return
        if self._actor.getCurrentAnim() != animation:
            self._actor.loop(animation)

    def _kill(self, bot, battle):
        bot.die()

        # Show the standard kill text
        if bot.team == self.team:
            message = "{self} killed its teammate {target}!"
            self.record_stat("teamkills", 1)
        else:
            message = "{self} just pwned {target}!"
            self.record_stat("kills", 1)
            self.kills += 1
        battle.announcer.announce(
            message.format(self=self.name, target=bot.name),
            color=self.team, sfx=Announcement.Ownage)

        # Show special text for kill streaks
        if self.kills > 1:
            message, sfx = KILLSTREAK_MESSAGES.get(
                self.kills, MEGA_KILLSTREAK_MESSAGE)
            battle.announcer.announce(
                message.format(self.name, self.kills),
                color=Color.Orange, sfx=sfx)

    def punch(self, battle):
        """Check the bots on the squares """
        # Ensure mutual kills animate correctly
        if not self._death_played:
            self._actor.play('punch')

        # Check the square in front of the bot and on the bot's square
        bots = (
            battle.get_bots_at_position(self.direction + self.position) +
            battle.get_bots_at_position(self.position)
        )

        # Annihilate those bots
        for bot in bots:
            if bot is not self:
                self._kill(bot, battle)

    def die(self):
        self.alive = False
        self._name_label.hide()
        self.record_stat("deaths", 1)
        if self._interval:
            self._interval.pause()
        if not self._death_played:
            self._actor.play('death')
            self._death_played = True

    def delete(self):
        self._model.removeNode()
        self._actor.cleanup()
        self._name_label.removeNode()
