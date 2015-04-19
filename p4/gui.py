from __future__ import print_function, division, unicode_literals
import pygame
from time import sleep

from enums import *


CELL_SIZE = 50
BACKGROUND = (255, 255, 255)
FOREGROUND = (0, 0, 0)

OBJECT_COLOR = (0, 125, 0)
AGENT_COLOR = (125, 0, 0)
PULLING_COLOR = (0, 255, 0)

SLEEP_TIME_DEFAULT = 0.5
SLEEP_TIME_DELTA = 0.1

TITLE = 'Evolved neural network for solving the Beer Tracker problem'


class BeerTrackerGUI:
    def __init__(self, world, agent):
        self.world = world
        self.window_w, self.window_h = world.width * CELL_SIZE, (world.height + 1) * CELL_SIZE

        pygame.init()
        self.sleep_time = SLEEP_TIME_DEFAULT

        self.paused = False
        self.window = pygame.display.set_mode((self.window_w, self.window_h))

        def simulation_gui(**kwargs):
            tick = kwargs.get('tick')
            print(tick, end='\n' if (tick + 1) % 50 == 0 else '\t')
            self.draw_state()
            sleep(self.sleep_time)

            while self.paused:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.unpause()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.pause()
                    elif event.key == pygame.K_PLUS:
                        # go faster
                        sleep_time = max(self.sleep_time - SLEEP_TIME_DELTA, SLEEP_TIME_DELTA)
                    elif event.key == pygame.K_MINUS:
                        # go slower
                        self.sleep_time += SLEEP_TIME_DELTA

        world.simulate(agent, after_tick=simulation_gui)
        print()

    def draw_state(self):
        self.window.fill(BACKGROUND)

        pygame.draw.rect(self.window, OBJECT_COLOR, pygame.Rect(
            self.world.active_object.leftmost * CELL_SIZE,
            (self.world.height - self.world.active_object.y_position) * CELL_SIZE,
            self.world.active_object.width * CELL_SIZE,
            CELL_SIZE
        ))

        pygame.draw.rect(self.window, AGENT_COLOR, pygame.Rect(
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
