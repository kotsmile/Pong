from commands import commands


def core():
    while True:
        request = input('> ').split(' ')
        try:
            for c in commands:
                if c.check(request):
                    break
        except IndexError:
            print('Incorrect request. Please try again.')


if __name__ == '__main__':
    core()
