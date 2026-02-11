import pygame as pg
from pygame.sprite import Sprite
from settings import *

vec = pg.math.Vector2

class Player(Sprite):
    def __init__(self, game, x, y):
        # basic variables
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
    
    def get_keys(self):
        self.vel = vec(0, 0)

        # determine the direction of movement based on key presses
        keys = pg.key.get_pressed()
        if keys[pg.K_a]: self.vel.x = -1
        if keys[pg.K_d]: self.vel.x = 1
        if keys[pg.K_w]: self.vel.y = -1
        if keys[pg.K_s]: self.vel.y = 1

        # normalize the vector so all directions have the same speed
        # multiply by PLAYER_SPEED to make it move at the desired speed
        if self.vel.magnitude() != 0:
            self.vel = (self.vel / self.vel.magnitude()) * PLAYER_SPEED

    def update(self):
        # get WASD input
        self.get_keys()

        # update player position based on input
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt

class Mob(Sprite):
    def __init__(self, game, x, y):
        # basic variables
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel = vec(1, 0)
        self.pos = vec(x, y) * TILESIZE
        self.speed = 5
    
    def update(self):
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed *= -1
            self.pos.y += TILESIZE
        self.pos += self.speed * self.vel
        self.rect.center = self.pos

class Wall(Sprite):
    def __init__(self, game, x, y):
        # basic variables
        self.groups = game.all_sprites, game.walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
    
    def update(self):
        pass

class Collectible(Sprite):
    def __init__(self, game, x, y):
        # basic variables
        self.groups = game.all_sprites, game.collectibles
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
    
    def update(self):
        pass
