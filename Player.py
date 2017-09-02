import pygame
from Constants import *
from Projectives import *
from Playergui import Interface
# from Main import button


class Character:

    def __init__(self, name):
        self.x = START_X
        self.y = START_Y
        self.dir = CHAR_R
        self.name = name
        self.hp = HP_MAX
        self.mp = MP_MAX
        self.gold = GOLD
        self.status = ALIVE
        self.image_pack = PLAYERPACK
        self.subimages = []
        self.hand = 1  # right or left hand shoots
        self.hand_shots = 0  # shoots after cooldown
        self.cd = 0  # cooldown time var (msec)
        self.moving = [0, 0, 0, 0]
        self.inteface = Interface()
        self.collides = False

        # отрисовка игрока
        temp = pygame.image.load(PLAYERPACK).convert_alpha()
        self.subimages.append(temp.subsurface(0, 0, 200, 300))
        self.subimages.append(temp.subsurface(200, 0, 230, 300))
        self.subimages.append(temp.subsurface(430, 0, 170, 300))
        self.subimages.append(temp.subsurface(600, 0, 200, 300))

        # отрисовка трупов
        self.corpsepack = CORPSEPACK
        self.subcorpse = []
        tempc = pygame.image.load(CORPSEPACK).convert_alpha()
        self.subcorpse.append(tempc.subsurface(0, 0, 270, 260))
        self.subcorpse.append(tempc.subsurface(270, 0, 270, 260))
        self.subcorpse.append(tempc.subsurface(540, 0, 240, 260))
        self.subcorpse.append(tempc.subsurface(780, 0, 250, 260))

        for i in range(0, len(self.subimages)):
            width = self.subimages[i].get_width()
            height = self.subimages[i].get_height()
            self.subimages[i] = pygame.transform.scale(self.subimages[i], (int(width * scale), int(height * scale)))

        for i in range(0, len(self.subcorpse)):
            width = self.subcorpse[i].get_width()
            height = self.subcorpse[i].get_height()
            self.subcorpse[i] = pygame.transform.scale(self.subcorpse[i], (int(width * scale), int(height * scale)))



    def move(self):
        if self.status == ALIVE:
            if self.moving[CHAR_R] == 1:
                self.dir = CHAR_R
                self.x += PLAYER_SPEED
            if self.moving[CHAR_L] == 1:
                self.dir = CHAR_L
                self.x -= PLAYER_SPEED
            if self.moving[CHAR_U] == 1:
                self.dir = CHAR_U
                self.y -= PLAYER_SPEED
            if self.moving[CHAR_D] == 1:
                self.dir = CHAR_D
                self.y += PLAYER_SPEED

                # столкновение со стенками окна
            if self.x <= -LEFT_GAP:
                self.x = -LEFT_GAP
            if self.y <= -UP_GAP:
                self.y = -UP_GAP
            if self.x >= WIDTH - RIGHT_GAP:
                self.x = WIDTH - RIGHT_GAP
            if self.y >= HEIGHT - DOWN_GAP:
                self.y = HEIGHT - DOWN_GAP

    # прорисовка игрока
    def render(self, screen):
        if self.status == ALIVE:
            screen.blit(self.subimages[self.dir], (self.x, self.y))
        else:
            screen.blit(self.subcorpse[self.dir], (self.x, self.y))

    # прорисовка интерфейса
    def render_ui(self, screen):
        # HP & MP BARS
        if self.status == ALIVE:
            pygame.draw.line(screen, RED, (self.x + 10, self.y), (self.x + self.hp + 10, self.y), HPMP_THICKNESS)
            pygame.draw.line(screen, BLUE, (self.x + 10, self.y + HPMP_THICKNESS),
                             (self.x + self.mp + 10, self.y + HPMP_THICKNESS), HPMP_THICKNESS)

    def regen(self):
        if self.status == ALIVE:
            if self.hp < 100:
                self.hp += HP_REGEN
            if self.mp < 100:
                self.mp += MP_REGEN
            if self.gold < 100:
                self.gold += GOLD_REGEN


