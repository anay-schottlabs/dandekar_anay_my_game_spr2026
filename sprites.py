import pygame as pg
from pygame.sprite import Sprite
from settings import *

vec = pg.math.Vector2

# returns True if both objects are colliding
# returns False if the objects are not colliding
def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

def collide_with_walls(sprite, group, dir):
    # collisions in the x direction
    if dir == "x":
        # get wall collisions
        # "False" means that we don't rmove the wall
        # after we collide with it
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            print("collided with wall from x dir")
            # check if the left side of the sprite hit the wall
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            # check if the right side of the sprite hit the wall
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            # reset the velocity if we hit a wall
            # so that we do not move through the wall
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    # collisions in the y direction
    if dir == "y":
        # get wall collisions
        # "False" means that we don't remove the wall
        # after we collide with it
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            print("collided with wall from y dir")
            # check if the top side of the sprite hit the wall
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            # check if the bottom side of the sprite hit the wall
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            # reset the velocity if we hit a wall
            # so that we do not move through the wall
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

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
        self.hit_rect = PLAYER_HIT_RECT
    
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

        # check wall collisions
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, "x")
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, "y")

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
        self.image = game.wall_image
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
        self.image = game.coin_image
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
    
    def update(self):
        pass
