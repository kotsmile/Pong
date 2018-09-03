import pygame
from collections import namedtuple
from pygame.locals import *



pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

WIDTH = 600
HEIGHT = 400

V = namedtuple('Coordinates', ['x', 'y'])

LEFT_SIDE = V(0, HEIGHT // 2)
RIGHT_SIDE = V(WIDTH, HEIGHT // 2) #see position

ACTION_NONE = 'none'
ACTION_UP = 'up'
ACTION_DOWN = 'down'


def draw_rect(surf, color, x1, y1, x2, y2):
    r = pygame.Rect((x1, y1), ((x2-x1), (y2-y1)))
    pygame.draw.rect(surf, color, r)


class Player(object):
    PLAYER_VELOCITY = 10
    PLAYER_WIDTH = 10
    PLAYER_HEIGHT = 50

    def __init__(self, side):
        self.side = side
        self.x = self.side.x
        self.y = self.side.y
        self.v = 0
        self.score = 0

    def restart(self):
        pass

    def move(self, action):
        pass

    def draw(self, surface):
        if self.side == LEFT_SIDE:
            draw_rect(surface, BLACK, self.x, self.y - self.PLAYER_HEIGHT // 2, self.x + self.PLAYER_WIDTH, self.y + self.PLAYER_HEIGHT // 2)
        if self.side == RIGHT_SIDE:
            draw_rect(surface, BLACK, self.x - self.PLAYER_WIDTH, self.y - self.PLAYER_HEIGHT // 2, self.x, self.y + self.PLAYER_HEIGHT // 2)


class Ball(object):
    BALL_VELOCITY = 10
    BALL_SIZE = 10

    def __init__(self):
        self.x = WIDTH*0.5 - self.BALL_SIZE
        self.y = HEIGHT*0.5 - self.BALL_SIZE
        self.v_x = self.BALL_VELOCITY
        self.v_y = 0
        self.goal = 0

    def restart(self):
        self.__init__()

    def move(self):
        pass

    def collide(self, p1, p2):
        pass

    def draw(self, surface):
        draw_rect(surface, RED, self.x, self.y, self.x + self.BALL_SIZE, self.y + self.BALL_SIZE)


class PongGame(object):

    def __init__(self):
        self.shape = [2, 6, 1]

    def new(self, g=False):
        self.player_left = Player(LEFT_SIDE)
        self.player_right = Player(RIGHT_SIDE)
        self.ball = Ball()
        self.timer = 0
        self.running = True
        self.g = g
        if self.g:
            self.g_init()

    def g_init(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        self.surface = pygame.Surface(self.screen.get_size())
        self.surface = self.surface.convert()
        self.surface.fill(WHITE)

        self.screen.blit(self.surface, (0, 0))
        self.FPS = 20
        self.fpsClock = pygame.time.Clock()
        self.fpsClock.tick(self.FPS)

    def draw(self):
        self.surface.fill(WHITE)
        self.player_left.draw(self.surface)
        self.player_right.draw(self.surface)
        self.ball.draw(self.surface)

        self.screen.blit(self.surface, (0, 0))
        pygame.display.flip()
        pygame.display.update()

    def next(self, a1, a2):

        self.timer += 1
        self.player_right.move(a1)
        self.player_left.move(a1)
        self.ball.move()
        self.ball.collide(self.player_left, self.player_right)

        if self.g:
            self.draw()

