import os
import pygame
from pygame import display
from game_on_true import game_on
from menu import menu
from setting import setting
from utilities import size

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
            if setting(screensize):
                screensize = size()
                screen = display.set_mode(screensize)
        elif choice == 'exit':
            running = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()  # Récupère la position du clic de la souris
                print(f"Coordonnées du clic: ({mouse_x}, {mouse_y})")

    pygame.quit()

if __name__ == "__main__":
    main()