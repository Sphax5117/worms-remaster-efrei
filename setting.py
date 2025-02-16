import pygame
from sys import exit 
from utilities import size
import os

def setting(screensize):
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"  # Force window to top-left
    pygame.init()

    # initialization of the screen of the side of the screen and we set a caption for the window
    screen = pygame.display.set_mode((screensize)) # need to add ((0,0), pygame.FULLSCREEN) for the full screen
    pygame.display.set_caption("Settings")

    # helps to limit the game to 60fps
    clock = pygame.time.Clock()

    # Button settings
    button_color = (100, 100, 255)
    button_rect = pygame.Rect(300, 350, 200, 50)
    font = pygame.font.Font(None, 36)
    button_text = font.render("Auto Resize", True, (255, 255, 255))
    text_rect = button_text.get_rect(center=button_rect.center)

    # the principal loop that is True when the game is live
    while True:

        # That help to exit the game when we use the red cross on the windows
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            # Detect mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    # Get full screen size
                    info = size()
                    screen = pygame.display.set_mode((info), pygame.NOFRAME)
                    return(True)


        # fill the screen with a black background
        screen.fill((0, 0, 0))

        # Draw button
        pygame.draw.rect(screen, button_color, button_rect)
        screen.blit(button_text, text_rect)

        # update the game every 60 seconds
        pygame.display.update()
        clock.tick(60)

