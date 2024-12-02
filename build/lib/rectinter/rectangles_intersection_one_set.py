from rectinter.rectangles_edges_intersection_one_set import edges_intersection_one_set
from rectinter.rectangles_enclosure_one_set import rectangles_enclosure_one_set


def rectinter_one_set(rectangles):
    """
    returns all pairs of intersecting rectangles
    rectangles: list of tuples (x_min, y_min, x_max, y_max)
    """
    intersections = []
    edges_intersections = edges_intersection_one_set(rectangles)
    enclosures = rectangles_enclosure_one_set(rectangles)
    for i, edges in enumerate(edges_intersections):
        for edge in edges:
            enclosures[i].append(edge)
    for enclosure in enclosures:
        intersections.append(enclosure)
    intersections = [list(set(x)) for x in intersections]
    return [sorted(x) for x in intersections]
