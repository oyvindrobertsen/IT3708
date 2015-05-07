from __future__ import print_function, division, unicode_literals
import pygame
from time import sleep

from enums import *

from flatland import State

CELL_SIZE = 50
LINE_WIDTH = 2
BACKGROUND = (255, 255, 255)
FOREGROUND = (0, 0, 0)

FOOD_COLOR = (0, 125, 0)
POISON_COLOR = (125, 0, 0)

SLEEP_TIME_DEFAULT = 1.0
SLEEP_TIME_DELTA = 0.25

TITLE = 'Reinforcement learning in flatland'


class FlatlandGUI:
    def __init__(self, flatland, actions, states, q):
        """
        takes a fresh board and a list of actions and visualizes
        """
        self.flatland = flatland
        self.q = q
        states = states + states[-1:]
        self.window_w, self.window_h = flatland.w * CELL_SIZE, flatland.h * CELL_SIZE

        pygame.init()
        sleep_time = SLEEP_TIME_DEFAULT

        self.paused = True
        self.window = pygame.display.set_mode((self.window_w, self.window_h))

        self.pause()

        state_i = 0

        for action in actions + [NOOP]:
            self.draw_state(states[state_i].foods_eaten)
            state_i += 1

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

    def draw_state(self, foods_eaten):
        self.window.fill(BACKGROUND)

        for x in xrange(self.flatland.w):
            x1 = x * CELL_SIZE - 1
            pygame.draw.line(self.window, FOREGROUND, (x1, 0), (x1, self.window_h), LINE_WIDTH)

        for y in xrange(self.flatland.h):
            y1 = y * CELL_SIZE - 1
            pygame.draw.line(self.window, FOREGROUND, (0, y1), (self.window_w, y1), LINE_WIDTH)

        temp_state = State()
        temp_state.foods_eaten = foods_eaten
        for y, row in enumerate(self.flatland.grid):
            for x, cell in enumerate(row):
                # Draw start cell
                if (x, y) == (self.flatland.agent_start_x, self.flatland.agent_start_y):
                    self.fill_cell(x, y, (14, 144, 210))
                if (x, y) == self.flatland.agent_position:
                    self.draw_circle_in_cell(x, y, (0, 0, 125), radius=CELL_SIZE // 4)
                elif cell > 0:
                    self.draw_circle_in_cell(x, y, FOOD_COLOR)
                elif cell == -1:
                    self.draw_circle_in_cell(x, y, POISON_COLOR)
                else:
                    # Draw knowledge
                    temp_state.position = (x, y)
                    cur_pos_values = self.q.get(temp_state, {})
                    best_action = max(cur_pos_values.iterkeys(), key=lambda key: cur_pos_values[key]) \
                        if cur_pos_values else NOOP
                    if not best_action == NOOP:
                        self.draw_arrow_in_cell(x, y, (0, 0, 125), best_action)

        pygame.display.flip()

    def draw_circle_in_cell(self, cell_x, cell_y, color, radius=CELL_SIZE // 8):
        offset = CELL_SIZE // 2
        coord = cell_x * CELL_SIZE + offset, cell_y * CELL_SIZE + offset
        pygame.draw.circle(self.window, color, coord, radius)

    def draw_arrow_in_cell(self, cell_x, cell_y, color, direction):
        if direction == UP:
            top = ((cell_x * CELL_SIZE) + (CELL_SIZE // 2), (cell_y * CELL_SIZE) + (LINE_WIDTH * 10))
            b_left = ((cell_x * CELL_SIZE) + (LINE_WIDTH * 10), ((cell_y + 1) * CELL_SIZE) - (LINE_WIDTH * 10))
            b_right = (((cell_x + 1) * CELL_SIZE) - (LINE_WIDTH * 10), ((cell_y + 1) * CELL_SIZE) - (LINE_WIDTH * 10))
        elif direction == RIGHT:
            top = (((cell_x + 1) * CELL_SIZE) - (LINE_WIDTH * 10), (cell_y * CELL_SIZE) + (CELL_SIZE // 2))
            b_left = ((cell_x * CELL_SIZE) + (LINE_WIDTH * 10), (cell_y * CELL_SIZE) + (LINE_WIDTH * 10))
            b_right = ((cell_x * CELL_SIZE) + (LINE_WIDTH * 10), ((cell_y+1) * CELL_SIZE) - (LINE_WIDTH * 10))
        elif direction == LEFT:
            top = ((cell_x * CELL_SIZE) + (LINE_WIDTH * 10), (cell_y * CELL_SIZE) + (CELL_SIZE // 2))
            b_left = (((cell_x + 1) * CELL_SIZE) - (LINE_WIDTH * 10), ((cell_y + 1) * CELL_SIZE) - (LINE_WIDTH * 10))
            b_right = (((cell_x + 1) * CELL_SIZE) - (LINE_WIDTH * 10), (cell_y * CELL_SIZE) + (LINE_WIDTH * 10))
        elif direction == DOWN:
            top = ((cell_x * CELL_SIZE) + (CELL_SIZE // 2), ((cell_y + 1) * CELL_SIZE) - (LINE_WIDTH * 10))
            b_left = (((cell_x + 1) * CELL_SIZE) - (LINE_WIDTH * 10), (cell_y * CELL_SIZE) + (LINE_WIDTH * 10))
            b_right = ((cell_x * CELL_SIZE) + (LINE_WIDTH * 10), (cell_y * CELL_SIZE) + (LINE_WIDTH * 10))
        else:
            top = (0, 0)
            b_left = (0, 0)
            b_right = (0, 0)


        pygame.draw.polygon(self.window, color, [top, b_left, b_right])

    def fill_cell(self, cell_x, cell_y, color):
        area = (cell_x * CELL_SIZE) + LINE_WIDTH - 1, (cell_y * CELL_SIZE) + LINE_WIDTH - 1, CELL_SIZE - LINE_WIDTH, CELL_SIZE - LINE_WIDTH
        pygame.draw.rect(self.window, color, area)

    def pause(self):
        self.paused = True
        pygame.display.set_caption("{} - {}".format(TITLE, 'Paused'))

    def unpause(self):
        self.paused = False
        pygame.display.set_caption(TITLE)
