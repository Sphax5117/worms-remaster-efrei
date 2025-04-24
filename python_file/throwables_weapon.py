import pygame as pg
import math

class ThrowableWeapon(pg.sprite.Sprite):
    def __init__(self, pos, angle, power, gravity=0.5, damage=10):
        super().__init__()
        self.image = pg.Surface((10, 10))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=pos)
        self.pos = pg.Vector2(pos)
        self.velocity = pg.Vector2(
            power * math.cos(math.radians(angle)),
            -power * math.sin(math.radians(angle))
        )
        self.gravity = gravity
        self.damage = damage
        self.alive = True

    def update(self, obstacles_group):
        # Apply gravity
        self.velocity.y += self.gravity
        self.pos += self.velocity
        self.rect.center = self.pos

        for obstacle in obstacles_group:
            if pg.sprite.collide_mask(self, obstacle):
                self.on_impact()
                break

        if self.rect.top > 1000 or self.rect.left > 2000 or self.rect.right < 0:
            self.kill()

    def on_impact(self):
        print("Impact detected override this method")
        self.kill()


class ExplodingSlipper(ThrowableWeapon):
    def __init__(self, pos, angle, power):
        super().__init__(pos, angle, power, gravity=0.6, damage=25)
        self.image.fill((200, 100, 0))  # Chausson = marron/orange

    def on_impact(self):
        print("Chausson explosif a explosé !")

        self.kill()
