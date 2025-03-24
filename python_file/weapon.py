import pygame as pg
import random
import math


# class bullet
class Bullet(pg.sprite.Sprite):
    def __init__(self, pos, direction, speed=10, damage=5):
        super().__init__()
        self.image = pg.Surface((5, 5))  # Taille de la balle
        self.image.fill((255, 0, 0))  # Couleur rouge
        self.rect = self.image.get_rect(center=pos)
        self.direction = pg.Vector2(direction).normalize()
        self.speed = speed
        self.damage = damage

    def update(self):
        """moove the bullet and destroy it if out of the screen."""
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        # destroy the bullet if out of the screen
        if self.rect.right < 0 or self.rect.left > 800 or self.rect.bottom < 0 or self.rect.top > 600:
            self.kill()


# base class for the weapon
class Weapon(pg.sprite.Sprite):
    def __init__(self, name, damage, fire_range, ammo, sprite_path):
        super().__init__()
        self.name = name
        self.damage = damage
        self.fire_range = fire_range
        self.ammo = ammo
        self.image = pg.image.load(sprite_path).convert_alpha()
        self.image = pg.transform.scale(self.image, (50, 50))  # Redimensionner
        self.rect = self.image.get_rect()

    def fire(self, pos, direction, bullets_group):
        """gun fire method, to define in function on the weapon"""
        if self.ammo > 0:
            self.ammo -= 1
            bullet = Bullet(pos, direction)
            bullets_group.add(bullet)  # Ajoute la balle au groupe de balles
            print(f"{self.name} a tiré! Munitions restantes: {self.ammo}")
        else:
            print(f"{self.name} n'a plus de munitions!")

    def reload(self, amnt):
        """reload with a specific amount of bullet"""
        self.ammo += amnt
        print(f"{self.name} rechargé avec {amnt} munitions.")


# Shotgun (test)
class Shotgun(Weapon):
    def __init__(self):
        super().__init__("Shotgun", damage=5, fire_range=200, ammo=6, sprite_path="assets/weapons/shotgun.png")
        self.pellets = 6  # Nombre de balles par tir

    def fire(self, pos, direction, bullets_group):
        """spreading of the shotgun"""
        if self.ammo > 0:
            self.ammo -= 1
            for _ in range(self.pellets):
                angle_offset = random.uniform(-15, 15)  # Dispersion en degrés
                angle_rad = math.radians(angle_offset)
                new_dir = pg.Vector2(
                    math.cos(angle_rad) * direction.x - math.sin(angle_rad) * direction.y,
                    math.sin(angle_rad) * direction.x + math.cos(angle_rad) * direction.y
                ).normalize()

                bullet = Bullet(pos, new_dir)
                bullets_group.add(bullet)

            print(f"{self.name} a tiré! Munitions restantes: {self.ammo}")
        else:
            print(f"{self.name} n'a plus de munitions!")
