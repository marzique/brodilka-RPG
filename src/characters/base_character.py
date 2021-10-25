import pygame

from src import constants
from src.constants import TILE_SIZE_PX
from src.core.utils import draw_outline


class BaseCharacter:
    def __init__(self, name: str, coords: tuple):
        self.name = name
        self.x, self.y = coords
        self.hp = constants.HP_MAX
        self.mp = constants.MP_MAX
        self.level = 1
        self.alive = True
        self.direction = constants.CHAR_R
        self.gold = constants.GOLD
        self.moving = [0, 0, 0, 0]
        self.projectile_objects = []
        self.charpack_list, self.corpsepack_list = self.load_character_sprites()
        self.image = None
        self.can_move = True
        self.size = (constants.CHARACTER_HEIGHT, constants.CHARACTER_WIDTH)

    @property
    def rect(self):
        height, width = self.size
        return pygame.Rect(self.x, self.y, height, width)

    @staticmethod
    def load_character_sprites():
        characterpack = pygame.image.load('data/player1.png').convert_alpha()
        charpack_list = [
            # TODO: fixed tile values
            characterpack.subsurface(0, 0, 31, 31),
            characterpack.subsurface(31, 0, 31, 31),
            characterpack.subsurface(63, 0, 31, 31),
            characterpack.subsurface(95, 0, 31, 31)
        ]

        # TODO: use 32x32px corsepack
        corpsepack = pygame.image.load(constants.CORPSEPACK).convert_alpha()
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

        return charpack_list, corpsepack_list

    def process_input(self, event):
        print('Processing needed player input...')

    def update(self):
        self.image = self.get_current_image()
        self.move()
        self.projectiles_move()

    def render(self, screen):
        coords = (self.x, self.y)
        for projectile in self.projectile_objects:
            projectile.render(screen)
        screen.blit(self.image, coords)
        if constants.DEBUG:
            draw_outline(screen, self.image, coords)

    def get_current_image(self):
        if self.alive:
            sub_dict = self.charpack_list
        else:
            sub_dict = self.corpsepack_list
        return sub_dict[self.direction]

    def projectiles_move(self):
        for projectile in self.projectile_objects:
            if projectile.flew_away():
                self.projectile_objects.remove(projectile)
            else:
                projectile.move()

    def move(self):
        print('Trying to move...')

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
