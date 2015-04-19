from __future__ import print_function, division, unicode_literals
import pygame
from time import sleep

from enums import *


CELL_SIZE = 50
BACKGROUND = (255, 255, 255)
FOREGROUND = (0, 0, 0)

SAFE_COLOR = (0, 125, 0)
DANGER_COLOR = (255, 0, 0)
AGENT_COLOR = (125, 0, 255)
PULLING_COLOR = (0, 255, 0)

SLEEP_TIME_DEFAULT = 0.5
SLEEP_TIME_DELTA = 0.1

TITLE = 'Evolved neural network for solving the Beer Tracker problem'


class BeerTrackerGUI:
    def __init__(self, world, agent):
        self.world = world
        self.agent = agent
        self.window_w, self.window_h = world.width * CELL_SIZE, (world.height + 1) * CELL_SIZE

        pygame.init()
        self.sleep_time = SLEEP_TIME_DEFAULT

        self.paused = False
        self.pause()

        self.window = pygame.display.set_mode((self.window_w, self.window_h))
        self.font = pygame.font.SysFont("sans-serif", 30)

        def simulation_gui(**kwargs):
            self.draw_state(**kwargs)
            sleep(self.sleep_time)

            while self.paused:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.unpause()
                        elif event.key == pygame.QUIT or event.key == pygame.K_q:
                            return

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.QUIT or event.key == pygame.K_q:
                        return
                    elif event.key == pygame.K_SPACE:
                        self.pause()
                    elif event.key == pygame.K_PLUS:
                        # go faster
                        sleep_time = max(self.sleep_time - SLEEP_TIME_DELTA, SLEEP_TIME_DELTA)
                    elif event.key == pygame.K_MINUS:
                        # go slower
                        self.sleep_time += SLEEP_TIME_DELTA

        world.simulate(self.agent, after_tick=simulation_gui)

    def draw_state(self, **kwargs):
        self.window.fill(BACKGROUND)

        self.window.blit(
            self.font.render('Time: {}'.format(kwargs.get('tick')), True, (0, 0, 0)),
            (10, 10)
        )
        self.window.blit(
            self.font.render('Points: {}'.format(self.world.agent.points), True, (0, 0, 0)),
            (10, 50)
        )

        pygame.draw.rect(
            self.window,
            SAFE_COLOR if self.world.active_object.width <= 4 else DANGER_COLOR,
            pygame.Rect(
                self.world.active_object.leftmost * CELL_SIZE,
                (self.world.height - self.world.active_object.y_position) * CELL_SIZE,
                self.world.active_object.width * CELL_SIZE,
                CELL_SIZE
            ))

        agent_color = PULLING_COLOR if self.agent.actions[-1] == PULL else AGENT_COLOR
        pygame.draw.rect(
            self.window,
            agent_color,
            pygame.Rect(
                self.world.agent.leftmost * CELL_SIZE,
                self.world.height * CELL_SIZE,
                TRACKER_WIDTH * CELL_SIZE,
                CELL_SIZE
            ))

        if self.world.agent.rightmost < self.world.agent.leftmost:
            pygame.draw.rect(
                self.window,
                agent_color,
                pygame.Rect(
                    0,
                    self.world.height * CELL_SIZE,
                    (self.world.agent.rightmost + 1) * CELL_SIZE,
                    CELL_SIZE
                ))

        pygame.display.flip()

    def pause(self):
        self.paused = True
        pygame.display.set_caption("{} - {}".format(TITLE, 'Paused'))

    def unpause(self):
        self.paused = False
        pygame.display.set_caption(TITLE)
