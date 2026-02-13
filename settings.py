import pygame as pg

# ----- game variables -----

WIDTH = 800
HEIGHT = 600
TITLE = "First Game"
FPS = 60
TILESIZE = 32

# ----- player values -----

# this value is removed from the player's hitbox size
# this allows it to move through small gaps easily
PLAYER_HITBOX_CLEARANCE = 5
PLAYER_SPEED = 500
PLAYER_HIT_RECT = pg.Rect(0, 0, TILESIZE - PLAYER_HITBOX_CLEARANCE, TILESIZE - PLAYER_HITBOX_CLEARANCE)

# ----- color values -----

# colors are stored as tuples with RGB values

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
