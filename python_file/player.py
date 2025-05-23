import pygame
from pathlib import Path
from pygame.sprite import Sprite

class Keylistener:
    def __init__(self):
        self.keys = []
    
    def add_key(self, key):
        if key not in self.keys:
            self.keys.append(key)
    
    def remove_key(self, key):
        if key in self.keys:
            self.keys.remove(key)
    
    def key_pressed(self, key):
        return key in self.keys

class Player(Sprite):
    def __init__(self, keylistener, x=100, y=100, costume = None):
        super().__init__()
        self.keylistener = keylistener
        base_path = Path(__file__).resolve().parent

        #for the mamy
        if costume == "mamy":

            #loading animations
            self.left_frames = []
            for frame in range(117, 126):
                frame_path = base_path / '..' / 'frame grand mère' / f'tile{frame}.png'
                image = pygame.image.load(str(frame_path)).convert_alpha()
                self.left_frames.append(image)

            #static images
            self.images = {
                "down": pygame.image.load(str(base_path / '..' / 'frame grand mère' / 'tile132.png')).convert_alpha(),
                "up": pygame.image.load(str(base_path / '..' / 'frame grand mère' / 'tile132.png')).convert_alpha(),
                "still" : pygame.image.load(str(base_path / '..' / 'frame grand mère' / 'tile080.png')).convert_alpha()
            }
        
        #for the papy
        elif costume == "papy":

            #loading animations
            self.left_frames = []
            for frame in range(117, 126):
                frame_path = base_path / '..' / 'frame papy' / f'tile{frame}.png'
                image = pygame.image.load(str(frame_path)).convert_alpha()
                self.left_frames.append(image)

            #static images
            self.images = {
                "down": pygame.image.load(str(base_path / '..' / 'frame papy' / 'tile132.png')).convert_alpha(),
                "up": pygame.image.load(str(base_path / '..' / 'frame papy' / 'tile132.png')).convert_alpha(),
                "still" : pygame.image.load(str(base_path / '..' / 'frame papy' / 'tile080.png')).convert_alpha()
            }

        self.image = self.images["down"]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
        self.current_frame = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.015
        self.mask = pygame.mask.from_surface(self.image)

        #gravity and jump
        self.velocity_y = 0
        self.gravity = 0.4     #gentler gravity
        self.jump_strength = -15  #jump more powerful (higher)
        self.on_ground = False

        #nervous jump
        self.is_jumping = False
        self.jump_cut_power = 0.4  #cut less violently for small jumps

    def update(self, obstacles):
        self.apply_gravity()
        self.handle_movement()
        self.handle_collision(obstacles)

    def apply_gravity(self):
        self.velocity_y += self.gravity
        self.rect.y += int(self.velocity_y)

    def handle_movement(self):
        self.is_moving = False

        if self.keylistener.key_pressed(pygame.K_LEFT):
            self.move_left()
            self.is_moving = True
        if self.keylistener.key_pressed(pygame.K_RIGHT):
            self.move_right()
            self.is_moving = True

        #beginning of the jump
        if self.keylistener.key_pressed(pygame.K_UP) and self.on_ground:
            self.velocity_y = self.jump_strength
            self.on_ground = False
            self.is_jumping = True

        #nervous jump (if you release space key during a jump)
        if not self.keylistener.key_pressed(pygame.K_UP) and self.is_jumping:
            if self.velocity_y < 0:  #only if we go up
                self.velocity_y *= self.jump_cut_power
            self.is_jumping = False
    
        if not self.is_moving:
            self.set_idle_image()

    def set_idle_image(self):
        self.image = self.images["still"]
        self.mask = pygame.mask.from_surface(self.image)

    def animate(self):
        self.animation_timer += 1 / 60.0
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.left_frames)

    def move_left(self):
        self.rect.x -= self.speed
        self.animate()
        self.image = self.left_frames[self.current_frame]
        self.mask = pygame.mask.from_surface(self.image)

    def move_right(self):
        self.rect.x += self.speed
        self.animate()
        self.image = pygame.transform.flip(self.left_frames[self.current_frame], True, False)
        self.mask = pygame.mask.from_surface(self.image)

    def handle_collision(self, obstacles):
        self.on_ground = False

        #vertical collision
        for obstacle in obstacles:
            if pygame.sprite.collide_mask(self, obstacle):
                if self.velocity_y > 0:  # Tombe
                    self.rect.bottom = obstacle.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.is_jumping = False
                elif self.velocity_y < 0:  # Monte
                    self.rect.top = obstacle.rect.bottom
                    self.velocity_y = 0

        #horizontal collision
        for obstacle in obstacles:
            if pygame.sprite.collide_mask(self, obstacle):
                if self.keylistener.key_pressed(pygame.K_LEFT):
                    self.rect.left = obstacle.rect.right
                if self.keylistener.key_pressed(pygame.K_RIGHT):
                    self.rect.right = obstacle.rect.left
