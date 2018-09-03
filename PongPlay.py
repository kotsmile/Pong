import PongGame
import pygame
from pygame.locals import *
import sys

FPS = 1000


def play():

    game = PongGame.PongGame(graphic=True)
    game.FPS = 20
    pygame.key.set_repeat(1, 20)

    while game.running:

        action1 = PongGame.Action.NONE
        action2 = 0
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_w:
                    action1 = PongGame.Action.UP
                if event.key == K_s:
                    action1 = PongGame.Action.DOWN
                if event.key == K_UP:
                    action2 = PongGame.Action.UP
                if event.key == K_DOWN:
                    action2 = PongGame.Action.DOWN

        game.next(action1, action2)

    play()
