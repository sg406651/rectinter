import pytest
from random import seed
from rectinter.rectangles_intersection_one_set import rectinter_one_set
from rectinter import slow_rectangles_intersection_one_set
from rectinter import random_rectangles


def test_enclosures():
    rectangles = [(0, 0, 10, 10), 
                  (1, 1, 9, 9),
                  (2, 2, 8, 8),
                  (3, 3, 7, 7),
                  (4, 4, 6, 6)]
    enclosures = rectinter_one_set(rectangles)
    correct_enclosures = [[1, 2, 3, 4], [0, 2, 3, 4], [0, 1, 3, 4], [0, 1, 2, 4], [0, 1, 2, 3]]
    assert enclosures == correct_enclosures

 
def test_intersections():
    rectangles = [(2, 2, 7, 7),
                  (0, 0, 3, 3),
                  (0, 6, 3, 9),
                  (6, 0, 9, 3),
                  (6, 6, 9, 9)]
    intersections = rectinter_one_set(rectangles)
    correct_intersections = [[1, 2, 3, 4], [0], [0], [0], [0]]
    assert intersections == correct_intersections


def test_empty():
    rectangles = []
    intersections = rectinter_one_set(rectangles)
    slow_intersections = slow_rectangles_intersection_one_set(rectangles)
    assert intersections == slow_intersections


def test_y_axis_aligned():
    rectangles = [(0, 10, 0, 10),
                  (10, 4, 14, 6)]
    intersections = rectinter_one_set(rectangles)
    slow_intersections = slow_rectangles_intersection_one_set(rectangles)
    assert intersections == slow_intersections

seed(0)
def test_random():
    rectangles = random_rectangles(100, 0, 0, 100, 100)
    intersections = rectinter_one_set(rectangles)
    slow_intersections = slow_rectangles_intersection_one_set(rectangles)
    assert intersections == slow_intersections

