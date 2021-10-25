import pygame

from src import constants
from src.characters.base_character import BaseCharacter
from src.constants import TILE_SIZE_PX
from src.gui import GUI
from src.projectiles import Bullet


class Player(BaseCharacter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.range_shots_limit = 0  # shoots after cooldown
        self.cooldown_time = 0  # msec
        self.interface = GUI(self)
        self.size = (constants.PLAYER_HEIGHT, constants.PLAYER_WIDTH)

    def process_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.shoot()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                if self.alive:
                    self.kill()
                else:
                    self.resurrect()
        self._process_wasd(event)

    def _process_wasd(self, event):
        """
           [W]
        [A][S][D] : Keys handler

        CHAR_D, CHAR_U, CHAR_R, CHAR_L = (0, 1, 2, 3)
        """
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_s]:
                self.moving[0] = 1
            if keys[pygame.K_w]:
                self.moving[1] = 1
            if keys[pygame.K_d]:
                self.moving[2] = 1
            if keys[pygame.K_a]:
                self.moving[3] = 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                self.moving[constants.CHAR_R] = 0
            if event.key == pygame.K_a:
                self.moving[constants.CHAR_L] = 0
            if event.key == pygame.K_w:
                self.moving[constants.CHAR_U] = 0
            if event.key == pygame.K_s:
                self.moving[constants.CHAR_D] = 0

    def update(self):
        super().update()
        self.regen()
        self.cooldown()

    def handle_collissions(self, tilemap):
        current_tile = tilemap.get_tile_properties(self.x // TILE_SIZE_PX, self.y // TILE_SIZE_PX, 0) or {}
        if current_tile.get('type') == 'blocker':
            print('IM BLOCKED!!!!')

    def render(self, screen):
        super().render(screen)
        self.interface.render(screen)

    def cooldown(self):
        if self.range_shots_limit == constants.BULLETS_CD:
            self.cooldown_time = pygame.time.get_ticks()
            self.range_shots_limit += 1
        elif self.range_shots_limit > constants.BULLETS_CD:
            if pygame.time.get_ticks() - self.cooldown_time >= constants.TIME_CD:
                self.range_shots_limit = 0

    def regen(self):
        if self.alive:
            if self.hp < 100:
                self.hp += constants.HP_REGEN
            if self.mp < 100:
                self.mp += constants.MP_REGEN

    def move(self):
        if self.can_move:
            # TODO: modify x, y to make collisions
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

    def shoot(self):
        if self.mp >= constants.SHOT_MP:
            if self.range_shots_limit < constants.BULLETS_CD and self.alive:
                x = self.x
                y = self.y
                if self.direction == constants.CHAR_D:
                    x = self.x + 16
                    y = self.y + 16
                if self.direction == constants.CHAR_U:
                    x = self.x + 16
                    y = self.y + 16
                if self.direction == constants.CHAR_R:
                    x = self.x + 16
                    y = self.y + 16
                if self.direction == constants.CHAR_L:
                    x = self.x + 16
                    y = self.y + 16
                self.projectile_objects.append(Bullet(x, y, self.direction))
                self.range_shots_limit += 1
                self.mp -= constants.SHOT_MP
