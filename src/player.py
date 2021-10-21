import pygame

from . import constants
from .projectives import Bullet
from .playergui import Interface


class Character:

    def __init__(self, name):
        self.x = constants.START_X
        self.y = constants.START_Y
        self.dir = constants.CHAR_R
        self.name = name
        self.hp = constants.HP_MAX
        self.mp = constants.MP_MAX
        self.gold = constants.GOLD
        self.status = constants.ALIVE
        self.image_pack = constants.PLAYERPACK
        self.subimages = []
        self.hand = 1  # right or left hand shoots
        self.hand_shots = 0  # shoots after cooldown
        self.cooldown_time = 0  # msec
        self.moving = [0, 0, 0, 0]
        self.interface = Interface()
        self.collides = False
        self.player_rect = pygame.Rect(self.x, self.y, 250, 250)

        # отрисовка игрока
        temp = pygame.image.load(constants.PLAYERPACK).convert_alpha()
        self.subimages.append(temp.subsurface(0, 0, 200, 300))
        self.subimages.append(temp.subsurface(200, 0, 230, 300))
        self.subimages.append(temp.subsurface(430, 0, 170, 300))
        self.subimages.append(temp.subsurface(600, 0, 200, 300))

        # отрисовка трупов
        self.corpsepack = constants.CORPSEPACK
        self.subcorpse = []
        tempc = pygame.image.load(self.corpsepack).convert_alpha()
        self.subcorpse.append(tempc.subsurface(0, 0, 270, 260))
        self.subcorpse.append(tempc.subsurface(270, 0, 270, 260))
        self.subcorpse.append(tempc.subsurface(540, 0, 240, 260))
        self.subcorpse.append(tempc.subsurface(780, 0, 250, 260))

        for i in range(0, len(self.subimages)):
            width = self.subimages[i].get_width()
            height = self.subimages[i].get_height()
            self.subimages[i] = pygame.transform.scale(self.subimages[i], (int(width * constants.SCALE), int(height * constants.SCALE)))

        for i in range(0, len(self.subcorpse)):
            width = self.subcorpse[i].get_width()
            height = self.subcorpse[i].get_height()
            self.subcorpse[i] = pygame.transform.scale(self.subcorpse[i], (int(width * constants.SCALE), int(height * constants.SCALE)))

    def move(self):
        if self.status == constants.ALIVE:
            if self.moving[constants.CHAR_R] == 1:
                self.dir = constants.CHAR_R
                self.x += constants.PLAYER_SPEED
            if self.moving[constants.CHAR_L] == 1:
                self.dir = constants.CHAR_L
                self.x -= constants.PLAYER_SPEED
            if self.moving[constants.CHAR_U] == 1:
                self.dir = constants.CHAR_U
                self.y -= constants.PLAYER_SPEED
            if self.moving[constants.CHAR_D] == 1:
                self.dir = constants.CHAR_D
                self.y += constants.PLAYER_SPEED

                # столкновение со стенками окна
            if self.x <= -constants.LEFT_GAP:
                self.x = -constants.LEFT_GAP
            if self.y <= -constants.UP_GAP:
                self.y = -constants.UP_GAP
            if self.x >= constants.WIDTH - constants.RIGHT_GAP:
                self.x = constants.WIDTH - constants.RIGHT_GAP
            if self.y >= constants.HEIGHT - constants.DOWN_GAP:
                self.y = constants.HEIGHT - constants.DOWN_GAP

    # прорисовка игрока
    def render(self, screen):
        if self.status == constants.ALIVE:
            sub_dict = self.subimages
        else:
            sub_dict = self.subcorpse
        screen.blit(sub_dict[self.dir], (self.x, self.y))

    def render_ui(self, screen):
        if self.status == constants.ALIVE:
            pygame.draw.line(screen, constants.RED, (self.x + 10, self.y), (self.x + self.hp + 10, self.y),
                             constants.HPMP_THICKNESS)
            pygame.draw.line(screen, constants.BLUE, (self.x + 10, self.y + constants.HPMP_THICKNESS),
                             (self.x + self.mp + 10, self.y + constants.HPMP_THICKNESS), constants.HPMP_THICKNESS)

    def regen(self):
        if self.status == constants.ALIVE:
            if self.hp < 100:
                self.hp += constants.HP_REGEN
            if self.mp < 100:
                self.mp += constants.MP_REGEN
            if self.gold < 100:
                self.gold += constants.GOLD_REGEN

    def handle_collisions(self, rectangle):
        self.player_rect = pygame.Rect(self.x, self.y, 250, 250)
        return self.player_rect.colliderect(rectangle)
        # self.collides = True


