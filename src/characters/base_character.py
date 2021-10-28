import pygame

from src.constants import TILE_SIZE_PX, CHAR_R, HP_MAX, MP_MAX, GOLD, CORPSEPACK, Colors, DEBUG
from src.core.utils import get_topleft


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
        self.direction = CHAR_R
        self.gold = GOLD
        self.moving = [0, 0, 0, 0]
        self.projectile_objects = []
        self.charpack_list = []
        self.corpsepack_list = []
        self.load_character_sprites()
        self.image = self.charpack_list[self.direction]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.rect_border = self.get_rect_border()
        self.colliding_blockers = {}
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
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.rect_border = self.get_rect_border()

    def projectiles_move(self):
        for projectile in self.projectile_objects:
            if projectile.flew_away():
                self.projectile_objects.remove(projectile)
            else:
                projectile.move()

    def get_rect_border(self):
        return pygame.Rect(self.rect.left - 1, self.rect.top - 1, TILE_SIZE_PX + 2, TILE_SIZE_PX + 2)

    def render(self, screen):
        self.projectiles_render(screen)
        coords = (self.x, self.y)
        screen.blit(self.image, coords)
        if DEBUG:
            self.highlight_colliding_tiles(screen)

    def projectiles_render(self, screen):
        for projectile in self.projectile_objects:
            projectile.render(screen)

    def highlight_colliding_tiles(self, screen):
        for x, y in self.get_colliding_tiles_toplefts():
            tile_rect = pygame.Rect(x, y, TILE_SIZE_PX, TILE_SIZE_PX)
            pygame.draw.rect(screen, Colors.RED, tile_rect, 1)

    def update_blockers(self):
        blockers = {}
        names = ['topleft', 'topright', 'bottomleft', 'bottomright']
        for i, coords in enumerate(self.get_colliding_tiles_toplefts()):
            if self.map_level.is_blocker(*coords):
                tile_rect = pygame.Rect(*coords, TILE_SIZE_PX, TILE_SIZE_PX)
                blockers[names[i]] = tile_rect
        self.colliding_blockers = blockers

    def get_colliding_tiles_toplefts(self):
        x, y = get_topleft(self.x, self.y)
        corners = [
            (x, y),
            (x + TILE_SIZE_PX, y),
            (x, y + TILE_SIZE_PX),
            (x + TILE_SIZE_PX, y + TILE_SIZE_PX)
        ]
        return corners

    def kill(self):
        self.alive = self.can_move = False
        self.hp = 0
        self.mp = 0

    def resurrect(self):
        self.alive = self.can_move = True
        self.hp = 100
        self.mp = 100
