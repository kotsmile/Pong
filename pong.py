from commands import commands


def core():

    while True:
        request = input('> ').split(' ')

        for c in commands:
            if c.check(request):
                break



if __name__ == '__main__':
    core()
