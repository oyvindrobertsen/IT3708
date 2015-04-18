from __future__ import print_function, division

import numpy as np

from utils import sigmoid, tuplize


class BaseNeuron:
    def __init__(self, activation):
        self.y = activation

    def input(self, value):
        raise NotImplementedError()

    @property
    def output(self):
        return self.y


class Neuron(BaseNeuron):
    def __init__(self):
        BaseNeuron.__init__(self, None)
        self.prev_y = 0
        self.s = None

        self.t = None
        self.g = None

    def input(self, value):
        assert self.t is not None
        assert self.g is not None

        self.s = value
        self.prev_y = self.y
        self.y = (self.prev_y + self.dy)

    @property
    def dy(self):
        return (1 / self.t) * (-self.prev_y + self.s)

    @property
    def output(self):
        return sigmoid(self.g * self.y)


class BiasNeuron(BaseNeuron):
    pass


class NeuralNetwork:
    def __init__(self, layers):
        assert len(layers) >= 2

        self.layers = layers
        self.cross_connections = None
        self.inter_connections = None

    def neuron_count(self, layer_no):
        return (
            sum(isinstance(neuron, Neuron) for neuron in self.layers[layer_no]),
            sum(isinstance(neuron, BiasNeuron) for neuron in self.layers[layer_no])
        )

    def get_phenotype_size(self):
        return {
            'cross': [
                (sum(self.neuron_count(i)), self.neuron_count(i + 1)[0]) for i in xrange(len(self.layers) - 1)
            ],
            'inter': [
                tuplize(self.neuron_count(i)[0]) for i in xrange(1, len(self.layers))
            ],
            'neurons': sum(self.neuron_count(i)[0] for i in xrange(len(self.layers)))
        }

    def set_layer(self, layer_no, values):
        for i, value in enumerate(values):
            self.layers[layer_no][i].activation = value

    def get_layer_values(self, layer_no):
        return np.array([n.output for n in self.layers[layer_no]])

    def propagate_input(self, values):
        """
        takes input values, forward propagates them through the network
        and returns the activation values for the output layer
        """
        assert self.cross_connections is not None
        assert len(values) == self.neuron_count(0)[0]

        self.set_layer(0, values)

        for layer_no in xrange(len(self.layers) - 1):
            a = self.get_layer_values(layer_no)
            b = self.cross_connections[layer_no]
            cross_sum = a.dot(b)

            c = self.get_layer_values(layer_no + 1)
            d = self.inter_connections[layer_no]  # no inter connections for layer 0, so no +1
            inter_sum = c.dot(d)

            self.set_layer(layer_no + 1, np.add(cross_sum, inter_sum))

        return self.layers[-1]
