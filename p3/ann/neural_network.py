from __future__ import print_function, division

from numpy.random import rand as random_matrix
import numpy as np

from utils import sigmoid


class NeuralNetwork:
    def __init__(self, layers, bias={}, activation_function=sigmoid, activation_threshold=0.0):
        assert len(layers) >= 2

        self.n_regular_neurons = layers
        self.bias_neurons = bias

        self.connections = None

        self.neuron_layers = [
            np.concatenate((np.zeros(n), self.bias_neurons.get(i, []))) for i, n in enumerate(layers)
        ]

        self.vector_activation_function = np.vectorize(lambda x: activation_function(x - activation_threshold))

    def get_matrix_dimensions(self):
        return [
            (self.n_regular_neurons[i] + len(self.bias_neurons.get(i, [])), self.n_regular_neurons[i + 1]) for i in xrange(len(self.n_regular_neurons) - 1)
        ]

    def set_layer(self, layer_no, values):
        """
        possible bias neurons sit at the end of the layer, so assignment shouldn't touch those
        """
        self.neuron_layers[layer_no][:self.n_regular_neurons[layer_no]] = values

    def propagate_input(self, values):
        """
        takes input values, forward propagates them through the network
        and returns the activation values for the output layer
        """
        assert self.connections is not None
        assert len(values) == self.n_regular_neurons[0]

        self.set_layer(0, np.array(values))

        for layer_no in xrange(len(self.n_regular_neurons) - 1):
            a = self.neuron_layers[layer_no]
            b = self.connections[layer_no]

            self.set_layer(layer_no + 1, self.vector_activation_function(a.dot(b)))

        return self.neuron_layers[-1]


if __name__ == '__main__':
    # number of normal neurons per layer
    layers = [3, 5, 2]

    # values of any bias neurons in the key layer
    bias = {0: [1.0]}

    nn = NeuralNetwork(layers, bias)
    nn.connections = [random_matrix(a, b) for (a, b) in nn.get_matrix_dimensions()]

    nn.propagate_input([1, 0, 1])
