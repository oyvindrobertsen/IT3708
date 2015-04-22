from __future__ import division, print_function

from copy import deepcopy

import matplotlib.pyplot as plt

from problems.utils import *


def log_generation(generation_number, *stuff):
    print(
        'G{:<3}:\t{}'.format(
            generation_number,
            ',\t'.join(str(round(x, 2) if isinstance(x, float) else x) for x in stuff)
        )
    )


class Individual(object):
    def __init__(self, genotype):
        self.genotype = genotype
        self.phenotype = None
        self.fitness = None
        self.mature = False

    def __repr__(self):
        # return ''.join(map(str, self.genotype))
        return str(self.fitness)


class EARunner(object):
    '''
    Simple EA implementation
    '''

    def __init__(self, **kwargs):
        self.problem = kwargs['problem']
        self.population_size = kwargs['population_size']
        self.generations = kwargs['generations']
        self.crossover_rate = kwargs['crossover_rate']
        self.mutation_rate = kwargs['mutation_rate']
        self.adult_selection = kwargs['adult_selection']
        self.number_of_adults = int(self.population_size * kwargs['adult_to_child_ratio'])
        self.select_parent = kwargs['parent_selection']
        self.crossover = kwargs['crossover_function']
        self.mutate = kwargs['mutation_function']
        self.threshold = kwargs['threshold']
        self.averages = []
        self.maximums = []
        self.std_devs = []

    def solve(self, **kwargs):
        # Generate an initial population
        self.population = self.problem.create_initial_population(self.population_size - self.number_of_adults)
        # Start evolution
        analyze_after_loop = True
        last_best = None

        for generation in range(self.generations):
            self.problem.pre_generation_hook()
            # Genotype to phenotype conversion
            # Analyzing population of this generation, logging
            total = 0
            generation_max_fitness = -100
            generation_max_phenotype = None
            fitnesses = []
            done = False

            for individual in self.population:
                # Convert to phenotype
                if individual.phenotype is None:
                    individual.phenotype = self.problem.geno_to_pheno(individual.genotype)
                # Evaluate fitness
                individual.fitness = self.problem.fitness(individual.phenotype)

                if self.threshold and individual.fitness >= self.threshold:
                    done = True
                    analyze_after_loop = False
                total += individual.fitness
                fitnesses.append(individual.fitness)
                if individual.fitness > generation_max_fitness:
                    last_best = individual
                    generation_max_fitness = individual.fitness
                    generation_max_phenotype = individual.phenotype

            avg = total / len(self.population)
            self.averages.append(avg)
            self.maximums.append(generation_max_fitness)
            std_dev = np.std(np.array(fitnesses))
            self.std_devs.append(std_dev)
            log_generation(generation, generation_max_fitness, avg, std_dev)

            if done:
                break

            # Adult selection
            self.population = self.adult_selection(self.population, number_of_adults=self.number_of_adults, **kwargs)

            # Parent selection
            # We need max population_size - len(population) pairs, to fill the population
            open_slots = self.population_size - len(self.population)
            # We calculate temperature inversely proportionate to progression wether we use it in parent selection or not
            temperature = max(1, self.generations - len(self.averages))
            parents = [(self.select_parent(self.population, temperature=temperature),
                        self.select_parent(self.population, temperature=temperature, **kwargs)) for _ in range(open_slots)]

            children = []
            while len(children) < open_slots:
                parent_1, parent_2 = parents.pop()
                roll = random.random()
                if roll < self.crossover_rate:
                    children.append(self.crossover(parent_1, parent_2, **kwargs))
                else:
                    child_1 = Individual(deepcopy(parent_1.genotype))
                    child_2 = Individual(deepcopy(parent_2.genotype))
                    children.append(child_1)
                    if open_slots > len(children):
                        children.append(child_2)
            children = self.mutate(children, self.mutation_rate, self.problem.mutate_genome_component, **kwargs)
            self.population = self.population + children

        self.problem.visualization(phenotype=last_best.phenotype)

        # Analyze last generated generation if we didn't find a solution
        if analyze_after_loop:
            total = 0
            generation_max_fitness = -1
            generation_max_phenotype = None
            fitnesses = []
            done = False
            for individual in self.population:
                # Convert to phenotype
                if individual.phenotype is None:
                    individual.phenotype = self.problem.geno_to_pheno(individual.genotype)
                # Evaluate fitness
                if not individual.fitness:
                    individual.fitness = self.problem.fitness(individual.phenotype)

                if individual.fitness > self.threshold or individual.fitness == 1.0:
                    done = True
                    analyze_after_loop = False
                total += individual.fitness
                fitnesses.append(individual.fitness)
                if individual.fitness > generation_max_fitness:
                    generation_max_fitness = individual.fitness
                    generation_max_phenotype = individual.phenotype

            avg = total / len(self.population)
            self.averages.append(avg)
            self.maximums.append(generation_max_fitness)
            std_dev = np.std(np.array(fitnesses))
            self.std_devs.append(std_dev)
            log_generation(len(self.averages) - 1, generation_max_fitness, avg, std_dev)

    def plot(self):
        plt.title(self.problem)
        plt.plot(self.averages)
        plt.plot(self.maximums)
        plt.plot(self.std_devs)
        plt.legend(['averages', 'maximums', 'standard deviation'], loc='best')
        plt.show()
