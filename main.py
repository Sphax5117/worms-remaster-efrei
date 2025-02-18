#all the import mandatory 
import pygame
from game_on import game_on
from menu import menu
from setting import setting
from utilities import size


#the main function who regroups all the functions
def main():
    run = True

    screensize  = (800, 800)

    #loop to launch the game
    while run:
        choice_menu = menu(screensize)

        if choice_menu == 'start':
            game_on()
        elif choice_menu == 'setting' and setting(screensize):
            screensize = size()
        elif choice_menu == 'exit':
            run = False
    
    return
    

main()
