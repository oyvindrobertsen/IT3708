from __future__ import print_function, division
from copy import deepcopy
from random import random as r, choice

from ea.problems import Problem
from ea.ea import Individual
from ann.neural_network import NeuralNetwork
from gui import FlatlandGUI
from utils import tuple_add, random_bitstring, normalize_bitstring, matrix_fit, sigmoid, TorusWorld
from enums import *


class Flatland(TorusWorld):
    def __init__(self, dimensions, f, p, t, minimum_activation=0.0):
        self.f = f
        self.p = p
        self.t = t

        TorusWorld.__init__(self, dimensions)

        self.agent_x, self.agent_y = choice(self.get_coordinates_of_value(EMPTY))
        self.agent_heading = choice(AGENT_DIRECTIONS)

        self.minimum_activation = minimum_activation

        self.food_eaten = 0
        self.poison_eaten = 0

    def generate_tile(self):
        return FOOD if r() < self.f else POISON if r() < self.p else EMPTY

    @property
    def agent_position(self):
        return self.agent_x, self.agent_y

    @property
    def left_direction(self):
        return AGENT_DIRECTIONS[AGENT_DIRECTIONS.index(self.agent_heading) - 1]

    @property
    def right_direction(self):
        return AGENT_DIRECTIONS[(AGENT_DIRECTIONS.index(self.agent_heading) + 1) % len(AGENT_DIRECTIONS)]

    @property
    def forward_coordinate(self):
        return self.absolute_coordinates(*tuple_add(self.agent_position, DELTAS[self.agent_heading]))

    @property
    def left_coordinate(self):
        return self.absolute_coordinates(*tuple_add(self.agent_position, DELTAS[self.right_direction]))

    @property
    def right_coordinate(self):
        return self.absolute_coordinates(*tuple_add(self.agent_position, DELTAS[self.left_direction]))

    def agent_forward(self):
        self.agent_x, self.agent_y = self.forward_coordinate

        if self.get_tile(self.agent_x, self.agent_y) == FOOD:
            self.food_eaten += 1
        elif self.get_tile(self.agent_x, self.agent_y) == POISON:
            self.poison_eaten += 1

        self.set_tile(self.agent_x, self.agent_y, EMPTY)

    def agent_turn_left(self):
        self.agent_heading = self.left_direction

    def agent_turn_right(self):
        self.agent_heading = self.right_direction

    def get_sensor_readings(self):
        return {
            'forward': self.get_tile(*self.forward_coordinate),
            'left': self.get_tile(*self.left_coordinate),
            'right': self.get_tile(*self.right_coordinate)
        }

    def perform_action(self, action):
        assert action in ACTIONS

        if action == LEFT:
            self.agent_turn_left()
            self.agent_forward()
        elif action == FORWARD:
            self.agent_forward()
        elif action == RIGHT:
            self.agent_turn_right()
            self.agent_forward()

    def simulate(self, agent):
        actions = []
        while self.t > 0:
            sensors = self.get_sensor_readings()
            input_layer = [
                int(sensors['left'] == FOOD),
                int(sensors['forward'] == FOOD),
                int(sensors['right'] == FOOD),
                int(sensors['left'] == POISON),
                int(sensors['forward'] == POISON),
                int(sensors['right'] == POISON)
            ]
            output = agent.propagate_input(input_layer)

            action_i = max(range(len(output)), key=lambda i: output[i])

            if output[action_i] > self.minimum_activation:
                action = ACTIONS[action_i]
            else:
                action = NOOP

            self.perform_action(action)

            self.t -= 1

            actions.append(action)

        return actions

    @property
    def score(self):
        food_score = self.food_eaten / ((self.food_eaten + self.get_count_of_value(FOOD)) or 1)
        poison_score = self.poison_eaten / ((self.poison_eaten + self.get_count_of_value(POISON)) or 1)
        return food_score - poison_score

    def new_flatland_same_parameters(self):
        return Flatland(dimensions=(self.w, self.h), f=self.f, p=self.p, t=self.t)


class FlatlandProblem(Problem):
    def __init__(self, n_bits, layers, bias, f, p, t,
                 dimensions=(10, 10),
                 static=True,
                 activation_function=sigmoid,
                 activation_threshold=0.0,
                 minimum_activation=0.0,
                 num_scenarios=1
    ):
        self.n_bits = n_bits
        self.layers = layers  # layer 0: [left food, fwd food, right food, left poison, fwd poison, right poison]
        self.bias = bias
        self.neural_network = NeuralNetwork(layers, bias, activation_function, activation_threshold)
        self.n_weights = sum(a * b for a, b in self.neural_network.get_matrix_dimensions())
        self.genotype_size = self.n_bits * self.n_weights
        self.static = static
        self.num_scenarios = num_scenarios
        self.flatland = Flatland(dimensions, f, p, t, minimum_activation=minimum_activation)

    @property
    def dynamic(self):
        return not self.static

    def create_initial_population(self, population_size):
        return [Individual(random_bitstring(self.genotype_size)) for _ in xrange(population_size)]

    def geno_to_pheno(self, genotype):
        """
        Converts each consecutive self.number_of_bits-sized chunk in the genotype to a float between 0 and 1
        """
        weight = lambda i: normalize_bitstring(genotype[i:i + self.n_bits])
        matrix_dimensions = self.neural_network.get_matrix_dimensions()
        return matrix_fit([weight(i) for i in xrange(0, self.genotype_size, self.n_bits)], matrix_dimensions)

    def mutate_genome_component(self, component):
        return 0 if int(component) else 1

    def generate_new_scenario(self):
        return self.flatland.new_flatland_same_parameters()

    def fitness(self, phenotype, scenarios=None):
        # 1.: feed weights from phenotype into network
        # 2.: run timesteps with these weights
        # 3.: evaluate performance

        if not scenarios:
            scenarios = [self.flatland]

        scenarios = deepcopy(scenarios)

        self.neural_network.connections = phenotype

        scores = []
        for scenario in scenarios:
            scenario.simulate(agent=self.neural_network)
            scores.append(scenario.score)

        return sum(scores) / len(scores)

    def visualization(self, **kwargs):
        individual = kwargs.get('individual')
        board = kwargs.get('board')

        flatland = deepcopy(board)

        self.neural_network.connections = individual.phenotype

        actions = flatland.simulate(agent=self.neural_network)

        print('F: {}/{}, P: {}/{}'.format(
            flatland.food_eaten,
            flatland.food_eaten + flatland.get_count_of_value(FOOD),
            flatland.poison_eaten,
            flatland.poison_eaten + flatland.get_count_of_value(POISON)
        ))
        print('Fitness: ', self.fitness(individual.phenotype, scenarios=[board]))

        FlatlandGUI(deepcopy(board), actions)
