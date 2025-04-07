import pygame
import os
from sys import exit
from pathlib import Path

# Get the absolute path to the `menu.py` file
base_path = Path(__file__).resolve().parent

rules =  base_path / '..' / 'assets' / 'rules' / 'rules.png'

def setting(screensize):
    # Step 1: Initialize pygame
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"  # Force window to top-left
    pygame.init()
    pygame.display.set_caption("Display Rules")

    # Step 2: Set up the screen size
    screen_width, screen_height = screensize
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Step 3: Load and scale the image
    rules_img_path = str(rules)
    if not os.path.exists(rules_img_path):
        print(f"Error: The file '{rules_img_path}' does not exist.")
        pygame.quit()
        exit()

    rules_img = pygame.image.load(rules_img_path)
    rules_img = pygame.transform.smoothscale(rules_img, (screen_width, screen_height))

    # Step 4: Main display loop
    running = True
    clock = pygame.time.Clock()
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw the image
        screen.blit(rules_img, (0, 0))

        # Update display
        pygame.display.update()
        clock.tick(60)  # Limit the frame rate to 60 FPS

    # Clean up resources
    pygame.quit()
    exit()


if __name__ == "__main__":
    # Set screen size dynamically
    screensize = (1280, 720)  # Example resolution
    display_rules(screensize)
