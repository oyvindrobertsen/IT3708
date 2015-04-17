from __future__ import print_function, division, unicode_literals
import pygame
from time import sleep

from beer_tracker import TRACKER_WIDTH
from enums import *


CELL_SIZE = 50
BACKGROUND = (255, 255, 255)
FOREGROUND = (0, 0, 0)

OBJECT_COLOR = (0, 125, 0)
AGENT_COLOR = (125, 0, 0)
PULLING_COLOR = (0, 255, 0)

SLEEP_TIME_DEFAULT = 1.0
SLEEP_TIME_DELTA = 0.25

TITLE = 'Evolved neural network for solving the Beer Tracker problem'


class BeerTrackerGUI:
    def __init__(self, world, actions):
        self.world = world
        self.window_w, self.window_h = world.width * CELL_SIZE, (world.height + 1) * CELL_SIZE

        pygame.init()
        sleep_time = SLEEP_TIME_DEFAULT

        self.paused = False
        self.window = pygame.display.set_mode((self.window_w, self.window_h))

        self.last_action = None
        self.next_action = actions[0][0]

        while True:
            self.draw_state()

            if not self.paused and actions:
                action, param = actions.pop(0)
                self.world.perform_action((action, param))
                self.last_action = action
                try:
                    self.next_action = actions[0][0]
                except IndexError:
                    self.next_action = None
                self.world.tick()
                print('.')

            sleep(sleep_time)

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

    def draw_state(self):
        self.window.fill(BACKGROUND)

        pygame.draw.rect(self.window, OBJECT_COLOR, pygame.Rect(
            self.world.active_object.leftmost * CELL_SIZE,
            (self.world.height - self.world.active_object.y_position) * CELL_SIZE,
            self.world.active_object.width * CELL_SIZE,
            CELL_SIZE
        ))

        agent_color = PULLING_COLOR if PULL in (self.last_action, self.next_action) else AGENT_COLOR

        pygame.draw.rect(self.window, agent_color, pygame.Rect(
            self.world.agent.leftmost * CELL_SIZE,
            self.world.height * CELL_SIZE,
            TRACKER_WIDTH * CELL_SIZE,
            CELL_SIZE
        ))

        pygame.display.flip()

    def pause(self):
        self.paused = True
        pygame.display.set_caption("{} - {}".format(TITLE, 'Paused'))

    def unpause(self):
        self.paused = False
        pygame.display.set_caption(TITLE)
