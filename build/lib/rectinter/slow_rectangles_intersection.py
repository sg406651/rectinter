def do_rectangles_intersect(rect1, rect2):
    """
    Check if two rectangles intersect.
    
    Each rectangle is defined by a tuple (x1, y1, x2, y2), where:
    (x1, y1) is the bottom-left corner, and
    (x2, y2) is the top-right corner.
    """

    x1_1, y1_1, x2_1, y2_1 = rect1
    x1_2, y1_2, x2_2, y2_2 = rect2
    
    if x1_1 > x2_2 or x1_2 > x2_1:
        return False
    
    if y1_1 > y2_2 or y1_2 > y2_1:
        return False
    
    return True

def slow_rectangles_intersection_one_set(rectangles):
    """
    Find all intersecting rectangles.
    
    rectangles (list of tuples): List of rectangles defined by their bottom-left and top-right corners.
    
    returns list of tuples: List of intersecting rectangle pairs.
    """
    n = len(rectangles)
    intersecting_pairs = [[] for _ in range(n)]
    
    for i in range(n):
        for j in range(i + 1, n):
            if do_rectangles_intersect(rectangles[i], rectangles[j]):
                intersecting_pairs[i].append(j)
                intersecting_pairs[j].append(i)
    return [sorted(x) for x in intersecting_pairs]


def slow_rectangles_intersection_two_sets(set_A, set_B):
    """
    Find all intersecting rectangles between two sets.
    
    set_A (list of tuples): List of rectangles from set A.
    set_B (list of tuples): List of rectangles from set B.

    returns list of tuples: List of intersecting rectangle pairs.
    """
    n_A = len(set_A)
    n_B = len(set_B)
    intersections_A = [[] for _ in range(n_A)]
    intersections_B = [[] for _ in range(n_B)]
    
    for i in range(n_A):
        for j in range(n_B):
            if do_rectangles_intersect(set_A[i], set_B[j]):
                intersections_A[i].append(j)
                intersections_B[j].append(i)
    intersections_A = [sorted(x) for x in intersections_A]
    intersections_B = [sorted(x) for x in intersections_B]
    return intersections_A, intersections_B
