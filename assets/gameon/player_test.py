import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT = False, False, False
        self.is_jumping, self.on_ground = False, False
        self.gravity, self.friction = 0.35, -0.12
        # Load animation frames from image files
        self.frames = [
            pygame.image.load('assets\mamy frame couoée\tile117.png').convert_alpha(),
            pygame.image.load('assets\mamy frame couoée\tile118.png').convert_alpha(),
            pygame.image.load('assets\mamy frame couoée\tile119.png').convert_alpha(),
            pygame.image.load('assets\mamy frame couoée\tile120.png').convert_alpha()
        ]
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]  # Set first frame
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(0, 0)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)
        self.animation_timer = 0  # Timer to track animation speed

    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, dt, tiles):
        self.horizontal_movement(dt)
        self.checkCollisionx(tiles)
        self.vertical_movement(dt)
        self.checkCollisionsy(tiles)
    
    def animate(self, dt):
        """Cycles through frames to create an animation effect."""
        self.animation_timer += dt
        if self.animation_timer > 100:  # Change frame every 100 milliseconds
            self.animation_index = (self.animation_index + 1) % len(self.frames)
            self.image = self.frames[self.animation_index]
            self.animation_timer = 0

    def horizontal_movement(self, dt):
        self.acceleration.x = 0
        if self.LEFT_KEY:
            self.acceleration.x -= 0.3
        elif self.RIGHT_KEY:
            self.acceleration.x += 0.3

        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(4)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * 0.5) * (dt * dt)
        self.rect.x = self.position.x

    def vertical_movement(self, dt):
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 7:
            self.velocity.y = 7
        self.position.y += self.velocity.y * dt + (self.acceleration.y * 0.5) * (dt * dt)
        self.rect.bottom = self.position.y

    def limit_velocity(self, max_vel):
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
        if abs(self.velocity.x) < 0.01:
            self.velocity.x = 0

    def jump(self):
        if self.on_ground:
            self.is_jumping = True
            self.velocity.y -= 8
            self.on_ground = False

    def get_hits(self, tiles):
        return [tile for tile in tiles if self.rect.colliderect(tile.rect)]

    def checkCollisionx(self, tiles):
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.x > 0:
                self.position.x = tile.rect.left - self.rect.width
            elif self.velocity.x < 0:
                self.position.x = tile.rect.right
            self.velocity.x = 0
            self.rect.x = self.position.x

    def checkCollisionsy(self, tiles):
        self.on_ground = False
        self.rect.bottom += 1  
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.y > 0:
                self.on_ground = True
                self.is_jumping = False
                self.velocity.y = 0
                self.position.y = tile.rect.top
                self.rect.bottom = self.position.y
            elif self.velocity.y < 0:
                self.velocity.y = 0
                self.position.y = tile.rect.bottom + self.rect.height
                self.rect.top = self.position.y