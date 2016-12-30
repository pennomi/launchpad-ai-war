from __future__ import print_function, unicode_literals
from importlib import import_module
import os
import random

from panda3d.core import Point3, Vec3

from game.announcer import Announcer, Announcement, make_label, Color
from game.bot import Bot, Actions


# TODO: What if the reset timer was the amount of time since the last death?
# TODO: 15-20 seconds would be fine there
RESET_TIMER = 60  # 1 minute


# noinspection PyProtectedMember
class BattleArena:
    radius = 10
    tick = 0
    camera_pos = Vec3(10, 0, 30)
    camera_look = Vec3(0, 0, 0)
    bots = []
    announcer = Announcer()

    def __init__(self):
        # Load the arena model
        self.model = loader.loadModel("models/Arena.egg")
        self.model.reparentTo(render)
        self.reset_label = make_label("", Color.White)
        self.reset_label.setY(-0.9)

        # Load the bots dynamically
        self.bot_classes = list(self.get_classes())
        print("Loading bots:", [c.__name__ for c in self.bot_classes])

        # Set up the battle
        self.reset()

    def reset(self):
        # TODO: Add some sort of start/end animation?

        # Clean up messages
        self.announcer.reset()

        # Setup
        self.tick = 0
        self.announcer.announce(
            "Welcome to the LAUNCHPAD BATTLE ARENA!", color=(0.2, 1, 0.2, 1))

        # Spawn the bots
        for b in self.bots:
            b._write_global_stats()
            b.delete()
        self.bots = []
        random.shuffle(self.bot_classes)
        bots_offset = len(self.bot_classes) // 2
        for i, cls in enumerate(self.bot_classes):
            self.bots.append(cls(
                Color.Blue if i % 2 else Color.Red,
                Vec3(-bots_offset + i + random.randint(0, 1),
                     -6 if i % 2 else 6 + random.randint(-1, 1),
                     0),
                0 if i % 2 else 180
            ))

    def update(self, dt):
        """Once a second, have each bot send in its orders. Then have those
        bots animate their actions.
        """
        self.tick += 1

        # Check reset parameters
        living_bots = [b for b in self.bots if b.alive]
        if not living_bots:  # Everyone's dead
            self.reset()
        elif self.tick > RESET_TIMER:  # Out of time
            self.reset()
        elif len({b.team for b in living_bots}) == 1:  # Only one team left
            self.reset()

        # Update the reset timer
        self.reset_label.setText(
            "{} seconds left in match".format(RESET_TIMER - self.tick))

        # Calculate any collisions between any bots from last time
        self._kill_overlapping_bots()

        living_bots = [b for b in self.bots if b.alive]
        # First get all orders (so later bots don't have more information)
        for b in living_bots:
            b._get_orders(self.tick, self.get_visible_objects(b))
        # TODO: Instead sort the list by action priority then iterate once
        # TODO: For instance, suicide comes first
        # Punching comes first
        for b in [b for b in living_bots if b._orders == Actions.Punch]:
            b._execute_orders(dt, self)
        # Then move everyone (no dodging!)
        for b in [b for b in living_bots if b._orders != Actions.Punch]:
            b._execute_orders(dt, self)

        # Play the sound that summarizes this round best
        self.announcer.play_sound()

    def get_bots_at_position(self, v):
        return [b for b in self.bots if b.position == v and b.alive]

    def _kill_overlapping_bots(self):
        """Calculate which bots are at the same position and kill them."""
        for b in self.bots:
            if not b.alive:
                continue
            bots = self.get_bots_at_position(b.position)
            if len(bots) > 1:
                self.announcer.announce(
                    "{} collided!".format(" & ".join(str(b) for b in bots)),
                    sfx=Announcement.Carnage)
                for _ in bots:
                    _.die()
                    _.record_stat("collisions", 1)

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
        if not bot.alive:
            return []

        objects = []

        # Get the direction the bot is facing
        facing = bot.direction

        for other in self.bots:
            # Don't track self or dead things
            if bot == other or not other.alive:
                continue

            # Get the relative vector of the bots
            v = other.position - bot.position
            v.normalize()

            # Get the angle between the two vectors
            relative_angle = facing.relativeAngleDeg(v)

            # Check if it's small enough
            if abs(relative_angle) <= 45:  # ie. a 90 degree cone
                objects.append(other)

        return objects

    # noinspection PyUnresolvedReferences
    def update_camera(self, dt):
        """Try to keep everyone in view at the same time."""
        # Use the actual model position here for smoother camera movement
        line = furthest_points(c._model.getPos() for c in self.bots if c.alive)

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
        camera_speed = dt
        self.camera_pos += (camera_pos - self.camera_pos) * camera_speed
        self.camera_look += (center - self.camera_look) * camera_speed
        camera.setPos(render, *self.camera_pos)
        camera.lookAt(Point3(*self.camera_look))


def furthest_points(point_list):
    """Taking a list of points, calculate which two are furthest away from
    each other. (Inefficient algorithm, but who cares with a dozen points?)
    """
    greatest_distance = 0
    best_points = None
    for p1 in point_list:
        for p2 in point_list:
            distance = (p1 - p2).length()
            if distance > greatest_distance:
                greatest_distance = distance
                best_points = (p1, p2)
    return best_points
