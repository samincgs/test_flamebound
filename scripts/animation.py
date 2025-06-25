import os

from .utils import load_imgs, load_json, save_json

ANIMATIONS_PATH = 'data/images/animations/'
COLORKEY = (0, 0, 0)

class Animation:
    def __init__(self, config, images):
        self.config = config
        self.images = images
        self.frame = 0
        self.frame_index = 0
                
    @property
    def img(self):
        return self.images[self.frame_index]
    
    @property
    def type(self):
        return self.config['type']
    
    @property
    def duration(self):
        return sum(self.config['frames'])
    
    @property
    def outline(self):
        return self.config['outline']
    
    def copy(self):
        return Animation(self.config, self.images)
        
    def update(self, dt):
        self.frame += dt * 60 * self.config['speed']
        if self.config['loop']:
            if self.frame > self.duration:
                self.frame -= self.duration
        
        self.frame_index = int(self.frame / self.duration * len(self.config['frames']))
        self.frame_index = min(self.frame_index, len(self.config['frames']) - 1)
        
class AnimationManager:
    def __init__(self):
        self.animations = {}
        self.generate_config() # save config if it isnt there
        
        # load animations
        for entity_id in os.listdir(ANIMATIONS_PATH):
            if os.path.isdir(ANIMATIONS_PATH + entity_id):  
                for anim_state in os.listdir(ANIMATIONS_PATH + entity_id):
                    animation_path = ANIMATIONS_PATH + entity_id + '/' + anim_state
                    if os.path.isdir(animation_path):
                        anim_id = entity_id + '/' + anim_state
                        config = load_json(ANIMATIONS_PATH + entity_id + '/' + 'config.json')['animations'][anim_state]
                        self.animations[anim_id] = Animation(config, load_imgs(f'{ANIMATIONS_PATH}{entity_id}/{anim_state}'))
                    
    
             
    def generate_config(self):
        if not os.path.isdir(ANIMATIONS_PATH):
            os.mkdir('data/images/animations')

        for entity_id in os.listdir(ANIMATIONS_PATH):  
            if os.path.isdir(ANIMATIONS_PATH + entity_id):  
                if 'config.json' not in os.listdir(ANIMATIONS_PATH + entity_id):
                    config = {"id": entity_id, "animations": {}}      
                    for anim_state in os.listdir(ANIMATIONS_PATH + entity_id):
                        config['animations'][anim_state] = {}
                        config['animations'][anim_state]['type'] = anim_state
                        config['animations'][anim_state]["frames"] = [5] * len(os.listdir(ANIMATIONS_PATH + entity_id + '/' + anim_state))
                        config['animations'][anim_state]["loop"] = False
                        config['animations'][anim_state]["speed"] = 1.0
                        config['animations'][anim_state]["offset"] = [0, 0]
                        config['animations'][anim_state]["outline"] = None
            
                    save_json(f'{ANIMATIONS_PATH}{entity_id}/config.json', config)
                                   
    def new(self, anim_id):
        return self.animations[anim_id].copy()