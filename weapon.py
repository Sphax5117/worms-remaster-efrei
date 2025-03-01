import pygame as pg


class Weapon:
    def __init__(self, name, damage, fire_range, ammo, sprite_path):
        self.name = name
        self.damage = damage
        self.fire_range = fire_range
        self.ammo = ammo
        self.sprite = pg.image.load(sprite_path)
        self.sprite = pg.transform.scale(self.sprite, (50, 50))  # optional resize

    def fire(self, pos, direction):
        """gun fire method, to define as function of the weapons that we will set up"""
        if self.ammo > 0:
            self.ammo -= 1
            print(f"{self.name} a tiré! Munitions restantes: {self.ammo}")
        else:
            print(f"{self.name} n'a plus de munitions!")

    def reload(self, amnt):
        """reload method with a specific amount"""
        self.ammo += amnt
        print(f"{self.name} rechargé avec {amnt} munitions.")

    def draw(self, screen, position):
        """Display the weapons on the screen"""
        screen.blit(self.sprite, position)


class Bullet:
    def __init__(self, pos, direction, speed=10, damage=5):
        self.pos = pg.Vector2(pos)
        self.direction = direction
        self.speed = speed
        self.damage = damage
        sel.alive
