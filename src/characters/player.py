import math

import pygame

from src.characters.base_character import BaseCharacter
from src.constants import TILE_SIZE_PX, PLAYER_HEIGHT, PLAYER_WIDTH, DEBUG, CHAR_R, CHAR_L, CHAR_U, CHAR_D, \
    BULLETS_CD, TIME_CD, HP_REGEN, MP_REGEN, SHOT_MP, Colors
from src.gui import GUI
from src.projectiles import Bullet
from src.core.utils import get_topleft


class Player(BaseCharacter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.range_shots_limit = 0  # shoots after cooldown
        self.cooldown_time = 0  # msec
        self.interface = GUI(self)
        self.size = (PLAYER_HEIGHT, PLAYER_WIDTH)
        self.accel_x = 0
        self.accel_y = 0
        self.collided_rect_outline = None
        self.colliding_tiles_toplefts = set()
        self.colliding_blockers = []
        self.current_tile = None

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
                self.moving[CHAR_R] = 0
            if event.key == pygame.K_a:
                self.moving[CHAR_L] = 0
            if event.key == pygame.K_w:
                self.moving[CHAR_U] = 0
            if event.key == pygame.K_s:
                self.moving[CHAR_D] = 0

    def update(self):
        super().update()
        self.move()
        print(self.x, self.y)
        print(self.colliding_blockers)
        self.projectiles_move()
        self.regen()
        self._cooldown()

    def handle_collissions(self):
        self.update_blockers()

    def update_blockers(self):
        blockers = []
        for x, y in self.get_colliding_tiles_toplefts():
            if self.map_level.is_blocker(x, y):
                tile_rect = pygame.Rect(x, y, TILE_SIZE_PX, TILE_SIZE_PX)
                blockers.append(tile_rect)
        self.colliding_blockers = blockers

    def get_colliding_tiles_toplefts(self):
        x, y = get_topleft(self.x, self.y)
        corners = [(x, y), (x + TILE_SIZE_PX, y), (x, y + TILE_SIZE_PX), (x + TILE_SIZE_PX, y + TILE_SIZE_PX)]
        return corners

    def collide_with_blockers(self):
        x_stopped = None
        y_stopped = None
        for tile in self.colliding_blockers:
            if tile.right >= self.rect.left and self.accel_x < 0:
                print('LEFT')
                self.accel_x = 0
                x_stopped = self.rect.left + 1
            elif tile.left <= self.rect.right and self.accel_x > 0:
                print('RIGHT')
                self.accel_x = 0
                x_stopped = self.rect.right - TILE_SIZE_PX - 1

            elif tile.top <= self.rect.bottom and self.accel_y > 0:
                print('DOWN')
                self.accel_y = 0
                y_stopped = self.rect.top - 1
            elif tile.bottom >= self.rect.top and self.accel_y < 0:
                print('UP')
                self.accel_y = 0
                y_stopped = self.rect.bottom - TILE_SIZE_PX + 1
        return x_stopped, y_stopped

    def collide_with_border(self):
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
        # print(self.x, self.y)

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
        """Move player in 2D space according to keys pressed checked at self.moved list."""
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

            x_stopped, y_stopped = self.collide_with_blockers()
            self.x = x_stopped or self.x + self.accel_x
            self.y = y_stopped or self.y + self.accel_y
            self.collide_with_border()
            self.fade_speed()
            self.limit_max_speed()

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

    def projectiles_move(self):
        for projectile in self.projectile_objects:
            if projectile.flew_away():
                self.projectile_objects.remove(projectile)
            else:
                projectile.move()

    def render(self, screen):
        super().render(screen)
        self.interface.render(screen)
        if DEBUG:
            for tile_rect in self.colliding_blockers:
                pygame.draw.rect(screen, Colors.RED, tile_rect, 1)
