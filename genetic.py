import network
import random
import pong_game
import pygame
import pong_play
from pygame.locals import *

BASE = 10
BOLD = '\033[1m'
END = '\033[0m'

GAME = pong_game.PongGame()


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
        m = max(l)
        h = 100
        for j in range(len(l)):
            if l[j] == m:
                h = j

        return choice[h]

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
        dnaW = dna.split('I')
        w_dna = dnaW[0].split('|')
        b_dna = dnaW[1].split('|')
        i = 0
        for layers in self.nn.weights:
            for r in layers:
                for w in r:
                    w = decrypt(w_dna[i])
                    i += 1
        i = 0
        for layers in self.nn.biases:
            for r in layers:
                for b in r:
                    b = decrypt(b_dna[i])
                    i += 1


class Population(object):

    def __init__(self, size, game, goal, shape, mutate_rate=0.05, graph=False):

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
            for b1, b2 in zip(self.brains, self.brains[::-1]):

                self.game.new()

                j = 0
                while self.game.running:

                    data_left = self.game.get_data(pong_game.LEFT_SIDE)
                    data_right = self.game.get_data(pong_game.RIGHT_SIDE)
                    self.game.next(b1.ask(data_left), b2.ask(data_right))
                    j += 1
                    if j > 50000:
                        self.game.running = False

                b1.fitness = ((self.game.player_left.score**2-self.game.player_right.score)**2)*self.game.player_left.knock
                b2.fitness = ((self.game.player_left.score-self.game.player_right.score**2)**2)*self.game.player_right.knock
                i += 1
                #print(i)

            self.brains.sort(key=lambda a: a.fitness, reverse=True)
            print('demo')
            if self.graph:
                demo(self.brains[0], self.brains[1], once=True)

            if self.generation > 5:
                break
            self.next_generation()

        print(BOLD + 'DONE!!!' + END)

        self.brains.sort(key=lambda a: a.fitness, reverse=True)

        pong_play.play_vs_computer(self.brains[0])
        answer = input('Save this brain?[y/n]')
        if answer == 'y':
            name = input('Please write name')
            with open(name + '.txt', 'w') as f:
                f.write(self.brains[0].get_dna())


        #demo(self.brains[0], self.brains[1])

    def next_generation(self):

        self.generation += 1

        fitness_g = [b.fitness for b in self.brains]
        self.delta = max(fitness_g) - self.best_fitness
        self.best_fitness = max(fitness_g)

        self.brains.sort(key=lambda a: a.fitness, reverse=True)
        self.best_brain = self.brains[0]

        self.sum_of_fitness = sum(fitness_g)

        self.fitnesses.append(self.best_fitness)

        new_brains = [self.find_parent().child(self.find_parent()) for _ in range(self.size)]
        for b in new_brains:
            b.mutate(self.mutate_rate)

        self.brains = new_brains
        self.info()

    def find_parent(self):

        pick = self.sum_of_fitness * random.random()
        sum_of_fitness = 0

        for b in self.brains:

            sum_of_fitness += b.fitness

            if sum_of_fitness >= pick:
                return b

    def info(self):
        print('\n')
        print('+--------------' + BOLD + 'INFO' + END + '--------------+')
        print(BOLD + 'GENERATION: ' + END + str(self.generation))
        print(BOLD + 'BEST FITNESS: ' + END + str(max(self.fitnesses)))
        print(BOLD + 'FITNESS: ' + END + str(self.best_fitness))
        print(BOLD + 'DELTA: ' + END + str(self.delta))
        print('+--------------------------------+')