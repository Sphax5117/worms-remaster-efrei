import pygame
import time
from sys import exit
 
def testpygames():
    pygame.init

    #initialization of the screen
    screen = pygame.display.set_mode((1200, 600))
    pygame.display.set_caption('Worms.exe')

    #limit the game to 60 fps
    clock = pygame.time.Clock()

    #structure of the game, simples bridges
    bridge_surface = pygame.Surface((1500, 10))
    bridge_surface.fill('Brown')

    #backround surface 
    #backround_image = pygame.image.load('')

    #players need to have a better well organised folder
    player1 = pygame.image.load('players.png')
    player2 = pygame.image.load('players.png')
    #for the scale of the player
    player1 = pygame.transform.scale(player1, (20,20))
    player2 = pygame.transform.scale(player1, (20,20))
    #con,sider the player as a rectangle for better positioning
    player1_rect = player1.get_rect(midbottom = (260,500))
    player2_rect = player2.get_rect(midbottom = (400, 500))
    #for the gravity of the player
    player1_gravity = 0
    player2_gravity = 0

    #management for turns (1 or 2)
    player_turn = pygame.USEREVENT + 1
    pygame.time.set_timer(player_turn, 45000)
    current_player = 1


    while True:

        #to exit the windows
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == player_turn:
                if current_player == 1:
                    current_player = 2
                elif current_player == 2:
                    current_player = 1
           

        #display the backround on the screen
        screen.fill((0, 0, 0))
                
        #display the brige on the screen 
        screen.blit(bridge_surface,(0,500))
        

        #display the players1 + gravity
        player1_gravity += 0.5
        player1_rect.y += player1_gravity
        if player1_rect.bottom >= 500:
            player1_rect.bottom = 500
        screen.blit(player1, player1_rect)

        #display the players2 + gravity
        player2_gravity += 0.5
        player2_rect.y += player2_gravity
        if player2_rect.bottom >= 500:
            player2_rect.bottom = 500
        screen.blit(player2, player2_rect)

        keys = pygame.key.get_pressed()

        #Players 1
        #pour les mouvements ici droite et gauche ou on prends on compte la collision entre deux joueur

        if current_player == 1:
            if keys[pygame.K_RIGHT]:
                player1_rect.x += 2


                if player1_rect.colliderect(player2_rect):
                    player1_rect.x -= 2
            
            if keys[pygame.K_LEFT]:
                player1_rect.x -= 2

                if player1_rect.colliderect(player2_rect):
                    player1_rect.x += 2
            
            if keys[pygame.K_UP] and player1_rect.bottom >= 500 and current_player == 1:
                player1_gravity = -9
 
        elif current_player == 2:
            if keys[pygame.K_RIGHT]:
                player2_rect.x += 2


                if player2_rect.colliderect(player1_rect):
                    player2_rect.x -= 2
            
            if keys[pygame.K_LEFT]:
                player2_rect.x -= 2

                if player2_rect.colliderect(player1_rect):
                    player2_rect.x += 2
            
            if keys[pygame.K_UP] and player2_rect.bottom >= 500 and current_player == 2:
                player2_gravity = -9


        #update everything
        pygame.display.update()

        #limit the game to 60 fps
        clock.tick(60)


testpygames()