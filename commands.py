import pong_play
import genetic
import pong_game
import network



class Command(object):

    def __init__(self, call, description, execute, ignore=False):
        self.call = call
        self.description = description
        self.execute = execute
        self.ignore = ignore

    def check(self, line):
        if line[0] == self.call or self.ignore:
            if len(line) > 1:
                self.execute(line[1:])
            else:
                self.execute()
            return True
        return False


commands = []
b = genetic.Brain(network.NeuralNetwork([2, 10, 3]))

commands.append(Command('play', 'Start the Pong for two players', lambda: pong_play.play()))
commands.append(Command('genetic', 'Start genetic algorithm',
                        lambda: genetic.Population(50, pong_game.PongGame(), 100000000, [2, 10, 3], mutate_rate=0.05, graph=True)))

commands.append(Command('test', 'none', lambda: pong_play.play_vs_computer(b)))
commands.append(Command('list', 'Show list of commands',
                        lambda: [print(i.call + '\t' + i.description) for i in commands]))
commands.append(Command('', '', lambda: print('Can\'t recognize request'), ignore=True))