#importation of all the usefull librairy
import pygame
from sys import exit 
import os

def game_on():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"  # Force window to top-left
    pygame.init() 

    #initialization of the screen of the side of the screen and we set a caption for the window
    screen = pygame.display.set_mode((1500,750)) #need to add ((0,0), pygame.FULLSCREEN) for the full screen
    pygame.display.set_caption("Funny Granny")
    backround_img = pygame.image.load('assets/gameon/skybox.png')
    maps_img = pygame.image.load('assets/gameon/test.png')

    #sclae the image
    ackround_img = pygame.transform.scale(backround_img, (1500,750))
    maps_img = pygame.transform.scale(maps_img, (1500, 750))

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
        screen.blit(backround_img, (0,0))
        screen.blit(maps_img, (0,0))

        #update the game every 60 seconds
        pygame.display.update()
        clock.tick(60)



    return