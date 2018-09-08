import pong_game
import pygame
from pygame.locals import *
import genetic
import network

FPS = 1000


def play(master=False):

    game = pong_game.PongGame()
    game.new(g=True, master=master)
    game.FPS = 20

    while True:

        while game.running:

            action1 = pong_game.ACTION_NONE
            action2 = pong_game.ACTION_NONE

            if pygame.key.get_pressed()[K_w]:
                action1 = pong_game.ACTION_UP
            if pygame.key.get_pressed()[K_s]:
                action1 = pong_game.ACTION_DOWN
            if pygame.key.get_pressed()[K_UP]:
                action2 = pong_game.ACTION_UP
            if pygame.key.get_pressed()[K_DOWN]:
                action2 = pong_game.ACTION_DOWN

            for event in pygame.event.get():

                if event.type == QUIT:
                    return

            # elif event.type == KEYDOWN:
            #     if event.key == K_w:
            #         action1 = PongGame.ACTION_UP
            #     elif event.key == K_s:
            #         action1 = PongGame.ACTION_DOWN
            #     if event.key == K_UP:
            #         action2 = PongGame.ACTION_UP
            #     elif event.key == K_DOWN:
            #         action2 = PongGame.ACTION_DOWN

            game.next(action1, action2)

        game.new(g=True, master=master)


def play_vs_computer(brain):

    game = pong_game.PongGame()
    game.new(g=True)
    game.FPS = 20

    while True:

        while game.running:

            action1 = brain.ask(game.get_data(pong_game.LEFT_SIDE))
            action2 = pong_game.ACTION_NONE

            if pygame.key.get_pressed()[K_UP]:
                action2 = pong_game.ACTION_UP
            if pygame.key.get_pressed()[K_DOWN]:
                action2 = pong_game.ACTION_DOWN

            for event in pygame.event.get():

                if event.type == QUIT:
                    return

            # elif event.type == KEYDOWN:
            #     if event.key == K_w:
            #         action1 = PongGame.ACTION_UP
            #     elif event.key == K_s:
            #         action1 = PongGame.ACTION_DOWN
            #     if event.key == K_UP:
            #         action2 = PongGame.ACTION_UP
            #     elif event.key == K_DOWN:
            #         action2 = PongGame.ACTION_DOWN

            game.next(action1, action2)

        game.new(g=True)


def ai_start(file_name, master=False):
    shape = ''
    dna = ''
    with open('brains/' + file_name + '.txt', 'r') as f:
        s = f.read()
        s = s.split('R')
        shape = list(map(int, s[0].split('l')))
        dna = s[1]
    brain = genetic.Brain(network.NeuralNetwork(shape))
    brain.set_dna(dna)

    game = pong_game.PongGame()
    game.new(g=True, master=master)
    game.FPS = 20

    while True:

        while game.running:

            action1 = brain.ask(game.get_data(pong_game.LEFT_SIDE))
            action2 = pong_game.ACTION_NONE

            if pygame.key.get_pressed()[K_UP]:
                action2 = pong_game.ACTION_UP
            if pygame.key.get_pressed()[K_DOWN]:
                action2 = pong_game.ACTION_DOWN

            for event in pygame.event.get():

                if event.type == QUIT:
                    return

            # elif event.type == KEYDOWN:
            #     if event.key == K_w:
            #         action1 = PongGame.ACTION_UP
            #     elif event.key == K_s:
            #         action1 = PongGame.ACTION_DOWN
            #     if event.key == K_UP:
            #         action2 = PongGame.ACTION_UP
            #     elif event.key == K_DOWN:
            #         action2 = PongGame.ACTION_DOWN

            game.next(action1, action2)

        game.new(g=True)


def ai_master(brain):
    game = pong_game.PongGame()
    game.new(g=True, master=True)
    game.FPS = 20

    while game.running:

        action1 = pong_game.ACTION_NONE
        action2 = pong_game.ACTION_NONE

        if pygame.key.get_pressed()[K_w]:
            action1 = pong_game.ACTION_UP
        if pygame.key.get_pressed()[K_s]:
            action1 = pong_game.ACTION_DOWN
        if pygame.key.get_pressed()[K_UP]:
            action2 = pong_game.ACTION_UP
        if pygame.key.get_pressed()[K_DOWN]:
            action2 = pong_game.ACTION_DOWN

        for event in pygame.event.get():

            if event.type == QUIT:
                return

        # elif event.type == KEYDOWN:
        #     if event.key == K_w:
        #         action1 = PongGame.ACTION_UP
        #     elif event.key == K_s:
        #         action1 = PongGame.ACTION_DOWN
        #     if event.key == K_UP:
        #         action2 = PongGame.ACTION_UP
        #     elif event.key == K_DOWN:
        #         action2 = PongGame.ACTION_DOWN

        game.next(action1, action2)


