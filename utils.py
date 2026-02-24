import pygame as pg
from settings import *

class Map:
    def __init__(self, filename):
        # creating the data for building a map using a list
        self.data = []

        with open(filename, "rt") as file:
            for line in file:
                self.data.append(line.strip())
        
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)

        print(self.tilewidth)
        print(self.tileheight)

        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
    
    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        new_image = pg.transform.scale(image, (width, height))
        image = new_image
        return image

# this class creates a countdown timer for a cooldown
class Cooldown:
    def __init__(self, time):
        self.start_time = 0
        self.time = time * 1000 # convert to ms
    
    def start(self):
        self.start_time = pg.time.get_ticks()
    
    def ready(self):
        # sets current time to 
        current_time = pg.time.get_ticks()
        # if the difference between current and start time are greater than self.time
        # return True
        if current_time - self.start_time >= self.time:
            return True
        return False
    
    def get_seconds(self):
        current_time = pg.time.get_ticks()
        return 0 if self.ready() else self.time - (current_time - self.start_time)
