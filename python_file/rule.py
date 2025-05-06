import pygame
import os
from sys import exit
from pathlib import Path

#to get the path of the different usefull sprite
base_path = Path(__file__).resolve().parent
rules_path = base_path / '..' / 'assets' / 'rules' / 'rules.png'
exit_button_path = base_path / '..' / 'assets' / 'rules' / 'setting_exit.png'

#definiton of the rule game that is in the menu
def rule(screensize):
    #initalize pygame + the screen + caption
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0" 
    pygame.init()
    pygame.display.set_caption("Display Rules")

    #set up screen + usefull variables
    screen_width, screen_height = screensize
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    padding = 15

    #assets and sprite
    rules_img_str = str(rules_path)
    rules_img = pygame.image.load(rules_img_str).convert_alpha()
    rules_img = pygame.transform.smoothscale(rules_img, (screen_width, screen_height))
    exit_button_str = str(exit_button_path)
    exit_button = pygame.image.load(exit_button_str).convert_alpha()
    exit_button_rect = exit_button.get_rect(topleft=(0, 0))
    exit_button_rect.topleft = (0, 0) 

    #the big loop to dsiplay it
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #handle the click of the user
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button_rect.collidepoint(event.pos[0] - 15, event.pos[1] - 15):
                    return

        #display the buttons and the screen
        screen.blit(rules_img, (0, 0))
        screen.blit(exit_button, (exit_button_rect.x + padding, exit_button_rect.y + padding))

        #update and limit the fps
        pygame.display.update()
        clock.tick(60)
        



