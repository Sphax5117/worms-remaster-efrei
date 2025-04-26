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
        #apply gravity
        self.velocity.y += self.gravity
        self.pos += self.velocity
        self.rect.center = self.pos

        #collision detection
        for obstacle in obstacles_group:
            if pg.sprite.collide_mask(self, obstacle):
                self.on_impact()
                break

        #out of bounds check
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
        self.groups()[0].add(puddle)  
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
        self.image.fill((100, 255, 100, 180))  
        self.rect = self.image.get_rect(center=pos)
        self.timer = 5.0  

    def update(self, *args):
        dt = 1 / 60.0
        self.timer -= dt
        if self.timer <= 0:
            self.kill()

    def slow_effect(self, player):
        player.speed = max(2, player.speed - 3)


### a faire ###
# - limiter le nombre d'utilisation des armes (genre on peut tirer 3 fois max sinon c'est op) et utiliser que 1 seule armes sur les 45 secondes des tours
# - afficher l'armes que on est en train d'utiliser sur le player, ou un message en haut de l'écran ou jsp juste que on sache
# - faire affihcer les sprites qui sont dans assets/items 
# - BONUS, ajouter l'armes qui eparpille les bullets la, trouver un nom, et demander a tom de faire un sprite 
# - changer les trajectoires pour en avoir 1 qui est plus droite (celle qui explose pas par exemple) faire genre un snipe pour tirer de loin
# - BONUS, afficher la trajectoires a l'écran pour que les joueurs puissent viser à l'aide la trajectoire
# - verifier l'erreur du fait que on ne peut utiliser que 1 des deux armes, les deux sont pareils si on appuis sur 1 ou 2
# - ajouter des commentaires pas chat sur le programme