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

    # resolution design
    DESIGN_W = 1920
    DESIGN_H = 1080

    # assets
    base_path = Path(__file__).resolve().parent
    bg = base_path / '..' / 'assets' / 'gameon' / 'bg.png'
    cloud2 = base_path / '..' / 'assets' / 'gameon' / '3.png'
    cloud3 = base_path / '..' / 'assets' / 'gameon' / '4.png'
    cloud4 = base_path / '..' / 'assets' / 'gameon' / '5.png'
    mapimg = base_path / '..' / 'assets' / 'gameon' / 'maptest.png'

    screen_width, screen_height = screensize
    clock = pygame.time.Clock()

    # Load and scale assets with convert/convert_alpha for better blitting
    background_img = pygame.transform.scale(pygame.image.load(str(bg)).convert(), (screen_width, screen_height))
    cloud_layer_2 = pygame.transform.scale(pygame.image.load(str(cloud2)).convert_alpha(), (screen_width, screen_height - 10))
    cloud_layer_5 = pygame.transform.scale(pygame.image.load(str(cloud4)).convert_alpha(), (screen_width, screen_height - 10))
    map_img = pygame.transform.smoothscale(pygame.image.load(str(mapimg)).convert_alpha(), (screen_width, screen_height))

    cloud_w = cloud_layer_2.get_width()
    cloud_x_5 = random.randint(0, screen_width)
    cloud_speed_5 = 20

    # SPRITE GROUPS
    all_sprites = pygame.sprite.LayeredUpdates()
    solid_obstacles = pygame.sprite.Group()
    keylistener = Keylistener()
    player = Player(keylistener, screen_width // 2, screen_height // 2)
    all_sprites.add(player, layer=1)  # player above obstacles
    player_group = pygame.sprite.Group(player)

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                keylistener.add_key(event.key)
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.KEYUP:
                keylistener.remove_key(event.key)

        # Cloud layers with integer cast and modulo for wrapping
        cloud_x_5 = (cloud_x_5 - cloud_speed_5 * delta_time) % (screen_width + cloud_w)

        screen.blit(background_img, (0, 0))
        screen.blit(cloud_layer_5, (int(cloud_x_5), 0))
        screen.blit(map_img, (0, 0))


        all_sprites.update(solid_obstacles)
        player_group.draw(screen)

        # Show FPS in the window title for debugging
        pygame.display.set_caption(f"Funny Granny - FPS: {clock.get_fps():.2f}")

        pygame.display.update()