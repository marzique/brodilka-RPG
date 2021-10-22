from src import constants
from src.characters.base_character import BaseCharacter
from src.projectiles import Bullet


class Player(BaseCharacter):
    def shoot(self):
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
