from src.constants import BULLET_SPEED
from src.projectiles.base_projectile import BaseProjectile


class Bullet(BaseProjectile):
    IMAGE_FILE = 'data/BULLETS.png'
    SPEED = BULLET_SPEED
