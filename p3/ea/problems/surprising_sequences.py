from __future__ import division

import random

from problems import Problem
from problems.utils import *
from ea import EARunner, Individual

class SurprisingSequences(Problem):

    def __init__(self, genotype_size=10, symbol_set_size=5):
        self.genotype_size = genotype_size
        self.symbol_set_size=symbol_set_size

    def fitness(self, phenotype):
        '''
        We calculate number of violating sequences in the phenotype.
        '''
        found = set()
        violations = 0
        for i in range(self.genotype_size):
            for j in range(i + 1, self.genotype_size):
                a = phenotype[i]
                b = phenotype[j]
                seq = (a, b, j - i)
                if seq in found:
                    violations += 1
                else:
                    found.add(seq)
        return 1 / (1 + violations)


    def create_initial_population(self, population_size):
        return [Individual([random.randint(0, self.symbol_set_size-1) for _ in range(self.genotype_size)]) for _ in range(population_size)]
    
    def geno_to_pheno(self, genotype):
        return genotype

    def mutate_genome_component(self, component):
        return random.randint(0, self.symbol_set_size-1)


def main():
    # Configure the problem
    genotype_size = 94
    symbol_set_size = 37
    problem = SurprisingSequences(genotype_size, symbol_set_size)

    # Configure the runner
    population_size = 200
    generations = 20000
    crossover_rate = 0.09
    mutation_rate = 0.01
    adult_selection = over_production
    adult_to_child_ratio = 0.3
    parent_selection = tournament_selection
    k = 32
    epsilon = 0.05
    crossover_function = one_point_crossover
    mutation_function = per_genome_component
    threshold = 1.0
    runner = EARunner(
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
    runner.solve()
    runner.plot()


if __name__ == '__main__':
    main()

