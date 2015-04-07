from __future__ import print_function, division
from random import random as r, randint, choice


NORTH = 'N'
WEST = 'W'
SOUTH = 'S'
EAST = 'E'
AGENT_DIRECTIONS = (NORTH, WEST, SOUTH, EAST)

FOOD = 'F'
POISON = 'P'
EMPTY = ' '


def gen_flatland(w, h, f, p):
    gen_tile = lambda: FOOD if r() < f else POISON if r() < p else EMPTY

    grid = [[gen_tile() for _ in xrange(w)] for _ in xrange(h)]

    while True:
        x, y = randint(0, w - 1), randint(0, h - 1)
        if grid[y][x] == EMPTY:
            grid[y][x] = choice(AGENT_DIRECTIONS)
            break

    return grid