import network
import random
import pong_game

BASE = 10
BOLD = '\033[1m'
END = '\033[0m'


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
        return self

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

    def __init__(self, size, game, goal, shape, mutate_rate=0.01, graph=False):

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

    def demo(self, brain1, brain2, once=False):
        if once:
            self.game.new(g=True)
            while self.game.running:
                data_left = self.game.get_data(pong_game.LEFT_SIDE)
                data_right = self.game.get_data(pong_game.RIGHT_SIDE)
                self.game.next(brain1.ask(data_left), brain2.ask(data_right))
        else:
            while True:
                self.game.new(g=True)
                while self.game.running:
                    data_left = self.game.get_data(pong_game.LEFT_SIDE)
                    data_right = self.game.get_data(pong_game.RIGHT_SIDE)
                    self.game.next(brain1.ask(data_left), brain2.ask(data_right))

    def learn(self):

        while self.best_fitness <= self.goal:

            for b1, b2 in zip(self.brains, self.brains[::-1]):

                self.game.new()

                j = 0
                while self.game.running:

                    data_left = self.game.get_data(pong_game.LEFT_SIDE)
                    data_right = self.game.get_data(pong_game.RIGHT_SIDE)
                    self.game.next(b1.ask(data_left), b2.ask(data_right))
                    j += 1
                    if j > 100000:
                        self.game.running = False

                b1.fitness = self.game.timer*self.game.player_left.score
                b2.fitness = self.game.timer*self.game.player_right.score

            best_brain = None
            self.next_generation()
            if self.graph:
                for b in self.brains:
                    if b.fitness == self.best_fitness:
                        best_brain = b
                        break
                self.demo(best_brain, best_brain, once=True)

        print(BOLD + 'DONE!!!' + END)

        best_brain = None

        for b in self.brains:
            if b.fitness == self.best_fitness:
                best_brain = b
                break

        self.demo(best_brain, best_brain)

    def next_generation(self):

        self.generation += 1

        fitness_g = [b.fitness for b in self.brains]
        self.delta = max(fitness_g) - self.best_fitness
        self.best_fitness = max(fitness_g)

        for b in self.brains:
            if b.fitness == self.best_fitness:
                self.best_brain = b

        self.sum_of_fitness = sum(fitness_g)

        self.fitnesses.append(self.best_fitness)

        new_brains = [self.find_parent().child(self.find_parent()).mutate(self.mutate_rate) for _ in range(self.size)]

        self.brains = new_brains
        self.info()

    def find_parent(self):

        pick = self.sum_of_fitness * random.random()
        self.sum_of_fitness = 0

        for b in self.brains:

            self.sum_of_fitness += b.fitness

            if self.sum_of_fitness >= pick:
                return b




    def info(self):
        print('\n')
        print('+--------------' + BOLD + 'INFO' + END + '--------------+')
        print(BOLD + 'GENERATION: ' + END + str(self.generation))
        print(BOLD + 'BEST FITNESS: ' + END + str(max(self.fitnesses)))
        print(BOLD + 'FITNESS: ' + END + str(self.best_fitness))
        print(BOLD + 'DELTA: ' + END + str(self.delta))
        print('+--------------------------------+')