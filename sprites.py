import pygame as pg
from pygame.sprite import Sprite
from settings import *
from utils import *
from os import path

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
        # self.spritesheet = Spritesheet(path.join(game.img_dir, "player_art.png"))
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.hit_rect = PLAYER_HIT_RECT
        self.jumping = False
        self.walking = False
        self.frame_change_ticks = {
            "standing": 350,
            "jumping": 600,
            "walking": 500
        }
    
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

    def load_images(self):
        self.standing_frames = [
            # self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE),
            # self.spritesheet.get_image(TILESIZE, 0, TILESIZE, TILESIZE)
        ]

        self.jumping_frames = [
        ]

        self.walking_frames = [
        ]

        self.all_animations = [
            self.standing_frames,
            self.jumping_frames,
            self.walking_frames
        ]

        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        
        for animation in self.all_animations:
            for frame in animation:
                frame.set_colorkey(BLACK)
    
    def animate(self):
        now = pg.time.get_ticks()
        # standing animation
        if not self.jumping and not self.walking:
            if now - self.last_update < self.frame_change_ticks["standing"]:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
        # jumping animation
        elif self.jumping:
            if now - self.last_update < self.frame_change_ticks["jumping"]:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jumping)
        # walking animation
        elif self.walking:
            if now - self.last_update < self.frame_change_ticks["walking"]:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking)

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
        self.spritesheet = Spritesheet(path.join(game.img_dir, "coin_art.png"))
        self.load_images()
        self.image = self.spinning_frames[0]
        self.current_frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_change_ticks = 600
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
    
    # gets images for the coin's animation
    def load_images(self):
        # a list of all the frames in order
        self.spinning_frames = [
            # the first frame starts from the top left
            self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE),
            # the second frame is the top right
            self.spritesheet.get_image(TILESIZE, 0, TILESIZE, TILESIZE),
            # the third frame is on the bottom left
            self.spritesheet.get_image(0, TILESIZE, TILESIZE, TILESIZE),
            # the fourth frame is on the bottom right
            self.spritesheet.get_image(TILESIZE, TILESIZE, TILESIZE, TILESIZE)
        ]

        # any black pixels will be turned transparent
        for frame in self.spinning_frames:
            frame.set_colorkey(BLACK)
    
    def animate(self):
        # get the current time
        now = pg.time.get_ticks()
        # check if it's been a certain amount of time
        # this amount is specified in the constructor
        # it determines how long until we move to the next animation frame
        if now - self.last_update > self.frame_change_ticks:
            # reset the time
            self.last_update = now
            # use the next frame
            # the % is the modulo operator, it does division and gets the remainder
            # if the +1 is out of bounds, the math works out to return a zero
            # this zero is the first index in the array and restarts the animation
            # it lets everything loop smoothly
            self.current_frame = (self.current_frame + 1) % len(self.spinning_frames)
            # set the current image of the sprite to the current animation frame
            self.image = self.spinning_frames[self.current_frame]
    
    def update(self):
        self.animate()
