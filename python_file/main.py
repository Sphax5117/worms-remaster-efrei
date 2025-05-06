import os
import pygame
from pygame import display
from menu import menu
from rule import rule
from game_on import game_on

def main():
    #initialization of the screen and of pygame
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    #screen configuration 
    info = pygame.display.Info()
    screensize = (info.current_w, info.current_h)
    screen = display.set_mode(screensize)
    pygame.display.set_caption("Funny Granny")
    
    #the loop of all the game 
    running = True

    while running:
        #to display the menu
        choice = menu(screensize, screen)

        if choice == 'start':
            #to launch the game
            game_on(screen, screensize) 
        elif choice == 'setting':
            #to access to the rules
            rule(screensize)
        elif choice == 'exit':
            #to exit the game
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()