import random


def random_rectangles(n, xmin=0, ymin=0, xmax=100, ymax=100):
    """
    Generate n random rectangles.
    """
    rectangles = []
    for _ in range(n):
        x_axis = random.sample(range(xmin, xmax), 2)
        x_axis = sorted(x_axis)
        x1 = x_axis[0]
        x2 = x_axis[1]
        y_axis = random.sample(range(ymin, ymax), 2)
        y_axis = sorted(y_axis)
        y1 = y_axis[0]
        y2 = y_axis[1]
        rectangles.append((x1, y1, x2, y2))
    return rectangles
