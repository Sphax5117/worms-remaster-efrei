import pygame
import os
import random
import math
from sys import exit
from pathlib import Path
from throwables_weapon import ExplodingSlipper, BurningSoup, ToiletPaperRoll, BoomerangDenture

from player import Player, Keylistener
from collision import WallLine
from readyscreen import readyscreen


def print_trajectory(screen, start_pos, mouse_pos, weapon):
    # physical parameter
    if weapon == "slipper":
        power = 15
        gravity = 0.6
    elif weapon == "soup":
        power = 15
        gravity = 0.5
    else:
        return  # no print if no weapon

    # calculation of speed
    dx = mouse_pos[0] - start_pos[0]
    dy = mouse_pos[1] - start_pos[1]
    angle = math.atan2(-dy, dx)
    speed_x = power * math.cos(angle)
    speed_y = -power * math.sin(angle)

    # simulation by pts
    num_pts = 50  # number of pts
    t_interval = 0.2  # times interval

    for i in range(num_pts):
        t = i * t_interval
        x = start_pos[0] + speed_x * t
        y = start_pos[1] + speed_y * t + 0.5 * gravity * (t ** 2)

        #stop if point go out the screen
        if x < 0 or x > screen.get_width() or y < 0 or y > screen.get_height():
            break

        # draw the trajectory in color
        couleur = (255, 0, 0) if weapon == "slipper" else (0, 150, 0)  #red for slipper and green for soup
        pygame.draw.circle(screen, couleur, (int(x), int(y)), 3)  #draw the circle


