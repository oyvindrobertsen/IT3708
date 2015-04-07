from __future__ import division

import random
import matplotlib.pyplot as plt

from problems import Problem
from problems.utils import *
from ea import EARunner, Individual

class LOLZ(Problem):

    def __init__(self, genotype_size=20, z=5):
        self.z = z
        self.genotype_size = genotype_size
        
    def fitness(self, phenotype):
        '''
        Fitness, higher is better.
        '''
        counter = 0
        count = phenotype[0]
        for bit in phenotype:
            if bit != count:
                break
            counter += 1
        if count == 0:
            counter = min(self.z, counter)
        discrepancy = self.genotype_size - counter
        return 1 - (discrepancy / self.genotype_size)

    def create_initial_population(self, population_size):
        return [Individual([random.choice((0,1)) for _ in range(self.genotype_size)]) for _ in range(population_size)]
    
    def geno_to_pheno(self, genotype):
        return genotype

    def mutate_genome_component(self, component):
        if component:
            return 0
        return 1


def main():
    # Configure the problem
    genotype_size = 40
    z = 21
    problem = LOLZ(genotype_size, z)

    # Configure the runner
    population_size = 600
    generations = 100
    crossover_rate = 0.80
    mutation_rate = 0.01
    adult_selection = full_replacement
    adult_to_child_ratio = 0.5
    parent_selection = tournament_selection
    k = 8
    epsilon = 0.05
    crossover_function = one_point_crossover
    mutation_function = per_genome
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
            mutation_function = mutation_function,
            threshold=threshold
            )
    runner1.solve()


    runner2 = EARunner(
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
            mutation_function = mutation_function,
            threshold=threshold
            )
    runner2.solve()

    runner3 = EARunner(
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
            mutation_function = mutation_function,
            threshold=threshold
            )
    runner3.solve()

    runner4 = EARunner(
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
            mutation_function = mutation_function,
            threshold=threshold
            )
    runner4.solve()

    runner5 = EARunner(
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
            mutation_function = mutation_function,
            threshold=threshold
            )
    runner5.solve()

    runner6 = EARunner(
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
            mutation_function = mutation_function,
            threshold=threshold
            )
    runner6.solve()

    runner7 = EARunner(
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
            mutation_function = mutation_function,
            threshold=threshold
            )
    runner7.solve()

    runner8 = EARunner(
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
            mutation_function = mutation_function,
            threshold=threshold
            )
    runner8.solve()

    plt.title('Average fitnesses of 8 runs with max 100 generations of the LOLZ problem')
    plt.plot(runner1.averages)
    plt.plot(runner2.averages)
    plt.plot(runner3.averages)
    plt.plot(runner4.averages)
    plt.plot(runner5.averages)
    plt.plot(runner6.averages)
    plt.plot(runner7.averages)
    plt.plot(runner8.averages)
    plt.show()


if __name__ == '__main__':
    main()

