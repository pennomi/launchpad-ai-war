from __future__ import print_function
from importlib import import_module
import os
import random

from direct.gui.OnscreenText import OnscreenText
from panda3d.core import Point3, Vec3, TextNode
from game.util import furthest_points
from game.bot import Bot, Teams, Actions


RESET_TIMER = 2 * 60  # 2 minutes


def make_label(m):
    return OnscreenText(
        text=m, pos=Vec3(-1.2, .25, 0), scale=0.05,
        fg=(1.0, 1.0, 1.0, 1.0), align=TextNode.ALeft,
        shadow=(0, 0, 0, 1),
    )


# noinspection PyProtectedMember
class BattleArena:
    radius = 10
    tick = 0
    camera_pos = Vec3(10, 0, 30)
    camera_look = Vec3(0, 0, 0)
    first_blood = 0  # 0 for not triggered, 1 for triggering, 2 for played
    bots = []

    def __init__(self):
        # Load the arena model
        self.model = loader.loadModel("models/Arena.egg")
        self.model.reparentTo(render)
        self.reset_label = make_label("")
        self.reset_label.setY(-0.9)

        # Prepare several death message text boxes
        self.death_messages = []

        # Load the bots dynamically
        self.bot_classes = list(self.get_classes())
        print("Loading bots:", [c.__name__ for c in self.bot_classes])

        # Set up the battle
        self.reset()

    def reset(self):
        self.first_blood = 0
        self.tick = 0

        # Clean up messages
        for m in self.death_messages:
            m.removeNode()
        self.death_messages = []
        self.announce("Welcome to the LAUNCHPAD BATTLE ARENA!",
                      color=(0.2, 1, 0.2, 1))

        # Spawn the bots
        for b in self.bots:
            b.delete()
        self.bots = []
        random.shuffle(self.bot_classes)
        bots_offset = len(self.bot_classes) // 2
        for i, cls in enumerate(self.bot_classes):
            self.bots.append(cls(
                Teams.Blue if i % 2 else Teams.Red,
                Vec3(-bots_offset + i + random.randint(0, 1),
                     -6 if i % 2 else 6 + random.randint(-1, 1),
                     0),
                0 if i % 2 else 180
            ))

    def announce(self, message, color=(1.0, 1.0, 1.0, 1.0), sfx=None):
        # Add the label
        l = make_label(message)
        l.setColorScale(color)
        self.death_messages.append(l)

        # Layout the messages
        d = len(self.death_messages)
        for i, m in enumerate(self.death_messages):
            offset = max(5 - d, 0)
            m.setY((d - i + offset) / 15. + .5)

        if sfx:
            if self.first_blood == 0:
                self.first_blood = 1
                sound = loader.loadSfx("sound/announcer/FirstBlood.wav")
                sound.play()
            # Don't play over the top of the first blood announcement
            if self.first_blood == 2:
                sound = loader.loadSfx("sound/announcer/{}.wav".format(sfx))
                sound.play()

    def update(self, dt):
        """Once a second, have each bot send in its orders. Then have those
        bots animate their actions.
        """
        self.tick += 1
        living_bots = [b for b in self.bots if b._hp > 0]
        # First get all orders (so later bots don't have more information)
        for b in living_bots:
            b._get_orders(self.tick, self.get_visible_objects(b))
        # Then move everyone (so we can dodge)
        for b in [b for b in living_bots if b._orders != Actions.Punch]:
            b._execute_orders(dt, self)
        # Punching comes last
        for b in [b for b in living_bots if b._orders == Actions.Punch]:
            b._execute_orders(dt, self)
        # Calculate any collisions between any bots
        self.kill_overlapping_bots()
        # Tell sfx that they're ok to play again
        if self.first_blood == 1:
            self.first_blood = 2

        # Check reset parameters
        if not living_bots:
            self.reset()
        else:
            t = living_bots[0].team
            if all([b.team == t for b in living_bots]):
                self.reset()
        if self.tick > RESET_TIMER:
            self.reset()

        # update the reset timer
        self.reset_label.setText(
            "{} seconds left in match".format(RESET_TIMER - self.tick))

    def get_object_at_position(self, v):
        for b in self.bots:
            if b.get_position() == v and b._hp > 0:
                return b
        return None

    def kill_overlapping_bots(self):
        for b in self.bots:
            if b._hp <= 0:
                continue
            other = self.get_object_at_position(b.get_position())
            if other and b and other != b:
                self.announce(
                    "{} and {} collided!".format(
                        b.get_name(), other.get_name()),
                    sfx="Carnage")
                b.take_damage(999)
                other.take_damage(999)

    def get_classes(self):
        """Dynamically import all Bot subclasses from files at `game.ai.*`
        and return them in a list.
        """
        classes = set()
        for path in os.listdir(os.path.join('game', 'ai')):
            import_path = 'game.ai.{}'.format(path.split('.')[0])
            module = import_module(import_path)
            attrs = dir(module)
            for a in attrs:
                attr = getattr(module, a)
                if hasattr(attr, '__bases__') and Bot in attr.__bases__:
                    classes.add(attr)
        return classes

    def get_visible_objects(self, bot):
        if bot._hp <= 0:
            return []

        objects = []

        # Get the direction the bot is facing
        facing = bot.get_direction()

        for other in self.bots:
            # Don't track self
            if bot == other or other._hp <= 0:
                continue

            # Get the relative vector of the bots
            v = other._model.getPos() - bot._model.getPos()
            v.normalize()

            # Get the angle between the two vectors
            relative_angle = facing.relativeAngleDeg(v)

            # Check if it's small enough
            if abs(relative_angle) <= 45:  # ie. a 90 degree cone
                objects.append(other)

        return objects

    def update_camera(self, dt):
        """Try to keep everyone in view at the same time."""
        living_players = [c for c in self.bots if c._hp > 0]
        line = furthest_points(c._model.getPos() for c in living_players)

        if line:
            direction = line[1] - line[0]
            center = (line[0] + line[1]) / 2

            # Set the camera position
            direction.normalize()
            camera_offset = direction.cross(Vec3(0, 0, 1))
            camera_offset.normalize()
            camera_offset *= 20

            # Choose the way that's closer to the current camera position
            d1 = abs((center + camera_offset - self.camera_pos).length())
            d2 = abs((center - camera_offset - self.camera_pos).length())
            camera_pos = Vec3(center)
            camera_pos += camera_offset if d1 < d2 else -camera_offset
            camera_pos.z = 25
        else:
            camera_pos = Vec3(10, 10, 10)
            center = Vec3(0, 0, 0)

        # Smoothly interpolate.
        camera_speed = 2 * dt
        self.camera_pos += (camera_pos - self.camera_pos) * camera_speed
        self.camera_look += (center - self.camera_look) * camera_speed
        camera.setPos(render, *self.camera_pos)
        camera.lookAt(Point3(*self.camera_look))
