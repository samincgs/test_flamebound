import pygame

from .utils import palette_swap

class Particle:
    def __init__(self, game, pos, velocity, p_type, decay_rate=0.1, start_frame=0, custom_color=None, physics=None):
        self.game = game
        self.pos = list(pos)
        self.velocity = velocity
        self.type = p_type
        self.decay_rate = decay_rate
        self.frame = start_frame
        self.custom_color = custom_color
        self.physics = physics
        
        self.rotation = 0
        
    @property
    def img(self):
        return self.game.assets[self.type][int(self.frame)]
       
    def update(self, dt):
        pass
    
    
    def render(self, surf, offset=(0, 0)):
        pass
        
        
            