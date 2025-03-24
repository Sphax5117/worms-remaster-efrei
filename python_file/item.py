import pygame
import players
from sys import exit
pygame.init()
class Item:
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
        if self.rect.colliderect(self.rect) and not self.collected:
            self.collected = True
            self.effect()
            return True
        return False

    def heal_player_soup(self):
        self.health=min(self.health+20,100)
        print(f'Healing {self.health}')

    def pill_boost(self):
        self.speed+=5
        self.defense+=5
        print(f"Speed and defense boosted! Speed: {self.speed}, Defense: {self.defense}")

    pill=Item("pill",,pill_boost)
    soup=Item("soup",,heal_player_soup)
    items=[pill,soup]
