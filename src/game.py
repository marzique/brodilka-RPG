import pygame
import random

from pygame import DOUBLEBUF, QUIT
from pygame.constants import HWSURFACE

from .import constants
from .import player


button = pygame.Rect(500, 500, 50, 50)  # creates a rect object


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT), HWSURFACE | DOUBLEBUF)
        self.running = True
        self.background = pygame.image.load(constants.BACKGROUND)
        # self.projective_objects = []                                        # снаряды
        self.player = player.Player(constants.PLAYER_NAME)
        # self.mob = Mob('MAGE')
        self.clock = pygame.time.Clock()

    def main_loop(self):
        pygame.init()
        pygame.display.set_caption(constants.WINDOW_NAME)
        while self.running:
            self.player.move()
            self.events()
            self.bullets_move()
            self.render()
            self.player.regen()
            self.cooldown()
            self.clock.tick(constants.FPS)

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()  # gets mouse position
                if button.collidepoint(mouse_pos):
                    print('button was pressed at {0}'.format(mouse_pos))

            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                movement_matrix = [0, 0, 0, 0]
                if keys[pygame.K_RIGHT]:
                    movement_matrix[0] = 1
                if keys[pygame.K_LEFT]:
                    movement_matrix[1] = 1
                if keys[pygame.K_UP]:
                    movement_matrix[2] = 1
                if keys[pygame.K_DOWN]:
                    movement_matrix[3] = 1
                self.player.moving = movement_matrix

                # PLAYERS EVENTS ON BUTTONS TEST
                if event.key == pygame.K_SPACE:
                    if self.player.status != constants.DEAD:
                        self.player.status = constants.DEAD
                        self.player.hp = 0
                        self.player.mp = 0
                    else:
                        self.player.status = constants.ALIVE
                        self.player.hp = random.randrange(1, 100)
                        self.player.mp = random.randrange(1, 100)

                        # СТРЕЛЬБА С ДВУХ СТВОЛОВ
                if event.key == pygame.K_z:
                    self.player.shoot()
            # отжатие клавиш
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.moving[constants.CHAR_R] = 0
                if event.key == pygame.K_LEFT:
                    self.player.moving[constants.CHAR_L] = 0
                if event.key == pygame.K_UP:
                    self.player.moving[constants.CHAR_U] = 0
                if event.key == pygame.K_DOWN:
                    self.player.moving[constants.CHAR_D] = 0

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.player.render(self.screen)
        self.player.render_ui(self.screen)
        self.add_button()
        for i in self.player.projective_objects:
            i.render(self.screen)
        self.render_ammo()
        pygame.display.flip()

    # replace to player class!!
    def render_ammo(self):
        if 10 - self.player.hand_shots >= 0:
            self.add_text("Ammo left: " + str(10 - self.player.hand_shots),
                          constants.WIDTH * 0.6, constants.HEIGHT - constants.HEIGHT * 0.95, constants.FONT1, 20, constants.WHITE)
        else:
            self.add_text("Ammo left: " + '0', constants.WIDTH * 0.6, constants.HEIGHT - constants.HEIGHT * 0.95, constants.FONT1, 20, constants.RED)
            self.add_text("RELOADING...", constants.WIDTH * 0.6, constants.HEIGHT - constants.HEIGHT * 0.92, constants.FONT1, 20, constants.RED)

    def cooldown(self):             #TODO replace to player class
        if self.player.hand_shots == constants.BULLETS_CD:
            self.player.cd = pygame.time.get_ticks()
            self.player.hand_shots += 1
        elif self.player.hand_shots > constants.BULLETS_CD:
            if pygame.time.get_ticks() - self.player.cd >= constants.TIME_CD:
                self.player.hand_shots = 0

    def reload(self):               #TODO replace to player class
        self.player.cd = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.player.cd >= constants.TIME_CD:
            self.player.hand_shots = 0

    def bullets_move(self):         #TODO replace to player class
        for i in self.player.projective_objects:
            # удалить обьект после определенной дистанции
            if i.x - i.start_x >= constants.BULLET_DISTANCE or i.y - i.start_y >= constants.BULLET_DISTANCE:
                self.player.projective_objects.remove(i)
            else:
                i.move()

    def add_text(self, text, x_pos, y_pos, font_type, font_size, color):
        text = str(text)
        pygame.font.init()
        # font = pygame.font.Font(font_type, font_size)
        font = pygame.font.Font(font_type, font_size)
        text = font.render(text, False, color)
        self.screen.blit(text, (x_pos, y_pos))

    def add_button(self):
        pygame.draw.rect(self.screen, [173, 100, 170], button, 5)
