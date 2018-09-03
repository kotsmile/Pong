from enum import Enum
from collections import namedtuple
import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600

FPS = 20

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


def draw_rect(surf, color, x1, y1, x2, y2):
    r = pygame.Rect((x1, y1), (x2, y2))
    pygame.draw.rect(surf, color, r)


def draw_ellipse(surf, color, x, y, a, b):
    r = pygame.Rect((x, y), (x + a, y + b))
    pygame.draw.ellipse(surf, color, r)


class Player(object):
    PLAYER_VELOCITY = 10
    PLAYER_WIDTH = 10
    PLAYER_HEIGHT = 50

    def __init__(self, side):
        self.side = side
        self.x = self.side.value.x
        self.y = self.side.value.y
        self.velocity = 0
        self.score = 0
        self.v = 0

    def restart(self):
        self.x = self.side.value.x
        self.y = self.side.value.y
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
        draw_rect(surface, Color.BLACK, self.x, self.y, self.x + self.PLAYER_WIDTH, self.y + self.PLAYER_HEIGHT)


class Ball(object):
    BALL_X_VELOCITY = 10
    BALL_WIDTH = 10
    BALL_HEIGHT = 10

    def __init__(self):
        self.x = WIDTH*0.5 - self.BALL_WIDTH*0.5
        self.y = HEIGHT*0.5 - self.BALL_HEIGHT*0.5
        self.v_x = self.BALL_X_VELOCITY
        self.v_y = 0
        self.goal = 0

    def restart(self):
        self.x = WIDTH * 0.5 - self.BALL_WIDTH * 0.5
        self.y = HEIGHT * 0.5 - self.BALL_HEIGHT * 0.5
        self.v_x = self.BALL_X_VELOCITY
        self.v_y = 0
        self.goal = 0

    def move(self):
        self.x += self.v_x
        self.y += self.v_y
        if self.x <= 0:
            self.goal = Side.LEFT
        elif self.x >= WIDTH:
            self.goal = Side.RIGHT

    def collide(self, players):
        for p in players:
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

    def draw(self, surface):
        draw_ellipse(surface, Color.RED, self.x, self.y, self.BALL_WIDTH, self.BALL_HEIGHT)


class PongGame(object):

    def __init__(self, graphic=True):
        self.graphic = graphic
        self.player_left = Player(Side.LEFT)
        self.player_right = Player(Side.RIGHT)
        self.ball = Ball()
        self.running = True
        self.timer = 0
        self.end_score = 10

        if graphic:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
            self.surface = pygame.Surface(self.screen.get_size())
            self.surface = self.surface.convert()
            self.surface.fill(Color.WHITE)

            self.screen.blit(self.surface, (0, 0))
            self.FPS = FPS
            self.fpsClock = pygame.time.Clock()
            self.fpsClock.tick(self.FPS)

    def draw(self):
        self.surface.fill(Color.WHITE)

        self.player_left.draw(self.surface)
        self.player_right.draw(self.surface)
        self.ball.draw(self.surface)

        font = pygame.font.Font("fonts/opensans.ttf", 36)
        text = font.render('{0} : {1}'.format(str(self.player_left.score), str(self.player_right.score)), 1, Color.BLACK)
        textpos = text.get_rect()
        textpos.centerx = 20
        self.surface.blit(text, textpos)
        self.screen.blit(self.surface, (WIDTH // 2, 0))

        pygame.display.flip()
        pygame.display.update()
        # self.fpsClock.tick(self.FPS + self.score / 2)

    def next(self, action1, action2):

        self.timer += 1

        self.player_left.move(action1)
        self.player_right.move(action2)
        self.ball.move()
        self.ball.collide([self.player_left, self.player_right])

        if self.ball.goal != 0:
            if self.ball.goal == Side.LEFT:
                self.player_left.score += 1
            elif self.ball.goal == Side.RIGHT:
                self.player_right.score += 1

            self.player_right.restart()
            self.player_left.restart()
            self.ball.restart()
                
        if self.graphic:
            self.draw()




