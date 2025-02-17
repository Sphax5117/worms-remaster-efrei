import pygame

def size():
    pygame.init()

    #to get the info of the current screen and ajust it to the fullscreen
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    w, h = screen.get_size()

    return (w,h)

