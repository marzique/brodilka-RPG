import pygame

from src.characters.base_character import BaseCharacter
from src.constants import TILE_SIZE_PX, DEBUG, RIGHT, LEFT, TOP, BOTTOM, BULLETS_CD, TIME_CD, \
    HP_REGEN, MP_REGEN, SHOT_MP, Colors
from src.core.utils import debug
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
        self.accel_step = 0.05


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
        self.regen()
        self._cooldown()
        print(self.x, self.y)

    def render(self, screen):
        super().render(screen)
        self.interface.render(screen)
        self.draw_player_border(screen)

    @debug
    def draw_player_border(self, screen):
        pygame.draw.rect(screen, Colors.GOLD, self.rect, 1)

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
                self.moving[RIGHT] = 0
            if event.key == pygame.K_a:
                self.moving[LEFT] = 0
            if event.key == pygame.K_w:
                self.moving[TOP] = 0
            if event.key == pygame.K_s:
                self.moving[BOTTOM] = 0

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
        if self.can_move:
            # accelerate on keypress
            if self.moving[RIGHT]:
                self.direction = RIGHT
                self.accel_x += self.accel_step
            if self.moving[LEFT]:
                self.direction = LEFT
                self.accel_x -= self.accel_step
            if self.moving[TOP]:
                self.direction = TOP
                self.accel_y -= self.accel_step
            if self.moving[BOTTOM]:
                self.direction = BOTTOM
                self.accel_y += self.accel_step

            self.x += self.accel_x
            self.y += self.accel_y
            self.rect.x = self.x
            self.collide_with_walls('x')
            self.rect.y = self.y
            self.collide_with_walls('y')
            self.limit_max_speed()
            self.fade_speed()

    def collide_with_walls(self, direction):
        blockers = pygame.sprite.spritecollide(self, self.map_level.blockers, False)
        if direction == 'x':
            if blockers:
                if self.accel_x > 0:
                    self.x = blockers[0].rect.left - self.rect.width
                if self.accel_x < 0:
                    self.x = blockers[0].rect.right
                self.accel_x = 0
                self.rect.x = self.x
        if direction == 'y':
            if blockers:
                if self.accel_y > 0:
                    self.y = blockers[0].rect.top - self.rect.height
                if self.accel_y < 0:
                    self.y = blockers[0].rect.bottom
                self.accel_y = 0
                self.rect.y = self.y

    def fade_speed(self):
        accel_fade = 0.95
        fade_stop = 0.001
        if not self.moving[RIGHT] and not self.moving[LEFT]:
            self.accel_x *= accel_fade
            if abs(self.accel_x) < fade_stop:
                self.accel_x = 0
        if not self.moving[TOP] and not self.moving[BOTTOM]:
            self.accel_y *= accel_fade
            if abs(self.accel_y) < fade_stop:
                self.accel_y = 0

    def limit_max_speed(self):
        accel_threshold = 1
        moving_x = bool(self.moving[RIGHT] or self.moving[LEFT])
        moving_y = bool(self.moving[TOP] or self.moving[BOTTOM])
        if moving_x and moving_y:  # diagonal adjustment
            accel_threshold *= 0.7071
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
                if self.direction == BOTTOM:
                    x = self.x + 16
                    y = self.y + 16
                if self.direction == TOP:
                    x = self.x + 16
                    y = self.y + 16
                if self.direction == RIGHT:
                    x = self.x + 16
                    y = self.y + 16
                if self.direction == LEFT:
                    x = self.x + 16
                    y = self.y + 16
                self.projectile_objects.append(Bullet(x, y, self.direction))
                self.range_shots_limit += 1
