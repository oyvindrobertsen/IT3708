import random
import math

random.seed(0)


def sigmoid(x):
    return math.tanh(x)


def dsigmoid(y):
    return 1.0 - y**2


def make_matrix(I, J, fill=0.0):
    ret = []
    for i in range(I):
        ret.append([fill] * J)
    return ret


class NeuralNetwork(object):
    '''
    TODO: Support more than one hidden layer? More nodetypes?
    '''
    def __init__(self, n_input, n_hidden, n_output):
        self.n_input = n_input + 1 # bias node
        self.n_hidden = n_hidden
        self.n_output = n_output

        self.i_node_activations = [1.0] * self.n_input
        self.h_node_activations = [1.0] * self.n_hidden
        self.o_node_activations = [1.0] * self.n_output

        self.i_weights = make_matrix(self.n_input, n_hidden)
        self.o_weights = make_matrix(self.n_hidden, n_output)

        for i in range(self.n_input):
            for j in range(self.n_hidden):
                self.i_weights[i][j] = random.uniform(-0.2, 0.2)

        for i in range(self.n_hidden):
            for j in range(self.n_output):
                self.o_weights[i][j] = random.uniform(-2.0, 2.0)

        self.i_change = make_matrix(self.n_input, self.n_hidden)
        self.o_change = make_matrix(self.n_hidden, self.n_output)


    def update(self, inputs):
        if len(inputs) != self.n_input - 1:
            raise ValueError, 'wrong number of inputs'

        # Input layer
        for i in range(self.n_input - 1):
            self.i_node_activations[i] = inputs[i]

        # Hidden layer
        for i in range(self.n_hidden):
            total = 0.0
            for j in range(self.n_input):
                total = total + self.i_node_activations[j] * self.i_weights[j][i]
            self.h_node_activations[i] = sigmoid(total)

        # Output layer
        for i in range(self.n_output):
            total = 0.0
            for j in range(self.n_hidden):
                total = total + self.h_node_activations[j] * self.o_weights[j][i]
            self.o_node_activations[i] = sigmoid(total)

        return self.o_node_activations[:]


    def back_propagate(self, targets, N, M):
        if len(targets) != self.n_output:
            raise ValueError, 'wrong number of target values'

        # Error terms for output layer
        output_deltas = [0.0] * self.n_output
        for i in range(self.n_output):
            error = targets[i] - self.o_node_activations[i]
            output_deltas[i] = dsigmoid(self.o_node_activations[i]) * error

        # Error terms for hidden layer
        hidden_deltas = [0.0] * self.n_hidden
        for i in range(self.n_hidden):
            error = 0.0
            for j in range(self.n_output):
                error = error + output_deltas[j] * self.o_weights[i][j]
            hidden_deltas[i] = dsigmoid(self.h_node_activations[i]) * error

        # Update output weights
        for i in range(self.n_hidden):
            for j in range(self.n_output):
                change = output_deltas[j] * self.h_node_activations[i]
                self.o_weights[i][j] = self.o_weights[i][j] + N * change + M * self.o_change[i][j]
                self.o_change[i][j] = change

        # Update input weights
        for i in range(self.n_input):
            for j in range(self.n_hidden):
                change = hidden_deltas[j] * self.i_node_activations[i]
                self.i_weights[i][j] = self.i_weights[i][j] + N * change + M * self.i_change[i][j]
                self.i_change[i][j] = change

        error = 0.0
        for i in range(len(targets)):
            error = error + 0.5 * (targets[i] - self.o_node_activations[i])**2
        return error


    def test(self, patterns):
        for p in patterns:
            print p[0], ' -> ', self.update(p[0])


    def weights(self):
        print 'Input weights:'
        for weight in self.i_weights:
            print weight
        print
        print 'Output weights:'
        for weight in self.o_weights:
            print weight


    def train(self, patterns, iterations=1000, N=0.5, M=0.1):
        # N: learning rate
        # M: momentum factor
        for i in range(iterations):
            error = 0.0
            for p in patterns:
                inputs = p[0]
                targets = p[1]
                self.update(inputs)
                error = error + self.back_propagate(targets, N, M)

def demo():
    # Teach network XOR function
    pat = [
        [[0,0], [0]],
        [[0,1], [1]],
        [[1,0], [1]],
        [[1,1], [0]]
    ]

    # create a network with two input, two hidden, and one output nodes
    n = NeuralNetwork(2, 2, 1)
    # train it with some patterns
    n.train(pat)
    # test it
    n.test(pat)



if __name__ == '__main__':
    demo()
