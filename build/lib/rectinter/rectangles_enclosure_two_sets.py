from numba import typed, types
from numba.typed import Dict


def create_interval_bst(sorted_list: list):
    """
    creates a segment tree from a sorted list of points
    """
    def build_bst(start, end):
        if start == end - 1:
            node = [sorted_list[start], sorted_list[end], None, None, []]
            nodes.append(node)
            return len(nodes) - 1
        
        mid = (start + end) // 2
        node_index = len(nodes)
        node = [sorted_list[start], sorted_list[end], None, None, []]
        nodes.append(node)
        
        left_child = build_bst(start, mid)
        if left_child is not None:
            node[2] = left_child
        
        right_child = build_bst(mid, end)
        if right_child is not None:
            node[3] = right_child
        
        return node_index

    nodes = []
    build_bst(0, len(sorted_list) - 1)
    return nodes


def create_auxiliary_table(n: int):
    """
    creates auxiliary table to eficiently delete queries
    """
    return typed.List([Dict.empty(key_type=types.int64, value_type=types.int64) for _ in range(n)])


def insert_query_inner(bst, A, node: int, query):
    """
    marks the node with the query interval according to the canonical covering in Bentleys 1980
    bst: list of nodes, bst[0] is the root
    A: auxiliary table of length equal to number of queries, it stores the index of of the query interval in the list of intervals and the index of the node in the bst
    node: [x_min, x_max, left_child, right_child, A_intervals, B_intervals]
    query: (x_min, x_max, idx)
    set_idx: 0 or 1 for set A or B
    """
    if query[0] <= bst[node][0] and query[1] >= bst[node][1]:
        bst[node][4].append(query[2])
        A[query[2]][node] = len(bst[node][4]) - 1
        return
    
    left_child = bst[node][2]
    right_child = bst[node][3]

    if left_child is not None and query[0] <= bst[left_child][1] and query[1] >= bst[left_child][0]:
        insert_query_inner(bst, A, left_child, query)
    if right_child is not None and query[0] <= bst[right_child][1] and query[1] >= bst[right_child][0]:
        insert_query_inner(bst, A, right_child, query)


def insert_query(bst, A, query):
    """
    inserts a query into the bst
    bst: list of nodes, bst[0] is the root
    A: auxiliary table of length equal to number of queries, it stores the index of of the query interval in the list of intervals and the index of the node in the bst
    query: (x_min, x_max, idx)
    set_idx: 0 or 1 for set A or B
    """
    insert_query_inner(bst, A, 0, query)


def query_point_inner(bst, node, x):
    """
    returns all intervals containing a point
    bst: list of nodes, bst[0] is the root
    node: [x_min, x_max, left_child, right_child, intervals]
    x: point query
    set_idx: 0 or 1 for set A or B
    """
    res = []
    if x >= bst[node][0] and x <= bst[node][1]:
        res.extend(bst[node][4])
    left_child = bst[node][2]
    right_child = bst[node][3]

    if left_child is not None and x <= bst[left_child][1]:
        res.extend(query_point_inner(bst, left_child, x))
    elif right_child is not None and x <= bst[right_child][1]:
        res.extend(query_point_inner(bst, right_child, x))
    return res


def query_point(bst, x):
    return query_point_inner(bst, 0, x)


def delete_query(bst, A, query):
    """
    deletes a query from the bst
    bst: list of nodes, bst[0] is the root
    A: auxiliary table of length equal to number of queries, it stores the index of of the query interval in the list of intervals and the index of the node in the bst
    query: (x_min, x_max, idx)
    set_idx: 0 or 1 for set A or B
    """
    if query[2] >= len(A) or not A[query[2]]:
        return

    for node in list(A[query[2]].keys()):
        node_array = bst[node][4]
        query_idx = A[query[2]][node]
        last_idx = len(node_array) - 1
        if query_idx != last_idx:
            last = node_array[last_idx]
            A[last][node] = query_idx
            node_array[query_idx] = last
        node_array.pop()
        del A[query[2]][node]

    A[query[2]] = Dict.empty(key_type=types.int64, value_type=types.int64)



def centroid(rectangle):
    return (rectangle[0] + rectangle[2]) / 2, (rectangle[1] + rectangle[3]) / 2


def rectangles_enclosure_two_sets(set_A, set_B):
    """
    returns all pairs of intersecting rectangles between sets A and B (indexes 0 and 1 respectively)
    set_A: list of tuples (x_min, y_min, x_max, y_max)
    set_B: list of tuples (x_min, y_min, x_max, y_max)
    """
    if set_A == [] or set_B == []:
        return [], []
    x_axes_A = []
    x_axes_B = []
    y_axes = []
    
    for i, rect in enumerate(set_A):
        y_centroid = (rect[1] + rect[3]) / 2
        x_axes_A.append((rect[0], 0, i, 0))
        x_axes_A.append((rect[2], 0, i, 2))
        y_axes.append((rect[1], 0, i, 0))
        y_axes.append((rect[3], 0, i, 2))
        y_axes.append((y_centroid, 0, i, 1))
    
    for i, rect in enumerate(set_B):
        y_centroid = (rect[1] + rect[3]) / 2
        x_axes_B.append((rect[0], 1, i, 0))
        x_axes_B.append((rect[2], 1, i, 2))
        y_axes.append((rect[1], 1, i, 0))
        y_axes.append((rect[3], 1, i, 2))
        y_axes.append((y_centroid, 1, i, 1))
    
    # x_axes and y_axes are of the form (value, set_idx, idx, type)
    sorted_x_A = sorted(x_axes_A, key=lambda x: x[0])
    sorted_x_B = sorted(x_axes_B, key=lambda x: x[0])
    sorted_y = sorted(y_axes, key=lambda x: x[0])
    
    A = create_auxiliary_table(len(set_A))
    B = create_auxiliary_table(len(set_B))

    x_intervals_A = [x[0] for x in sorted_x_A]
    x_intervals_B = [x[0] for x in sorted_x_B]
    bst_A = create_interval_bst(x_intervals_A)
    bst_B = create_interval_bst(x_intervals_B)
    
    set_A_enclosers = [[] for _ in range(len(set_A))]
    set_B_enclosers = [[] for _ in range(len(set_B))]
    
    for rect in sorted_y:
        set_idx = rect[1]
        idx = rect[2]
        type = rect[3]
        if set_idx == 0:
            if type == 0:
                insert_query(bst_A, A, (set_A[idx][0], set_A[idx][2], idx))
            elif type == 2:
                delete_query(bst_A, A, (set_A[idx][0], set_A[idx][2], idx))
            else:
                x = set_A[idx][0] / 2 + set_A[idx][2] / 2
                enclosure = query_point(bst_B, x)
                for enc in enclosure:
                    set_A_enclosers[idx].append(enc)
                    set_B_enclosers[enc].append(idx)    
        else:
            if type == 0:
                insert_query(bst_B, B, (set_B[idx][0], set_B[idx][2], idx))
            elif type == 2:
                delete_query(bst_B, B, (set_B[idx][0], set_B[idx][2], idx))
            else:
                x = set_B[idx][0] / 2 + set_B[idx][2] / 2
                enclosure = query_point(bst_A, x)
                for enc in enclosure:
                    set_B_enclosers[idx].append(enc)
                    set_A_enclosers[enc].append(idx)
    return set_A_enclosers, set_B_enclosers

