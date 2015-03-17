from __future__ import division

import random
import numpy as np

import matplotlib.pyplot as plt

from problems import Problem
from problems.utils import *
from ea import EARunner, Individual

class OneMax(Problem):

    def __init__(self, genotype_size=20, rndm=False):
        if genotype_size and not rndm:
            self.genotype_size = genotype_size
            self.ideal = [1 for _ in range(self.genotype_size)]
        else:
            self.genotype_size = genotype_size
            self.ideal = [random.choice((0,1)) for _ in range(self.genotype_size)]
        
    def fitness(self, phenotype):
        '''
        Fitness, higher is better.
        '''
        error = 0
        for i in range(self.genotype_size):
            if phenotype[i] != self.ideal[i]:
                error += 1
        return 1 - (error / self.genotype_size)

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
    random = True
    problem = OneMax(genotype_size, random)

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


    generations_random = []

    for i in range(50):
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
        generations_random.append(len(runner1.averages))

    genotype_size = 40
    random = False
    problem = OneMax(genotype_size, random)

    generations_not_random = []

    for i in range(50):
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
        generations_not_random.append(len(runner1.averages))



    plt.title('Number of generations spent searching ')
    plt.plot(generations_not_random)
    plt.plot(generations_random)
    plt.legend(['One Max (avg = ' + str(np.mean(generations_not_random)) + ')', 'Random string (avg = ' + str(np.mean(generations_random)) + ')'], loc='best')
    plt.show()






if __name__ == '__main__':
    main()
