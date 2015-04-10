from __future__ import print_function, division

from flatland import FlatlandProblem
from ea.ea import EARunner
from ea.problems.utils import *

if __name__ == "__main__":
    layers = [6, 3]
    bias = {0: [1.0]}
    problem = FlatlandProblem(
        1,
        layers,
        bias,
        f=0.33,
        p=0.33,
        t=60,
        activation_threshold=0.0,
        minimum_activation=0.1,
        static=False
    )

    # Configure the runner
    population_size = 200
    generations = 100
    crossover_rate = 0.5
    mutation_rate = 0.01
    adult_selection = generational_mixing
    adult_to_child_ratio = 0.5
    parent_selection = tournament_selection
    k = 8
    epsilon = 0.15
    crossover_function = one_point_crossover
    mutation_function = per_genome_component
    threshold = 1.0

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
