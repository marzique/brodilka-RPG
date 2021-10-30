import math

import pygame

from src.characters.base_character import BaseCharacter
from src.constants import TILE_SIZE_PX, DEBUG, CHAR_R, CHAR_L, CHAR_U, CHAR_D, BULLETS_CD, TIME_CD, \
    HP_REGEN, MP_REGEN, SHOT_MP, Colors
from src.gui import GUI
from src.projectiles import Bullet


class Player(BaseCharacter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.range_shots_limit = 0  # shoots after cooldown
        self.cooldown_time = 0  # msec
        self.interface = GUI(self)
        self.prev_x = self.x
        self.prev_y = self.y

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

    def update(self):
        super().update()
        self.update_blockers()
        self.move()
        self.regen()
        self._cooldown()
        print(self.x, self.y)

    def render(self, screen):
        super().render(screen)
        self.interface.render(screen)
        if DEBUG:
            # player rect
            pygame.draw.rect(screen, Colors.GOLD, self.rect, 1)
            # player rect border
            pygame.draw.rect(screen, Colors.LTBLUE, self.rect_border, 1)

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
                self.moving[CHAR_R] = 0
            if event.key == pygame.K_a:
                self.moving[CHAR_L] = 0
            if event.key == pygame.K_w:
                self.moving[CHAR_U] = 0
            if event.key == pygame.K_s:
                self.moving[CHAR_D] = 0

    def collide_with_map_border(self):
        """
        Collide with borders of the map.
        Should serve as a fallback check for mistakes in levels.
        By default all level maps should have border of blocker type tiles.
        """
        map_width = self.map_level.tilemap.width * TILE_SIZE_PX
        map_height = self.map_level.tilemap.height * TILE_SIZE_PX
        tile_center = TILE_SIZE_PX // 2
        center_x = self.x + tile_center
        center_y = self.y + tile_center
        moving_x = abs(self.accel_x)
        moving_y = abs(self.accel_y)

        if center_x > map_width and moving_x:
            self.x = map_width - tile_center
            self.accel_x = 0
        if center_x < 0 and moving_x:
            self.x = 0 - tile_center
            self.accel_x = 0
        if center_y < 0 and moving_y:
            self.y = 0 - tile_center
            self.accel_y = 0
        if center_y > map_height and moving_y:
            self.y = map_height - tile_center
            self.accel_y = 0

    def _cooldown(self):
        if self.range_shots_limit == BULLETS_CD:
            self.cooldown_time = pygame.time.get_ticks()
            self.range_shots_limit += 1
        elif self.range_shots_limit > BULLETS_CD:
            if pygame.time.get_ticks() - self.cooldown_time >= TIME_CD:
                self.range_shots_limit = 0

    def regen(self):
        if self.alive:
            if self.hp < 100:
                self.hp += HP_REGEN
            if self.mp < 100:
                self.mp += MP_REGEN

    def move(self):
        """Update x and y of the player"""
        accel_step = 0.05
        if self.can_move:
            # accelerate on keypress
            if self.moving[CHAR_R]:
                self.direction = CHAR_R
                self.accel_x += accel_step
            if self.moving[CHAR_L]:
                self.direction = CHAR_L
                self.accel_x -= accel_step
            if self.moving[CHAR_U]:
                self.direction = CHAR_U
                self.accel_y -= accel_step
            if self.moving[CHAR_D]:
                self.direction = CHAR_D
                self.accel_y += accel_step

            self.collide_with_blockers()
            self.collide_with_map_border()
            self.fade_speed()
            self.limit_max_speed()

    def collide_with_blockers(self):
        for name, tile in self.colliding_blockers.items():
            # print(self.colliding_blockers)
            on_the_same_line = self.map_level.on_the_same_line(tile, self)
            if on_the_same_line:
                if tile.right >= self.rect_border.left and self.accel_x < 0:
                    if name in ['topleft', 'bottomleft']:
                        print('LEFT')
                        self.accel_x = 0
                        self.x = self.prev_x
                if tile.left <= self.rect_border.right and self.accel_x > 0:
                    if name in ['topright', 'bottomright']:
                        print('RIGHT')
                        self.accel_x = 0
                        self.x = self.prev_x
        self.x += self.accel_x
        self.prev_x = self.x

        for name, tile in self.colliding_blockers.items():
            in_the_same_row = self.map_level.in_the_same_row(tile, self)
            if in_the_same_row:
                if tile.top <= self.rect_border.bottom and self.accel_y > 0:
                    if name in ['bottomleft', 'bottomright']:
                        print('DOWN')
                        self.accel_y = 0
                        self.y = self.prev_y
                if tile.bottom >= self.rect_border.top and self.accel_y < 0:
                    if name in ['topleft', 'topright']:
                        print('UP')
                        self.accel_y = 0
                        self.y = self.prev_y
        self.y += self.accel_y
        self.prev_y = self.y


    def fade_speed(self):
        accel_fade = 0.95
        fade_stop = 0.001
        if not self.moving[CHAR_R] and not self.moving[CHAR_L]:
            self.accel_x *= accel_fade
            if abs(self.accel_x) < fade_stop:
                self.accel_x = 0
        if not self.moving[CHAR_U] and not self.moving[CHAR_D]:
            self.accel_y *= accel_fade
            if abs(self.accel_y) < fade_stop:
                self.accel_y = 0

    def limit_max_speed(self):
        accel_threshold = 1
        moving_x = bool(self.moving[CHAR_R] or self.moving[CHAR_L])
        moving_y = bool(self.moving[CHAR_U] or self.moving[CHAR_D])
        if moving_x and moving_y:  # diagonal adjustment
            accel_threshold = math.sqrt(2)/2 * accel_threshold

        if abs(self.accel_x) > accel_threshold:
            if self.accel_x > 0:
                self.accel_x = accel_threshold
            else:
                self.accel_x = -accel_threshold
        if abs(self.accel_y) > accel_threshold:
            if self.accel_y > 0:
                self.accel_y = accel_threshold
            else:
                self.accel_y = -accel_threshold

    def shoot(self):
        if self.mp >= SHOT_MP:
            self.mp -= SHOT_MP
            if self.range_shots_limit < BULLETS_CD and self.alive:
                x = self.x
                y = self.y
                if self.direction == CHAR_D:
                    x = self.x + 16
                    y = self.y + 16
                if self.direction == CHAR_U:
                    x = self.x + 16
                    y = self.y + 16
                if self.direction == CHAR_R:
                    x = self.x + 16
                    y = self.y + 16
                if self.direction == CHAR_L:
                    x = self.x + 16
                    y = self.y + 16
                self.projectile_objects.append(Bullet(x, y, self.direction))
                self.range_shots_limit += 1
