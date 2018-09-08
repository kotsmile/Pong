import network
import random
import pong_game
import pygame
import pong_play
from pygame.locals import *
import numpy as np

BASE = 9
BOLD = '\033[1m'
END = '\033[0m'

GAME = pong_game.PongGame()


def save_brain(brain, file_name):
    with open('brains/' + file_name + '.txt', 'w') as f:
        f.write('l'.join(list(map(str, brain.nn.shape))) + 'R' + brain.get_dna())


def demo(b1, b2, once=False):
    GAME.new(g=True)

    while GAME.running:

        a1 = b1.ask(GAME.get_data(pong_game.LEFT_SIDE))
        a2 = b2.ask(GAME.get_data(pong_game.RIGHT_SIDE))
        GAME.next(a1, a2)
        for event in pygame.event.get():

            if event.type == QUIT:
                return

            else:
                pass

    if not once:
        demo(b1, b2, once=False)


def crypt(n):
    if n < 0:
        return '1' + bin(int(n * 10 ** BASE))[3:]
    return '0' + bin(int(n * 10 ** BASE))[2:]


def decrypt(a):
    if a[0] == '1':
        return -float(int(a[1:], 2)) / 10 ** BASE
    return float(int(a[1:], 2)) / 10 ** BASE


class Brain(object):

    def __init__(self, nn):
        self.nn = nn
        self.fitness = 0

    def ask(self, data):
        choice = {0: pong_game.ACTION_NONE, 1: pong_game.ACTION_UP, 2: pong_game.ACTION_DOWN}
        l = self.nn.feed_forward(data)

        return choice[l.index(max(l))]

    def mutate(self, mutate_rate):
        dna = self.get_dna()
        new_dna = ''
        change = {'1': '0', '0': '1', '|': '|', 'I': 'I'}
        for n in dna:
            if random.random() <= mutate_rate:
                new_dna += change[n]
            else:
                new_dna += n
        self.set_dna(new_dna)

    def child(self, another_brain):
        baby = Brain(self.nn)
        baby.set_dna(self.get_dna().split('I')[0] + 'I' + another_brain.get_dna().split('I')[1])
        return baby

    def copy(self):
        return Brain(self.nn)

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
        return w_dna[1:] + 'I' + b_dna[1:]

    def set_dna(self, dna):
        dna = dna.split('I')
        w_dna = list(map(decrypt, dna[0].split('|')))
        b_dna = list(map(decrypt, dna[1].split('|')))
        i = 0
        n_w = []
        for layers in self.nn.weights:
            p = []
            for r in layers:
                h = []
                for _ in r:
                    h.append(w_dna[i])
                    i += 1
                p.append(h)
            n_w.append(np.array(p))

        i = 0
        n_b = []
        for layers in self.nn.biases:
            p = []
            for r in layers:
                h = []
                for _ in r:
                    h.append(b_dna[i])
                    i += 1
                p.append(h)
            n_b.append(np.array(p))
        self.nn.weights = n_w
        self.nn.biases = n_b



class Population(object):

    def __init__(self, size, game, goal, shape, max_generation=10, mutate_rate=0.05, graph=False):

        self.max_generation = max_generation
        self.graph = graph
        self.size = size
        self.mutate_rate = mutate_rate
        self.best_fitness = 0
        self.best_generation = 'none'
        self.generation = 0
        self.fitnesses = []
        self.brains = [Brain(network.NeuralNetwork(shape)) for _ in range(size)]
        self.game = game
        self.goal = goal
        self.learn()

    def learn(self):

        while self.best_fitness <= self.goal:
            i = 0
            for b in self.brains:

                self.game.new(master=True)


                j = 0
                while self.game.running:

                    self.game.next(b.ask(self.game.get_data(pong_game.LEFT_SIDE)))
                    j += 1
                    if j > 100000:
                        self.game.running = False

                b.fitness = self.game.player_left.knock
                i += 1
                pong_play.ai_master(b)
                print(i)

            self.brains.sort(key=lambda a: a.fitness, reverse=True)
            if self.graph:
                demo(self.brains[0], self.brains[0], once=True)

            if self.generation >= self.max_generation:
                break
            self.next_generation()

        print(BOLD + 'DONE!!!' + END)

        self.brains.sort(key=lambda a: a.fitness, reverse=True)

        pong_play.play_vs_computer(self.brains[0])
        answer = input('Save this brain?[y/n]: ')
        if answer == 'y':
            name = input('Please write name: ')
            save_brain(self.brains[0], name)


        #demo(self.brains[0], self.brains[1])

    def next_generation(self):

        self.generation += 1

        fitness_g = [b.fitness for b in self.brains]
        delta = max(fitness_g) - self.best_fitness
        self.best_fitness = max(fitness_g)

        self.brains.sort(key=lambda a: a.fitness, reverse=True)
        self.best_brain = self.brains[0]
        save_brain(self.best_brain, 'gen' + str(self.generation) + '_fit' + str(self.best_fitness))

        self.sum_of_fitness = sum(fitness_g)

        self.fitnesses.append(self.best_fitness)

        new_brains = [self.find_parent() for _ in range(self.size)]
        #new_brains = [self.find_parent().child(self.find_parent()) for _ in range(self.size)]
        for b in new_brains:
            b.mutate(self.mutate_rate)

        self.brains = new_brains
        self.info(delta)

    def find_parent(self):

        pick = self.sum_of_fitness * random.random()
        sum_of_fitness = 0

        for b in self.brains:

            sum_of_fitness += b.fitness

            if sum_of_fitness >= pick:
                return b

    def info(self, delta):
        print('\n')
        print('+--------------' + BOLD + 'INFO' + END + '--------------+')
        print(BOLD + 'GENERATION: ' + END + str(self.generation))
        print(BOLD + 'BEST FITNESS: ' + END + str(max(self.fitnesses)))
        print(BOLD + 'FITNESS: ' + END + str(self.best_fitness))
        print(BOLD + 'DELTA: ' + END + str(delta))
        print('+--------------------------------+')

