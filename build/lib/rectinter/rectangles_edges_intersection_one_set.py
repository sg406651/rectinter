"""
Imagine the following set of rectangles: We want to find all pairs of intersecting rectangles.
input: list of rectangles of the form (x_min, y_min, x_max, y_max)
output: list of pairs of intersecting rectangles (edges intersections)
"""
import sortedcontainers as sc
from sortedcontainers import SortedKeyList


def intervals_overlap(x1,x2,y1,y2):
    return max(x1,y1) <= min(x2,y2)


def sort_rectangles(rectangles):
    x_axes = []
    for rect_idx, rect in enumerate(rectangles):
        x_min, y_min, x_max, y_max = rect
        x_axes.append((x_min, rect_idx, 'start'))
        x_axes.append((x_max, rect_idx, 'end'))
    return sorted(x_axes, key=lambda x: x[0])


def single_x_value_intersection(R, rectangles, interections, p):
    if p[2] == 'start':
        rect_idx = p[1]
        rectangle = rectangles[rect_idx]
        bot = rectangle[1]
        top = rectangle[3]
        A = R.bisect_key_left(bot)
        B = R.bisect_key_right(top) - 1
        p_intersections = []
        for edge in R[A:B+1]:
            interections[rect_idx].append(edge[1])
            interections[edge[1]].append(rect_idx)
        R.add((bot, rect_idx, 'start'))
        R.add((top, rect_idx, 'end'))
    elif p[2] == 'end':
        rect_idx = p[1]
        rectangle = rectangles[rect_idx]
        bot = rectangle[1]
        top = rectangle[3]
        A = R.bisect_key_left(bot)
        B = R.bisect_key_right(top) - 1
        p_intersections = []
        for edge in R[A:B+1]:
            interections[rect_idx].append(edge[1])
            interections[edge[1]].append(rect_idx)
        interections[rect_idx].extend(p_intersections)
        R.remove((bot, rect_idx, 'start'))
        R.remove((top, rect_idx, 'end'))


def multiple_x_value_intersection(R, rectangles, interections, container):
    for p in container:
        if p[2] == 'start':
            rect_idx = p[1]
            rectangle = rectangles[rect_idx]
            bot = rectangle[1]
            top = rectangle[3]
            R.add((bot, rect_idx, 'start'))
            R.add((top, rect_idx, 'end'))
    for p in container:
        rect_idx = p[1]
        rectangle = rectangles[rect_idx]
        bot = rectangle[1]
        top = rectangle[3]
        A = R.bisect_key_left(bot)
        B = R.bisect_key_right(top) - 1
        p_intersections = []
        for edge in R[A:B+1]:
            interections[rect_idx].append(edge[1])
            interections[edge[1]].append(rect_idx)
        interections[rect_idx].extend(p_intersections)
    for p in container:
        if p[2] =='end':
            rect_idx = p[1]
            rectangle = rectangles[rect_idx]
            bot = rectangle[1]
            top = rectangle[3]
            R.remove((bot, rect_idx, 'start'))
            R.remove((top, rect_idx, 'end'))
    
    intervals = []
    for p in container:
        rect_idx = p[1]
        rectangle = rectangles[rect_idx]
        bot = rectangle[1]
        top = rectangle[3]
        intervals.append((bot, top, rect_idx))
    for i in range(len(intervals)):
        for j in range(i+1, len(intervals)):
            if intervals_overlap(intervals[i][0], intervals[i][1], intervals[j][0], intervals[j][1]):
                interections[intervals[i][2]].append(intervals[j][2])
                interections[intervals[j][2]].append(intervals[i][2])


        

def edges_intersection_one_set(rectangles):
    if rectangles == []:
        return []
    intersections = [[] for _ in range(len(rectangles))]
    Q = sort_rectangles(rectangles)
    R = SortedKeyList(key=lambda x: x[0])
    container = [Q[0]]
    for p in Q[1:]:
        if p[0] == container[-1][0]:
            container.append(p)
        elif len(container) == 1:
            single_x_value_intersection(R, rectangles, intersections, container[0])
            container = [p]
        else:
            multiple_x_value_intersection(R, rectangles, intersections, container)
            container = [p]
    for idx, rect in enumerate(intersections):
        interections_set = set(rect)
        interections_set.discard(idx)
        intersections[idx] = list(interections_set)
    return intersections
