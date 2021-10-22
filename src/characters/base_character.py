from abc import abstractmethod, ABC

import pygame

from src import constants
from src.playergui import Interface


class AbstractCharacter(ABC):
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self, screen):
        pass


class BaseCharacter(AbstractCharacter):
    def __init__(self, name):
        self.name = name
        self.x = constants.START_X
        self.y = constants.START_Y
        self.hp = constants.HP_MAX
        self.mp = constants.MP_MAX
        self.alive = True
        self.direction = constants.CHAR_R
        self.gold = constants.GOLD
        self.hand = 1  # right or left hand shoots
        self.hand_shots = 0  # shoots after cooldown
        self.cooldown_time = 0  # msec
        self.moving = [0, 0, 0, 0]
        self.interface = Interface()
        self.projectile_objects = []        # bullets
        self.playerpack_list, self.corpsepack_list = self.load_player_sprites()
        self.can_move = True

    @property
    def rect(self):
        # TODO: 250 ??
        return pygame.Rect(self.x, self.y, 250, 250)

    @staticmethod
    def load_player_sprites():
        playerpack = pygame.image.load(constants.PLAYERPACK).convert_alpha()
        playerpack_list = [
            playerpack.subsurface(0, 0, 200, 300),
            playerpack.subsurface(200, 0, 230, 300),
            playerpack.subsurface(430, 0, 170, 300),
            playerpack.subsurface(600, 0, 200, 300)
        ]

        corpsepack = pygame.image.load(constants.CORPSEPACK).convert_alpha()
        corpsepack_list = [
            corpsepack.subsurface(0, 0, 270, 260),
            corpsepack.subsurface(270, 0, 270, 260),
            corpsepack.subsurface(540, 0, 240, 260),
            corpsepack.subsurface(780, 0, 250, 260)
        ]

        # scaling
        for i, subimage in enumerate(playerpack_list):
            width = subimage.get_width()
            height = subimage.get_height()
            playerpack_list[i] = pygame.transform.scale(
                subimage,
                (int(width * constants.SCALE), int(height * constants.SCALE))
            )

        for i, subcorpse in enumerate(corpsepack_list):
            width = subcorpse.get_width()
            height = subcorpse.get_height()
            corpsepack_list[i] = pygame.transform.scale(
                subcorpse,
                (int(width * constants.SCALE), int(height * constants.SCALE))
            )

        return playerpack_list, corpsepack_list

    def update(self):
        self.regen()
        self.move()
        self.projectile_move()
        self.cooldown()

    def render(self, screen):
        if self.alive:
            sub_dict = self.playerpack_list
        else:
            sub_dict = self.corpsepack_list
        screen.blit(sub_dict[self.direction], (self.x, self.y))
        self.render_ui(screen)
        for projectile in self.projectile_objects:
            projectile.render(screen)

    def cooldown(self):
        if self.hand_shots == constants.BULLETS_CD:
            self.cooldown_time = pygame.time.get_ticks()
            self.hand_shots += 1
        elif self.hand_shots > constants.BULLETS_CD:
            if pygame.time.get_ticks() - self.cooldown_time >= constants.TIME_CD:
                self.hand_shots = 0

    def render_ui(self, screen):
        if self.alive:
            pygame.draw.line(screen, constants.RED, (self.x + 10, self.y), (self.x + self.hp + 10, self.y),
                             constants.HPMP_THICKNESS)
            pygame.draw.line(screen, constants.BLUE, (self.x + 10, self.y + constants.HPMP_THICKNESS),
                             (self.x + self.mp + 10, self.y + constants.HPMP_THICKNESS), constants.HPMP_THICKNESS)

    def projectile_move(self):
        for projectile in self.projectile_objects:
            if projectile.x - projectile.start_x >= constants.BULLET_DISTANCE or projectile.y - projectile.start_y >= constants.BULLET_DISTANCE:
                self.projectile_objects.remove(projectile)
            else:
                projectile.move()

    def move(self):
        if self.can_move:
            if self.moving[constants.CHAR_R] == 1:
                self.direction = constants.CHAR_R
                self.x += constants.PLAYER_SPEED
            if self.moving[constants.CHAR_L] == 1:
                self.direction = constants.CHAR_L
                self.x -= constants.PLAYER_SPEED
            if self.moving[constants.CHAR_U] == 1:
                self.direction = constants.CHAR_U
                self.y -= constants.PLAYER_SPEED
            if self.moving[constants.CHAR_D] == 1:
                self.direction = constants.CHAR_D
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

    def regen(self):
        if self.alive:
            if self.hp < 100:
                self.hp += constants.HP_REGEN
            if self.mp < 100:
                self.mp += constants.MP_REGEN

    def handle_collisions(self, rectangle):
        return self.rect.colliderect(rectangle)

    def kill(self):
        self.alive = self.can_move = False
        self.hp = 0
        self.mp = 0

    def resurrect(self):
        self.alive = self.can_move = True
        self.hp = 100
        self.mp = 100
