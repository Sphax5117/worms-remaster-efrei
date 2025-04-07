import pygame
import os
from sys import exit
from pathlib import Path
import menu  # Assuming you have a menu.py with a menu() function

# Get the absolute path to the current file's directory
base_path = Path(__file__).resolve().parent

# Paths for assets
rules_path = base_path / '..' / 'assets' / 'rules' / 'rules.png'
exit_button_path = base_path / '..' / 'assets' / 'rules' / 'setting_exit.png'

def setting(screensize):
    # Step 1: Initialize pygame
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"  # Force window to top-left
    pygame.init()
    pygame.display.set_caption("Display Rules")

    # Step 2: Set up the screen size
    screen_width, screen_height = screensize
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Step 3: Load and scale the rules image
    rules_img_str = str(rules_path)
    if not os.path.exists(rules_img_str):
        print(f"Error: The file '{rules_img_str}' does not exist.")
        pygame.quit()
        exit()

    rules_img = pygame.image.load(rules_img_str).convert_alpha()
    rules_img = pygame.transform.smoothscale(rules_img, (screen_width, screen_height))

    # Load and position the exit button image
    exit_button_str = str(exit_button_path)
    if not os.path.exists(exit_button_str):
        print(f"Error: The file '{exit_button_str}' does not exist.")
        pygame.quit()
        exit()

    exit_button = pygame.image.load(exit_button_str).convert_alpha()
    # Set initial position (0,0); we'll add padding later by modifying its blit position.
    exit_button_rect = exit_button.get_rect(topleft=(0, 0))
    exit_button_rect.topleft = (0, 0)  # Top-left corner

    # Step 4: Main display loop for the settings screen
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            # Allow window to be closed via the X button.
            if event.type == pygame.QUIT:
                running = False

            # Check for mouse clicks.
            if event.type == pygame.MOUSEBUTTONDOWN:
                # event.pos is the mouse position at click.
                if exit_button_rect.collidepoint(event.pos[0] - 15, event.pos[1] - 15):
                    # The exit button was clicked—return to the menu.
                    return

        # Draw the rules background first.
        screen.blit(rules_img, (0, 0))
        # Add a bit of padding (15 pixels) to the exit button.
        padding = 15
        screen.blit(exit_button, (exit_button_rect.x + padding, exit_button_rect.y + padding))

        pygame.display.update()
        clock.tick(60)  # Limit to 60 FPS

    # Instead of quitting pygame here, simply return so the main program can go back to the menu.
    return

# For testing purposes, run the settings screen if this module is executed directly.
if __name__ == "__main__":
    screensize = (1280, 720)  # Example resolution
    setting(screensize)
