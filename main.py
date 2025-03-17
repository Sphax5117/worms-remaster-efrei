#all the import mandatory
import os

import pygame
from pygame import display

from game_on import game_on
from menu import menu
from setting import setting
from utilities import size


#the main function who regroups all the functions
def main():
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    info = pygame.display.Info() # get size of user's screen
    screen_width, screen_height = info.current_w, info.current_h #set tuple
    screen = display.set_mode((screen_width, screen_height ))
    run = True
<<<<<<< HEAD
    screensize  = (1200, 700)
=======


    screensize  = (screen_width, screen_height)
>>>>>>> 892ad33af9b5684817266b762f164d01d751d4ef

    #loop to launch the game
    while run:
        choice_menu = menu(screensize, screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if choice_menu == 'start':
            game_on(screen, screensize)
        elif choice_menu == 'setting' and setting(screensize):
            screensize = size()
        elif choice_menu == 'exit':
            run = False
    
    return
main()
