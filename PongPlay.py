import PongGame
import pygame
from pygame.locals import *
import sys

FPS = 1000


def play():

    game = PongGame.PongGame()
    game.new(g=True)
    game.FPS = 20
    pygame.key.set_repeat(1, 20)

    while True:

        while game.running:

            action1 = PongGame.ACTION_NONE
            action2 = 0
            for event in pygame.event.get():

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == KEYDOWN:
                    if event.key == K_w:
                        action1 = PongGame.ACTION_UP
                    if event.key == K_s:
                        action1 = PongGame.ACTION_DOWN
                    if event.key == K_UP:
                        action2 = PongGame.ACTION_UP
                    if event.key == K_DOWN:
                        action2 = PongGame.ACTION_DOWN

            game.next(action1, action2)

        game.new(g=True)


