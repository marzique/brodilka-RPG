import pygame

from src.constants import TILE_SIZE_PX, CHAR_R, HP_MAX, MP_MAX, GOLD, CORPSEPACK, DEBUG
from src.core.utils import draw_outline


class BaseCharacter(pygame.sprite.Sprite):
    def __init__(self, name: str, coords: tuple):
        super().__init__()
        self.name = name
        self.x, self.y = coords
        self.hp = HP_MAX
        self.mp = MP_MAX
        self.level = 1
        self.alive = True
        self.direction = CHAR_R
        self.gold = GOLD
        self.moving = [0, 0, 0, 0]
        self.projectile_objects = []
        self.charpack_list, self.corpsepack_list = self.load_character_sprites()
        self.image = None
        self.rect = None
        self.update_current_image()
        self.can_move = True

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

        return charpack_list, corpsepack_list

    def process_input(self, event):
        print('Processing needed player input...')

    def update(self):
        self.update_current_image()

    def render(self, screen):
        coords = (self.x, self.y)
        for projectile in self.projectile_objects:
            projectile.render(screen)
        screen.blit(self.image, coords)
        if DEBUG:
            draw_outline(screen, self.image, coords)

    def update_current_image(self):
        if self.alive:
            sub_dict = self.charpack_list
        else:
            sub_dict = self.corpsepack_list
        self.image = sub_dict[self.direction]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

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
