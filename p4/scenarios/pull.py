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
            (N(), N(), N())
        )),
        n_bits=8
    )

    # Configure the runner
    population_size = 40
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
{'inter': [array([[-1.31372549, -3.62745098],
       [-3.78431373,  0.21568627]]), array([[-4.05882353,  4.56862745, -0.56862745],
       [-4.80392157,  3.98039216,  3.62745098],
       [ 1.94117647,  3.50980392, -1.11764706]])], 'cross': [array([[-4.76470588, -1.2745098 ],
       [-1.58823529, -4.17647059],
       [ 4.56862745,  1.07843137],
       [ 3.11764706, -3.11764706],
       [-1.        , -2.21568627],
       [-0.21568627, -2.84313725]]), array([[ 4.29411765, -2.92156863,  4.60784314],
       [ 0.80392157,  0.45098039,  0.56862745],
       [-3.58823529, -0.01960784,  1.2745098 ]])], 'ts': [1.4745098039215687, 1.5215686274509803, 1.0509803921568628, 1.5137254901960784, 1.5019607843137255, 1.0666666666666667, 1.196078431372549, 1.4666666666666668, 1.423529411764706, 1.2823529411764705], 'gains': [1.0784313725490196, 2.427450980392157, 1.6745098039215687, 1.8784313725490196, 3.6823529411764704, 1.9411764705882353, 2.9294117647058826, 1.219607843137255, 2.207843137254902, 2.223529411764706]}
'''
