from __future__ import print_function, division

from numpy.random import rand as random_matrix
import numpy as np

from utils import vector_sigmoid


class NeuralNetwork:
    def __init__(self, layers):
        assert len(layers) > 2

        self.layers = layers

        self.connections = self.generate_initial_weights()
        # rows for the first layer, cols for the second

        self.neuron_layers = [np.array(0 for _ in xrange(layer)) for layer in layers]

        print(*self.connections, sep='\n')

    def generate_initial_weights(self):
        return [random_matrix(a, b) for (a, b) in zip(self.layers[:-1], self.layers[1:])]

    def input(self, *values):
        assert len(values) == self.layers[0]

        self.neuron_layers[0] = np.array(values)

        for layer_no in xrange(len(self.layers) - 1):
            a = self.neuron_layers[layer_no]
            b = self.connections[layer_no]

            self.neuron_layers[layer_no + 1] = vector_sigmoid(a.dot(b))

        print(self.neuron_layers)


nn = NeuralNetwork([3, 5, 2])
nn.input(1, 0, 1)
