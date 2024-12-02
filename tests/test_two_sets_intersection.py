import pytest
from random import seed
from rectinter import rectinter_two_sets
from rectinter import slow_rectangles_intersection_two_sets
from rectinter import random_rectangles


def test_enclosures_sym():
    set_A = [(0, 0, 10, 10), 
              (1, 1, 9, 9),
              (2, 2, 8, 8),
              (3, 3, 7, 7),
              (4, 4, 6, 6)]
    set_B = [(0, 0, 10, 10), 
              (1, 1, 9, 9),
              (2, 2, 8, 8),
              (3, 3, 7, 7),
              (4, 4, 6, 6)]
    enclosures = rectinter_two_sets(set_A, set_B)
    slow_enclosures = slow_rectangles_intersection_two_sets(set_A, set_B)
    assert enclosures == slow_enclosures


def test_intersections_sym():
    set_A = [(2, 2, 7, 7),
              (0, 0, 3, 3),
              (0, 6, 3, 9),
              (6, 0, 9, 3),
              (6, 6, 9, 9)]
    set_B = [(2, 2, 7, 7),
              (0, 0, 3, 3),
              (0, 6, 3, 9),
              (6, 0, 9, 3),
              (6, 6, 9, 9)]
    intersections = rectinter_two_sets(set_A, set_B)
    slow_intersections = slow_rectangles_intersection_two_sets(set_A, set_B)
    assert intersections == slow_intersections


def test_empty_first():
    set_A = []
    set_B = [(2, 2, 7, 7),
              (0, 0, 3, 3),
              (0, 6, 3, 9),
              (6, 0, 9, 3),
              (6, 6, 9, 9)]
    intersections = rectinter_two_sets(set_A, set_B)
    slow_intersections = slow_rectangles_intersection_two_sets(set_A, set_B)
    assert intersections == slow_intersections


def test_empty_second():
    set_A = [(2, 2, 7, 7),
              (0, 0, 3, 3),
              (0, 6, 3, 9),
              (6, 0, 9, 3),
              (6, 6, 9, 9)]
    set_B = []
    intersections = rectinter_two_sets(set_A, set_B)
    slow_intersections = slow_rectangles_intersection_two_sets(set_A, set_B)
    assert intersections == slow_intersections


def test_empty_both():
    set_A = []
    set_B = []
    intersections = rectinter_two_sets(set_A, set_B)
    slow_intersections = slow_rectangles_intersection_two_sets(set_A, set_B)
    assert intersections == slow_intersections


def test_y_axis_aligned():
    set_A = [(0, 10, 0, 10),
              (10, 4, 14, 6)]
    set_B = [(0, 10, 0, 10),
              (10, 4, 14, 6)]
    intersections = rectinter_two_sets(set_A, set_B)
    slow_intersections = slow_rectangles_intersection_two_sets(set_A, set_B)
    assert intersections == slow_intersections

seed(1)
def test_random():
    set_A = random_rectangles(100, 0, 0, 100, 100)
    set_B = random_rectangles(100, 0, 0, 100, 100)
    intersections_A, intersections_B = rectinter_two_sets(set_A, set_B)
    slow_intersections_A, slow_intersections_B = slow_rectangles_intersection_two_sets(set_A, set_B)
    assert intersections_A == slow_intersections_A
    assert intersections_B == slow_intersections_B