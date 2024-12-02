from rectinter.rectangles_edges_intersection_two_sets import edges_intersection_two_sets
from rectinter.rectangles_enclosure_two_sets import rectangles_enclosure_two_sets

def rectinter_two_sets(set_A, set_B):
    """
    returns all pairs of intersecting rectangles between sets A and B (indexes 0 and 1 respectively)
    set_A: list of tuples (x_min, y_min, x_max, y_max)
    set_B: list of tuples (x_min, y_min, x_max, y_max)
    """
    edges_intersections_A, edges_intersections_B = edges_intersection_two_sets(set_A, set_B)
    enclosures_A, enclosures_B = rectangles_enclosure_two_sets(set_A, set_B)
    for i, enclosure in enumerate(enclosures_A):
        edges_intersections_A[i].extend(enclosure)
    for i, enclosure in enumerate(enclosures_B):
        edges_intersections_B[i].extend(enclosure)
    for idx, rect in enumerate(edges_intersections_A):
        interections_set = set(rect)
        edges_intersections_A[idx] = list(interections_set)
    for idx, rect in enumerate(edges_intersections_B):
        interections_set = set(rect)
        edges_intersections_B[idx] = list(interections_set)
    for idx, rect in enumerate(edges_intersections_A):
        edges_intersections_A[idx] = sorted(rect)
    for idx, rect in enumerate(edges_intersections_B):
        edges_intersections_B[idx] = sorted(rect)
    return edges_intersections_A, edges_intersections_B

