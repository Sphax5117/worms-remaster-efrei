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