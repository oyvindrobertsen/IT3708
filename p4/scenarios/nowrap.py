from __future__ import print_function, division

from beer_tracker import BeerTrackerProblem, BeerTrackerWorld
from ctrnn.neural_network import NeuralNetwork, Neuron as N, BiasNeuron as B
from ea.ea import EARunner
from ea.problems.utils import *

'''
{'inter': [array([[ 0.41176471, -1.50980392, -4.7254902 ,  1.43137255],
       [ 2.1372549 , -2.7254902 , -0.49019608, -4.01960784],
       [-0.7254902 ,  0.25490196,  3.62745098, -1.11764706],
       [ 1.03921569,  1.78431373,  3.58823529,  1.50980392]]), array([[ 4.21568627, -4.25490196],
       [ 2.33333333,  4.09803922]])], 'cross': [array([[-1.58823529,  3.50980392, -0.76470588,  0.17647059],
       [-1.03921569, -4.96078431,  1.66666667, -1.70588235],
       [-4.01960784, -4.45098039,  3.07843137, -3.2745098 ],
       [-1.39215686,  4.25490196, -1.98039216, -0.17647059],
       [-4.60784314, -4.68627451, -4.01960784,  4.80392157],
       [ 0.64705882, -4.37254902, -1.07843137,  4.68627451],
       [-1.54901961, -3.31372549, -3.54901961, -4.80392157]]), array([[-0.92156863,  2.88235294],
       [ 3.94117647,  0.84313725],
       [-4.96078431, -0.68627451],
       [-4.64705882,  4.17647059],
       [ 2.76470588,  4.68627451]])], 'ts': [1.0235294117647058, 1.196078431372549, 1.4, 1.2705882352941176, 1.5019607843137255, 1.0823529411764705, 1.6588235294117646, 1.6274509803921569, 1.0313725490196077, 1.192156862745098, 1.7215686274509805, 1.6, 1.0313725490196077], 'gains': [3.7137254901960786, 4.137254901960784, 2.6941176470588237, 2.9137254901960787, 4.0588235294117645, 4.294117647058823, 1.7215686274509805, 4.341176470588236, 1.5333333333333332, 1.5176470588235293, 4.529411764705882, 3.1019607843137256, 3.854901960784314]}
'''


if __name__ == "__main__":
    problem = BeerTrackerProblem(
        world=BeerTrackerWorld(30, 15, wrap=False),
        neural_network=NeuralNetwork((
            (N(), N(), N(), N(), N(), N(), N()),
            (N(), N(), N(), N(), B(1.0)),
            (N(), N())
        )),
        n_bits=8,
        # ts_range=(1.0, 20.0),
        # gains_range=(1.0, 10.0)
    )

    # Configure the runner
    population_size = 100
    generations = 100
    adult_selection = generational_mixing
    adult_to_child_ratio = 0.7
    parent_selection = sigma_scaling_selection
    k = 8
    epsilon = 0.05
    crossover_rate = 0.7
    crossover_function = one_point_crossover
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
