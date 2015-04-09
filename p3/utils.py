from math import exp
import numpy


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
