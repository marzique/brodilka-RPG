import pygame

from src import constants
from src.characters.base_character import BaseCharacter
from src.projectiles import Bullet


class Player(BaseCharacter):
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
        """
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                self.moving[0] = 1
            if keys[pygame.K_a]:
                self.moving[1] = 1
            if keys[pygame.K_w]:
                self.moving[2] = 1
            if keys[pygame.K_s]:
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

    def shoot(self):
        # TODO: refactor this mess
        if self.mp >= constants.SHOT_MP:
            if self.hand_shots < constants.BULLETS_CD and self.alive:

                if self.direction == constants.CHAR_D:
                    if self.hand == 0:
                        self.projectile_objects.append(
                            Bullet(
                                self.x + 160 * constants.SCALE,
                                self.y + 260 * constants.SCALE,
                                self.direction
                            )
                        )
                        self.hand = 1
                        self.hand_shots += 1
                    elif self.hand == 1:
                        self.projectile_objects.append(
                            Bullet(
                                self.x + 50 * constants.SCALE,
                                self.y + 260 * constants.SCALE,
                                self.direction
                            )
                        )
                        self.hand = 0
                        self.hand_shots += 1
                if self.direction == constants.CHAR_U:
                    if self.hand == 0:
                        self.projectile_objects.append(
                            Bullet(
                                self.x + 150 * constants.SCALE,
                                self.y + 50 * constants.SCALE,
                                self.direction
                            )
                        )
                        self.hand = 1
                        self.hand_shots += 1
                    elif self.hand == 1:
                        self.projectile_objects.append(
                            Bullet(
                                self.x + 40 * constants.SCALE,
                                self.y + 50 * constants.SCALE,
                                self.direction)
                        )
                        self.hand = 0
                        self.hand_shots += 1
                if self.direction == constants.CHAR_R:
                    if self.hand == 0:
                        self.projectile_objects.append(
                            Bullet(
                                self.x + 200 * constants.SCALE,
                                self.y + 130 * constants.SCALE,
                                self.direction
                            )
                        )
                        self.hand = 1
                        self.hand_shots += 1
                    elif self.hand == 1:
                        self.projectile_objects.append(
                            Bullet(
                                self.x + 200 * constants.SCALE,
                                self.y + 170 * constants.SCALE,
                                self.direction
                            )
                        )
                        self.hand = 0
                        self.hand_shots += 1
                if self.direction == constants.CHAR_L:
                    if self.hand == 0:
                        self.projectile_objects.append(
                            Bullet(
                                self.x + 10 * constants.SCALE,
                                self.y + 130 * constants.SCALE,
                                self.direction
                            )
                        )
                        self.hand = 1
                        self.hand_shots += 1
                    elif self.hand == 1:
                        self.projectile_objects.append(
                            Bullet(
                                self.x + 10 * constants.SCALE,
                                self.y + 170 * constants.SCALE,
                                self.direction
                            )
                        )
                        self.hand = 0
                        self.hand_shots += 1
                self.mp -= constants.SHOT_MP
