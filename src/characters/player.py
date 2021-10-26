import math

import pygame

from src import constants
from src.characters.base_character import BaseCharacter
from src.constants import TILE_SIZE_PX
from src.gui import GUI
from src.projectiles import Bullet


class Player(BaseCharacter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tilemap = None  # O2O
        self.range_shots_limit = 0  # shoots after cooldown
        self.cooldown_time = 0  # msec
        self.interface = GUI(self)
        self.size = (constants.PLAYER_HEIGHT, constants.PLAYER_WIDTH)
        self.accel_x = 0
        self.accel_y = 0
        self.collided_rect_outline = None
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

    def update(self):
        super().update()
        self.move()
        self.projectiles_move()
        self.regen()
        self.cooldown()

    def render(self, screen):
        super().render(screen)
        self.interface.render(screen)
        if self.current_tile.get('type') == 'blocker':
            if constants.DEBUG:
                pygame.draw.rect(screen, [255, 0, 0], self.collided_rect_outline, 1)

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

    def handle_collissions(self, tilemap):
        self.tilemap = tilemap
        x = self.x // TILE_SIZE_PX
        y = self.y // TILE_SIZE_PX
        try:
            self.current_tile = tilemap.get_tile_properties(x, y, 0) or {}
        except ValueError:
            # print(f'Player outside the map, coords: {x, y} ')
            pass
        self.collided_rect_outline = pygame.Rect(x * TILE_SIZE_PX, y * TILE_SIZE_PX, TILE_SIZE_PX, TILE_SIZE_PX)

    def collide_with_border(self, tilemap):
        """
        Collide with borders of the map.
        Should server as a fallback check for mistakes in levels.
        By default all level maps should have border of blocker type tiles.
        """
        map_width = tilemap.width * TILE_SIZE_PX
        map_height = tilemap.height * TILE_SIZE_PX
        tile_center = TILE_SIZE_PX // 2
        center_x = self.x + tile_center
        center_y = self.y + tile_center
        collides = False

        if self.moving[constants.CHAR_R] == 1:
            if center_x >= map_width:
                self.x = map_width - tile_center
                self.accel_x = 0
                collides = True
        if self.moving[constants.CHAR_L] == 1:
            if center_x <= 0:
                self.x = 0 - tile_center
                self.accel_x = 0
                collides = True
        if self.moving[constants.CHAR_U] == 1:
            if center_y <= 0:
                self.y = 0 - tile_center
                self.accel_y = 0
                collides = True
        if self.moving[constants.CHAR_D] == 1:
            if center_y >= map_height:
                self.y = map_height - tile_center
                self.accel_y = 0
                collides = True

        # print(self.x, self.y)
        return collides

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
        """
        Move player in 2D space according to keys pressed checked at self.moved list.
        Acceleration is applied.
        """
        if self.collide_with_border(self.tilemap):
            return

        accel_step = 0.05
        accel_fade = 0.90
        accel_threshold = 1
        moving_x = bool(self.moving[constants.CHAR_R] or self.moving[constants.CHAR_L])
        moving_y = bool(self.moving[constants.CHAR_U] or self.moving[constants.CHAR_D])
        if moving_x and moving_y:
            accel_threshold = math.sqrt(2)/2 * accel_threshold
        fade_stop = 0.001
        dx = self.accel_x
        dy = self.accel_y

        if self.can_move:
            # accelerate on keypress
            if self.moving[constants.CHAR_R] == 1:
                self.direction = constants.CHAR_R
                self.accel_x += accel_step
            if self.moving[constants.CHAR_L] == 1:
                self.direction = constants.CHAR_L
                self.accel_x -= accel_step
            if self.moving[constants.CHAR_U] == 1:
                self.direction = constants.CHAR_U
                self.accel_y -= accel_step
            if self.moving[constants.CHAR_D] == 1:
                self.direction = constants.CHAR_D
                self.accel_y += accel_step
            # limit max speed
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
            # inertia
            if not self.moving[constants.CHAR_R] and not self.moving[constants.CHAR_L]:
                self.accel_x *= accel_fade
                if abs(self.accel_x) < fade_stop:
                    self.accel_x = 0
            if not self.moving[constants.CHAR_U] and not self.moving[constants.CHAR_D]:
                self.accel_y *= accel_fade
                if abs(self.accel_y) < fade_stop:
                    self.accel_y = 0
            # print(f'player accel: {self.accel_x, self.accel_y}')
            self.x += dx
            self.y += dy

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

    def projectiles_move(self):
        for projectile in self.projectile_objects:
            if projectile.flew_away():
                self.projectile_objects.remove(projectile)
            else:
                projectile.move()
