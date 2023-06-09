import math
RESOLUTION = WIDTH, HEIGHT = 1280, 720
FRAMERATE= 60
PLAYER_POS = 1.5, 5.5
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_ROTATION_SPEED = 0.005
MOVEMENT_DELAY = 1000
ROTATION_DELAY = 1000
FOV = math.pi/3
HALF_FOV = FOV/2
RAY_AMOUNT = WIDTH//2 #floor div in python, in case i forgot about it myself. (i too dumb to remember)
HALF_RAY_AMOUNT = RAY_AMOUNT /2
DELTA_ANGLE = FOV/RAY_AMOUNT
DRAW_DISTANCE = 20

SCREEN_DISTANCE = (WIDTH//2)/ math.tan(HALF_FOV)
TEXTURE_SCALE = WIDTH//RAY_AMOUNT #maintain performance without spending too much resource on textures.
TEXTURE_SIZE = 64
FLOOR_COLOR = 255,255,255