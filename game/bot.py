from enum import Enum

from direct.actor.Actor import Actor
from direct.interval.LerpInterval import LerpPosHprInterval
from panda3d.core import Vec3, NodePath, TextNode
from game.util import make_fov


class Teams(tuple, Enum):
    Blue = (0, 0, 1, 1)
    Green = (0, 1, 0, 1)
    Red = (1, 0, 0, 1)


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
    Punch = 7  # Unleash a powerful melee attack
    Shoot = 8  # Fire a weak bullet forward

    # Lame Stuff
    DoNothing = 9
    Suicide = 10


class Bot:

    def __init__(self, team, position, direction):
        self._orders = Actions.DoNothing
        self._hp = 5
        self._death_played = False
        self._interval = None

        self.team = team

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

        # Floating Label
        text = TextNode('node name')
        text.setText(self.__class__.__name__)
        text.setAlign(TextNode.ACenter)
        self._name_label = self._model.attachNewNode(text)
        self._name_label.setBillboardPointEye()
        self._name_label.setPos(Vec3(0, 0, 6))
        self._name_label.setScale(2, 2, 2)

        # Debug Field of View Cones
        # fov = make_fov()
        # fov.reparentTo(self._model)

    def update(self, tick_number, visible_objects):
        return Actions.DoNothing

    def get_position(self):
        """Return a rounded version of the position vector."""
        p = self._model.getPos()
        return Vec3(round(p.x, 2), round(p.y, 2), round(p.z, 2))

    def get_direction(self):
        """Return a rounded version of the direction vector."""
        v = render.getRelativeVector(self._model, Vec3(0, 1, 0))
        v.normalize()
        return Vec3(round(v.x, 2), round(v.y, 2), round(v.z, 2))

    def get_name(self):
        return self.__class__.__name__

    def _get_orders(self, tick_number, visible_objects):
        # If the health is too low, die.
        if self._hp <= 0:
            self._orders = Actions.Suicide
            return

        # noinspection PyBroadException
        try:
            self._orders = self.update(tick_number, visible_objects)
        except Exception as e:
            print(type(self), e)
            self._orders = Actions.Suicide

    def _execute_orders(self, tick_length, battle):
        # Pre-calculate some useful things
        new_pos = self._model.getPos()
        new_dir = self._model.getHpr()
        velocity = self.get_direction()

        if self._orders == Actions.MoveForward:
            new_pos += velocity
            self.safe_loop('walk')

        elif self._orders == Actions.MoveBackward:
            new_pos -= velocity
            self.safe_loop('reverse-walk')

        elif self._orders == Actions.StrafeLeft:
            new_pos += velocity
            self.safe_loop('walk')

        elif self._orders == Actions.StrafeRight:
            new_pos += velocity
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

        elif self._orders == Actions.Shoot:
            self.shoot(battle)

        elif self._orders == Actions.DoNothing:
            self.safe_loop('idle')

        elif self._orders == Actions.Suicide:
            self._hp = 0
            self.take_damage(999)

        else:  # Bad orders detected! Kill this bot.
            self._hp = 0
            self.take_damage(999)

        # Animate the motion
        if self._hp <= 0:
            return
        tick = tick_length - 0.05  # Shave off a tiny bit to finish the interval
        self._interval = LerpPosHprInterval(self._model, tick, new_pos, new_dir)
        self._interval.start()

    def safe_loop(self, animation):
        if self._actor.getCurrentAnim() != animation and self._hp > 0:
            self._actor.loop(animation)

    def punch(self, battle):
        self._actor.play('punch')
        hazard = self.get_direction() + self.get_position()
        bot = battle.get_object_at_position(hazard)
        if isinstance(bot, Bot):
            bot.take_damage(5)

    def shoot(self, battle):
        print("Shooting not implemented yet!")
        self._actor.play('throw')

    def take_damage(self, amount):
        self._hp -= amount
        if self._hp <= 0:
            self._name_label.hide()
            if self._interval:
                self._interval.pause()
            if not self._death_played:
                self._actor.play('death')
                self._death_played = True
