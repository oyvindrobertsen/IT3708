from __future__ import division, print_function
from copy import deepcopy
from random import randint

from ea.ea import Individual
from ea.problems import Problem
from enums import *
from gui import BeerTrackerGUI, FinishSimulationSignal
from utils import random_bitstring, normalize_bitstring, matrix_fit, scale

LARGE_CONST = 1
SMALL_CONST = 1


class BeerTrackerAgent(object):
    def __init__(self, world, brain):
        self.world = world
        self.brain = brain
        self.leftmost = 0
        self.reset_position()

        self.points = 0

        self.actions = []

        self.has_pull_option = self.brain.neuron_count(-1)[0] == 3

    def reset_position(self):
        self.leftmost = (self.world.width // 2) - (TRACKER_WIDTH // 2)

    @property
    def rightmost(self):
        r = self.leftmost + TRACKER_WIDTH - 1

        if self.world.wrap:
            return r % self.world.width

        return r

    @property
    def columns(self):
        if self.rightmost < self.leftmost:
            return range(self.leftmost, self.world.width) + range(0, self.rightmost + 1)

        return range(self.leftmost, self.rightmost + 1)

    def move(self, direction, steps):
        steps = int(steps)
        self.leftmost += direction * steps

        self.actions.append(direction * steps)

        self.leftmost %= self.world.width

    def get_sensor_readings(self):
        return [col_no in self.world.active_object.columns for col_no in self.columns]

    def act(self):
        out = self.brain.propagate_input(self.get_sensor_readings())

        if self.has_pull_option and out[2] > out[0] and out[2] > out[1]:
            self.world.pull()
            self.actions.append(PULL)
        elif out[0] > out[1]:
            self.move(LEFT, int(out[0] * 4.99))
        else:
            self.move(RIGHT, int(out[1] * 4.99))

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
            self.points -= 1
        else:
            self.points += 1

    def avoidance(self, obj):
        if obj.width >= 5:
            self.points += 2
        else:
            self.points -= 2

    def fail(self, obj):
        self.points -= 3


class BeerTrackerAgentWithWallSensors(BeerTrackerAgent):
    def get_sensor_readings(self):
        return super(BeerTrackerAgentWithWallSensors, self).get_sensor_readings() \
               + [self.leftmost <= 0, self.rightmost >= (self.world.width - 1)]

    def move(self, direction, steps):
        steps = int(steps)
        self.leftmost += direction * steps

        self.actions.append(direction * steps)

        if self.leftmost < 0:
            self.leftmost = 0
            self.points -= 1
        elif self.rightmost >= self.world.width:
            self.leftmost = self.world.width - TRACKER_WIDTH
            self.points -= 1


class BeerTrackerObject(object):
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


class BeerTrackerWorld(object):
    def __init__(self, width, height, wrap=True):
        self.width = width
        self.height = height
        self.wrap = wrap
        self.agent_class = BeerTrackerAgent if self.wrap else BeerTrackerAgentWithWallSensors

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
            self.agent.act()
            self.tick()
            if after_tick:
                try:
                    after_tick(tick=i)
                except FinishSimulationSignal:
                    after_tick = None


class BeerTrackerProblem(Problem):
    def __init__(self, world, neural_network, n_bits,
                 weight_range=(-5.0, 5.0),
                 bias_weight_range=(-10.0, 0.0),
                 gains_range=(1.0, 5.0),
                 ts_range=(1.0, 2.0)
    ):
        self.world = world
        self.neural_network = neural_network
        self.n_bits = n_bits

        self.weight_range = weight_range
        self.bias_weight_range = bias_weight_range
        self.gains_range = gains_range
        self.ts_range = ts_range

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

        agent = world.agent_class(world, brain)
        world.simulate(agent)

        return agent.points

    def visualization(self, *args, **kwargs):
        phenotype = kwargs.get('phenotype')
        network = self.neural_network
        network.assign_phenotype(phenotype)

        BeerTrackerGUI(
            world=self.world,
            agent=self.world.agent_class(
                world=self.world,
                brain=network
            )
        )
