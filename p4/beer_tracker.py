from __future__ import division, print_function
from copy import deepcopy
from random import randint
from math import ceil

from ea.ea import Individual
from ea.problems import Problem
from enums import *
from gui import BeerTrackerGUI
from utils import random_bitstring, normalize_bitstring, matrix_fit


class BeerTrackerAgent:
    def __init__(self, world, brain):
        self.world = world
        self.brain = brain
        self.leftmost = 0

        self.points = 0.0

        self.actions = []

    def reset_position(self):
        self.leftmost = (self.world.width // 2) - (TRACKER_WIDTH // 2)

    @property
    def rightmost(self):
        return (self.leftmost + TRACKER_WIDTH - 1) % self.world.width

    @property
    def columns(self):
        if self.rightmost < self.leftmost:
            return range(self.leftmost, self.world.width) + range(0, self.rightmost + 1)

        return range(self.leftmost, self.rightmost + 1)

    def move(self, direction, steps):
        steps = int(steps)
        self.leftmost += direction * steps

        self.actions.append(direction * steps)

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
        if obj.width >= 5:
            pass
            # self.points -= 1.0
        else:
            self.points += 1.0

    def avoidance(self, obj):
        if obj.width >= 5:
            self.points += 1.0
        else:
            pass
            # self.points -= 1.0

    def fail(self, obj):
        pass
        # self.points -= 1.0


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

        self.agent = None
        self.active_object = None

        self.max_points = 0

    def new_falling_object(self):
        width = randint(1, 6)
        left = randint(0, self.width - width)
        self.active_object = BeerTrackerObject(left, self.height, width)

    def tick(self):
        if self.active_object.y_position == 0:
            self.agent.interact(self.active_object)
            self.max_points += 1
            self.new_falling_object()
            return

        self.active_object.y_position -= 1

    def pull(self):
        self.active_object.y_position = 0

    def simulate(self, agent, after_tick=None):
        self.agent = agent

        self.new_falling_object()

        for i in xrange(TIMESTEPS):
            out = self.agent.brain.propagate_input(self.agent.get_sensor_readings())

            if max(out) < .2:
                pass
            elif out[0] > out[1]:
                self.agent.move(LEFT, ceil(((out[0] - .2) / .8) * 4))
            else:
                self.agent.move(RIGHT, ceil(((out[1] - .2) / .8) * 4))

            self.tick()
            if after_tick:
                after_tick(tick=i)

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


class BeerTrackerProblem(Problem):
    def __init__(self, world, neural_network, n_bits):
        self.world = world
        self.neural_network = neural_network
        self.n_bits = n_bits

        p = self.neural_network.get_phenotype_size()
        self.genotype_size = self.n_bits * (
            sum(a * b for a, b in p['inter']) + sum(a * b for a, b in p['cross']) + 2 * p['neurons']
        )

    def create_initial_population(self, population_size):
        return [Individual(random_bitstring(self.genotype_size)) for _ in xrange(population_size)]

    def geno_to_pheno(self, genotype):
        weight = lambda i: normalize_bitstring(genotype[i:i + self.n_bits])
        values = [weight(i) for i in xrange(0, self.genotype_size, self.n_bits)]

        ps = self.neural_network.get_phenotype_size()
        d = {}
        d['cross'], values = matrix_fit(values, ps['cross'], map=lambda x: -5.0 + 10.0 * x)
        d['inter'], values = matrix_fit(values, ps['inter'], map=lambda x: -5.0 + 10.0 * x)
        d['gains'] = map(lambda x: 1.0 + 4.0 * x, values[:ps['neurons']])
        d['ts'] = map(lambda x: 1.0 + x, values[ps['neurons']:])

        return d

    def mutate_genome_component(self, component):
        return 0 if int(component) else 1

    def fitness(self, phenotype):
        world = deepcopy(self.world)
        brain = deepcopy(self.neural_network)
        brain.assign_phenotype(phenotype)

        agent = BeerTrackerAgent(world, brain)
        world.simulate(agent)

        return agent.points / world.max_points

    def visualization(self, *args, **kwargs):
        individual = kwargs.get('individual')
        network = self.neural_network
        network.assign_phenotype(individual.phenotype)

        BeerTrackerGUI(
            world=self.world,
            agent=BeerTrackerAgent(
                world=self.world,
                brain=network
            )
        )
