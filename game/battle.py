from importlib import import_module
import os
import random
from panda3d.core import Point3, Vec3

from game.math import furthest_points
from game.bot import Bot, Teams


# noinspection PyProtectedMember
class BattleArena:
    radius = 10
    tick_number = 0
    camera_pos = Vec3(0, 0, 0)
    camera_look = Vec3(0, 0, 0)

    def __init__(self):
        # Load the arena model
        self.model = loader.loadModel("models/level1.egg")
        self.model.reparentTo(render)

        # Set up the map (for later)
        self.map = [[0 for _ in range(30)] for _ in range(30)]

        # Set up variables
        self.bots = []
        self.projectiles = []

        # Load the bots dynamically
        bot_classes = self.get_classes()
        print("Loading bots:", *[c.__name__ for c in bot_classes])
        for cls in bot_classes:
            self.bots.append(cls(
                random.choice(list(Teams)),
                Vec3(random.uniform(-3, 3), random.uniform(-3, 3), 0),
                random.choice([0, 90, 180, 360])
            ))

    def get_classes(self):
        """Dynamically import all Bot subclasses from files at `game.ai.*`
        and return them in a list.
        """
        classes = []
        for path in os.listdir(os.path.join('game', 'ai')):
            import_path = 'game.ai.{}'.format(path.split('.')[0])
            module = import_module(import_path)
            attrs = dir(module)
            for a in attrs:
                attr = getattr(module, a)
                if hasattr(attr, '__bases__') and Bot in attr.__bases__:
                    classes.append(attr)
        return classes

    def update(self, dt):
        """Once a second, have each bot send in its orders. Then have those
        bots animate their actions.
        """
        self.tick_number += 1
        for c in self.bots:
            c._get_orders(self.tick_number)
        for c in self.bots:
            c._execute_orders(dt)
        for p in self.projectiles:
            p.update(dt)

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
            camera_offset *= 10

            # Choose the way that's closer to the current camera position
            d1 = abs((center + camera_offset - self.camera_pos).length())
            d2 = abs((center - camera_offset - self.camera_pos).length())
            camera_pos = Vec3(center)
            camera_pos += camera_offset if d1 < d2 else -camera_offset
            camera_pos.z = 10
        else:
            camera_pos = Vec3(10, 10, 10)
            center = Vec3(0, 0, 0)

        # Smoothly interpolate.
        camera_speed = 2 * dt
        self.camera_pos += (camera_pos - self.camera_pos) * camera_speed
        self.camera_look += (center - self.camera_look) * camera_speed
        camera.setPos(render, *self.camera_pos)
        camera.lookAt(Point3(*self.camera_look))
