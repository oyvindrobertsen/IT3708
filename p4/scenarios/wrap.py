from __future__ import print_function, division

from beer_tracker import BeerTrackerProblem, BeerTrackerWorld
from ctrnn.neural_network import NeuralNetwork, Neuron as N, BiasNeuron as B
from ea.ea import EARunner
from ea.problems.utils import *

if __name__ == "__main__":
    problem = BeerTrackerProblem(
        world=BeerTrackerWorld(30, 15, wrap=True),
        neural_network=NeuralNetwork((
            (N(), N(), N(), N(), N(), B(1.0)),
            (N(), N(), B(1.0)),
            (N(), N())
        )),
        n_bits=8
    )

    # Configure the runner
    population_size = 60
    generations = 100
    adult_selection = generational_mixing
    adult_to_child_ratio = 0.4
    parent_selection = sigma_scaling_selection
    k = 8
    epsilon = 0.05
    crossover_rate = 0.4
    crossover_function = one_point_crossover
    n_points = 3
    mutation_rate = 0.05
    mutation_function = per_genome_component
    threshold = None

    runner1 = EARunner(
        problem=problem,
        population_size=population_size,
        generations=generations,
        crossover_rate=crossover_rate,
        mutation_rate=mutation_rate,
        adult_selection=adult_selection,
        adult_to_child_ratio=adult_to_child_ratio,
        parent_selection=parent_selection,
        k=k,
        epsilon=epsilon,
        crossover_function=crossover_function,
        mutation_function=mutation_function,
        threshold=threshold
    )
    runner1.solve()
    runner1.plot()
