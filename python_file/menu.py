import pygame
from sys import exit
import os
from pathlib import Path

#get the absolute path to the `menu.py` file + more stable and more sure
base_path = Path(__file__).resolve().parent
start_img_path = base_path / '..' / 'assets' / 'menu' / 'start_btn.png'
exit_img_path = base_path / '..' / 'assets' / 'menu' / 'exit_btn.png'
setting_img_path = base_path / '..' / 'assets' / 'menu' / 'setting_btn.png'
background_img_path = base_path / '..' / 'assets' / 'menu' / 'bg2.png'
music_path = base_path / '..' / 'Musics' / 'Funny Granny 2.mp3'


#definition of the menu to dsiplay it and used it
def menu(screensize, screen):
    #configuration of the screen + music handling
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"  
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("Funny Granny")

    #usefull variables
    run = True
    screen_width, screen_height = screensize
    start_img = pygame.image.load(str(start_img_path))
    exit_img = pygame.image.load(str(exit_img_path))
    setting_img = pygame.image.load(str(setting_img_path))
    backround_img = pygame.image.load(str(background_img_path))
    pygame.mixer.music.load(str(music_path))

    #for the music in loop
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    #scale the image (button and backround)
    start_img = pygame.transform.smoothscale(start_img, (screen_width//2.5, screen_height//9))
    exit_img = pygame.transform.smoothscale(exit_img, (screen_width//4.2, screen_height//9))
    setting_img = pygame.transform.smoothscale(setting_img, (screen_width//3, screen_height//9))
    backround_img = pygame.transform.smoothscale(backround_img, (screen_width, screen_height))

    #button class to have button with no absolute values and just depends on the size of the screen
    class Button():
        def __init__(self, x_factor, y_factor, image):
            self.image = image
            self.x_factor = x_factor  
            self.y_factor = y_factor  
            self.update_position(screen_width, screen_height)
            self.clicked = False

        def update_position(self, screen_width, screen_height):
            #update button position based on new screen size.
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
    start_button = Button(0.31, 0.45, start_img)
    exit_button = Button(0.4, 0.75, exit_img)
    setting_button = Button(0.35, 0.6, setting_img)


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
