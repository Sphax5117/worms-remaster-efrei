#all the import mandatory 
import pygame
from game_on import game_on
from menu import menu
from sys import exit

def main():
    #launch the menu() on python
    do = menu()

    if do == 1:
        game_on()
    if do == 2:
        pygame.quit()
        exit()
