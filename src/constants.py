import os
from dotenv import load_dotenv


##################################################### GAME OPTIONS ####################################################
# can be changed via .env file
load_dotenv()
WIDTH = int(os.getenv('WIDTH', 1280))
HEIGHT = int(os.getenv('HEIGHT', 720))
DEBUG = os.getenv('DEBUG', '').lower() == 'true'
#######################################################################################################################

TILE_SIZE_PX = 32

# player's image scaling  (велосипед жоский)
SCALE = 0.5

PLAYER_HEIGHT = 170
PLAYER_WIDTH = 100

# images
PLAYERPACK = 'data/RLUD.png'
CORPSEPACK = 'data/CORPSE.png'

# titles
WINDOW_NAME = 'RPG OPEN WORLD!'

# player movement and position binds
CHAR_D, CHAR_U, CHAR_R, CHAR_L = (0, 1, 2, 3)

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


class Fonts:
    main = 'data/fonts/manaspc.ttf'
    regular = 'data/fonts/Ubuntu-Regular.ttf'
    light = 'data/fonts/Ubuntu-Regular.ttf'
    bold = 'data/fonts/Ubuntu-Bold.ttf'


# GUI
HPMP_THICKNESS = 10


class Color:
    RED = (255, 0, 0)
    GREEN = (77, 146, 98)
    BLUE = (99, 155, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GOLD = (255, 219, 87)


class TileTypes:
    BLOCKER = 'blocker'
