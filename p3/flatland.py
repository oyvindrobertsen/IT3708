from __future__ import print_function, division
from copy import deepcopy
from random import random as r, choice

from ea.problems import Problem
from ea.ea import Individual
from ann.neural_network import NeuralNetwork
from utils import tuple_add, random_bitstring, normalize_bitstring


AGENT_DIRECTIONS = NORTH, WEST, SOUTH, EAST = 'N', 'W', 'S', 'E'
DELTAS = {
    NORTH: (0, -1),
    WEST: (-1, 0),
    SOUTH: (0, 1),
    EAST: (1, 0)
}

FOOD = 'F'
POISON = 'P'
EMPTY = ' '


class Flatland:
    def __init__(self, w, h, f, p, t):
        self.width = w
        self.height = h
        self.f = f
        self.p = p
        self.t = t

        self.grid = [[self.gen_tile() for x in xrange(w)] for y in xrange(h)]

        is_empty = lambda pos: self.get_tile(*pos) == EMPTY
        open_tiles = filter(is_empty, ((x, y) for x in xrange(w) for y in xrange(h)))

        self.agent_x, self.agent_y = choice(open_tiles)
        self.agent_heading = choice(AGENT_DIRECTIONS)

        self.food_eaten = 0
        self.poison_eaten = 0

    def gen_tile(self):
        return FOOD if r() < self.f else POISON if r() < self.p else EMPTY

    def get_tile(self, x, y):
        return self.grid[y][x]

    def abs_coords(self, x, y):
        return x % self.width, y % self.height

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
        return self.abs_coords(*tuple_add(self.agent_position, DELTAS[self.agent_heading]))

    @property
    def left_coordinate(self):
        return self.abs_coords(*tuple_add(self.agent_position, DELTAS[self.right_direction]))

    @property
    def right_coordinate(self):
        return self.abs_coords(*tuple_add(self.agent_position, DELTAS[self.left_direction]))

    def agent_forward(self):
        self.agent_x, self.agent_y = self.forward_coordinate

        if self.get_tile(self.agent_x, self.agent_y) == FOOD:
            self.food_eaten += 1
        elif self.get_tile(self.agent_x, self.agent_y) == POISON:
            self.poison_eaten += 1

        self.grid[self.agent_y][self.agent_x] = EMPTY

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

    @property
    def remaining_food(self):
        return sum(sum(cell == FOOD for cell in row) for row in self.grid)

    @property
    def remaining_poison(self):
        return sum(sum(cell == POISON for cell in row) for row in self.grid)

    def simulate(self, agent):
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

            # TODO: threshold?

            if action_i == 0:
                self.agent_turn_left()
            elif action_i == 2:
                self.agent_turn_right()

            self.agent_forward()

            self.t -= 1

    @property
    def score(self):
        return (self.food_eaten - self.poison_eaten) / (self.food_eaten + self.remaining_food)


class EvoFlatland(Problem):
    def __init__(self, n_bits, layers, bias, static=True):
        self.n_bits = n_bits
        self.layers = layers # layer 0: [left food, fwd food, right food, left poison, fwd poison, right poison]
        self.bias = bias
        self.nn = NeuralNetwork(layers, bias)
        self.n_weights = sum(a * b for a, b in self.nn.get_matrix_dimensions())
        self.genotype_size = self.n_bits * self.n_weights
        self.static = static
        W, H = (10, 10)
        F, P = 0.25, 0.25
        T = 60
        self.flatland = Flatland(W, H, F, P, T)

    def create_initial_population(self, population_size):
        return [Individual(random_bitstring(self.genotype_size)) for _ in xrange(population_size)]

    def geno_to_pheno(self, genotype):
        """
        Converts each consecutive self.number_of_bits-sized chunk in the genotype to a float between 0 and 1
        """
        return [normalize_bitstring(genotype[i:i + self.n_bits]) for i in xrange(0, self.genotype_size, self.n_bits)]

    def mutate_genome_component(self, component):
        return 0 if component else 1

    def fitness(self, phenotype):
        # 1.: feed weights from phenotype into network
        # 2.: run timesteps with these weights
        # 3.: evaluate performance

        flatland = deepcopy(self.flatland)

        self.nn.set_weights(phenotype)
        flatland.simulate(self.nn)
        return flatland.score
