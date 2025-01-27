
import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Menu Example")
font = pygame.font.SysFont(None, 48)

menu_options = ["Start Game", "Options", "Quit"]
selected_index = 0
clock = pygame.time.Clock()

running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                selected_index = (selected_index + 1) % len(menu_options)
            elif event.key == pygame.K_UP:
                selected_index = (selected_index - 1) % len(menu_options)
            elif event.key == pygame.K_RETURN:
                if menu_options[selected_index] == "Quit":
                    running = False
                # Handle other options as needed

    for i, option in enumerate(menu_options):
        color = (200, 200, 200) if i == selected_index else (100, 100, 100)
        text_surface = font.render(option, True, color)
        screen.blit(text_surface, (250, 150 + i * 60))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()