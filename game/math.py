

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