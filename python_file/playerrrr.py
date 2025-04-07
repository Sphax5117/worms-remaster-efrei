import pygame
from pathlib import Path

# Get the absolute path to the current file's directory
base_path = Path(__file__).resolve().parent

# For non‐animated directions, we still use single images:
grand_mere_down = base_path / '..' / 'frame grand mère' / 'tile132.png'
grand_mere_up   = base_path / '..' / 'frame grand mère' / 'tile132.png'

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

    def clear(self):
        self.keys.clear()

class Entity(pygame.sprite.Sprite):
    def __init__(self, keylistener: Keylistener):
        super().__init__()
        self.keylistener = keylistener

        # Load left animation frames (frame117 to frame125)
        self.left_frames = []
        for frame in range(117, 126):
            frame_path = base_path / '..' / 'frame grand mère' / f'tile{frame}.png'
            image = pygame.image.load(str(frame_path)).convert_alpha()
            self.left_frames.append(image)

        # Single images for up and down directions
        self.images = {
            "down": pygame.image.load(str(grand_mere_down)).convert_alpha(),
            "up": pygame.image.load(str(grand_mere_up)).convert_alpha()
        }

        # Start with a default image (down direction)
        self.image = self.images["down"]
        self.position = [100, 100]
        self.rect = self.image.get_rect(topleft=self.position)

        # Animation settings for left/right animations
        self.current_frame = 0       # Which frame in the left_frames list is being displayed
        self.animation_timer = 0.0   # Timer accumulator (in seconds)
        self.animation_speed = 0.015  # Reduced time per frame (faster animation)

    def update(self):
        self.check_move()
        self.rect.topleft = self.position

    def check_move(self):
        # Check key states (priority order)
        if self.keylistener.key_pressed(pygame.K_LEFT):
            self.move_left()
        elif self.keylistener.key_pressed(pygame.K_RIGHT):
            self.move_right()
        elif self.keylistener.key_pressed(pygame.K_UP):
            self.move_up()
        elif self.keylistener.key_pressed(pygame.K_DOWN):
            self.move_down()

    def animate(self):
        # Increase the timer assuming update is called about 60 times per second
        self.animation_timer += 1 / 60.0
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0  # reset timer
            # Cycle through the available frames
            self.current_frame = (self.current_frame + 1) % len(self.left_frames)

    def move_left(self):
        self.position[0] -= 5
        self.animate()  # update frame animation
        self.image = self.left_frames[self.current_frame]

    def move_right(self):
        self.position[0] += 5
        self.animate()  # update frame animation
        # For right, flip the left frame horizontally
        self.image = pygame.transform.flip(self.left_frames[self.current_frame], True, False)

    def move_up(self):
        self.position[1] -= 5
        self.image = self.images["up"]

    def move_down(self):
        self.position[1] += 5
        self.image = self.images["down"]
