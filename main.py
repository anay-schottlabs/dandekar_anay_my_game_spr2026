import pygame as pg
from pygame.locals import *
from settings import *
from sprites import *
from utils import *

# accesses the operating system
from os import path

# main game class
# will be instantiated to run the game
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) # define game window size
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True
        self.game_cooldown = Cooldown(5)
    
    # a method is a function tied to a Class
    def load_data(self):
        # accesses the file space that we're currently in
        # this can now access all files in the current directory
        self.game_dir = path.dirname(__file__)

        # creates a map with the "level1.txt file"
        # that is found in the current directory
        self.map = Map(path.join(self.game_dir, "level1.txt"))

        # logging that data was loaded successfully
        print("Loaded data.")

    def new(self):
        # load game data from file
        self.load_data()

        # groups to organize the sprites
        self.all_sprites = pg.sprite.Group()
        self.collectibles = pg.sprite.Group()
        self.walls = pg.sprite.Group()

        # instantiating some different types of sprites
        # self.player = Player(self, 15, 15)
        # self.mob = Mob(self, 4, 4)
        # self.coin1 = Collectible(self, 12, 5)
        # self.coin2 = Collectible(self, 10, 3)
        # self.coin3 = Collectible(self, 2, 9)
        # self.wall1 = Wall(self, 10, 10)

        for col, tiles in enumerate(self.map.data):
            for row, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, row, col)
                elif tile == "P":
                    self.player = Player(self, row, col)
                elif tile == "C":
                    Collectible(self, row, col)
                elif tile == "M":
                    Mob(self, row, col)

        self.run()

    def run(self):
        self.game_cooldown.start()

        while self.running:
            # delta time
            # divides by 1000 for milliseconds
            self.dt = self.clock.tick(FPS) / 1000

            # check to see if the player collides with the collectibles
            # if they do, the "True" part of this removes the collectible
            pg.sprite.spritecollide(self.player, self.collectibles, True)

            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            # quit event, closes the game
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def quit(self):
        pass

    def update(self):
        # update all sprites
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLUE)

        # writes some text on the screen
        self.draw_text("Hello World", 24, WHITE, WIDTH/2, TILESIZE)
        self.draw_text(str(self.game_cooldown.get_seconds()), 24, WHITE, WIDTH/2, HEIGHT/4)

        # render all of the sprites
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    # method to handle drawing text
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

if __name__ == "__main__":
    game = Game()

while game.running:
    game.new()

pg.quit()
