#all the import mandatory 
import pygame
from game_on import game_on
from menu import menu
from setting import setting

#the main function who regroups all the functions
def main():

    if menu() == 'start':
        game_on()
    elif menu() == 'setting':
        setting()

main()
