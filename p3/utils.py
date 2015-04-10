from __future__ import division
from math import exp
from random import getrandbits
import numpy as np


def tuple_add(*tuples):
    return tuple(map(sum, zip(*tuples)))


def sigmoid(x):
    # return tanh(x)
    return 1 / (1 + exp(-x))


def step(x, threshold=0.5):
    if x > threshold:
        return 1
    else:
        return 0


def random_bitstring(n):
    return ''.join(str(getrandbits(1)) for _ in xrange(n))


def normalize_bitstring(bitstring):
    return int(bitstring, base=2) / (2 ** len(bitstring) - 1)


def matrix_fit(array_data, matrix_dimensions):
    """
    fills the matrices with data from the 1D array
    """
    matrices = [np.zeros(md) for md in matrix_dimensions]
    for matrix in matrices:
        for i, row in enumerate(matrix):
            for j, col in enumerate(row):
                matrix[i][j] = array_data.pop()

    return matrices


class TorusWorld:
    def __init__(self, dimensions):
        self.w, self.h = dimensions
        self.grid = [[self.generate_tile() for _ in xrange(self.w)] for _ in xrange(self.h)]

    def generate_tile(self):
        raise NotImplementedError()

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
