import pygame
import os
from sys import exit
from playerrrr import Keylistener, Entity
from pathlib import Path

# Get the absolute path to the current file's directory
base_path = Path(__file__).resolve().parent

# Define paths to assets
BG_PATH = base_path / '..' / 'assets' / 'gameon' / 'bg.png'
CLOUD2_PATH = base_path / '..' / 'assets' / 'gameon' / '3.png'
CLOUD3_PATH = base_path / '..' / 'assets' / 'gameon' / '4.png'
CLOUD4_PATH = base_path / '..' / 'assets' / 'gameon' / '5.png'
MAP_PATH = base_path / '..' / 'assets' / 'gameon' / 'maptest.png'


def game_on(screen, screensize):
    # Force window to top-left
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
    pygame.init()

    pygame.display.set_caption("Funny Granny")

    # (Optional) If you want to enable hardware acceleration,
    # you could recreate the screen with flags. For example:
    # screen = pygame.display.set_mode(screensize, pygame.DOUBLEBUF | pygame.HWSURFACE)
    # Note that not all systems support these flags.

    screen_width, screen_height = screensize

    # Load and scale images (do this only once)
    background_img = pygame.transform.scale(pygame.image.load(str(BG_PATH)), (screen_width, screen_height))
    cloud_layer_2 = pygame.transform.scale(pygame.image.load(str(CLOUD2_PATH)), (screen_width, screen_height - 10))
    cloud_layer_3 = pygame.transform.scale(pygame.image.load(str(CLOUD3_PATH)), (screen_width, screen_height - 10))
    cloud_layer_4 = pygame.transform.scale(pygame.image.load(str(CLOUD4_PATH)), (screen_width, screen_height - 10))
    maps_img = pygame.transform.smoothscale(pygame.image.load(str(MAP_PATH)), (screen_width, screen_height))

    # Cloud positions and speeds
    cloud_x_2 = 0
    cloud_x_3 = 0
    cloud_x_4 = 0
    cloud_speed_2 = 60
    cloud_speed_3 = 40
    cloud_speed_4 = 80

    clock = pygame.time.Clock()

    # Initialize input and sprites
    keylistener = Keylistener()
    player = Entity(keylistener)
    all_sprites = pygame.sprite.Group(player)

    running = True
    while running:
        # Handle events first
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                keylistener.add_key(event.key)
            elif event.type == pygame.KEYUP:
                keylistener.remove_key(event.key)

        # Calculate delta time (in seconds)
        delta_time = clock.get_time() / 1000.0

        # Update cloud positions using delta_time
        cloud_x_2 -= cloud_speed_2 * delta_time
        cloud_x_3 -= cloud_speed_3 * delta_time
        cloud_x_4 -= cloud_speed_4 * delta_time

        # Reset cloud positions for seamless scrolling
        if cloud_x_2 <= -screen_width:
            cloud_x_2 = 0
        if cloud_x_3 <= -screen_width:
            cloud_x_3 = 0
        if cloud_x_4 <= -screen_width:
            cloud_x_4 = 0

        # Draw background and cloud layers
        screen.blit(background_img, (0, 0))
        screen.blit(cloud_layer_3, (cloud_x_3, 0))
        screen.blit(cloud_layer_3, (cloud_x_3 + screen_width, 0))
        screen.blit(cloud_layer_2, (cloud_x_2, 0))
        screen.blit(cloud_layer_2, (cloud_x_2 + screen_width, 0))
        screen.blit(cloud_layer_4, (cloud_x_4, 0))
        screen.blit(cloud_layer_4, (cloud_x_4 + screen_width, 0))
        screen.blit(maps_img, (0, 0))

        # Update and draw sprites
        all_sprites.update()
        all_sprites.draw(screen)

        # Update the display (flip is often faster for full-screen updates)
        pygame.display.flip()

        # Cap the frame rate at 60 FPS.
        # Calling tick() here delays as needed and also updates the clock for delta_time.
        clock.tick(60)

    pygame.quit()
    exit()


# Example of how you might call game_on if this module is executed directly:
if __name__ == '__main__':
    # You can set the screensize here
    screensize = (800, 600)
    # Create the display surface with the desired mode flags.
    screen = pygame.display.set_mode(screensize, pygame.DOUBLEBUF)
    game_on(screen, screensize)
