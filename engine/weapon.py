import pygame as pg
import math

class Weapon:
    def __init__(self, name, damage, range, ammo, sprite_pa):
        self.name = name
        self.damage = damage
        self.range = range
        self.ammo = ammo
        self.sprite = pg.image(sprite_pa)

    def fire(self, pos, direction):
        """gun fire method, to define as function of the weapons that we will set up"""
        pass

    def reload(self, amnt):
        """reload method with a specific amount"""
    self.ammo += amnt

    def draw(self,screen, position):
        """Display the weapons on the screen"""
        screen.blit(self.sprite, position)