import pygame
from pygame.sprite import Sprite

class Obstacle(Sprite):
    def __init__(self, x, y, is_solid=True, color=(255, 0, 0), width=50, height=50):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        # Fill image with a semi-transparent red color (debug!)
        self.image.fill((255, 0, 0, 120))  # semi-visible for debugging

        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_solid = is_solid

        if is_solid:
            # Ensure the mask is nonempty and fills the block
            solid_surface = pygame.Surface((width, height))
            solid_surface.fill((255, 255, 255))  # white for collision mask
            self.mask = pygame.mask.from_surface(solid_surface)
        else:
            self.mask = None


class Wall(Obstacle):
    # An invisible solid wall for collisions
    def __init__(self, x, y, width=50, height=50):
        super().__init__(x, y, is_solid=True, color=(255, 0, 0), width=width, height=height)


class WallLine:
    # Easily create a line of walls (horizontal or vertical)
    def __init__(self, start_x, start_y, num_blocks, direction='horizontal', block_width=50, block_height=50):
        self.start_x = start_x
        self.start_y = start_y
        self.num_blocks = num_blocks
        self.direction = direction
        self.block_width = block_width
        self.block_height = block_height

    def build(self, all_sprites, solid_obstacles):
        for i in range(self.num_blocks):
            if self.direction == 'horizontal':
                x = self.start_x + i * self.block_width
                y = self.start_y
            else:  # vertical
                x = self.start_x
                y = self.start_y + i * self.block_height

            wall = Wall(x, y, width=self.block_width, height=self.block_height)
            all_sprites.add(wall)
            solid_obstacles.add(wall)


class Decoration(Obstacle):
    # A decoration object without collision
    def __init__(self, x, y):
        super().__init__(x, y, is_solid=False, color=(100, 200, 100))
