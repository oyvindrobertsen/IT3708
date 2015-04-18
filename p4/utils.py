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

    return matrices, array_data


def tuplize(value, times=2):
    return tuple(value for _ in xrange(times))