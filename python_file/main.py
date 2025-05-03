import os
import pygame
from pygame import display
from menu import menu
from rule import rule
from game_on import game_on

def main():
    #initialization
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    #screen configuration 
    info = pygame.display.Info()
    screensize = (info.current_w, info.current_h)
    screen = display.set_mode(screensize)
    pygame.display.set_caption("Funny Granny")
    
    running = True
    while running:
        #to display the menu
        choice = menu(screensize, screen)

        if choice == 'start':
            game_on(screen, screensize)  #launch the game
        elif choice == 'setting':
            rule(screensize)
        elif choice == 'exit':
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()