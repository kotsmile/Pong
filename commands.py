import pong_play
import genetic
import pong_game

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


def l_c():
    for i in commands:
        print(i.call + '\t' + i.description)


commands = []

commands.append(Command('play', 'Start the Pong for two players', lambda: pong_play.play()))
commands.append(Command('genetic', 'Start genetic algorithm', lambda: genetic.Population(20, pong_game.PongGame(), 10000, [3, 20, 3], graph=True)))
commands.append(Command('list', 'Show list of commands', l_c))
commands.append(Command('', '', lambda: print('Can\'t recognize request'), ignore=True))