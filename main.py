#importation of all the usefull librairy
import pygame
import time
from sys import exit 

def game():

    pygame.init

    #initialization of the screen of the side of the screen and we set a caption for the window
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    pygame.display.set_caption("Funny Granny")

    #helps to limit the game to 60fps
    clock = pygame.time.Clock()


    #the principal loop that is True when the game is live
    while True:

        #That help to exit the game when we use the red cross on the windows
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        #fill the screen with a black backround
        screen.fill((0, 0, 0))

        #update the game every 60 seconds
        pygame.display.update()
        clock.tick(60)


game()