class Player(Character):

    def __init__(self, name):
        super().__init__(name)
        self.x = START_X
        self.y = START_Y
        self.dir = CHAR_R
        self.name = name
        self.hp = HP_MAX
        self.mp = MP_MAX
        self.gold = GOLD
        self.status = ALIVE
        self.image_pack = PLAYERPACK
        self.corpsepack = CORPSEPACK
        self.subimages = []
        self.subcorpse = []
        self.projective_objects = []        # bullets
        self.hand = 1                       # right or left hand shoots
        self.hand_shots = 0                 # shoots after cooldown
        self.cd = 0                         # cooldown time var (msec)
        self.player_rect = pygame.Rect(self.x, self.y, 250, 250)

        # отрисовка игрока
        temp = pygame.image.load(PLAYERPACK).convert_alpha()
        self.subimages.append(temp.subsurface(0, 0, 200, 300))
        self.subimages.append(temp.subsurface(200, 0, 230, 300))
        self.subimages.append(temp.subsurface(430, 0, 170, 300))
        self.subimages.append(temp.subsurface(600, 0, 200, 300))

        # отрисовка трупов

        tempc = pygame.image.load(CORPSEPACK).convert_alpha()
        self.subcorpse.append(tempc.subsurface(0, 0, 270, 260))
        self.subcorpse.append(tempc.subsurface(270, 0, 270, 260))
        self.subcorpse.append(tempc.subsurface(540, 0, 240, 260))
        self.subcorpse.append(tempc.subsurface(780, 0, 250, 260))

        for i in range(0,len(self.subimages)):
            width = self.subimages[i].get_width()
            height = self.subimages[i].get_height()
            self.subimages[i] = pygame.transform.scale(self.subimages[i], (int(width * scale), int(height * scale)))

        for i in range(0,len(self.subcorpse)):
            width = self.subcorpse[i].get_width()
            height = self.subcorpse[i].get_height()
            self.subcorpse[i] = pygame.transform.scale(self.subcorpse[i], (int(width * scale), int(height * scale)))

        self.moving = [0, 0, 0, 0]

    def move(self):
        if self.status == ALIVE:
            if self.moving[CHAR_R] == 1:
                self.dir = CHAR_R
                self.x += PLAYER_SPEED
            if self.moving[CHAR_L] == 1:
                self.dir = CHAR_L
                self.x -= PLAYER_SPEED
            if self.moving[CHAR_U] == 1:
                self.dir = CHAR_U
                self.y -= PLAYER_SPEED
            if self.moving[CHAR_D] == 1:
                self.dir = CHAR_D
                self.y += PLAYER_SPEED

                # столкновение со стенками окна
            if self.x <= -LEFT_GAP:
                self.x = -LEFT_GAP
            if self.y <= -UP_GAP:
                self.y = -UP_GAP
            if self.x >= WIDTH - RIGHT_GAP:
                self.x = WIDTH - RIGHT_GAP
            if self.y >= HEIGHT - DOWN_GAP:
                self.y = HEIGHT - DOWN_GAP

    def shoot(self):
        # добавление обькта пули
        if self.mp >= SHOT_MP:
            if self.hand_shots < BULLETS_CD and self.status == ALIVE:
                if self.dir == CHAR_D:
                    if self.hand == 0:
                        self.projective_objects.append(Bullet(self.x + 160 * scale,
                                                              self.y + 260 * scale,
                                                              self.dir))
                        self.hand = 1
                        self.hand_shots += 1
                    elif self.hand == 1:
                        self.projective_objects.append(Bullet(self.x + 50 * scale,
                                                              self.y + 260 * scale,
                                                              self.dir))
                        self.hand = 0
                        self.hand_shots += 1

                if self.dir == CHAR_U:
                    if self.hand == 0:
                        self.projective_objects.append(Bullet(self.x + 150 * scale,
                                                              self.y + 50 * scale,
                                                              self.dir))
                        self.hand = 1
                        self.hand_shots += 1
                    elif self.hand == 1:
                        self.projective_objects.append(Bullet(self.x + 40 * scale,
                                                              self.y + 50 * scale,
                                                              self.dir))
                        self.hand = 0
                        self.hand_shots += 1

                if self.dir == CHAR_R:
                    if self.hand == 0:
                        self.projective_objects.append(Bullet(self.x + 200 * scale,
                                                              self.y + 130 * scale,
                                                              self.dir))
                        self.hand = 1
                        self.hand_shots += 1
                    elif self.hand == 1:
                        self.projective_objects.append(Bullet(self.x + 200 * scale,
                                                              self.y + 170 * scale,
                                                              self.dir))
                        self.hand = 0
                        self.hand_shots += 1

                if self.dir == CHAR_L:
                    if self.hand == 0:
                        self.projective_objects.append(Bullet(self.x + 10 * scale,
                                                              self.y + 130 * scale,
                                                              self.dir))
                        self.hand = 1
                        self.hand_shots += 1
                    elif self.hand == 1:
                        self.projective_objects.append(Bullet(self.x + 10 * scale,
                                                              self.y + 170 * scale,
                                                              self.dir))
                        self.hand = 0
                        self.hand_shots += 1
                self.mp -= SHOT_MP

    # прорисовка игрока
    def render(self,screen):
        if self.status == ALIVE:
            screen.blit(self.subimages[self.dir], (self.x,self.y))
        else:
            screen.blit(self.subcorpse[self.dir], (self.x,self.y))


    # прорисовка интерфейса
    def render_ui(self, screen):
        # HP & MP BARS
        if self.status == ALIVE:
            pygame.draw.line(screen, RED, (self.x + 10, self.y), (self.x + self.hp + 10,self.y), HPMP_THICKNESS)
            pygame.draw.line(screen, BLUE, (self.x + 10, self.y + HPMP_THICKNESS), (self.x + self.mp + 10, self.y + HPMP_THICKNESS), HPMP_THICKNESS)


    def regen(self):
        if self.status == ALIVE:
            if self.hp < 100:
                self.hp += HP_REGEN
            if self.mp < 100:
                self.mp += MP_REGEN
            if self.gold < 100:
                self.gold += GOLD_REGEN


    def handle_collisions(self, rectangle):
        self.player_rect = pygame.Rect(self.x, self.y, 250, 250)
        return self.player_rect.colliderect(rectangle)
        # self.collides = True

