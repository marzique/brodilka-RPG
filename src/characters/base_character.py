import pygame

from src.constants import TILE_SIZE_PX, RIGHT, HP_MAX, MP_MAX, GOLD, CORPSEPACK, Colors, DEBUG, LEFT, TOP, BOTTOM, \
    HEIGHT, WIDTH
from src.core.utils import get_topleft, debug


class BaseCharacter(pygame.sprite.Sprite):
    def __init__(self, name: str, coords: tuple, map_level: 'MapLevel' = None):
        super().__init__()
        self.name = name
        self.x, self.y = coords
        self.map_level = map_level
        self.hp = HP_MAX
        self.mp = MP_MAX
        self.level = 1
        self.alive = True
        self.direction = RIGHT
        self.gold = GOLD
        self.moving = [0, 0, 0, 0]
        self.projectile_objects = []
        self.charpack_list = []
        self.corpsepack_list = []
        self.load_character_sprites()
        self.image = self.charpack_list[self.direction]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.accel_x = 0
        self.accel_y = 0
        self.can_move = True

    def load_character_sprites(self):
        characterpack = pygame.image.load('data/player1.png').convert_alpha()
        charpack_list = [
            characterpack.subsurface(0, 0, TILE_SIZE_PX, TILE_SIZE_PX),
            characterpack.subsurface(TILE_SIZE_PX, 0, TILE_SIZE_PX, TILE_SIZE_PX),
            characterpack.subsurface(TILE_SIZE_PX * 2, 0, TILE_SIZE_PX, TILE_SIZE_PX),
            characterpack.subsurface(TILE_SIZE_PX * 3, 0, TILE_SIZE_PX, TILE_SIZE_PX)
        ]

        # TODO: use 32x32px corsepack
        corpsepack = pygame.image.load(CORPSEPACK).convert_alpha()
        corpsepack_list = [
            corpsepack.subsurface(0, 0, 270, 260),
            corpsepack.subsurface(270, 0, 270, 260),
            corpsepack.subsurface(540, 0, 240, 260),
            corpsepack.subsurface(780, 0, 250, 260)
        ]
        for i, subcorpse in enumerate(corpsepack_list):
            corpsepack_list[i] = pygame.transform.scale(
                subcorpse,
                (TILE_SIZE_PX, TILE_SIZE_PX)
            )

        self.charpack_list = charpack_list
        self.corpsepack_list = corpsepack_list

    def process_input(self, event):
        print('Processing needed player input...')

    def update(self):
        self.projectiles_move()
        if self.alive:
            sub_dict = self.charpack_list
        else:
            sub_dict = self.corpsepack_list
        self.image = sub_dict[self.direction]

    def projectiles_move(self):
        for projectile in self.projectile_objects:
            if projectile.flew_away():
                self.projectile_objects.remove(projectile)
            else:
                projectile.move()

    def render(self, screen):
        self.projectiles_render(screen)
        coords = (self.x, self.y)
        screen.blit(self.image, coords)
        self.render_wasd(screen)

    def projectiles_render(self, screen):
        for projectile in self.projectile_objects:
            projectile.render(screen)

    @debug
    def render_wasd(self, screen) -> None:
        """Draw WASD keys and show which of them are currently pressed."""
        place_x = WIDTH - 4 * TILE_SIZE_PX
        place_y = HEIGHT - 2 * TILE_SIZE_PX
        size = TILE_SIZE_PX // 2
        top = pygame.Rect(place_x, place_y, size, size)
        left = pygame.Rect(place_x - size - 1, place_y + size + 1, size, size)
        bottom = pygame.Rect(place_x, place_y + size + 1, size, size)
        right = pygame.Rect(place_x + size + 1, place_y + size + 1, size, size)
        if self.moving[TOP]:
            top_color = Colors.RED
        else:
            top_color = Colors.WHITE
        if self.moving[LEFT]:
            left_color = Colors.RED
        else:
            left_color = Colors.WHITE
        if self.moving[BOTTOM]:
            bottom_color = Colors.RED
        else:
            bottom_color = Colors.WHITE
        if self.moving[RIGHT]:
            right_color = Colors.RED
        else:
            right_color = Colors.WHITE

        pygame.draw.rect(screen, top_color, top, 1)
        pygame.draw.rect(screen, left_color, left, 1)
        pygame.draw.rect(screen, bottom_color, bottom, 1)
        pygame.draw.rect(screen, right_color, right, 1)

    def kill(self):
        self.alive = self.can_move = False
        self.hp = 0
        self.mp = 0

    def resurrect(self):
        self.alive = self.can_move = True
        self.hp = 100
        self.mp = 100
