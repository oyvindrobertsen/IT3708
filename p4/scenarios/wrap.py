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

'''
{'inter': [array([[-1.82352941, -2.96078431],
       [ 2.68627451, -3.07843137]]), array([[-2.25490196,  4.80392157],
       [ 0.64705882,  0.17647059]])], 'cross': [array([[ 4.7254902 ,  4.80392157],
       [-3.70588235, -0.80392157],
       [-4.88235294,  0.52941176],
       [ 3.07843137, -1.39215686],
       [ 0.92156863, -0.45098039],
       [ 0.96078431, -1.58823529]]), array([[-4.68627451,  4.21568627],
       [ 3.78431373,  3.90196078],
       [-4.33333333, -1.78431373]])], 'ts': [1.3411764705882354, 1.5843137254901962, 1.1764705882352942, 1.772549019607843, 1.6313725490196078, 1.5411764705882351, 1.1372549019607843, 1.0745098039215686, 1.1647058823529413], 'gains': [3.227450980392157, 3.5098039215686274, 4.529411764705882, 2.1921568627450982, 3.603921568627451, 1.9254901960784314, 2.333333333333333, 3.243137254901961, 4.780392156862745]}
'''