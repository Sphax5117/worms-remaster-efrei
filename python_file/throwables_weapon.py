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

        # Collision detection
        for obstacle in obstacles_group:
            if pg.sprite.collide_mask(self, obstacle):
                self.on_impact()
                break

        # Out of bounds check
        if self.rect.top > 1000 or self.rect.left > 2000 or self.rect.right < 0:
            self.kill()

    def on_impact(self):
        print("Impact detected")
        self.kill()


class ExplodingSlipper(ThrowableWeapon):
    def __init__(self, pos, angle, power):
        super().__init__(pos, angle, power, gravity=0.6, damage=25)
        self.image.fill((200, 100, 0))

    def on_impact(self):
        print("Chausson explosif a explosé !")
        self.kill()

    @staticmethod
    def fire(player_pos, mouse_pos):
        dx = mouse_pos[0] - player_pos[0]
        dy = mouse_pos[1] - player_pos[1]
        angle = math.degrees(math.atan2(-dy, dx))
        power = 15
        return ExplodingSlipper(player_pos, angle, power)


class BurningSoup(ThrowableWeapon):
    def __init__(self, pos, angle, power):
        super().__init__(pos, angle, power, gravity=0.5, damage=10)
        self.image.fill((0, 150, 0))

    def on_impact(self):
        print(" Soupe brûlante répandue !")
        puddle = SoupPuddle(self.rect.center)
        self.groups()[0].add(puddle)  # Ajoute dans le même groupe que le projectile
        self.kill()

    @staticmethod
    def fire(player_pos, mouse_pos):
        dx = mouse_pos[0] - player_pos[0]
        dy = mouse_pos[1] - player_pos[1]
        angle = math.degrees(math.atan2(-dy, dx))
        power = 15
        return BurningSoup(player_pos, angle, power)


class SoupPuddle(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pg.Surface((40, 20), pg.SRCALPHA)
        self.image.fill((100, 255, 100, 180))  # Vert translucide
        self.rect = self.image.get_rect(center=pos)
        self.timer = 5.0  # Durée de vie en secondes

    def update(self, *args):
        dt = 1 / 60.0
        self.timer -= dt
        if self.timer <= 0:
            self.kill()

    def slow_effect(self, player):
        player.speed = max(2, player.speed - 3)
