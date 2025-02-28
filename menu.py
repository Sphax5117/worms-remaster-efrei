import pygame
from sys import exit
import os

def menu(screensize):
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"  # Force window to top-left
    pygame.init()
    pygame.mixer.init()

    #usefull variables
    run = True
    screen_width, screen_height = screensize
    start_img = pygame.image.load('assets/menu/start_bt.png')
    exit_img = pygame.image.load('assets/menu/exit_bt.png')
    setting_img = pygame.image.load('assets/menu/setting_bt.png')
    backround_img = pygame.image.load('assets/menu/bg.png')
    pygame.mixer.music.load('Musics/Funny Granny 2.mp3')

    #for the music in loop
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    #scale the image (button and backround)
    start_img = pygame.transform.scale(start_img, (300, 100))
    exit_img = pygame.transform.scale(exit_img, (300, 100))
    setting_img = pygame.transform.scale(setting_img, (300, 100)) 
    backround_img = pygame.transform.scale(backround_img, (screen_width, screen_height))  

    #initialization of the screen of the side of the screen and we set a caption for the window
    screen = pygame.display.set_mode((screensize)) 
    pygame.display.set_caption("Funny Granny")

    # Button class
    class Button():
        def __init__(self, x_factor, y_factor, image):
            self.image = image
            self.x_factor = x_factor  # Percentage of screen width
            self.y_factor = y_factor  # Percentage of screen height
            self.update_position(screen_width, screen_height)
            self.clicked = False
        
        def update_position(self, screen_width, screen_height):
            #Update button position based on new screen size.
            self.rect = self.image.get_rect()
            self.rect.topleft = (int(screen_width * self.x_factor), int(screen_height * self.y_factor))

        def draw(self):
            action = False
            pos = pygame.mouse.get_pos()

            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                    self.clicked = True
                    action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            screen.blit(self.image, (self.rect.x, self.rect.y))
            return action
        
    #helps to limit the menu to 60fps
    clock = pygame.time.Clock()

    #create some button instances
    start_button = Button(0.4, 0.45, start_img)  
    exit_button = Button(0.4, 0.6, exit_img)   
    setting_button = Button(0.4, 0.75, setting_img)  


    #the while loop for the menu
    while run:

        #fill the screen with a black backround
        screen.blit(backround_img, (0,0))

        #draw our button for the menu
        if start_button.draw():
            return 'start'
        
        if exit_button.draw():
            return 'exit'
        
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

