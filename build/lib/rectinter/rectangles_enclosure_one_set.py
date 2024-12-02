from numba import typed, types
from numba.typed import Dict


def create_interval_bst(sorted_list):
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


def create_auxiliary_table(n):
    """
    creates auxiliary table to eficiently delete queries
    """
    return typed.List([Dict.empty(key_type=types.int64, value_type=types.int64) for _ in range(n)])


def insert_query_inner(bst, A, node: int, query):
    """
    marks the node with the query interval according to the canonical covering in Bentleys 1980
    bst: list of nodes, bst[0] is the root
    A: auxiliary table of length equal to number of queries, it stores the index of of the query interval in the list of intervals and the index of the node in the bst
    node: [x_min, x_max, left_child, right_child, intervals]
    query: (x_min, x_max, idx)
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
    """
    insert_query_inner(bst, A, 0, query)


def query_point_inner(bst, node, x):
    """
    returns all intervals containing a point
    bst: list of nodes, bst[0] is the root
    node: [x_min, x_max, left_child, right_child, intervals]
    x: point query
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


def rectangles_enclosure_one_set(rectangles):
    """
    rectangles: list of tuples (x_min, y_min, x_max, y_max)
    returns a list of enclosures for each rectangle
    """
    if rectangles == []:
        return []
    x_axes = []
    y_axes = []
    for i, rect in enumerate(rectangles):
        x_centroid, y_centroid = centroid(rect)
        x_axes.append((rect[0], i, 0))
        x_axes.append((rect[2], i, 2))
        y_axes.append((rect[1], i, 0))
        y_axes.append((rect[3], i, 2))
        y_axes.append((y_centroid, i, 1))
    
    sorted_x = sorted(x_axes, key=lambda x: x[0])
    sorted_y = sorted(y_axes, key=lambda x: x[0])
    
    A = create_auxiliary_table(len(rectangles))
    x_intervals = [x[0] for x in sorted_x]
    bst_x = create_interval_bst(x_intervals)
    
    all_enclosures = [[] for _ in range(len(rectangles))]
    for rect in sorted_y:
        idx = rect[1]
        if rect[2] == 0:
            insert_query(bst_x, A, (rectangles[idx][0], rectangles[idx][2], idx))
        elif rect[2] == 2:
            delete_query(bst_x, A, (rectangles[idx][0], rectangles[idx][2], idx))
        else:
            x = rectangles[idx][0] / 2 + rectangles[idx][2] / 2
            enclosure = query_point(bst_x, x)
            if idx in enclosure:
                enclosure.remove(idx)
            for enc in enclosure:
                all_enclosures[enc].append(idx)
                all_enclosures[idx].append(enc)
        for i, enc in enumerate(all_enclosures):
            enc_new = list(set(enc))
            all_enclosures[i] = enc_new
    return all_enclosures
