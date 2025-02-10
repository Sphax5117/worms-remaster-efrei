import pygame
from sys import exit
class Item_heal:
    pygame.init()
    def __init__(self, x, y, item_type, item_path):
        self.item_type = item_type
        self.image=  pygame.image.load(item_path)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collected = False
        self.x = x
        self.y = y
        self.width = width
    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, self.rect)
    def check_collected(self):
        if self.rect.collidepoint(player_rect) and not self.collected:
            self.collected = True
            return True
        return False

    items = [
        Item(300, 250, "sword", sword_img),
        Item(500, 350, "gun", gun_img),
        Item(600, 200, "potion", potion_img)
    ]