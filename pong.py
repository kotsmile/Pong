

def core():
    while True:
        request = input('> ').split(' ')
        try:
            if request[0] == 'play':
                import pong_play
                pong_play.play()
            else:
                print('Can\'t recognize request.')
        except IndexError:
            print('Incorrect request. Please try again.')


if __name__ == '__main__':
    core()
