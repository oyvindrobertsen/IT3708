from __future__ import division, print_function
from ctrnn.neural_network import Neuron as N, BiasNeuron as B, NeuralNetwork


if __name__ == "__main__":
    nn = NeuralNetwork((
        (N(), N(), N(), N(), N(), B(1.0)),
        (N(), N(), B(1.0)),
        (N(), N())
    ))
    print(nn.get_phenotype_size())
    # btw = BeerTrackerWorld(30, 15, wrap=True)
    # btw.new_falling_object()
    # btw.terminal_print()
    # BeerTrackerGUI(btw, actions=[
    # (LEFT, 4),
    #     (LEFT, 1),
    #     (PULL, None)
    # ])