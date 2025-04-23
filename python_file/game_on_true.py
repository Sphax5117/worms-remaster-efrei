import pygame
import os
from sys import exit
from player_test import Player, Keylistener
from collisions import Obstacle, WallLine

def game_on(screen, screensize):
    # Configuration initiale
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
    pygame.display.set_caption("Funny Granny")
    screen_width, screen_height = screensize
    clock = pygame.time.Clock()
    # Chargement des assets
    background_img = pygame.transform.scale(pygame.image.load('assets/gameon/bg.png'), (screen_width, screen_height))
    cloud_layer_2 = pygame.transform.scale(pygame.image.load('assets/gameon/3.png'), (screen_width, screen_height - 10))
    cloud_layer_4 = pygame.transform.scale(pygame.image.load('assets/gameon/4.png'), (screen_width, screen_height - 10))
    cloud_layer_5 = pygame.transform.scale(pygame.image.load('assets/gameon/5.png'), (screen_width, screen_height - 10))
    map_img = pygame.transform.smoothscale(pygame.image.load('assets/gameon/maptest.png'), (screen_width, screen_height))

    # Positions et vitesses des nuages
    cloud_x_2 = cloud_x_4 = cloud_x_5 = 0
    cloud_speed_2, cloud_speed_4, cloud_speed_5 = 60, 40, 80

    # Initialisation des groupes de sprites
    all_sprites = pygame.sprite.Group()
    solid_obstacles = pygame.sprite.Group()

    # Création du joueur
    keylistener = Keylistener()
    player = Player(keylistener, screen_width // 2, screen_height // 2)
    all_sprites.add(player)

    # Liste de coordonnées des obstacles (x, y)
    obstacle_positions = [
        (565, 542),
        (617,542),
        (670,542),
        (565,590),
        (565,640),
        (565,690),
        (565,740),
        (565,790),
        (565,840),
        (565,890),
        (565,940),
        (565,990),
        (565,1040),
        (565,1090),
        (565,1140),
        (565,1190),
        (617,590),
        (617,640),
        (617,690),
        (617,740),
        (617,790),
        (617,840),
        (617,890),
        (617,940),
        (617,990),
        (617,1040),
        (617,1090),
        (617,1140),
        (617,1190),
        (670,590),
        (670,640),
        (670,690),
        (670,740),
        (670,790),
        (670,840),
        (670,890),
        (670,940),
        (670,990),
        (670,1040),
        (670,1090),
        (670,1140),
        (670,1190),
        (850,672),
        (850,722),
        (850,772),
        (850,822),
        (850,872),
        (850,922),
        (850,972),
        (850,1022),
        (850,1072),
        (850,1122),
        (850,1172),
        (850,1222),
        (900,672),
        (900,722),
        (900,772),
        (900,822),
        (900,872),
        (900,922),
        (900,972),
        (900,1022),
        (900,1072),
        (900,1122),
        (900,1172),
        (900,1222),


        # Ajouter d'autres positions ici
    ]
     # Création d'une ligne de mur
    wall_line = WallLine(48, 415, num_blocks=3, direction='horizontal',block_width=55, block_height=5)
    wall_line.build(all_sprites, solid_obstacles)
    wall_line = WallLine(370, 158, num_blocks=1, direction='horizontal',block_width=50, block_height=5)
    wall_line.build(all_sprites, solid_obstacles)
    wall_line = WallLine(750, 220, num_blocks=2, direction='horizontal',block_width=85, block_height=5)
    wall_line.build(all_sprites, solid_obstacles)
    wall_line = WallLine(1040, 417, num_blocks=2, direction='horizontal',block_width=82, block_height=5)
    wall_line.build(all_sprites, solid_obstacles)
    wall_line = WallLine(1580, 370, num_blocks=2, direction='horizontal',block_width=82, block_height=5)
    wall_line.build(all_sprites, solid_obstacles)
    wall_line = WallLine(1835, 155, num_blocks=1, direction='horizontal',block_width=55, block_height=5)
    wall_line.build(all_sprites, solid_obstacles)
    wall_line = WallLine(950, 672, num_blocks=10, direction='vertical',block_width=200, block_height=1000)
    wall_line.build(all_sprites, solid_obstacles)
    wall_line = WallLine(1235, 610, num_blocks=10, direction='vertical',block_width=500, block_height=1000)
    wall_line.build(all_sprites, solid_obstacles)
    wall_line = WallLine(125, 825, num_blocks=10, direction='vertical',block_width=280, block_height=1000)
    wall_line.build(all_sprites, solid_obstacles)



    TILE_SIZE = 50  # Taille d'une tuile, ajuste si nécessaire
    for position in obstacle_positions:
            x, y = position
            # Créer l'obstacle
            obstacle = Obstacle(x, y, width=TILE_SIZE, height=TILE_SIZE, is_solid=True)
            solid_obstacles.add(obstacle)
            all_sprites.add(obstacle)


    # Boucle principale du jeu
    running = True
    while running:
        delta_time = clock.tick(60) / 1000  # pour animations lissées

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                keylistener.add_key(event.key)
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.KEYUP:
                keylistener.remove_key(event.key)

        # Mise à jour des positions des nuages
        cloud_x_2 -= cloud_speed_2 * delta_time
        cloud_x_4 -= cloud_speed_4 * delta_time
        cloud_x_5 -= cloud_speed_5 * delta_time

        # Reset si les nuages dépassent
        if cloud_x_2 <= -screen_width:
            cloud_x_2 = 0
        if cloud_x_4 <= -screen_width:
            cloud_x_4 = 0
        if cloud_x_5 <= -screen_width:
            cloud_x_5 = 0

        # === Affichage ===
        screen.blit(background_img, (0, 0))
        screen.blit(cloud_layer_4, (cloud_x_4, 0))
        screen.blit(cloud_layer_4, (cloud_x_4 + screen_width, 0))
        screen.blit(cloud_layer_2, (cloud_x_2, 0))
        screen.blit(cloud_layer_2, (cloud_x_2 + screen_width, 0))
        screen.blit(cloud_layer_5, (cloud_x_5, 0))
        screen.blit(cloud_layer_5, (cloud_x_5 + screen_width, 0))

        screen.blit(map_img, (0, 0))  # Affiche la map AVANT les sprites (pour que le joueur soit au-dessus)

        # Mise à jour de tous les sprites
        all_sprites.update(solid_obstacles)  # <=== passe les obstacles ici
        all_sprites.draw(screen)

        pygame.display.update()

