from __future__ import division
from math import exp
from random import getrandbits
import numpy as np


def tuple_add(*tuples):
    return tuple(map(sum, zip(*tuples)))


class TorusWorld:
    def __init__(self, dimensions, grid):
        self.w, self.h = dimensions
        self.grid = grid

    def get_tile(self, x, y):
        return self.grid[y][x]

    def set_tile(self, x, y, value):
        self.grid[y][x] = value

    def absolute_coordinates(self, x, y):
        return x % self.w, y % self.h

    def get_count_of_value(self, value):
        return sum(sum(cell == value for cell in row) for row in self.grid)

    def get_coordinates_of_value(self, value):
        return list((x, y) for x in xrange(self.w) for y in xrange(self.w) if self.get_tile(x, y) == value)
