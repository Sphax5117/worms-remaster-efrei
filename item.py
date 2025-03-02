import pygame
from sys import exit
class Item:
    pygame.init()
    def __init__(self, x, y, item_type, item_path,effect):
        self.item_type = item_type
        self.image=  pygame.image.load(item_path)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collected = False
        self.effect=effect

    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, self.rect)

    def check_collected(self):
        if self.rect.colliderect(player_rect) and not self.collected:
            self.collected = True
            return True
        return False

    def heal_player_soup(self):
        self.health=min(self.health+20,100)
