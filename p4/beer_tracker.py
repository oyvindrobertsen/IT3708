from __future__ import division, print_function
from random import randint

from enums import *


TRACKER_WIDTH = 5


class BeerTrackerAgent:
    def __init__(self, world):
        self.world = world
        self.leftmost = (self.world.width // 2) - (TRACKER_WIDTH // 2)

    @property
    def rightmost(self):
        return (self.leftmost + TRACKER_WIDTH - 1) % self.world.width

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
        return [col_no in self.world.active_object.columns for col_no in self.columns]

    def interact(self, obj):
        if obj.y_position > 0:
            return

        object_cols = set(obj.columns)
        agent_cols = set(self.columns)

        if object_cols.issubset(agent_cols):
            self.capture(obj)
            return CAPTURE
        elif object_cols.intersection(agent_cols):
            self.fail(obj)
            return FAIL
        else:
            self.avoidance(obj)
            return AVOIDANCE

    def capture(self, obj):
        print('CAPTURE', obj.width)

    def avoidance(self, obj):
        print('AVOIDANCE', obj.width)

    def fail(self, obj):
        print('FAIL', obj.width)


class BeerTrackerObject:
    def __init__(self, left, y_position, width):
        self.leftmost = left
        self.y_position = y_position
        self.width = width

    @property
    def rightmost(self):
        return self.leftmost + self.width - 1

    @property
    def columns(self):
        return range(self.leftmost, self.rightmost + 1)


class BeerTrackerWorld:
    def __init__(self, width, height, wrap=True):
        self.width = width
        self.height = height
        self.wrap = wrap

        self.agent = BeerTrackerAgent(world=self)
        self.active_object = None

    def new_falling_object(self):
        width = randint(1, 6)
        left = randint(0, self.width - width)
        self.active_object = BeerTrackerObject(left, self.height, width)

    def tick(self):
        if self.active_object.y_position == 0:
            self.agent.interact(self.active_object)
            self.new_falling_object()
            return

        self.active_object.y_position -= 1

    def perform_action(self, action_tuple):
        action, param = action_tuple

        if action in DIRECTIONS:
            self.agent.move(action, param)
        elif action == PULL:
            self.pull()

    def pull(self):
        self.active_object.y_position = 0

    def terminal_print(self):
        for y in xrange(self.height, 0, -1):
            print('|', end='')
            for j in xrange(self.width):
                c = ' '
                if j in self.active_object.columns:
                    if y == self.active_object.y_position:
                        c = 'V'
                    elif y < self.active_object.y_position:
                        c = ':'
                print(c, sep='', end='')
            print('| {:>2}'.format(y))

        print(' ', end='')
        for y in xrange(self.width):
            print('^' if y in self.agent.columns else ' ', sep='', end='')
        print('   0')
