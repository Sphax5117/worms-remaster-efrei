import pygame
import os
import random
from sys import exit
from pathlib import Path

from player import Player, Keylistener
from collision import WallLine

def game_on(screen, screensize):
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
    pygame.display.set_caption("Funny Granny")
    font = pygame.font.SysFont(None, 150)

    # resolution design
    DESIGN_W = 1920
    DESIGN_H = 1080

    # assets
    base_path = Path(__file__).resolve().parent
    bg = base_path / '..' / 'assets' / 'gameon' / 'bg.png'
    cloud2 = base_path / '..' / 'assets' / 'gameon' / '3.png'
    cloud4 = base_path / '..' / 'assets' / 'gameon' / '5.png'
    mapimg = base_path / '..' / 'assets' / 'gameon' / 'maptest.png'
    arrow = base_path / '..' / 'assets' / 'gameon' / 'arrow.png'
    arrow_img = pygame.image.load(arrow).convert_alpha()
    arrow_img = pygame.transform.scale(arrow_img, (30,50))

    screen_width, screen_height = screensize
    clock = pygame.time.Clock()

    # Load and scale assets with convert/convert_alpha for better blitting
    background_img = pygame.transform.scale(pygame.image.load(str(bg)).convert(), (screen_width, screen_height))
    cloud_layer_2 = pygame.transform.scale(pygame.image.load(str(cloud2)).convert_alpha(), (screen_width, screen_height - 10))
    cloud_layer_5 = pygame.transform.scale(pygame.image.load(str(cloud4)).convert_alpha(), (screen_width, screen_height - 10))
    map_img = pygame.transform.smoothscale(pygame.image.load(str(mapimg)).convert_alpha(), (screen_width, screen_height))
    spawn_position = [(370, 158), (372, 158), (374, 158), (376,158), (376,158)]

    cloud_w = cloud_layer_2.get_width()
    cloud_x_5 = random.randint(0, screen_width)
    cloud_speed_5 = 20

    # SPRITE GROUPS
    all_sprites = pygame.sprite.LayeredUpdates()
    solid_obstacles = pygame.sprite.Group()
    all_sprites = pygame.sprite.LayeredUpdates()

    # create 4 players
    player_positions = random.sample(spawn_position, 4)
    players = []
    keylisteners = []
    active_player = 0
    controle_switch = 45
    switch_timer = 0

    #for 2 mamy and 2 papy
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


    # for the wall obstacle
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
        (WallLine, (560 / DESIGN_W, 542 / DESIGN_H), {'num_blocks': 10, 'direction': 'vertical', 'block_width': 170 / DESIGN_W, 'block_height': 10 / DESIGN_H})
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
        
        #timer to switch the player that you are currently using
        switch_timer += delta_time
        if switch_timer > controle_switch:
            # Clear keys for outgoing player (avoid stuck movement)
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
                keylisteners[active_player].add_key(event.key)
            elif event.type == pygame.KEYUP:
                keylisteners[active_player].remove_key(event.key)
        
        # Calculate time remaining for current player
        time_left = int(controle_switch - switch_timer)
        if time_left < 0:  # just in case!
            time_left = 0

        timer_text = font.render(str(time_left), True, (0, 0, 0))  # big black numbers
        timer_rect = timer_text.get_rect(midtop=(screen.get_width() // 2, 10))


        # Cloud layers with integer cast and modulo for wrapping
        cloud_x_5 = (cloud_x_5 - cloud_speed_5 * delta_time) % (screen_width + cloud_w)

        screen.blit(background_img, (0, 0))
        screen.blit(cloud_layer_5, (int(cloud_x_5), 0))
        screen.blit(map_img, (0, 0))
        screen.blit(timer_text, timer_rect)


        all_sprites.update(solid_obstacles)
        player_group.draw(screen)

        # Draw the arrow above the active player
        player = players[active_player]  # Player object, not the group!
        arrow_rect = arrow_img.get_rect(midbottom=(player.rect.centerx, player.rect.top - 8))
        screen.blit(arrow_img, arrow_rect)



        # Show FPS in the window title for debugging
        pygame.display.set_caption(f"Funny Granny - FPS: {clock.get_fps():.2f}")

        pygame.display.update()