#definition of the function taht allows to dsiplay a winning screen when a player is at 0 hearth 
def winning_screen(screen, winner_image):
    #fill the screen in a white screen and blit the image and wait 5 seconds
    screen.fill((255, 255, 255))  
    screen.blit(winner_image, (screen.get_width() // 2 - winner_image.get_width() // 2, screen.get_height() // 2 - winner_image.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(5000)


#definition of the game_on( ) function taht allows to play the game (mix of player, collision, weapon, ready screen and all)
def game_on(screen, screensize):
    #the ready screen
    #readyscreen(screen,screensize, 5)

    #initialize the screen + caption
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
    pygame.display.set_caption("Funny Granny")

    #usefull variables all used in the rest of the programm
    font = pygame.font.SysFont(None, 150)
    DESIGN_W = 1920
    DESIGN_H = 1080
    screen_width, screen_height = screensize
    clock = pygame.time.Clock()
    pass_turn = False
    controle_switch = 15
    switch_timer = 0

    #load all the assest needed (Base path for mare stability, and to patch the error of the system different)
    base_path = Path(__file__).resolve().parent
    bg = base_path / '..' / 'assets' / 'gameon' / 'bg.png'
    mapimg = base_path / '..' / 'assets' / 'gameon' / 'maptest.png'
    arrow = base_path / '..' / 'assets' / 'gameon' / 'arrow.png'
    health5 = base_path / '..' / 'assets' / 'lives' / 'health_5.png'
    health4 = base_path / '..' / 'assets' / 'lives' / 'health_4.png'
    health3 = base_path / '..' / 'assets' / 'lives' / 'health_3.png'
    health2 = base_path / '..' / 'assets' / 'lives' / 'health_2.png'
    health1 = base_path / '..' / 'assets' / 'lives' / 'health_1.png'
    lives3 = base_path / '..' / 'assets' / 'lives' / '3lives.png'
    lives2 = base_path / '..' / 'assets' / 'lives' / '2lives.png'
    lives1 = base_path / '..' / 'assets' / 'lives' / '1live.png'
    glasses = base_path /'..' / 'assets' / 'items' / 'glasses.png'
    marmel = base_path / '..' / 'assets' / 'items' / 'grenade_it.png'
    pill = base_path / '..' / 'assets' / 'items' / 'pill.png'
    toiletp = base_path / '..' / 'assets' / 'items' / 'toilet_paper.png'
    winningp = base_path / '..' / 'assets' / 'gameon' / 'grandpa_win.png'
    winningg = base_path /'..' / 'assets' / 'gameon' / 'grandma_win.png'
    winningp_img = pygame.image.load(winningp).convert_alpha()
    winningg_img = pygame.image.load(winningg).convert_alpha()
    glasses_img = pygame.image.load(glasses).convert_alpha()
    marmel_img = pygame.image.load(marmel).convert_alpha()
    pill_img = pygame.image.load(pill).convert_alpha()
    toiletp_img = pygame.image.load(toiletp).convert_alpha()
    lives3_img = pygame.image.load(lives3).convert_alpha()
    lives3_img = pygame.transform.scale(lives3_img, (200,60))
    lives2_img = pygame.image.load(lives2).convert_alpha()
    lives2_img = pygame.transform.scale(lives2_img, (200,60))
    lives1_img = pygame.image.load(lives1).convert_alpha()
    lives1_img = pygame.transform.scale(lives1_img, (200,60))
    health5_img = pygame.image.load(health5).convert_alpha()
    health5_img = pygame.transform.scale(health5_img, (100,10))
    health4_img = pygame.image.load(health4).convert_alpha()
    health4_img = pygame.transform.scale(health4_img, (100,10))
    health3_img = pygame.image.load(health3).convert_alpha()
    health3_img = pygame.transform.scale(health3_img, (100,10))
    health2_img = pygame.image.load(health2).convert_alpha()
    health2_img = pygame.transform.scale(health2_img, (100,10))
    health1_img = pygame.image.load(health1).convert_alpha()
    health1_img = pygame.transform.scale(health1_img, (100,10))
    arrow_img = pygame.image.load(arrow).convert_alpha()
    arrow_img = pygame.transform.scale(arrow_img, (30, 50))
    background_img = pygame.transform.scale(pygame.image.load(str(bg)).convert(), (screen_width, screen_height))
    map_img = pygame.transform.smoothscale(pygame.image.load(str(mapimg)).convert_alpha(), (screen_width, screen_height))

    ground_rect = pygame.Rect(-500, screen_height - 70, screen_width + 1000, 20)

    #position of the random spawnes
    spawn_position_ratios = [
        (376 / DESIGN_W, 160 / DESIGN_H),
        (49 / DESIGN_W, 250 / DESIGN_H),
        (750 / DESIGN_W, 120 / DESIGN_H),
        (1835 / DESIGN_W, 50 / DESIGN_H),
        (1835 / DESIGN_W, 120 / DESIGN_H),
        (1050 / DESIGN_W, 310 / DESIGN_H),
        (1300 / DESIGN_W, 500 / DESIGN_H)
    ]

    #definiton off all the sprite needed + group them
    all_sprites = pygame.sprite.LayeredUpdates()
    solid_obstacles = pygame.sprite.Group()
    all_sprites = pygame.sprite.LayeredUpdates()
    projectiles = pygame.sprite.Group()

    ###create the 4 players###
    player_positions = [
        (int(x_r * screen_width), int(y_r * screen_height))
        for (x_r, y_r) in random.sample(spawn_position_ratios, 4)
    ]

    #needed varaibles
    players = []
    keylisteners = []
    active_player = 0
    player_health={0:5, 1:5, 2:5, 3:5}
    lives_papy = 3
    lives_mamy = 3
    actual_weapon = "slipper"
    print_trajectory_active = False   # True = printed by default

    #loop for the creation of player, papy and mamy
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
    ###end of the creation of the players###


    #creation of walls that are basicaly the collision
    wall_definitions_ratios = [
        (WallLine, (48 / DESIGN_W, 415 / DESIGN_H), {'num_blocks': 3, 'direction': 'horizontal', 'block_width': 55 / DESIGN_W, 'block_height': 5 / DESIGN_H}),
        (WallLine, (370 / DESIGN_W, 158 / DESIGN_H), {'num_blocks': 1, 'direction': 'horizontal', 'block_width': 50 / DESIGN_W, 'block_height': 5 / DESIGN_H}),
        (WallLine, (750 / DESIGN_W, 220 / DESIGN_H), {'num_blocks': 2, 'direction': 'horizontal', 'block_width': 85 / DESIGN_W, 'block_height': 5 / DESIGN_H}),
        (WallLine, (1040 / DESIGN_W, 417 / DESIGN_H), {'num_blocks': 2, 'direction': 'horizontal', 'block_width': 82 / DESIGN_W, 'block_height': 5 / DESIGN_H}),
        (WallLine, (1580 / DESIGN_W, 370 / DESIGN_H), {'num_blocks': 2, 'direction': 'horizontal', 'block_width': 82 / DESIGN_W, 'block_height': 5 / DESIGN_H}),
        (WallLine, (1835 / DESIGN_W, 155 / DESIGN_H), {'num_blocks': 1, 'direction': 'horizontal', 'block_width': 55 / DESIGN_W, 'block_height': 5 / DESIGN_H}),
        (WallLine, (850 / DESIGN_W, 672 / DESIGN_H), {'num_blocks': 10, 'direction': 'vertical', 'block_width': 300 / DESIGN_W, 'block_height': 2 / DESIGN_H}),
        (WallLine, (1230 / DESIGN_W, 610 / DESIGN_H), {'num_blocks': 10, 'direction': 'vertical', 'block_width': 520 / DESIGN_W, 'block_height': 2 / DESIGN_H}),
        (WallLine, (120 / DESIGN_W, 825 / DESIGN_H), {'num_blocks': 10, 'direction': 'vertical', 'block_width': 300 / DESIGN_W, 'block_height': 2 / DESIGN_H}),
        (WallLine, (560 / DESIGN_W, 650 / DESIGN_H), {'num_blocks': 10, 'direction': 'vertical', 'block_width': 170 / DESIGN_W, 'block_height': 2 / DESIGN_H}),
        (WallLine, (213 / DESIGN_W, 280 / DESIGN_H), {'num_blocks': 2, 'direction': 'horizontal', 'block_width': 85 / DESIGN_W, 'block_height': 5 / DESIGN_H}),
        (WallLine, (985 / DESIGN_W, 305 / DESIGN_H), {'num_blocks': 1, 'direction': 'horizontal', 'block_width': 75 / DESIGN_W, 'block_height': 5 / DESIGN_H}),
        (WallLine, (1730 / DESIGN_W, 260 / DESIGN_H), {'num_blocks': 1, 'direction': 'horizontal', 'block_width': 70 / DESIGN_W, 'block_height': 5 / DESIGN_H}),
        (WallLine, (505 / DESIGN_W, 478 / DESIGN_H), {'num_blocks': 1, 'direction': 'horizontal', 'block_width': 70 / DESIGN_W, 'block_height': 5 / DESIGN_H}),
        (WallLine, (1330 / DESIGN_W, 478 / DESIGN_H), {'num_blocks': 1, 'direction': 'horizontal', 'block_width': 70 / DESIGN_W, 'block_height': 5 / DESIGN_H}),
        (WallLine, (1350 / DESIGN_W, 108 / DESIGN_H), {'num_blocks': 1, 'direction': 'horizontal', 'block_width': 70 / DESIGN_W, 'block_height': 5 / DESIGN_H})
    ]

    #use to place the collision depend on the screensize of the user
    for wall_cls, (x_r, y_r), kwargs in wall_definitions_ratios:
        k = kwargs.copy()
        k['block_width'] = int(k['block_width'] * screen_width)
        k['block_height'] = int(k['block_height'] * screen_height)
        wall_x = int(x_r * screen_width)
        wall_y = int(y_r * screen_height)
        wall_line = wall_cls(wall_x, wall_y, **k)
        wall_line.build(all_sprites, solid_obstacles)

    ###the principal loop###
    running = True

    while running:
        #clock usefull for limiting the fps of the game + times to switch between players
        delta_time = clock.tick(60) / 1000

        #creation of the clock for the switch player (when 15 second are gone it switch player)
        switch_timer += delta_time
        if switch_timer > controle_switch or pass_turn == True:
            keylisteners[active_player].keys.clear()
            active_player = (active_player + 1) % 4
            switch_timer = 0
            pass_turn = False

        #loop to use the weapons (1,2,3,4) and to exit the game with exit
        for event in pygame.event.get():
            #to exit the game
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                #to change the weapon (to detect the touch)
                elif event.key == pygame.K_1:
                    actual_weapon = "slipper"
                elif event.key == pygame.K_2:
                    actual_weapon = "soup"
                elif event.key == pygame.K_3:
                    actual_weapon = "toilet"
                elif event.key == pygame.K_4:
                    actual_weapon = "boomerang"
                elif event.key == pygame.K_p:
                    print_trajectory_active = not print_trajectory_active  # bascule in the states
                    print(f"Trajectoire {'active' if print_trajectory_active else 'desactive'}")
                keylisteners[active_player].add_key(event.key)
            elif event.type == pygame.KEYUP:
                keylisteners[active_player].remove_key(event.key)
            #to actually use the weapons that the player press the touch
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    try:
                        player = players[active_player]
                        mouse_pos = pygame.mouse.get_pos()
                        # to choose weapon
                        if actual_weapon == "slipper":
                            proj = ExplodingSlipper.fire(player.rect.center, mouse_pos)
                            projectiles.add(proj)
                        elif actual_weapon == "soup":
                            proj = BurningSoup.fire(player.rect.center, mouse_pos)
                            projectiles.add(proj)
                        elif actual_weapon == "toilet":
                            rolls = ToiletPaperRoll.fire(player.rect.center, mouse_pos)
                            for roll in rolls:
                                projectiles.add(roll)
                        elif actual_weapon == "boomerang":
                            proj = BoomerangDenture.fire(player.rect.center, mouse_pos)
                            projectiles.add(proj)
                    except Exception as e:
                        print(f"Erreur lors du tir : {e}")

        #to print timer for the players
        time_left = int(controle_switch - switch_timer)
        if time_left < 0:
            time_left = 0
        timer_text = font.render(str(time_left), True, (0, 0, 0))
        timer_rect = timer_text.get_rect(midtop=(screen.get_width() // 2, 10))

        #to draw all the sprite need in the screen + update them
        pygame.draw.rect(screen, (255, 0, 0), ground_rect) 
        screen.blit(background_img, (0, 0))
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

        if print_trajectory_active and actual_weapon in ["slipper", "soup"]:
            print_trajectory(screen, player.rect.center, pygame.mouse.get_pos(), actual_weapon)

        #display of the health bar above the player head 
        for key in player_health.keys():
            if player_health[key]==5:
                health5_rect= health5_img.get_rect(midbottom=(players[key].rect.centerx, players[key].rect.top - 4))
                screen.blit(health5_img, health5_rect)
            elif player_health[key] == 4 :
                health4_rect = health4_img.get_rect(midbottom = (players[key].rect.centerx, players[key].rect.top - 4))
                screen.blit(health4_img, health4_rect)
            elif player_health[key] == 3 :
                health3_rect = health3_img.get_rect(midbottom = (players[key].rect.centerx, players[key].rect.top - 4))
                screen.blit(health3_img, health3_rect)
            elif player_health[key] == 2 :
                health2_rect = health2_img.get_rect(midbottom = (players[key].rect.centerx, players[key].rect.top - 4))
                screen.blit(health2_img, health2_rect)
            elif player_health[key]==1:
                health1_rect = health1_img.get_rect(midbottom = (players[key].rect.centerx, players[key].rect.top - 4))
                screen.blit(health1_img, health1_rect)
            
        #papy lives at the top left corner
        if lives_papy == 3 :
            lives3_rect = lives3_img.get_rect(center = (100,30))
            screen.blit(lives3_img, lives3_rect)
        elif lives_papy == 2 :
            lives2_rect = lives2_img.get_rect(center = (100,30))
            screen.blit(lives2_img, lives2_rect)
        elif lives_papy == 1 :
            lives1_rect = lives1_img.get_rect(center =(100,30))
            screen.blit(lives1_img, lives1_rect)

        #mamy lives at the top right corner 
        if lives_mamy == 3 :
            lives3_rect = lives3_img.get_rect(center=(screen_width-100,30))
            screen.blit(lives3_img, lives3_rect)
        elif lives_mamy == 2 :
            lives2_rect = lives2_img.get_rect(center= (screen_width-100,30))
            screen.blit(lives2_img, lives2_rect)
        elif lives_mamy == 1 :
            lives1_rect = lives1_img.get_rect(center = (screen_width-100,30))
            screen.blit(lives1_img, lives1_rect)

        count_projectiles=0

        
        #collisions with the player and projectiles 
        for projectile in projectiles:
            for i, p in enumerate(players):
                if player_health[i] > 0 and pygame.sprite.collide_mask(projectile, p) and i != active_player and (i % 2) != active_player % 2:
                    player_health[i] -= 1
                    count_projectiles +=1
                    projectile.kill()
                    #lives handling:
                    if player_health[i] == 0:
                        player_health[i] = 5
                        if i % 2 == 0:                                
                            lives_mamy -= 1
                        else:
                            lives_papy -= 1
                    break 
                elif pygame.sprite.collide_mask(projectile, p) and i != active_player and i % 2 == active_player % 2:
                    projectile.kill()
                else :
                    #to display the winning screen if somone is at 0 hearth
                    if lives_papy ==0:
                        winning_screen(screen, winningg_img)
                        running = False
                    elif lives_mamy == 0 :
                        winning_screen(screen, winningp_img)
                        running = False
        
        #check for collisions with the ground
        for i, player in enumerate(players):
            random_spawn = random.choice(spawn_position_ratios)
            if player.rect.colliderect(ground_rect): 
                if player_health[i] > 0: 
                    player_health[i] -= 5
                    player.rect.topleft = (int(random_spawn[0] * screen_width), int(random_spawn[1] * screen_height))

                    if player_health[i] == 0:
                        player_health[i] = 5
                        if i % 2 == 0:
                            lives_mamy -= 1
                        else:
                            lives_papy -= 1
                pass_turn = True
            else:
                if lives_papy ==0:
                    winning_screen(screen, winningg_img)
                    running = False
                elif lives_mamy == 0 :
                    winning_screen(screen, winningp_img)
                    running = False
        

        #display the number of fps (needed for the debugging) + the nale of the game + update 
        pygame.display.set_caption(f"Funny Granny - FPS: {clock.get_fps():.2f}")
        pygame.display.update()