class Player(Character):

    def __init__(self, name):
        super().__init__(name)
        self.x = constants.START_X
        self.y = constants.START_Y
        self.dir = constants.CHAR_R
        self.name = name
        self.hp = constants.HP_MAX
        self.mp = constants.MP_MAX
        self.gold = constants.GOLD
        self.status = constants.ALIVE
        self.image_pack = constants.PLAYERPACK
        self.corpsepack = constants.CORPSEPACK
        self.subimages = []
        self.subcorpse = []
        self.projective_objects = []        # bullets
        self.hand = 1                       # right or left hand shoots
        self.hand_shots = 0                 # shoots after cooldown
        self.cd = 0                         # cooldown time var (msec)
        self.player_rect = pygame.Rect(self.x, self.y, 250, 250)

        # отрисовка игрока
        temp = pygame.image.load(constants.PLAYERPACK).convert_alpha()
        self.subimages.append(temp.subsurface(0, 0, 200, 300))
        self.subimages.append(temp.subsurface(200, 0, 230, 300))
        self.subimages.append(temp.subsurface(430, 0, 170, 300))
        self.subimages.append(temp.subsurface(600, 0, 200, 300))

        # отрисовка трупов
        tempc = pygame.image.load(constants.CORPSEPACK).convert_alpha()
        self.subcorpse.append(tempc.subsurface(0, 0, 270, 260))
        self.subcorpse.append(tempc.subsurface(270, 0, 270, 260))
        self.subcorpse.append(tempc.subsurface(540, 0, 240, 260))
        self.subcorpse.append(tempc.subsurface(780, 0, 250, 260))

        for i in range(0,len(self.subimages)):
            width = self.subimages[i].get_width()
            height = self.subimages[i].get_height()
            self.subimages[i] = pygame.transform.scale(self.subimages[i], (int(width * constants.SCALE), int(height * constants.SCALE)))

        for i in range(0,len(self.subcorpse)):
            width = self.subcorpse[i].get_width()
            height = self.subcorpse[i].get_height()
            self.subcorpse[i] = pygame.transform.scale(self.subcorpse[i], (int(width * constants.SCALE), int(height * constants.SCALE)))

        self.moving = [0, 0, 0, 0]

    def shoot(self):
        # добавление обькта пули
        if self.mp >= constants.SHOT_MP:
            if self.hand_shots < constants.BULLETS_CD and self.status == constants.ALIVE:
                if self.dir == constants.CHAR_D:
                    if self.hand == 0:
                        self.projective_objects.append(Bullet(self.x + 160 * constants.SCALE,
                                                              self.y + 260 * constants.SCALE,
                                                              self.dir))
                        self.hand = 1
                        self.hand_shots += 1
                    elif self.hand == 1:
                        self.projective_objects.append(Bullet(self.x + 50 * constants.SCALE,
                                                              self.y + 260 * constants.SCALE,
                                                              self.dir))
                        self.hand = 0
                        self.hand_shots += 1

                if self.dir == constants.CHAR_U:
                    if self.hand == 0:
                        self.projective_objects.append(Bullet(self.x + 150 * constants.SCALE,
                                                              self.y + 50 * constants.SCALE,
                                                              self.dir))
                        self.hand = 1
                        self.hand_shots += 1
                    elif self.hand == 1:
                        self.projective_objects.append(Bullet(self.x + 40 * constants.SCALE,
                                                              self.y + 50 * constants.SCALE,
                                                              self.dir))
                        self.hand = 0
                        self.hand_shots += 1

                if self.dir == constants.CHAR_R:
                    if self.hand == 0:
                        self.projective_objects.append(Bullet(self.x + 200 * constants.SCALE,
                                                              self.y + 130 * constants.SCALE,
                                                              self.dir))
                        self.hand = 1
                        self.hand_shots += 1
                    elif self.hand == 1:
                        self.projective_objects.append(Bullet(self.x + 200 * constants.SCALE,
                                                              self.y + 170 * constants.SCALE,
                                                              self.dir))
                        self.hand = 0
                        self.hand_shots += 1

                if self.dir == constants.CHAR_L:
                    if self.hand == 0:
                        self.projective_objects.append(Bullet(self.x + 10 * constants.SCALE,
                                                              self.y + 130 * constants.SCALE,
                                                              self.dir))
                        self.hand = 1
                        self.hand_shots += 1
                    elif self.hand == 1:
                        self.projective_objects.append(Bullet(self.x + 10 * constants.SCALE,
                                                              self.y + 170 * constants.SCALE,
                                                              self.dir))
                        self.hand = 0
                        self.hand_shots += 1
                self.mp -= constants.SHOT_MP


class Mob(Character):
    def __init__(self, name):
        super().__init__(name)
        self.x = constants.START_X_MOB
        self.y = constants.START_Y_MOB
        self.dir = constants.CHAR_L
        self.status = constants.ALIVE
        self.subimages = []
        self.subcorpse = []
        self.hand_shots = 0  # shoots after cooldown
        self.cd = 0  # cooldown time var (msec)
        self.moving = [0, 0, 0, 0]
        self.speed = constants.MOB_SPEED
