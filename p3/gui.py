from __future__ import print_function, division, unicode_literals
import pygame
import sys
from time import sleep

from flatland import FOOD, POISON


CELL_SIZE = 100
BACKGROUND = (255, 255, 255)
FOREGROUND = (0, 0, 0)

GREEN = (0, 125, 0)
RED = (125, 0, 0)


def flatland_gui(flatland):
    window_w, window_h = flatland.width * CELL_SIZE, flatland.height * CELL_SIZE

    pygame.init()

    window = pygame.display.set_mode((window_w, window_h))

    def circle_in_cell(cell_x, cell_y, color, radius=CELL_SIZE // 8):
        offset = CELL_SIZE // 2
        coord = cell_x * CELL_SIZE + offset, cell_y * CELL_SIZE + offset
        pygame.draw.circle(window, color, coord, radius)

    while True:
        window.fill(BACKGROUND)
        for x in xrange(flatland.width):
            x1 = x * CELL_SIZE - 1
            pygame.draw.line(window, FOREGROUND, (x1, 0), (x1, window_h), 2)

        for y in xrange(flatland.height):
            y1 = y * CELL_SIZE - 1
            pygame.draw.line(window, FOREGROUND, (0, y1), (window_w, y1), 2)

        for y, row in enumerate(flatland.grid):
            for x, cell in enumerate(row):
                if (x, y) == flatland.agent_position:
                    circle_in_cell(x, y, (0, 0, 125), radius=CELL_SIZE // 4)
                elif cell == FOOD:
                    circle_in_cell(x, y, GREEN)
                elif cell == POISON:
                    circle_in_cell(x, y, RED)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        sleep(0.5)
