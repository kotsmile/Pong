from enum import Enum
import pygame

pygame.init()

X_MAX = 800
Y_MAX = 600

FPS = 20


class Side(Enum):
    LEFT = (0, Y_MAX * 0.5)
    RIGHT = (X_MAX, Y_MAX * 0.5)


class Action(Enum):
    NONE = 0
    UP = 1
    DOWN = 2


class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)


def draw_rect(surf, color, x, y, a, b):
    pygame.draw.rect(surf, color, [x, y, x + a, y + b])


class Player(object):
    PLAYER_VELOCITY = 10
    PLAYER_X_MAX = 10
    PLAYER_Y_MAX = 50

    def __init__(self, side):
        self.side = side
        self.x = self.side.value[0]
        self.y = self.side.value[1]
        self.velocity = 0
        self.score = 0
        self.v = 0

    def restart(self):
        self.x = self.side.value[0]
        self.y = self.side.value[1]
        self.velocity = 0
        self.score = 0
        self.v = 0

    def move(self, action):
        if action == Action.UP and self.y > 0:
            self.v = -self.PLAYER_VELOCITY
            self.y -= self.PLAYER_VELOCITY
        elif action == Action.DOWN and (self.y + self.PLAYER_Y_MAX) < X_MAX:
            self.v = self.PLAYER_VELOCITY
            self.y += self.PLAYER_VELOCITY
        elif action == Action.NONE:
            self.v = 0

    def draw(self, surface):
        if self.side == Side.RIGHT:
            draw_rect(surface, Color.BLACK.value, self.x - self.PLAYER_X_MAX, self.y, self.PLAYER_X_MAX, self.PLAYER_Y_MAX)
        else:
            draw_rect(surface, Color.BLACK.value, self.x - self.PLAYER_X_MAX, self.y, self.PLAYER_X_MAX,
                      self.PLAYER_Y_MAX)


class Ball(object):
    BALL_X_VELOCITY = 10
    BALL_X_MAX = 10
    BALL_Y_MAX = 10

    def __init__(self):
        self.x = X_MAX*0.5 - self.BALL_X_MAX*0.5
        self.y = Y_MAX*0.5 - self.BALL_Y_MAX*0.5
        self.v_x = self.BALL_X_VELOCITY
        self.v_y = 0
        self.goal = 0

    def restart(self):
        self.x = X_MAX * 0.5 - self.BALL_X_MAX * 0.5
        self.y = Y_MAX * 0.5 - self.BALL_Y_MAX * 0.5
        self.v_x = self.BALL_X_VELOCITY
        self.v_y = 0
        self.goal = 0

    def move(self):
        self.x += self.v_x
        self.y += self.v_y
        if self.x <= 0:
            self.goal = Side.LEFT
        elif self.x >= X_MAX:
            self.goal = Side.RIGHT

    def collide(self, players):
        for p in players:
            if p.side == Side.LEFT:
                if (p.x + p.PLAYER_X_MAX) >= self.x and p.y <= self.y <= (p.y + p.PLAYER_Y_MAX):
                    self.v_x *= -1
                    self.v_y += p.v
            elif p.side == Side.RIGHT:
                if p.x <= (self.x + self.BALL_X_MAX) and p.y <= self.y <= (p.y + p.PLAYER_Y_MAX):
                    self.v_x *= -1
                    self.v_y += p.v
        if self.y + self.BALL_Y_MAX >= X_MAX or self.y <= 0:
            self.v_y *= -1

    def draw(self, surface):
        draw_rect(surface, Color.RED.value, self.x, self.y, self.BALL_X_MAX, self.BALL_Y_MAX)


class PongGame(object):

    def __init__(self, graphic=False):
        self.graphic = graphic
        self.player_left = Player(Side.LEFT)
        self.player_right = Player(Side.RIGHT)
        self.ball = Ball()
        self.running = True
        self.timer = 0
        self.end_score = 11

        if graphic:
            self.screen = pygame.display.set_mode((X_MAX, Y_MAX), 0, 32)
            self.surface = pygame.Surface(self.screen.get_size())
            self.surface = self.surface.convert()
            self.surface.fill(Color.WHITE.value)

            self.screen.blit(self.surface, (0, 0))
            self.FPS = FPS
            self.fpsClock = pygame.time.Clock()
            self.fpsClock.tick(self.FPS)

    def draw(self):
        self.surface.fill(Color.WHITE.value)

        self.player_left.draw(self.surface)
        self.player_right.draw(self.surface)
        self.ball.draw(self.surface)

        font = pygame.font.Font("fonts/opensans.ttf", 36)
        text = font.render('{0} : {1}'.format(str(self.player_left.score), str(self.player_right.score)), 1, Color.BLACK.value)
        textpos = text.get_rect()
        textpos.centerx = 20
        self.surface.blit(text, textpos)
        self.screen.blit(self.surface, (X_MAX // 2, 0))

        pygame.display.update()
        self.fpsClock.tick(self.FPS)

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

        if self.player_left.score >= self.end_score or self.player_right.score >= self.end_score:
            self.running = False

        if self.graphic:
            self.draw()




