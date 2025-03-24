# importation of all the useful libraries
import pygame
from sys import exit
import os


def game_on(screen, screensize):
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"  # Force window to top-left
    pygame.init()

    # Initialization of the screen and caption
    pygame.display.set_caption("Funny Granny")

    # Load images
    backround_img = pygame.image.load('assets/gameon/bg.png')  # Skybox background
    cloud_layer_2 = pygame.image.load('assets/gameon/3.png')  # Cloud layer 3
    cloud_layer_4 = pygame.image.load('assets/gameon/4.png')  # Cloud layer 4
    cloud_layer_5 = pygame.image.load('assets/gameon/5.png')  # Cloud layer 5
    maps_img = pygame.image.load('assets/gameon/test.png')  # Platform

    screen_width, screen_height = screensize

    # Scale images
    backround_img = pygame.transform.scale(backround_img, (screen_width, screen_height))
    cloud_layer_2 = pygame.transform.scale(cloud_layer_2, (screen_width, screen_height -10))
    cloud_layer_4 = pygame.transform.scale(cloud_layer_4, (screen_width, screen_height - 10))
    cloud_layer_5 = pygame.transform.scale(cloud_layer_5, (screen_width, screen_height -10))
    maps_img = pygame.transform.smoothscale(maps_img, (screen_width, screen_height))

    # Initial positions and speeds for cloud layers
    cloud_x_2 = 0  # Starting x position for 2.png
    cloud_x_4 = 0  # Starting x position for 4.png
    cloud_x_5 = 0  # Starting x position for 5.png

    cloud_speed_2 = 30  # Speed for cloud layer 2
    cloud_speed_4 = 20  # Speed cloud  4 (
    cloud_speed_5 = 50  # Speed cloud  5

    clock = pygame.time.Clock()

    delta_time = 0

    # The main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        cloud_x_2 -= cloud_speed_2 * delta_time  # Update based on time
        cloud_x_4 -= cloud_speed_4 * delta_time  # Update for cloud layer 4
        cloud_x_5 -= cloud_speed_5 * delta_time  # Update for cloud layer 5

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

        # Update the display
        pygame.display.update()

        # Tick the clock and calculate delta_time (time between frames)
        delta_time = clock.tick(10) / 1000  # Convert milliseconds to seconds
