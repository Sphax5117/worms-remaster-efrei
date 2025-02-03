import pygame
from sys import exit
screen = pygame.display.set_mode((800,800)) #need to add ((0,0), pygame.FULLSCREEN) for the full screen

#class for button
class Button():
    #define the class for the buttons
    def __init__(self, x, y, image):
        self.image = image 
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    
    #define a function to draw all the buttons
    def draw(self):
        action = False

        #get the mouse position (usefull for the click)
        pos = pygame.mouse.get_pos()

        #check is our mouse is over the button (1) and clicked (2) only one time
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        #checked if the mouse is released
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw the button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

def menu():
    pygame.init()

    #usefull variables
    run = True
    start_img = pygame.image.load('graphics_temp/start_btn.png')
    exit_img = pygame.image.load('graphics_temp/exit_btn.png')
    setting_img = pygame.image.load('graphics_temp/setting.jpeg')

    #initialization of the screen of the side of the screen and we set a caption for the window
    screen = pygame.display.set_mode((800,800)) #need to add ((0,0), pygame.FULLSCREEN) for the full screen
    pygame.display.set_caption("Funny Granny")

    #helps to limit the menu to 60fps
    clock = pygame.time.Clock()

    #create some button instances
    start_button = Button(100, 300, start_img)
    exit_button = Button(450,300, exit_img)
    setting_button = Button(600, 600, setting_img)


    #the while loop for the menu
    while run:

        #fill the screen with a black backround
        screen.fill((48, 106, 192))

        #draw our button for the menu
        if start_button.draw():
            return 'start'
        
        if exit_button.draw():
            run = False
        
        if setting_button.draw():
            return 'setting'

        #That help to exit the game when we use the red cross on the windows
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        #update the game every 60 seconds
        pygame.display.update()
        clock.tick(60)

