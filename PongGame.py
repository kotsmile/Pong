import pygame
from collections import namedtuple
import time

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

WIDTH = 600
HEIGHT = 400

V = namedtuple('Coordinates', ['x', 'y'])

PHEIGHT = 80
LEFT_SIDE = V(0, HEIGHT // 2 - PHEIGHT // 2)
RIGHT_SIDE = V(WIDTH, HEIGHT // 2 - PHEIGHT // 2)  # see position

ACTION_NONE = 'none'
ACTION_UP = 'up'
ACTION_DOWN = 'down'


def draw_rect(surf, color, x1, y1, x2, y2):
    r = pygame.Rect((x1, y1), ((x2 - x1), (y2 - y1)))
    pygame.draw.rect(surf, color, r)


def draw_ellipse(surf, color, x1, y1, x2, y2):
    r = pygame.Rect((x1, y1), ((x2 - x1), (y2 - y1)))
    pygame.draw.ellipse(surf, color, r)


class Player(object):
    PLAYER_VELOCITY = 10
    PLAYER_WIDTH = 10
    PLAYER_HEIGHT = 100

    def __init__(self, side):
        self.side = side
        self.x = self.side.x
        self.y = self.side.y
        self.v = 0
        self.score = 0

    def restart(self):
        score = self.score
        self.__init__(self.side)
        self.score = score

    def move(self, action):
        if action == ACTION_UP and self.y > 0:
            self.v = -self.PLAYER_VELOCITY
            self.y -= self.PLAYER_VELOCITY
        elif action == ACTION_DOWN and (self.y + self.PLAYER_HEIGHT) < HEIGHT:
            self.v = self.PLAYER_VELOCITY
            self.y += self.PLAYER_VELOCITY
        elif action == ACTION_NONE:
            self.v = 0

    def draw(self, surface):
        if self.side == LEFT_SIDE:
            draw_rect(surface, BLACK, self.x, self.y, self.x + self.PLAYER_WIDTH, self.y + self.PLAYER_HEIGHT)
        if self.side == RIGHT_SIDE:
            draw_rect(surface, BLACK, self.x - self.PLAYER_WIDTH, self.y, self.x, self.y + self.PLAYER_HEIGHT)


class Ball(object):
    BALL_VELOCITY = 5
    BALL_SIZE = 15

    def __init__(self, side):
        self.side = side
        self.x = WIDTH * 0.5 - self.BALL_SIZE // 2
        self.y = HEIGHT * 0.5 - self.BALL_SIZE // 2
        if self.side == RIGHT_SIDE:
            self.v_x = -self.BALL_VELOCITY
        elif self.side == LEFT_SIDE:
            self.v_x = self.BALL_VELOCITY
        self.v_y = 0
        self.goal = 0

    def restart(self):
        self.__init__(self.goal)

    def move(self):
        self.x += self.v_x
        self.y += self.v_y
        if self.x <= -2 * self.BALL_SIZE:
            self.goal = LEFT_SIDE
        elif self.x >= WIDTH + self.BALL_SIZE:
            self.goal = RIGHT_SIDE

    def collide(self, *players):
        for p in players:
            if p.side == LEFT_SIDE:
                if (p.x + p.PLAYER_WIDTH) >= self.x and (p.y + p.PLAYER_HEIGHT) > self.y > (p.y - self.BALL_SIZE):
                    self.v_x *= -1
                    self.v_y += p.v // 2
            elif p.side == RIGHT_SIDE:
                if p.x - p.PLAYER_WIDTH <= (self.x + self.BALL_SIZE) and (p.y + p.PLAYER_HEIGHT) > self.y > (
                        p.y - self.BALL_SIZE):
                    self.v_x *= -1
                    self.v_y += p.v // 2

        if self.y + self.BALL_SIZE >= HEIGHT or self.y <= 0:
            self.v_y *= -1

    def draw(self, surface):
        draw_ellipse(surface, RED, self.x, self.y, self.x + self.BALL_SIZE, self.y + self.BALL_SIZE)


class PongGame(object):

    def __init__(self):
        self.shape = [2, 6, 1]

    def new(self, g=False):
        self.player_left = Player(LEFT_SIDE)
        self.player_right = Player(RIGHT_SIDE)
        self.ball = Ball(LEFT_SIDE)
        self.timer = 0
        self.running = True
        self.end_score = 11
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

        font = pygame.font.Font("fonts/opensans.ttf", 36)
        text = font.render('{1} : {0}'.format(str(self.player_left.score), str(self.player_right.score)), 1,
                           BLACK)
        textpos = text.get_rect()
        self.surface.blit(text, textpos)

        self.screen.blit(self.surface, (0, 0))
        pygame.display.flip()
        pygame.display.update()

    def next(self, a1, a2):

        if self.g:
            self.draw()

        self.timer += 1
        self.ball.collide(self.player_left, self.player_right)
        self.player_left.move(a1)
        self.player_right.move(a2)
        self.ball.move()

        if self.ball.goal != 0:
            if self.g:
                time.sleep(0.5)

            if self.ball.goal == LEFT_SIDE:
                self.player_left.score += 1
            elif self.ball.goal == RIGHT_SIDE:
                self.player_right.score += 1

            if self.player_left.score >= self.end_score or self.player_right.score >= self.end_score:
                self.running = False

            self.player_right.restart()
            self.player_left.restart()
            self.ball.restart()
