from __future__ import division
from math import exp
from random import getrandbits


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
