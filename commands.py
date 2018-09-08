import pong_play
import genetic
import pong_game
import network



class Command(object):

    def __init__(self, call, description, execute, param=None,ignore=False):
        self.call = call
        self.description = description
        self.execute = execute
        self.ignore = ignore
        self.param = param

    def check(self, line):
        if line[0] == self.call or self.ignore:
            if self.param:
                line = line[1:]
                args = {}
                for p in self.param:
                    if p in line:
                        i = line.index(p)
                        args[p] = line[i + 1]
                    else:
                        args[p] = self.param[p]



                self.execute(args)
            else:
                self.execute()
            return True
        return False


def quary(line):
    line = line.split(' ')
    try:
        for c in commands:
            if c.check(line):
                break
    except IndexError:
        print('Incorrect request. Please try again.')


commands = []

commands.append(Command('play', 'Start the Pong for two players', lambda p: pong_play.play(master=bool(p['-m'])), param={'-m': False}))
commands.append(Command('genetic', 'Start genetic algorithm',
                        lambda args: genetic.Population(int(args['-s']), pong_game.PongGame(), 100000000,
                                                        [2, int(args['-n']), 3], max_generation=int(args['-mg']),
                                                        mutate_rate=float(args['-mr']), graph=bool(args['-g'])),
                        param={'-s': 10, '-n': 10, '-mg': 5, '-mr': 0.05, '-g' : False}))

commands.append((Command('s', 'short cut', lambda: quary('genetic -s 500 -n 20 -mg 20 -mr 0.08'))))

commands.append(Command('ai', 'Play vs AI', lambda p: pong_play.ai_start(p['-f']), param={'-f': None}))
commands.append(Command('list', 'Show list of commands',
                        lambda: [print(i.call + '\t' + i.description) for i in commands]))
commands.append(Command('', '', lambda: print('Can\'t recognize request'), ignore=True))