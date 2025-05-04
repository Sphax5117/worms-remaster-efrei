import pygame
import os
import random
from sys import exit
from pathlib import Path
from throwables_weapon import ExplodingSlipper, BurningSoup, ToiletPaperRoll, BoomerangDenture

from player import Player, Keylistener
from collision import WallLine
from readyscreen import readyscreen

def game_on(screen, screensize):
    #The ready screen
    readyscreen(screen,screensize, 5)


    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
    pygame.display.set_caption("Funny Granny")
    font = pygame.font.SysFont(None, 150)

    DESIGN_W = 1920
    DESIGN_H = 1080

    # load asset
    base_path = Path(__file__).resolve().parent
    bg = base_path / '..' / 'assets' / 'gameon' / 'bg.png'
    cloud2 = base_path / '..' / 'assets' / 'gameon' / '3.png'
    cloud4 = base_path / '..' / 'assets' / 'gameon' / '5.png'
    mapimg = base_path / '..' / 'assets' / 'gameon' / 'maptest.png'
    arrow = base_path / '..' / 'assets' / 'gameon' / 'arrow.png'
    health5= base_path / '..' / 'assets' / 'lives' / 'health_5.png'
    health5_img = pygame.image.load(health5).convert_alpha()
    health5_img = pygame.transform.scale(health5_img, (100,10))
    arrow_img = pygame.image.load(arrow).convert_alpha()
    arrow_img = pygame.transform.scale(arrow_img, (30, 50))

    screen_width, screen_height = screensize
    clock = pygame.time.Clock()

    background_img = pygame.transform.scale(pygame.image.load(str(bg)).convert(), (screen_width, screen_height))
    cloud_layer_2 = pygame.transform.scale(pygame.image.load(str(cloud2)).convert_alpha(), (screen_width, screen_height - 10))
    cloud_layer_5 = pygame.transform.scale(pygame.image.load(str(cloud4)).convert_alpha(), (screen_width, screen_height - 10))
    map_img = pygame.transform.smoothscale(pygame.image.load(str(mapimg)).convert_alpha(), (screen_width, screen_height))

    # pos des spawn random
    spawn_position_ratios = [
        (376 / DESIGN_W, 160 / DESIGN_H),
        (49 / DESIGN_W, 250 / DESIGN_H),
        (750 / DESIGN_W, 120 / DESIGN_H),
        (1835 / DESIGN_W, 50 / DESIGN_H),
        (1835 / DESIGN_W, 120 / DESIGN_H),
        (1050 / DESIGN_W, 310 / DESIGN_H),
        (1300 / DESIGN_W, 500 / DESIGN_H)
    ]

    cloud_w = cloud_layer_2.get_width()
    cloud_x_5 = random.randint(0, screen_width)
    cloud_speed_5 = 20

    all_sprites = pygame.sprite.LayeredUpdates()
    solid_obstacles = pygame.sprite.Group()
    all_sprites = pygame.sprite.LayeredUpdates()
    projectiles = pygame.sprite.Group()

    player_positions = [
        (int(x_r * screen_width), int(y_r * screen_height))
        for (x_r, y_r) in random.sample(spawn_position_ratios, 4)
    ]

    players = []
    keylisteners = []
    active_player = 0
    controle_switch = 45
    switch_timer = 0
    player_health={1:5, 2:5, 3:5, 4:5}

    arme_actuelle = "slipper"  # default weapon

    # creation of player, papy and mamy
    for i, pos in enumerate(player_positions):
        kl = Keylistener()
        keylisteners.append(kl)
        if i %2 == 0:
            costume = "mamy"      
        elif i %2 == 1:
            costume = "papy" 
        p = Player(kl, *pos, costume=costume)
        players.append(p)
        all_sprites.add(p, layer=1)

    player_group = pygame.sprite.Group(players)

    # creation wall and obstacle
    wall_definitions_ratios = [
        (WallLine, (48 / DESIGN_W, 415 / DESIGN_H), {'num_blocks': 3, 'direction': 'horizontal', 'block_width': 55 / DESIGN_W, 'block_height': 5 / DESIGN_H}),
        (WallLine, (370 / DESIGN_W, 158 / DESIGN_H), {'num_blocks': 1, 'direction': 'horizontal', 'block_width': 50 / DESIGN_W, 'block_height': 5 / DESIGN_H}),
        (WallLine, (750 / DESIGN_W, 220 / DESIGN_H), {'num_blocks': 2, 'direction': 'horizontal', 'block_width': 85 / DESIGN_W, 'block_height': 5 / DESIGN_H}),
        (WallLine, (1040 / DESIGN_W, 417 / DESIGN_H), {'num_blocks': 2, 'direction': 'horizontal', 'block_width': 82 / DESIGN_W, 'block_height': 5 / DESIGN_H}),
        (WallLine, (1580 / DESIGN_W, 370 / DESIGN_H), {'num_blocks': 2, 'direction': 'horizontal', 'block_width': 82 / DESIGN_W, 'block_height': 5 / DESIGN_H}),
        (WallLine, (1835 / DESIGN_W, 155 / DESIGN_H), {'num_blocks': 1, 'direction': 'horizontal', 'block_width': 55 / DESIGN_W, 'block_height': 5 / DESIGN_H}),
        (WallLine, (850 / DESIGN_W, 672 / DESIGN_H), {'num_blocks': 10, 'direction': 'vertical', 'block_width': 300 / DESIGN_W, 'block_height': 10 / DESIGN_H}),
        (WallLine, (1230 / DESIGN_W, 610 / DESIGN_H), {'num_blocks': 10, 'direction': 'vertical', 'block_width': 520 / DESIGN_W, 'block_height': 10 / DESIGN_H}),
        (WallLine, (120 / DESIGN_W, 825 / DESIGN_H), {'num_blocks': 10, 'direction': 'vertical', 'block_width': 300 / DESIGN_W, 'block_height': 10 / DESIGN_H}),
        (WallLine, (560 / DESIGN_W, 650 / DESIGN_H), {'num_blocks': 10, 'direction': 'vertical', 'block_width': 170 / DESIGN_W, 'block_height': 10 / DESIGN_H}),
        (WallLine, (213 / DESIGN_W, 280 / DESIGN_H), {'num_blocks': 2, 'direction': 'horizontal', 'block_width': 85 / DESIGN_W, 'block_height': 5 / DESIGN_H}),
        (WallLine, (985 / DESIGN_W, 305 / DESIGN_H), {'num_blocks': 1, 'direction': 'horizontal', 'block_width': 75 / DESIGN_W, 'block_height': 5 / DESIGN_H}),
        (WallLine, (1730 / DESIGN_W, 260 / DESIGN_H), {'num_blocks': 1, 'direction': 'horizontal', 'block_width': 70 / DESIGN_W, 'block_height': 5 / DESIGN_H}),
        (WallLine, (505 / DESIGN_W, 478 / DESIGN_H), {'num_blocks': 1, 'direction': 'horizontal', 'block_width': 70 / DESIGN_W, 'block_height': 5 / DESIGN_H}),
        (WallLine, (1330 / DESIGN_W, 478 / DESIGN_H), {'num_blocks': 1, 'direction': 'horizontal', 'block_width': 70 / DESIGN_W, 'block_height': 5 / DESIGN_H}),
        (WallLine, (1350 / DESIGN_W, 108 / DESIGN_H), {'num_blocks': 1, 'direction': 'horizontal', 'block_width': 70 / DESIGN_W, 'block_height': 5 / DESIGN_H})
    ]

    for wall_cls, (x_r, y_r), kwargs in wall_definitions_ratios:
        k = kwargs.copy()
        k['block_width'] = int(k['block_width'] * screen_width)
        k['block_height'] = int(k['block_height'] * screen_height)
        wall_x = int(x_r * screen_width)
        wall_y = int(y_r * screen_height)
        wall_line = wall_cls(wall_x, wall_y, **k)
        wall_line.build(all_sprites, solid_obstacles)

    running = True
    while running:
        delta_time = clock.tick(60) / 1000

        switch_timer += delta_time
        if switch_timer > controle_switch:
            # automatique change of player after a certain time
            keylisteners[active_player].keys.clear()
            active_player = (active_player + 1) % 4
            switch_timer = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # touche pour changer d'armes
                elif event.key == pygame.K_1:
                    arme_actuelle = "slipper"
                elif event.key == pygame.K_2:
                    arme_actuelle = "soup"
                elif event.key == pygame.K_3:
                    arme_actuelle = "toilet"
                elif event.key == pygame.K_4:
                    arme_actuelle = "boomerang"
                keylisteners[active_player].add_key(event.key)
            elif event.type == pygame.KEYUP:
                keylisteners[active_player].remove_key(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    try:
                        player = players[active_player]
                        mouse_pos = pygame.mouse.get_pos()
                        # to choose weapon
                        if arme_actuelle == "slipper":
                            proj = ExplodingSlipper.fire(player.rect.center, mouse_pos)
                            projectiles.add(proj)
                        elif arme_actuelle == "soup":
                            proj = BurningSoup.fire(player.rect.center, mouse_pos)
                            projectiles.add(proj)
                        elif arme_actuelle == "toilet":
                            rolls = ToiletPaperRoll.fire(player.rect.center, mouse_pos)
                            for roll in rolls:
                                projectiles.add(roll)
                        elif arme_actuelle == "boomerang":
                            proj = BoomerangDenture.fire(player.rect.center, mouse_pos)
                            projectiles.add(proj)
                        print("Tir effectué par:", arme_actuelle)  # Petit debug sympa
                    except Exception as e:
                        print(f"Erreur lors du tir : {e}")

        # print timer for the players
        time_left = int(controle_switch - switch_timer)
        if time_left < 0:
            time_left = 0

        timer_text = font.render(str(time_left), True, (0, 0, 0))
        timer_rect = timer_text.get_rect(midtop=(screen.get_width() // 2, 10))

        # cloud mooving (paralaxe)
        cloud_x_5 = (cloud_x_5 - cloud_speed_5 * delta_time) % (screen_width + cloud_w)

        screen.blit(background_img, (0, 0))
        screen.blit(cloud_layer_5, (int(cloud_x_5), 0))
        screen.blit(map_img, (0, 0))
        screen.blit(timer_text, timer_rect)

        all_sprites.update(solid_obstacles)
        player_group.draw(screen)
        projectiles.update(solid_obstacles)
        projectiles.draw(screen)

        #arrow on top of the player to know which one we are playing with
        player = players[active_player]
        arrow_rect = arrow_img.get_rect(midbottom=(player.rect.centerx, player.rect.top - 8))
        screen.blit(arrow_img, arrow_rect)

        health5_rect=health5_img.get_rect(midbottom=(300,200))
        screen.blit(health5_img, health5_rect)
        

        for projectile in projectiles :
            if pygame.sprite.collide_mask(projectile, player):
                player_health[active_player]-= 1
                projectile.kill()

        pygame.display.set_caption(f"Funny Granny - FPS: {clock.get_fps():.2f}")
        pygame.display.update()


# elif event.type == pygame.MOUSEBUTTONDOWN:
# if event.button == 1:  # Left mouse button
# pos = pygame.mouse.get_pos()
# print()

###  a faire ##
# - limiter le nombre d'utilisation des armes (genre on peut tirer 3 fois max sinon c'est op) et utiliser que 1 seule armes sur les 45 secondes des tours
# - afficher l'armes que on est en train d'utiliser sur le player, ou un message en haut de l'écran ou jsp juste que on sache
# - faire affihcer les sprites qui sont dans assets/items
# - BONUS, ajouter l'armes qui eparpille les bullets la, trouver un nom, et demander a tom de faire un sprite
# - changer les trajectoires pour en avoir 1 qui est plus droite (celle qui explose pas par exemple) faire genre un snipe pour tirer de loin
# - BONUS, afficher la trajectoires a l'écran pour que les joueurs puissent viser à l'aide la trajectoire
# - verifier l'erreur du fait que on ne peut utiliser que 1 des deux armes, les deux sont pareils si on appuis sur 1 ou 2
# - ajouter des commentaires pas chat sur le programme