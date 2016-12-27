import math
import random
from panda3d.core import Point3D, deg2Rad, NodePath
from panda3d.egg import EggData, EggVertexPool, EggPolygon, EggVertex, \
    loadEggData


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


def make_fov(sweep=90, steps=16, scale=100):
    """Make a fan model so we can visualize the field of view for a bot."""
    z = 1 + random.uniform(-0.01, 0.01)

    data = EggData()

    vp = EggVertexPool('fan')
    data.addChild(vp)

    poly = EggPolygon()
    data.addChild(poly)

    v = EggVertex()
    v.setPos(Point3D(0, 0, z))
    poly.addVertex(vp.addVertex(v))

    rads = deg2Rad(sweep)

    for i in range(steps + 1):
        a = rads * i / steps
        y = math.sin(a)
        x = math.cos(a)

        v = EggVertex()
        v.setPos(Point3D(x*scale, y*scale, z))
        poly.addVertex(vp.addVertex(v))

    node = loadEggData(data)
    np = NodePath(node)
    np.setH(sweep/2)
    return np
