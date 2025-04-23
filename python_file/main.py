import os
import pygame
from pygame import display
from menu import menu
from rule import rule
from utilities import size
from game_on import game_on

def main():
    # Initialisation Pygame
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    
    # Configuration écran
    info = pygame.display.Info()
    screensize = (info.current_w, info.current_h)
    screen = display.set_mode(screensize)
    pygame.display.set_caption("Funny Granny")
    
    running = True
    while running:
        # Affiche le menu principal
        choice = menu(screensize, screen)

        if choice == 'start':
            game_on(screen, screensize)  # Lance directement le jeu complet
        elif choice == 'setting':
            rule(screensize)
        elif choice == 'exit':
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()