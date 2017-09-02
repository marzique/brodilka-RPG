import os

# window and graphic settings
WIDTH = 800
HEIGHT = 600
FPS = 60

# player's image scaling  (велосипед жоский)
scale = 0.5

# images
BACKGROUND = 'data/tempground.jpg'
PLAYERPACK = 'data/RLUD.png'
CORPSEPACK = 'data/CORPSE.png'

# titles
WINDOW_NAME = 'SHITTY GAME'
PLAYER_NAME = 'marz420'

# player movement and position binds
CHAR_R = 0  #1
CHAR_L = 1  #2
CHAR_U = 2  #3
CHAR_D = 3  #4

GORIGHT = [1, 0, 0, 0]
GOLEFT = [0, 1, 0, 0]
GOUP = [0, 0, 1, 0]
GODOWN = [0, 0, 0, 1]

                # PLAYERS subPICTURE HITBOX
LEFT_GAP = 20
UP_GAP = 20
RIGHT_GAP = 100
DOWN_GAP = 140

ALIVE = 1
DEAD = 0

START_X = 50
START_Y = 50

# Player characteristics
HP_MAX = 100
MP_MAX = 100
HP_REGEN = 0.1
MP_REGEN = 0.05
GOLD = 200
GOLD_REGEN = 1
SHOT_MP = 5

PLAYER_SPEED = 5
BULLET_SPEED = 12
BULLET_DISTANCE = 1000
BULLETS_CD = 10

# Mobs

MOB_SPEED = 4
START_X_MOB = START_X + 500 * scale
START_Y_MOB = START_Y + 500 * scale
# MAGE


# Time parameters
TIME_CD = 1500  # 1.5 ms

# fonts
FONT1 = 'data/fonts/hachicro.ttf'
FONT2 = 'data/fonts/Fipps-Regular.otf'

# GUI
HPMP_THICKNESS = 3
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
