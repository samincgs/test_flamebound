import pygame
import math

from .utils import normalize, outline

class Entity:
    def __init__(self, game, pos, size, e_type):
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.type = e_type
        
        self.active_animation = None
        self.action = None
        
        self.rotation = 0
        self.flip = [False, False]
        self.outline = False
        
        if not self.active_animation:
            self.set_action('idle')
                
    @property
    def img(self):
        if self.active_animation:
            img = self.active_animation.img
        if any(self.flip):
            img = pygame.transform.flip(img, self.flip[0], self.flip[1])
        if self.rotation:
            img = pygame.transform.rotate(img, self.rotation)
        return img
                
    @property 
    def center(self):
        return [self.pos[0] + self.size[0] // 2, self.pos[1] + self.size[1] // 2]
    
    @property
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    @property
    def anim_offset(self):
        offset = (0, 0)
        if self.active_animation:
            offset = self.active_animation.config['offset']
        return offset
    
    def set_action(self, action, force=False):
        if force or action != self.action:
            self.action = action
            self.active_animation = self.game.animations.new(self.type + '/' + self.action)
    
    def update(self, dt):
        if self.active_animation:
            self.active_animation.update(dt)
        
    
    def render(self, surf, offset=(0, 0)):
        img = self.img
        pos = ((self.pos[0] - offset[0] - self.anim_offset[0]), (self.pos[1] - offset[1] - self.anim_offset[1]))
        # if self.active_animation.outline:
        #     outline(surf, img, pos, self.active_animation.outline)
        surf.blit(img, pos)
        # pygame.draw.rect(surf, (255, 0, 0), pygame.Rect(int(self.pos[0] - offset[0]), int((self.pos[1] - offset[1])), *self.size), 1)
        
class PhysicsEntity(Entity):
    def __init__(self, game, pos, size, e_type):
        super().__init__(game, pos, size, e_type)
        self.speed = 0
        self.velocity = [0, 0]
        self.frame_movement = [0, 0]
        self.last_movement = [0, 0]
        self.velocity_normalization = [0, 0]
        self.acceleration = [0, 0]
        self.terminal_velocity = [250, 700]
        
        self.collision_directions = {'up': False, 'down': False, 'right': False, 'left': False}
    
    def physics_update(self, dt):   
        super().update(dt)  
        
        self.frame_movement[0] += self.velocity[0] * dt
        self.frame_movement[1] += self.velocity[1] * dt

        self.physics_movement(self.game.tilemap, movement=self.frame_movement)
        
        self.last_movement = self.frame_movement.copy()
        
        self.velocity[0] += self.acceleration[0] * dt
        self.velocity[1] += self.acceleration[1] * dt
        
        self.velocity[0] = min(self.velocity[0], self.terminal_velocity[0])
        self.velocity[1] = min(self.velocity[1], self.terminal_velocity[1])
        
        self.velocity[0] = normalize(self.velocity[0], self.velocity_normalization[0] * dt)
        self.velocity[1] = normalize(self.velocity[1], self.velocity_normalization[1] * dt)
                
        self.frame_movement = [0, 0]

           
    def move(self, movement, dt):
        self.frame_movement[0] += movement[0] * dt
        self.frame_movement[1] += movement[1] * dt
    
    def physics_movement(self, tilemap, movement=(0, 0)):
        self.collision_directions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        self.pos[0] += movement[0]
        tile_rects = tilemap.get_nearby_rects(self.center)
        collision_rects = tilemap.collision_check(self.rect, tile_rects)
        entity_rect = self.rect
        for rect in collision_rects:
            if movement[0] > 0:
                entity_rect.right = rect.left
                self.pos[0] = entity_rect.x
                self.collision_directions['right'] = True
            if movement[0] < 0:
                entity_rect.left = rect.right
                self.pos[0] = entity_rect.x
                self.collision_directions['left'] = True
            
        self.pos[1] += movement[1]
        tile_rects = tilemap.get_nearby_rects(self.center)
        collision_rects = tilemap.collision_check(self.rect, tile_rects)
        entity_rect = self.rect
        for rect in collision_rects:
            if movement[1] > 0:
                entity_rect.bottom = rect.top
                self.pos[1] = entity_rect.y
                self.collision_directions['down'] = True
            if movement[1] < 0:
                entity_rect.top = rect.bottom
                self.pos[1] = entity_rect.y
                self.collision_directions['up'] = True

            
        
                
        

                
        

        

            
