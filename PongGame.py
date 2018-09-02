from enum import Enum
from collections import namedtuple
import pygame


WIDTH = 800
HEIGHT = 600

V = namedtuple('Coordinates', ['x', 'y'])


class Side(Enum):
    LEFT = V(0, WIDTH * 0.5)
    RIGHT = V(HEIGHT, WIDTH * 0.5)


class Action(Enum):
    UP = 1
    DOWN = 2


class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)


def draw_box(surf, color, x1, y1, x2, y2):
    r = pygame.Rect((x1, y1), (x2, y2))
    pygame.draw.rect(surf, color, r)


class Player(object):
    PLAYER_VELOCITY = 10
    PLAYER_WIDTH = 10
    PLAYER_HEIGHT = 50

    def __init__(self, side):
        self.side = side
        self.x = side.value.x
        self.y = side.value.y
        self.velocity = 0
        self.score = 0
        self.v = 0

    def move(self, action):
        if action == Action.UP and self.y > 0:
            self.v = -self.PLAYER_VELOCITY
            self.y -= self.PLAYER_VELOCITY
        elif action == Action.DOWN and (self.y + self.PLAYER_HEIGHT) < WIDTH:
            self.v = self.PLAYER_VELOCITY
            self.y += self.PLAYER_VELOCITY
        else:
            self.v = 0

    def draw(self, surface):
        draw_box(surface, Color.BLACK, self.x, self.y, self.x + self.PLAYER_WIDTH, self.y + self.PLAYER_HEIGHT)


class Ball(object):
    BALL_X_VELOCITY = 10
    BALL_WIDTH = 10
    BALL_HEIGHT = 10

    def __init__(self):
        self.x = WIDTH * 0.5 - self.BALL_WIDTH * 0.5
        self.y = HEIGHT * 0.5 - self.BALL_HEIGHT * 0.5
        self.v_x = self.BALL_X_VELOCITY
        self.v_y = 0

    def move(self):
        self.x += self.v_x
        self.y += self.v_y

    def collide(self, player):
        for p in player:
            if p.side == Side.LEFT:
                if (p.x + p.PLAYER_WIDTH) >= self.x:
                    self.v_x *= -1
                    self.v_y += p.v
            elif p.side == Side.RIGHT:
                if p.x <= (self.x + self.BALL_WIDTH):
                    self.v_x *= -1
                    self.v_y += p.v
        if self.y + self.BALL_HEIGHT >= WIDTH or self.y <= 0:
            self.v_y *= -1
