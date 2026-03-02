import pygame as pg
from settings import *

class Map:
    def __init__(self, filename):
        # creating the data for building a map using a list
        self.data = []

        with open(filename, "rt") as file:
            # go over each line of the file
            for line in file:
                # each line is a new element in the list
                # strip() removes whitespace at the start and end of the line
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
        # template of the image with its width and height
        image = pg.Surface((width, height))
        # get a portion of the spritesheet via the parameters of this method
        # we first pass in the spritesheet image
        # next is the destination, which is the coordinates of the upper left corner of the entire spritesheet
        # the final argument is the rect for the portion we want
        # x and y are where the rect starts
        # width and height are the size of the portion of the image we're cutting
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # make sure that the image size is the desired size
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
