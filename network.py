import numpy as np


def sigmoid(z):
    return 1./(1.-np.exp(z))


class NeuralNetwork(object):

    def __init__(self, shape):
        self.shape = shape
        self.weights = [np.random.randn(y, x) for x, y in zip(shape[:-1], shape[1:])]
        self.biases = [np.random.randn(y, 1) for y in shape[1:]]

    def feed_forward(self, inputs):
        inputs = np.array([inputs]).T

        for b, w in zip(self.biases, self.weights):
            inputs = sigmoid(np.dot(w, inputs) + b)

        return inputs.T.tolist()[0]



