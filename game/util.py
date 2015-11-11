import math
import random
from panda3d.core import Point3D, deg2Rad, NodePath
from panda3d.egg import EggData, EggVertexPool, EggPolygon, EggVertex, \
    loadEggData


def furthest_points(point_list):
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


def bresenham(start, end):
    """Bresenham's Line Algorithm
    Produces a list of tuples from start and end
    From http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm
    """
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points
