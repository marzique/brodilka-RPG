from src import constants
from src.projectiles.base_projectile import BaseProjectile


class Bullet(BaseProjectile):
    IMAGE_FILE = 'data/BULLETS.png'
    SPEED = constants.BULLET_SPEED
