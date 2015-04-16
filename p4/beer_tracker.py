from __future__ import division, print_function
from random import randint
import numpy as np

DIRECTIONS = LEFT, RIGHT = -1, 1

TRACKER_WIDTH = 5

EMPTY = ' '
OBJECT = 'O'


class BeerTrackerAgent:
    def __init__(self, world):
        self.world = world
        self.leftmost = (self.world.width // 2) - (TRACKER_WIDTH // 2)

    @property
    def rightmost(self):
        return (self.leftmost + TRACKER_WIDTH) % self.world.width

    @property
    def columns(self):
        if self.rightmost < self.leftmost:
            return range(self.leftmost, self.world.width) + range(0, self.rightmost)

        return range(self.leftmost, self.rightmost + 1)

    def move(self, direction, steps):
        self.leftmost += direction * steps

        if self.world.wrap:
            self.leftmost %= self.world.width
        else:
            if self.leftmost < 0:
                self.leftmost = 0
            elif self.rightmost >= self.world.width:
                self.leftmost -= (self.rightmost - self.world.width)

    def get_sensor_readings(self):
        return [OBJECT in self.world.get_column(i) for i in self.columns]

    def capture(self, size):
        print('CAPTURE')

    def avoidance(self, size):
        print('AVOIDANCE')

    def fail(self, size):
        print('FAIL')


class BeerTrackerWorld:
    def __init__(self, width, height, wrap=True):
        self.width = width
        self.height = height
        self.wrap = wrap

        self.grid = np.array([[EMPTY for _ in xrange(self.width)] for _ in xrange(self.height)])
        self.agent = BeerTrackerAgent(world=self)

    def get_column(self, i):
        return self.grid[:, i]

    def add_falling_object(self):
        object_width = randint(1, 6)
        left = randint(0, self.width - object_width)
        self.grid[0][left:left + object_width].fill(OBJECT)

    def tick(self):
        if OBJECT in self.grid[-1]:
            size = list(self.grid[-1]).count(OBJECT)
            l = list(self.grid[-1]).index(OBJECT)
            r = l + size

            object_cols = set(range(l, r))
            agent_cols = set(self.agent.columns)
            if object_cols.issubset(agent_cols):
                self.agent.capture(size)
            elif object_cols.intersection(agent_cols):
                self.agent.fail(size)
            else:
                self.agent.avoidance(size)

            self.grid[-1].fill(EMPTY)
            self.add_falling_object()
            return

        for i, row in enumerate(self.grid):
            if OBJECT in row:
                self.grid[i + 1] = self.grid[i]
                self.grid[i].fill(EMPTY)
                return

    def pull(self):
        for i, row in enumerate(self.grid):
            if OBJECT in row:
                self.grid[-1] = self.grid[i]
                self.grid[i].fill(EMPTY)
                return

    def terminal_print(self):
        for row in self.grid:
            print('|', end='')
            print(*row, sep='', end='')
            print('|')
        print(' ', end='')
        for i in xrange(self.width):
            print('^' if i in self.agent.columns else ' ', sep='', end='')
        print(' ')


if __name__ == "__main__":
    btw = BeerTrackerWorld(30, 15, wrap=True)
    btw.add_falling_object()
    btw.terminal_print()
    btw.agent.move(LEFT, 4)
    btw.tick()
    btw.agent.move(LEFT, 4)
    btw.tick()
    btw.agent.move(LEFT, 4)
    btw.tick()
    btw.agent.move(LEFT, 4)
    btw.tick()
    btw.pull()
    btw.terminal_print()
    btw.tick()
    print(btw.agent.get_sensor_readings())
