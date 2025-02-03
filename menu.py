import pygame
from sys import exit

def menu():
    pygame.init

    #usefull variables
    start_button = pygame.image.load('players.png')
    exit_button = pygame.image.load('players.png')

    #initialization of the screen of the side of the screen and we set a caption for the window
    screen = pygame.display.set_mode((800,800)) #need to add ((0,0), pygame.FULLSCREEN) for the full screen
    pygame.display.set_caption("Funny Granny")

    #display all the variables in the screen
    screen.blit(start_button, (200,200))

    #helps to limit the menu to 60fps
    clock = pygame.time.Clock()

    #the while loop for the menu
    while True:

        #That help to exit the game when we use the red cross on the windows
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        #fill the screen with a black backround
        screen.fill((48, 106, 192))

        #update the game every 60 seconds
        pygame.display.update()
        clock.tick(60)

#class for button
class Button():
    #define the class for the buttons
    def __init__(self, x, y, image):
        self.image = image 
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    #define a function to draw all the buttons
    def draw(self):

