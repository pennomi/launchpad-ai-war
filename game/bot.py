from enum import Enum

from direct.actor.Actor import Actor
from direct.interval.LerpInterval import LerpPosHprInterval
from panda3d.core import Vec3


class Teams(tuple, Enum):
    Blue = (.25, .25, 1, 1)
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

    # Attacking
    Punch = 6  # Unleash a powerful melee attack
    Shoot = 7  # Fire a weak bullet forward

    # Lame Stuff
    DoNothing = 8
    Suicide = 9


class Bot:
    _orders = Actions.DoNothing
    _hp = 5
    _death_played = False

    def __init__(self, team, position: Vec3, direction: int):
        self.team = team

        # Load the animations
        self._model = Actor("models/RockGolem", {
            'idle': 'models/RockGolem-idle',
            'walk': 'models/RockGolem-walk',
            'reverse-walk': 'models/RockGolem-walk',
            'punch': 'models/RockGolem-punch',
            'death': 'models/RockGolem-death',
        })
        self._model.setPlayRate(2.65, 'walk')
        self._model.setPlayRate(-2.65, 'reverse-walk')
        self._model.setPlayRate(4, 'punch')

        # Initialize the model
        self._model.setBlend(frameBlend=True)
        self._model.setScale(.15, .15, .15)
        self._model.reparentTo(render)
        self._model.loop('idle')
        self._model.setPos(position)
        self._model.setHpr(direction, 0, 0)
        self._model.setColorScale(*self.team)

    def update(self, tick_number):
        return Actions.DoNothing

    def _get_orders(self, tick_number):
        if self._hp <= 0:
            return

        # noinspection PyBroadException
        try:
            self._orders = self.update(tick_number)
        except Exception as e:
            print(type(self), e)
            self._orders = Actions.Suicide

    def _execute_orders(self, tick_length):
        # Pre-calculate some useful things
        new_pos = self._model.getPos()
        new_dir = self._model.getHpr()
        velocity = render.getRelativeVector(self._model, Vec3(0, -1, 0))
        velocity.normalize()

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

        elif self._orders == Actions.TurnRight:
            new_dir.x -= 90
            self.safe_loop('walk')

        elif self._orders == Actions.Punch:
            self.punch()

        elif self._orders == Actions.Shoot:
            self.shoot()

        elif self._orders == Actions.DoNothing:
            self.safe_loop('idle')

        elif self._orders == Actions.Suicide:
            self._hp = 0
            self.die()

        else:  # Bad orders detected! Kill this bot.
            self._hp = 0
            self.die()

        # Animate the motion
        LerpPosHprInterval(self._model, tick_length, new_pos, new_dir).start()

    def safe_loop(self, animation: str) -> None:
        if self._model.getCurrentAnim() != animation:
            self._model.loop(animation)

    def die(self) -> None:
        if not self._death_played:
            self._model.play('death')
            self._death_played = True

    def punch(self) -> None:
        print("Punching not implemented yet!")
        self._model.play('punch')

    def shoot(self) -> None:
        print("Shooting not implemented yet!")
        self._model.play('shoot')
