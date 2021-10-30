import os
from dotenv import load_dotenv


load_dotenv()
# can be changed via .env file
WIDTH = int(os.getenv('WIDTH', 1280))
HEIGHT = int(os.getenv('HEIGHT', 720))
DEBUG = os.getenv('DEBUG', '').lower() == 'true'
#######################################################################################################################

TILE_SIZE_PX = 32
# player's image scaling
SCALE = 0.5
PLAYER_HEIGHT = 170
PLAYER_WIDTH = 100
# images
PLAYERPACK = 'data/RLUD.png'
CORPSEPACK = 'data/CORPSE.png'
# texts
WINDOW_NAME = 'RPG OPEN WORLD!'
# player movement and position binds
BOTTOM, TOP, RIGHT, LEFT = (0, 1, 2, 3)
# Player characteristics
HP_MAX = 100
MP_MAX = 100
HP_REGEN = 0.1
MP_REGEN = 0.05
GOLD = 200
GOLD_REGEN = 1
SHOT_MP = 5
PLAYER_SPEED = 1
BULLET_SPEED = 16
BULLET_DISTANCE = 1000
BULLETS_CD = 10
# Time parameters
TIME_CD = 1500  # 1.5 ms
# GUI
HPMP_THICKNESS = 10


class Colors:
    RED = (255, 0, 0)
    GREEN = (33, 255, 33)
    BLUE = (33, 55, 255)
    LTBLUE = (0, 229, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GOLD = (255, 219, 87)


class Fonts:
    main = 'data/fonts/manaspc.ttf'
    regular = 'data/fonts/Ubuntu-Regular.ttf'
    light = 'data/fonts/Ubuntu-Regular.ttf'
    bold = 'data/fonts/Ubuntu-Bold.ttf'


class TileTypes:
    BLOCKER = 'blocker'
