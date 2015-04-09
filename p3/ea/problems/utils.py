from __future__ import division

import sys
import random
import math
import numpy as np


def set_adult(individual):
    individual.mature = True
    return individual


# Adult selection

def full_replacement(population, **kwargs):
    return list(map(set_adult, filter(lambda ind: not ind.mature, population)))


def over_production(population, **kwargs):
    if kwargs['number_of_adults']:
        number_of_adults = kwargs.pop('number_of_adults')
    else:
        sys.exit('over_production adult selection requires number of adults to be specified.')
    children = sorted(
        list(filter(lambda ind: not ind.mature, population)),
        cmp=lambda x, y: cmp(x.fitness, y.fitness),
        reverse=True)[:number_of_adults]
    return list(map(set_adult, children))


def generational_mixing(population, **kwargs):
    if kwargs['number_of_adults']:
        number_of_adults = kwargs.pop('number_of_adults')
    else:
        sys.exit('generational_mixing adult selection requires number of adults to be specified.')
    return list(
        map(set_adult, sorted(population, cmp=lambda x, y: cmp(x.fitness, y.fitness), reverse=True)[:number_of_adults]))


# Parent selection

# These are clumsy and have great potential for better code reuse.
# They work, however.

def fitness_proportionate_selection(population, **kwargs):
    fitnesses = [individual.fitness for individual in population]
    total_fitness = sum(fitnesses)
    roll = random.uniform(0, total_fitness)
    total = 0
    for individual in population:
        total += individual.fitness
        if total > roll:
            return individual


def sigma_scaling_selection(population, **kwargs):
    fitnesses = [individual.fitness for individual in population]
    avg = np.mean(fitnesses)
    std_dev = max(0.001, np.std(fitnesses))
    sigma_scaled = list(map(lambda fitness: 1 + ((fitness - avg) / (2 * std_dev)), fitnesses))
    total_fitness = sum(sigma_scaled)
    roll = random.uniform(0, total_fitness)
    total = 0
    for i in range(len(population)):
        total += sigma_scaled[i]
        if total > roll:
            return population[i]


def boltzmann_selection(population, temperature=1, **kwargs):
    fitnesses = [individual.fitness for individual in population]
    exp_avg = np.mean([math.exp(individual.fitness / temperature) for individual in population])
    temp_scaled = list(map(lambda ind: math.exp(ind.fitness / temperature) / exp_avg, population))
    total_fitness = sum(temp_scaled)
    roll = random.uniform(0, total_fitness)
    total = 0
    for i in range(len(population)):
        total += temp_scaled[i]
        if total > roll:
            return population[i]


def tournament_selection(population, k=1, epsilon=0.2, **kwargs):
    group = random.sample(population, k)
    roll = random.random()
    if roll < epsilon:
        return random.choice(group)
    else:
        return max(group, key=lambda ind: ind.fitness)


# Crossover

def one_point_crossover(parent_1, parent_2, **kwargs):
    from ea.ea import Individual

    roll = random.random()
    cutoff = int(len(parent_1.genotype) * roll)
    child_genotype = parent_1.genotype[:cutoff] + parent_2.genotype[cutoff:]
    return Individual(child_genotype)


def braid(parent_1, parent_2, **kwargs):
    from ea.ea import Individual

    child_genotype = []
    for i in range(len(parent_1.genotype)):
        if i % 2 == 0:
            child_genotype.append(parent_2.genotype[i])
        else:
            child_genotype.append(parent_1.genotype[i])
    return Individual(child_genotype)


# Mutation

def per_genome_component(population, rate, component_modifier, **kwargs):
    for individual in population:
        for i in range(len(individual.genotype)):
            roll = random.random()
            if roll <= rate:
                replacement = component_modifier(individual.genotype[i])
                individual.genotype = replace_element_i(individual.genotype, i, replacement)
    return population


def per_genome(population, rate, component_modifier, **kwargs):
    for individual in population:
        roll = random.random()
        if roll <= rate:
            rand_index = random.randint(0, len(individual.genotype) - 1)
            replacement = component_modifier(individual.genotype[rand_index])
            individual.genotype = replace_element_i(individual.genotype, rand_index, replacement)
    return population


def replace_element_i(s, i, replacement):
    l = list(s)
    l[i] = replacement
    return ''.join(str(x) for x in l)