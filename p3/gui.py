from __future__ import print_function, division, unicode_literals
import pygame
from time import sleep

from enums import *
from utils import tuple_add


CELL_SIZE = 100
BACKGROUND = (255, 255, 255)
FOREGROUND = (0, 0, 0)

FOOD_COLOR = (0, 125, 0)
POISON_COLOR = (125, 0, 0)

SLEEP_TIME_DEFAULT = 1.0
SLEEP_TIME_DELTA = 0.25

TITLE = 'Evolved neural network for solving the Flatland problem'


class FlatlandGUI:
    def __init__(self, flatland, actions):
        """
        takes a fresh board and a list of actions and visualizes
        """
        self.flatland = flatland
        self.window_w, self.window_h = flatland.w * CELL_SIZE, flatland.h * CELL_SIZE

        pygame.init()
        sleep_time = SLEEP_TIME_DEFAULT

        self.paused = True
        self.window = pygame.display.set_mode((self.window_w, self.window_h))

        self.pause()

        for action in actions + [NOOP]:
            self.draw_state()

            while self.paused:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.unpause()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.QUIT:
                        return

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.pause()
                    elif event.key == pygame.K_PLUS:
                        # go faster
                        sleep_time = max(sleep_time - SLEEP_TIME_DELTA, SLEEP_TIME_DELTA)
                    elif event.key == pygame.K_MINUS:
                        # go slower
                        sleep_time += SLEEP_TIME_DELTA

            sleep(sleep_time)
            flatland.perform_action(action)

        pygame.display.set_caption("{} - {}".format(TITLE, 'Finished'))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

    def draw_state(self):
        self.window.fill(BACKGROUND)

        for x in xrange(self.flatland.w):
            x1 = x * CELL_SIZE - 1
            pygame.draw.line(self.window, FOREGROUND, (x1, 0), (x1, self.window_h), 2)

        for y in xrange(self.flatland.h):
            y1 = y * CELL_SIZE - 1
            pygame.draw.line(self.window, FOREGROUND, (0, y1), (self.window_w, y1), 2)

        for y, row in enumerate(self.flatland.grid):
            for x, cell in enumerate(row):
                if (x, y) == self.flatland.agent_position:
                    self.draw_circle_in_cell(x, y, (0, 0, 125), radius=CELL_SIZE // 4)
                    offset = CELL_SIZE // 2
                    coord = x * CELL_SIZE + offset, y * CELL_SIZE + offset
                    coord = tuple_add(coord, map(lambda x: 20 * x, DELTAS[self.flatland.agent_heading]))
                    pygame.draw.circle(self.window, (255, 255, 0), coord, CELL_SIZE // 10)
                elif cell == FOOD:
                    self.draw_circle_in_cell(x, y, FOOD_COLOR)
                elif cell == POISON:
                    self.draw_circle_in_cell(x, y, POISON_COLOR)

        pygame.display.flip()

    def draw_circle_in_cell(self, cell_x, cell_y, color, radius=CELL_SIZE // 8):
        offset = CELL_SIZE // 2
        coord = cell_x * CELL_SIZE + offset, cell_y * CELL_SIZE + offset
        pygame.draw.circle(self.window, color, coord, radius)

    def pause(self):
        self.paused = True
        pygame.display.set_caption("{} - {}".format(TITLE, 'Paused'))

    def unpause(self):
        self.paused = False
        pygame.display.set_caption(TITLE)
