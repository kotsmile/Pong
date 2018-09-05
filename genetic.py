import numpy as np
import network

BASE = 10


def crypt(n):
    if n < 0:
        return '1' + bin(int(n * 10 ** BASE))[3:]
    return '0' + bin(int(n * 10 ** BASE))[2:]


def decrypt(a):
    if a[0] == '1':
        return -float(int(a[1:], 2)) / 10 ** BASE
    return float(int(a[1:], 2)) / 10 ** BASE


class Brain(object):

    def __init__(self, shape):
        self.nn = network.NeuralNetwork(shape)

    def get_dna(self):
        w_dna = ''
        for layers in self.nn.weights:
            for r in layers:
                for w in r:
                    w_dna += '|' + crypt(w)

        b_dna = ''
        for layers in self.nn.biases:
            for r in layers:
                for b in r:
                    b_dna += '|' + crypt(b)

        return w_dna + 'I' + b_dna

    def set_dna(self, dna):
        dna = dna.split('I')
        w_dna = dna[0]
        b_dna = dna[1]
        nn = network.NeuralNetwork(self.nn.shape)
    
