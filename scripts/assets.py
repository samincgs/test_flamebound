from .animation import AnimationManager
from .font import Font

FONT_PATH = 'data/fonts/'

class Assets:
    def __init__(self):
        
        self.animations = AnimationManager()
        
        self.fonts = {
            'white': Font(),
            'black': Font(font_color=(0, 0, 1))
        }