from sortedcontainers import SortedKeyList


def intervals_overlap(x1,x2,y1,y2):
    return max(x1,y1) <= min(x2,y2)


def sort_rectangles(set_A, set_B):
    x_axes = []
    for rect_idx, rect in enumerate(set_A):
        x_min, y_min, x_max, y_max = rect
        x_axes.append((x_min, rect_idx, 'start', 'A'))
        x_axes.append((x_max, rect_idx, 'end', 'A'))
    for rect_idx, rect in enumerate(set_B):
        x_min, y_min, x_max, y_max = rect
        x_axes.append((x_min, rect_idx, 'start', 'B'))
        x_axes.append((x_max, rect_idx, 'end', 'B'))
    return sorted(x_axes, key=lambda x: x[0])


def single_x_value_intersection(R_A, R_B, set_A, set_B, interections_A, interections_B, p):
    if p[3] == 'A':
        rect_idx = p[1]
        rectangle = set_A[rect_idx]
        bot = rectangle[1]
        top = rectangle[3]
        p_intersections = []
        A = R_B.bisect_key_left(bot)
        B = R_B.bisect_key_right(top) - 1
        for edge in R_B[A:B+1]:
            # p_intersections.append(edge[1])
            interections_A[rect_idx].append(edge[1])
            interections_B[edge[1]].append(rect_idx)
        # interections_A[rect_idx].extend(p_intersections)

        if p[2] == 'start':
            R_A.add((bot, rect_idx, 'start', 'A'))
            R_A.add((top, rect_idx, 'end', 'A'))
        else:
            R_A.remove((bot, rect_idx, 'start', 'A'))
            R_A.remove((top, rect_idx, 'end', 'A'))
    else:
        rect_idx = p[1]
        rectangle = set_B[rect_idx]
        bot = rectangle[1]
        top = rectangle[3]
        p_intersections = []
        A = R_A.bisect_key_left(bot)
        B = R_A.bisect_key_right(top) - 1
        for edge in R_A[A:B+1]:
            # p_intersections.append(edge[1])
            interections_B[rect_idx].append(edge[1])
            interections_A[edge[1]].append(rect_idx)
        # interections_B[rect_idx].extend(p_intersections)
        if p[2] == 'start':
            R_B.add((bot, rect_idx, 'start', 'B'))
            R_B.add((top, rect_idx, 'end', 'B'))
        else:
            R_B.remove((bot, rect_idx, 'start', 'B'))
            R_B.remove((top, rect_idx, 'end', 'B'))


def multiple_x_value_intersection(R_A, R_B, set_A, set_B, interections_A, interections_B, container):
    for p in container:
        if p[2] == 'start':
            if p[3] == 'A':
                rect_idx = p[1]
                rectangle = set_A[rect_idx]
                bot = rectangle[1]
                top = rectangle[3]
                R_A.add((bot, rect_idx, 'start', 'A'))
                R_A.add((top, rect_idx, 'end', 'A'))
            else:
                rect_idx = p[1]
                rectangle = set_B[rect_idx]
                bot = rectangle[1]
                top = rectangle[3]
                R_B.add((bot, rect_idx, 'start', 'B'))
                R_B.add((top, rect_idx, 'end', 'B'))
    for p in container:
        if p[3] == 'A':
            rect_idx = p[1]
            rectangle = set_A[rect_idx]
            bot = rectangle[1]
            top = rectangle[3]
            A = R_B.bisect_key_left(bot)
            B = R_B.bisect_key_right(top) - 1
            p_intersections = []
            for edge in R_B[A:B+1]:
                # p_intersections.append(edge[1])
                interections_A[rect_idx].append(edge[1])
                interections_B[edge[1]].append(rect_idx)
            # interections_A[rect_idx].extend(p_intersections)
        else:
            rect_idx = p[1]
            rectangle = set_B[rect_idx]
            bot = rectangle[1]
            top = rectangle[3]
            A = R_A.bisect_key_left(bot)
            B = R_A.bisect_key_right(top) - 1
            p_intersections = []
            for edge in R_A[A:B+1]:
                # p_intersections.append(edge[1])
                interections_B[rect_idx].append(edge[1])
                interections_A[edge[1]].append(rect_idx)
            # interections_B[rect_idx].extend(p_intersections)
    for p in container:
        if p[2] == 'end':
            if p[3] == 'A':
                rect_idx = p[1]
                rectangle = set_A[rect_idx]
                bot = rectangle[1]
                top = rectangle[3]
                R_A.remove((bot, rect_idx, 'start', 'A'))
                R_A.remove((top, rect_idx, 'end', 'A'))
            else:
                rect_idx = p[1]
                rectangle = set_B[rect_idx]
                bot = rectangle[1]
                top = rectangle[3]
                R_B.remove((bot, rect_idx, 'start', 'B'))
                R_B.remove((top, rect_idx, 'end', 'B'))
    
    A_intervals = []
    B_intervals = []
    for p in container:
        if p[3] == 'A':
            rect_idx = p[1]
            rectangle = set_A[rect_idx]
            bot = rectangle[1]
            top = rectangle[3]
            A_intervals.append((bot, top, rect_idx))
        else:
            rect_idx = p[1]
            rectangle = set_B[rect_idx]
            bot = rectangle[1]
            top = rectangle[3]
            B_intervals.append((bot, top, rect_idx))
    for A_int in A_intervals:
        for B_int in B_intervals:
            if intervals_overlap(A_int[0], A_int[1], B_int[0], B_int[1]):
                interections_A[A_int[2]].append(B_int[2])
                interections_B[B_int[2]].append(A_int[2])
                

def edges_intersection_two_sets(set_A, set_B):
    if set_A == [] and set_B == []:
        return [], []
    intersections_A = [[] for _ in range(len(set_A))]
    intersections_B = [[] for _ in range(len(set_B))]
    Q = sort_rectangles(set_A, set_B)
    R_A = SortedKeyList(key=lambda x: x[0])
    R_B = SortedKeyList(key=lambda x: x[0])
    container = [Q[0]]
    for p in Q[1:]:
        if p[0] == container[-1][0]:
            container.append(p)
        elif len(container) == 1:
            single_x_value_intersection(R_A, R_B, set_A, set_B, intersections_A, intersections_B, container[0])
            container = [p]
        else:
            multiple_x_value_intersection(R_A, R_B, set_A, set_B, intersections_A, intersections_B, container)
            container = [p]
    for idx, rect in enumerate(intersections_A):
        interections_set = set(rect)
        intersections_A[idx] = list(interections_set)
    for idx, rect in enumerate(intersections_B):
        interections_set = set(rect)
        intersections_B[idx] = list(interections_set)
    return intersections_A, intersections_B

