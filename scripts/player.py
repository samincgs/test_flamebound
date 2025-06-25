from .entities import PhysicsEntity

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, 'player')
        self.air_time = 0
        self.speed = 85
        self.acceleration[1] = 450

        
    def update(self, dt):
                
        self.air_time += dt
        
        self.move(((self.game.input.holding('right') - self.game.input.holding('left')) * self.speed, 0), dt)
        if self.game.input.pressed('jump'):
            self.velocity[1] = -150
        
        if self.frame_movement[0] > 0:
            self.flip[0] = False
        if self.frame_movement[0] < 0:
            self.flip[0] = True
        
        if self.air_time > 0.1:
            self.set_action('jump')
        elif self.frame_movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')
        
        self.physics_update(dt)
        if self.collision_directions['down'] or self.collision_directions['up']:
            self.air_time = 0
            self.velocity[1] = 0
        
            
