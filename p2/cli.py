#! /usr/bin/python
from argparse import ArgumentParser

from ea import EARunner
from problems import one_max
from problems.utils import *

def get_args():
    parser = ArgumentParser(description='Evolutionary algorithm implementation.')
    parser.add_argument('problem', help='the problem to solve', metavar='P')
    parser.add_argument('-p', '--population-size', help='number of individuals in the population', metavar='')
    parser.add_argument('-g', '--genotype_size', help='size of genotype in bits', metavar='')
    parser.add_argument('-n', '--generations', help='number of generations to run', metavar='')
    parser.add_argument('-c', '--crossover-rate', help='crossover rate, 0 -> 1', metavar='')
    parser.add_argument('-m', '--mutation-rate', help='mutation rate, 0 -> 1', metavar='')
    parser.add_argument('-a', '--adult-selection', help='specifies which adult selection strategy to use', metavar='')
    parser.add_argument('-r', '--adult-to-child-ratio', help='specifies the adult to child ratio of the population, 0 -> 1', metavar='')
    parser.add_argument('-s', '--parent-selection', help='specifies which parent selection strategy to use', metavar='')
    return parser.parse_args()

def get_problem(problem_name, genotype_size=None, adult_selection=None):
    '''
    Returns an instance of a problem class based on the problem name
    '''
    if problem_name == 'one_max':
        return one_max.OneMax(genotype_size, adult_selection)

def get_adult_selection(adult_selection_name):
    if adult_selection_name == 'full_replacement':
        return full_replacement
    elif adult_selection_name == 'over_production':
        return over_production
    elif adult_selection_name == 'generational_mixing':
        return generational_mixing
    else:
        return None

def get_parent_selection(parent_selection_name):
    if parent_selection_name == 'fitness_proportionate_selection':
        return fitness_proportionate_selection
    else:
        return None

def main():
    args = get_args()
    problem = get_problem(args.problem, int(args.genotype_size) if args.genotype_size else None)
    population_size = int(args.population_size) if args.population_size else 20
    generations = int(args.generations) if args.generations else 100
    crossover_rate = float(args.crossover_rate) if args.crossover_rate else 0.5
    mutation_rate = float(args.mutation_rate) if args.mutation_rate else 0.1
    adult_selection = get_adult_selection(args.adult_selection)
    adult_to_child_ratio = float(args.adult_to_child_ratio) if args.adult_to_child_ratio else 0.5
    parent_selection = get_parent_selection(args.parent_selection)
    runner = EARunner(problem, population_size, generations, crossover_rate, mutation_rate, adult_selection, adult_to_child_ratio, parent_selection)
    runner.solve()


if __name__ == '__main__':
    main()
