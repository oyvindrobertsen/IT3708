from __future__ import print_function, division
from copy import deepcopy
from random import random as r, choice

import matplotlib.pyplot as plt

from utils import tuple_add, TorusWorld
from enums import *


NONE_STEP = -2
POISON_STEP = -10
FOOD_STEP = 20
FINISH_STEP = 50


def calculate_reward(current, tile):
    """
    Given a flatland instance and a tile content returns the score associated with moving onto the tile
    """
    reward = NONE_STEP

    if current.done:
        reward = FINISH_STEP
    elif tile > 0:
        reward = FOOD_STEP
    elif tile == -1:
        reward = POISON_STEP
    return reward


class Flatland(TorusWorld):
    def __init__(self, dimensions, x, y, n_food, grid):
        TorusWorld.__init__(self, dimensions, grid)

        self.agent_x, self.agent_y = self.agent_start_x, self.agent_start_y = x, y

        self.n_food = n_food
        self.food_eaten = 0
        self.poison_eaten = 0

    @property
    def agent_position(self):
        return self.agent_x, self.agent_y

    @property
    def up_coordinate(self):
        return self.absolute_coordinates(*tuple_add(self.agent_position, DELTAS[NORTH]))

    @property
    def left_coordinate(self):
        return self.absolute_coordinates(*tuple_add(self.agent_position, DELTAS[WEST]))

    @property
    def right_coordinate(self):
        return self.absolute_coordinates(*tuple_add(self.agent_position, DELTAS[EAST]))

    @property
    def down_coordinate(self):
        return self.absolute_coordinates(*tuple_add(self.agent_position, DELTAS[SOUTH]))

    def perform_action(self, action):
        assert action in ACTIONS

        if action == LEFT:
            self.agent_x, self.agent_y = self.left_coordinate
        if action == UP:
            self.agent_x, self.agent_y = self.up_coordinate
        elif action == RIGHT:
            self.agent_x, self.agent_y = self.right_coordinate
        elif action == DOWN:
            self.agent_x, self.agent_y = self.down_coordinate

        tile_contents = self.get_tile(self.agent_x, self.agent_y)

        if tile_contents > 0:
            self.food_eaten += 1
        elif tile_contents == -1:
            self.poison_eaten += 1

        self.set_tile(self.agent_x, self.agent_y, 0)
        return tile_contents

    @property
    def done(self):
        return self.food_eaten == self.n_food and \
               self.agent_position == (self.agent_start_x, self.agent_start_y)

    @property
    def score(self):
        food_score = self.food_eaten / ((self.food_eaten + self.get_count_of_value(FOOD)) or 1)
        poison_score = self.poison_eaten / ((self.poison_eaten + self.get_count_of_value(POISON)) or 1)
        return food_score - poison_score


class State(object):
    def __init__(self, agent_position=(0, 0)):
        self.foods_eaten = ()  # Sorted tuple of eaten foods
        self.position = agent_position

    def __hash__(self):
        return hash((self.foods_eaten, self.position))

    def __eq__(self, other):
        return self.foods_eaten == other.foods_eaten and self.position == other.position

    def __repr__(self):
        return "({} : {})".format(self.foods_eaten, self.position)


class FlatlandQLearn(object):
    def __init__(self, k, scenario, learning_rate, discount_rate, temp):
        self.k = k
        self.scenario = scenario
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.temp = temp
        self.ts = []
        self.q = {}  # Q :: State, action -> value

    def update_q(self, start_state, end_state, action, reward):

        # max_aQ(s_{t+1}, a)
        end_values = self.q.get(end_state, {})
        best_end_value = max(end_values.values()) if end_values else 0

        # Q(at,st)
        start_values = self.q.get(start_state, {})
        old_value = start_values[action] if action in start_values.keys() else 0

        new_value = old_value + self.learning_rate * \
                                (reward + (self.discount_rate * best_end_value) - old_value)
        start_values[action] = new_value
        self.q[start_state] = start_values

    def choose_action(self, current_state):
        ret = choice((LEFT, UP, RIGHT, DOWN))

        if r() > self.temp:
            # Attempt to exploit knowledge
            values = self.q.get(current_state, {})
            ret = max(values.iterkeys(), key=(lambda key: values[key])) if values else ret
        return ret

    def learn(self):
        for i in range(self.k):
            print(i)
            t = 0
            game = deepcopy(self.scenario)
            current_state = State(game.agent_position)
            action_history = []
            state_history = []
            while not game.done and not t > 5000:
                # Select action to perform
                action = self.choose_action(current_state)
                action_history.append(action)

                # Have the agent perform the action
                tile = game.perform_action(action)

                # Calculate reward based on the result of the action
                reward = calculate_reward(game, tile)

                # Update state
                state_history.append(current_state)
                current_state = deepcopy(current_state)
                current_state.position = game.agent_position

                if reward == FOOD_STEP:
                    current_state.foods_eaten = tuple(sorted(current_state.foods_eaten + (tile,)))

                # Update Q
                self.update_q(state_history[-1], current_state, action, reward)

                t += 1
            self.ts.append(t)
            self.temp = max(self.temp - 1/self.k, 0)
        return action_history, state_history

    def plot_steps(self):
        plt.title("Steps")
        plt.plot(self.ts)
        plt.show()