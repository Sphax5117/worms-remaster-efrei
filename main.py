#all the import mandatory 
import pygame
from game_on import game_on
from menu import menu
from setting import setting

#the main function who regroups all the functions
def main():
    run = True

    #loop to launch the game
    while run:
        if menu() == 'start':
            game_on()
        elif menu() == 'setting':
            if setting() == True:
                game_on()
        elif menu() == 'exit':
            run = False
    

main()
