import pygame
import time

from scripts.assets import Assets
from scripts.input import Input
from scripts.tilemap import Tilemap
from scripts.player import Player

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Flamebound')
        
        self.screen = pygame.display.set_mode((750, 600))
        self.display = pygame.Surface((250, 200))
        self.clock = pygame.time.Clock()
        
        self.input = Input()
        self.assets = Assets()
        self.animations = self.assets.animations
        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load_map('data/maps/map_2.json') 
        
        self.dt = 0.1
        self.player = Player(self, (400, 200), (8, 16))

        self.scroll = [0, 0]
    
    
    def run(self):
        while True:
            
            self.display.fill((0, 0, 0))

            self.scroll[0] += (self.player.center[0] - self.display.get_width() // 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.center[1] - self.display.get_height() // 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render_visible(self.display, render_scroll)
            
            self.player.update(self.dt)
            self.player.render(self.display, render_scroll)
            
            self.input.update()
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.dt = self.clock.tick(60) / 1000
                
if __name__ == '__main__':
    Game().run()


    