class Mob(Character):

    def __init__(self, name):
        super().__init__(name)
        self.x = START_X_MOB
        self.y = START_Y_MOB
        self.dir = CHAR_L
        self.status = ALIVE
        self.subimages = []
        self.subcorpse = []
        self.hand_shots = 0  # shoots after cooldown
        self.cd = 0  # cooldown time var (msec)
        self.moving = [0, 0, 0, 0]
        self.speed = MOB_SPEED

    def move(self):
        if self.status == ALIVE:
            if self.moving[CHAR_R] == 1:
                self.dir = CHAR_R
                self.x += self.speed
            if self.moving[CHAR_L] == 1:
                self.dir = CHAR_L
                self.x -= self.speed
            if self.moving[CHAR_U] == 1:
                self.dir = CHAR_U
                self.y -= self.speed
            if self.moving[CHAR_D] == 1:
                self.dir = CHAR_D
                self.y += self.speed

                # столкновение со стенками окна
            if self.x <= -LEFT_GAP:
                self.x = -LEFT_GAP
            if self.y <= -UP_GAP:
                self.y = -UP_GAP
            if self.x >= WIDTH - RIGHT_GAP:
                self.x = WIDTH - RIGHT_GAP
            if self.y >= HEIGHT - DOWN_GAP:
                self.y = HEIGHT - DOWN_GAP

    # прорисовка моба
    def render(self, screen):
        if self.status == ALIVE:
            screen.blit(self.subimages[self.dir], (self.x, self.y))
        else:
            screen.blit(self.subcorpse[self.dir], (self.x, self.y))

    # прорисовка интерфейса
    def render_ui(self, screen):
        # HP & MP BARS
        if self.status == ALIVE:
            pygame.draw.line(screen, RED, (self.x + 10, self.y), (self.x + self.hp + 10, self.y), HPMP_THICKNESS)
            pygame.draw.line(screen, BLUE, (self.x + 10, self.y + HPMP_THICKNESS),
                             (self.x + self.mp + 10, self.y + HPMP_THICKNESS), HPMP_THICKNESS)

    def regen(self):
        if self.status == ALIVE:
            if self.hp < 100:
                self.hp += HP_REGEN
            if self.mp < 100:
                self.mp += MP_REGEN
            if self.gold < 100:
                self.gold += GOLD_REGEN

button = pygame.Rect(500, 500, 50, 50)  # creates a rect object