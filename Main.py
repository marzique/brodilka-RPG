import random

import sys
from Projectives import *
from pygame.locals import *
from Constants import *
from Player import *
from pygame.locals import *

class Main:

    def __init__(self,screen):
        self.screen = screen
        self.running = True
        self.background = pygame.image.load(BACKGROUND)
        # self.projective_objects = []                                        # снаряды
        self.player = Player(PLAYER_NAME)
        # self.mob = Mob('MAGE')
        self.main_loop()

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                                                                    # replace all events as methods to their classes
                                                                    # (e.g. moving,shot... -> player,..)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()                          # gets mouse position

                                                            # checks if mouse position is over the button
                                                            # note this method is constantly looking for collisions
                                                            # the only reason you dont see an evet activated when you
                                                            # hover over the button is because the method is bellow the
                                                            # mousedown event if it were outside it would be called the
                                                            # the moment the mouse hovers over the button

                if button.collidepoint(mouse_pos):
                    # pritns current location of mouse
                    print('button was pressed at {0}'.format(mouse_pos))

                        # нажатие клавиш
            elif event.type == KEYDOWN:
                # Передвижение по сторонам
                if event.key == K_RIGHT:
                    self.player.moving = [1, 0, 0, 0]
                if event.key == K_LEFT:
                    self.player.moving = [0, 1, 0, 0]
                if event.key == K_UP:
                    self.player.moving = [0, 0, 1, 0]
                if event.key == K_DOWN:
                    self.player.moving = [0, 0, 0, 1]

                    # PLAYERS EVENTS ON BUTTONS TEST
                if event.key == K_SPACE:
                    if self.player.status != DEAD:
                        self.player.status = DEAD
                        self.player.hp = 0
                        self.player.mp = 0
                    else:
                        self.player.status = ALIVE
                        self.player.hp = random.randrange(1, 100)
                        self.player.mp = random.randrange(1, 100)

                        # СТРЕЛЬБА С ДВУХ СТВОЛОВ
                if event.key == K_z:
                    self.player.shoot()
                                                        # отжатие клавиш
            elif event.type == KEYUP:
                if event.key == K_RIGHT:
                    self.player.moving[CHAR_R] = 0
                if event.key == K_LEFT:
                    self.player.moving[CHAR_L] = 0
                if event.key == K_UP:
                    self.player.moving[CHAR_U] = 0
                if event.key == K_DOWN:
                    self.player.moving[CHAR_D] = 0


    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.player.render(screen)
        # self.mob.render(screen)
        self.player.render_ui(screen)
        self.add_button()
        for i in self.player.projective_objects:
            i.render(screen)
        self.render_ammo()
        pygame.display.flip()

        # replace to player class!!
    def render_ammo(self):
        if 10 - self.player.hand_shots >= 0:
            self.add_text("Ammo left: " + str(10 - self.player.hand_shots),
                          WIDTH * 0.6, HEIGHT - HEIGHT * 0.95, FONT1, 20, WHITE)
        else:
            self.add_text("Ammo left: " + '0', WIDTH * 0.6, HEIGHT - HEIGHT * 0.95, FONT1, 20, RED)
            self.add_text("RELOADING...", WIDTH * 0.6, HEIGHT - HEIGHT * 0.92, FONT1, 20, RED)

    def cooldown(self):
        # задержка в мс
        if self.player.hand_shots == BULLETS_CD:
            self.player.cd = pygame.time.get_ticks()
            self.player.hand_shots += 1
        elif self.player.hand_shots > BULLETS_CD:
            if pygame.time.get_ticks() - self.player.cd >= TIME_CD:
                self.player.hand_shots = 0

    def reload(self):
        self.player.cd = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.player.cd >= TIME_CD:
            self.player.hand_shots = 0

    def bullets_move(self):
        for i in self.player.projective_objects:
            # удалить обьект после определенной дистанции
            if i.x - i.start_x >= BULLET_DISTANCE or i.y - i.start_y >= BULLET_DISTANCE:
                self.player.projective_objects.remove(i)
            else:
                i.move()


    def add_text(self, text, x_pos, y_pos, font_type, font_size, color):
        text = str(text)
        pygame.font.init()
        # font = pygame.font.Font(font_type, font_size)
        font = pygame.font.Font(font_type, font_size)
        text = font.render(text, False, color)
        screen.blit(text, (x_pos, y_pos))

    #     render(text, antialias, color, background=None) -> Surface

    def add_button(self):
        pygame.draw.rect(screen, [0, 255, 0], button, 5)

    def main_loop(self):
        while self.running == True:
            self.player.move()
            self.events()
            self.bullets_move()
            self.render()
            self.player.regen()
            self.cooldown()
            # print(self.player.moving, sesf.projectives)
            # print(str(self.player.cd) + ' ' + str(pygame.time.get_ticks()) + ' ' + str(self.player.hand_shots))
            clock.tick(FPS)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), HWSURFACE | DOUBLEBUF)
pygame.display.set_caption(WINDOW_NAME)
clock = pygame.time.Clock()

game = Main(screen)
