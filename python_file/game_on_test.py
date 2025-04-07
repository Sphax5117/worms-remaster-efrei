#importation
import pygame
from sys import exit
import os
from playerrrr import Keylistener, Entity

def game_on(screen, screensize):
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"  # Force window to top-left
    pygame.init()

    # Initialization of the screen and caption
    pygame.display.set_caption("Funny Granny")

    # Load and scale images only once during initialization
    screen_width, screen_height = screensize
    backround_img = pygame.transform.scale(pygame.image.load('assets/gameon/bg.png'), (screen_width, screen_height))
    cloud_layer_2 = pygame.transform.scale(pygame.image.load('assets/gameon/3.png'), (screen_width, screen_height - 10))
    cloud_layer_4 = pygame.transform.scale(pygame.image.load('assets/gameon/4.png'), (screen_width, screen_height - 10))
    cloud_layer_5 = pygame.transform.scale(pygame.image.load('assets/gameon/5.png'), (screen_width, screen_height - 10))
    maps_img = pygame.transform.smoothscale(pygame.image.load('assets/gameon/maptest.png'), (screen_width, screen_height))

    # Initial positions and speeds for cloud layers
    cloud_x_2 = 0  # Starting x position for 2.png
    cloud_x_4 = 0  # Starting x position for 4.png
    cloud_x_5 = 0  # Starting x position for 5.png

    # Adjusted cloud speeds (lower values for smoother animation)
    cloud_speed_2 = 60  # Adjust speed for cloud layer 2
    cloud_speed_4 = 40  # Adjust speed for cloud layer 4
    cloud_speed_5 = 80  # Adjust speed for cloud layer 5

    clock = pygame.time.Clock()

    # Initialize Keylistener
    keylistener = Keylistener()

    # Create Player Entity
    player = Entity(keylistener)
    all_sprites = pygame.sprite.Group(player)  # Add player to sprite group

    # The main game loop
    while True:
        delta_time = clock.tick(60) / 1000  # Convert milliseconds to seconds

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                keylistener.add_key(event.key)
            elif event.type == pygame.KEYUP:
                keylistener.remove_key(event.key)

        # Update cloud positions based on delta_time
        cloud_x_2 -= cloud_speed_2 * delta_time
        cloud_x_4 -= cloud_speed_4 * delta_time
        cloud_x_5 -= cloud_speed_5 * delta_time

        # Reset clouds when they move outside of screen
        if cloud_x_2 <= -screen_width:
            cloud_x_2 = 0
        if cloud_x_4 <= -screen_width:
            cloud_x_4 = 0
        if cloud_x_5 <= -screen_width:
            cloud_x_5 = 0

        # Draw each layer in the correct order
        screen.blit(backround_img, (0, 0))  # Draw the skybox
        screen.blit(cloud_layer_4, (cloud_x_4, 0))  # Draw cloud layer 4
        screen.blit(cloud_layer_4, (cloud_x_4 + screen_width, 0))  # Seamless second cloud layer 4
        screen.blit(cloud_layer_2, (cloud_x_2, 0))  # Draw cloud layer 2
        screen.blit(cloud_layer_2, (cloud_x_2 + screen_width, 0))  # Seamless second cloud layer 2
        screen.blit(cloud_layer_5, (cloud_x_5, 0))  # Draw cloud layer 5
        screen.blit(cloud_layer_5, (cloud_x_5 + screen_width, 0))  # Seamless second cloud layer 5
        screen.blit(maps_img, (0, 0))  # Draw the platforms

        # Update and draw all sprites
        all_sprites.update()
        all_sprites.draw(screen)

        # Update the display
        pygame.display.update()


