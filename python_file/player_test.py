import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, x=100, y=100):
        super().__init__()
        # Movement properties
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self.gravity = 0.35
        self.friction = -0.12
        self.max_speed = 4
        self.move_up_speed = -3
        self.move_down_speed = 3
        
        # State tracking
        self.on_ground = False
        self.facing_left = False
        
        # Animation frames
        self.animation_frames = {
            "left": [self._load_image("assets/frame grand mère/tile019.png")],
            "right": [self._load_image("assets/frame grand mère/tile041.png")],
            "up": [self._load_image("assets/frame grand mère/tile132.png")],
            "down": [self._load_image("assets/mamy frame couoée/tile117.png")]
        }
        self.current_animation = "down"
        self.image = self.animation_frames[self.current_animation][0]
        self.rect = self.image.get_rect(topleft=self.position)

    def _load_image(self, path):
        """Helper method to load images with error handling"""
        try:
            return pygame.image.load(path).convert_alpha()
        except:
            print(f"Failed to load image: {path}")
            surf = pygame.Surface((32, 32))
            surf.fill((255, 0, 255))
            return surf

    def update(self, dt, tilemap):
        """Update player position and state"""
        self._handle_input()
        self._apply_physics(dt)
        self._handle_collisions(tilemap.solid_tiles)
        self._update_animation_state()
        self.rect.topleft = self.position

    def _handle_input(self):
        """Handle keyboard input for movement"""
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -0.3
            self.facing_left = True
        elif keys[pygame.K_RIGHT]:
            self.acceleration.x = 0.3
            self.facing_left = False
        else:
            self.acceleration.x = 0
            
        # Vertical movement
        if keys[pygame.K_UP]:
            self.velocity.y = self.move_up_speed
        elif keys[pygame.K_DOWN]:
            self.velocity.y = self.move_down_speed

    def _apply_physics(self, dt):
        """Apply physics to movement"""
        # Apply friction to horizontal movement
        self.acceleration.x += self.velocity.x * self.friction
        
        # Update velocity
        self.velocity.x += self.acceleration.x * dt
        
        # Apply gravity only if not moving up/down
        if not (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_DOWN]):
            self.velocity.y += self.gravity
        
        # Limit speeds
        self.velocity.x = max(-self.max_speed, min(self.velocity.x, self.max_speed))
        self.velocity.y = min(self.velocity.y, 7)  # Terminal velocity
        
        # Update position
        self.position += self.velocity

    def _handle_collisions(self, solid_tiles):
        """Handle collisions with solid tiles"""
        # Store current position for collision testing
        old_position = self.position.copy()
        
        # Update rect position for collision detection
        self.rect.topleft = self.position
        
        # Reset ground state
        self.on_ground = False
        
        # Check collisions with all solid tiles
        for tile in solid_tiles:
            if self.rect.colliderect(tile.rect):
                # Horizontal collision
                if self.velocity.x > 0:  # Moving right into tile
                    self.position.x = tile.rect.left - self.rect.width
                elif self.velocity.x < 0:  # Moving left into tile
                    self.position.x = tile.rect.right
                self.velocity.x = 0
                
                # Vertical collision
                if self.velocity.y > 0:  # Landing on tile
                    self.position.y = tile.rect.top
                    self.on_ground = True
                    self.velocity.y = 0
                elif self.velocity.y < 0:  # Hitting tile from below
                    self.position.y = tile.rect.bottom
                    self.velocity.y = 0
                
                # Update rect to new position
                self.rect.topleft = self.position

    def _update_animation_state(self):
        """Update animation based on movement state"""
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            self.current_animation = "up"
        elif keys[pygame.K_DOWN]:
            self.current_animation = "down"
        elif self.velocity.x < -0.1:
            self.current_animation = "left"
        elif self.velocity.x > 0.1:
            self.current_animation = "right"
        else:
            self.current_animation = "down"  # Default to down animation
            
        self.image = self.animation_frames[self.current_animation][0]

    def draw(self, surface):
        """Draw the player"""
        surface.blit(self.image, self.rect)
