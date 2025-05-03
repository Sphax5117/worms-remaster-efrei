import pygame as pg
import math
import random

# basic class
class ThrowableWeapon(pg.sprite.Sprite):
    def __init__(self, pos, angle, puissance, gravite=0.5, degats=10):
        super().__init__()
        self.image = pg.Surface((10, 10))
        self.image.fill((255, 255, 0))  # Jaune defaut
        self.rect = self.image.get_rect(center=pos)
        self.pos = pg.Vector2(pos)

        # speed initial of projectil
        self.vitesse_vecteur = pg.Vector2(
            puissance * math.cos(math.radians(angle)),
            -puissance * math.sin(math.radians(angle))
        )
        self.gravite = gravite
        self.degats = degats

    def update(self, obstacles_group):
        # Gestion de la gravité + déplacement
        self.vitesse_vecteur.y += self.gravite
        self.pos += self.vitesse_vecteur
        self.rect.center = self.pos

        # verify the colision
        for obstacle in obstacles_group:
            if pg.sprite.collide_mask(self, obstacle):
                self.on_impact()
                break

        # Check hors screen
        if self.rect.top > 1000 or self.rect.left > 2000 or self.rect.right < 0:
            self.kill()

    def on_impact(self):
        print("Impact détecté - arme générique")
        self.kill()


class ExplodingSlipper(ThrowableWeapon):
    def __init__(self, pos, angle, puissance):
        super().__init__(pos, angle, puissance, gravite=0.6, degats=25)
        self.image.fill((200, 100, 0))  # Marron/orange

    def on_impact(self):
        print("chausson explosé sur l'obstacle !")
        self.kill()

    @staticmethod
    def fire(player_pos, mouse_pos):
        dx = mouse_pos[0] - player_pos[0]
        dy = mouse_pos[1] - player_pos[1]
        angle = math.degrees(math.atan2(-dy, dx))
        return ExplodingSlipper(player_pos, angle, puissance=15)


class BurningSoup(ThrowableWeapon):
    def __init__(self, pos, angle, puissance):
        super().__init__(pos, angle, puissance, gravite=0.5, degats=10)
        self.image.fill((0, 150, 0))  #Vert

    def on_impact(self):
        print("Soupe brûlante sur le sol")
        flaque = SoupPuddle(self.rect.center)
        self.groups()[0].add(flaque)
        self.kill()

    @staticmethod
    def fire(player_pos, mouse_pos):
        dx = mouse_pos[0] - player_pos[0]
        dy = mouse_pos[1] - player_pos[1]
        angle = math.degrees(math.atan2(-dy, dx))
        return BurningSoup(player_pos, angle, puissance=15)


class SoupPuddle(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pg.Surface((40, 20), pg.SRCALPHA)
        self.image.fill((100, 255, 100, 180))  # Vert clair sah
        self.rect = self.image.get_rect(center=pos)
        self.timer = 5.0  # Durée de vie (secondes)

    def update(self, *args):
        # supprime la flaque au bout d'un certain temps (erwan t un bg)
        dt = 1 / 60.0
        self.timer -= dt
        if self.timer <= 0:
            self.kill()


class ToiletPaperRoll(pg.sprite.Sprite):
    def __init__(self, pos, angle, vitesse=10, degats=5):
        super().__init__()
        self.image = pg.Surface((8, 8))
        self.image.fill((255, 255, 255))  # Blanc
        self.rect = self.image.get_rect(center=pos)
        self.pos = pg.Vector2(pos)

        # Mouvement linear
        self.vitesse_vecteur = pg.Vector2(
            vitesse * math.cos(math.radians(angle)),
            -vitesse * math.sin(math.radians(angle))
        )
        self.degats = degats

    def update(self, obstacles_group):
        self.pos += self.vitesse_vecteur
        self.rect.center = self.pos

        for obstacle in obstacles_group:
            if pg.sprite.collide_mask(self, obstacle):
                self.on_impact()
                break

        if self.rect.top > 1000 or self.rect.left > 2000 or self.rect.right < 0:
            self.kill()

    def on_impact(self):
        print("papier toilette a touché quelque chose")
        self.kill()

    @staticmethod
    def fire(player_pos, mouse_pos):
        dx = mouse_pos[0] - player_pos[0]
        dy = mouse_pos[1] - player_pos[1]
        angle = math.degrees(math.atan2(-dy, dx))
        rouleaux = []
        for _ in range(5):  # rouleaux envoyés avec écart
            offset = random.uniform(-5, 5)
            proj = ToiletPaperRoll(player_pos, angle + offset)
            rouleaux.append(proj)
        return rouleaux


class BoomerangDenture(pg.sprite.Sprite):
    def __init__(self, pos, angle, vitesse=8, degats=20):
        super().__init__()
        self.image = pg.Surface((14, 14))
        self.image.fill((255, 200, 200))  # pink
        self.rect = self.image.get_rect(center=pos)
        self.start_pos = pg.Vector2(pos)
        self.pos = pg.Vector2(pos)

        # Init direction
        self.vitesse_vecteur = pg.Vector2(
            vitesse * math.cos(math.radians(angle)),
            -vitesse * math.sin(math.radians(angle))
        )
        #to modify to change the distance of the dentier
        self.portee_max = 250
        self.en_retour = False
        self.degats = degats

    def update(self, obstacles_group):
        self.pos += self.vitesse_vecteur
        self.rect.center = self.pos

        distance = self.pos.distance_to(self.start_pos)
        if distance >= self.portee_max and not self.en_retour:
            #Le dentier invers the trajectoire for revenir in the place initiale
            self.vitesse_vecteur *= -1
            self.en_retour = True

        for obstacle in obstacles_group:
            if pg.sprite.collide_mask(self, obstacle):
                self.on_impact()
                break

        if self.rect.top > 1000 or self.rect.left > 2000 or self.rect.right < 0:
            self.kill()

    def on_impact(self):
        print("dentier boomerang a touché sa cible")
        self.kill()

    @staticmethod
    def fire(player_pos, mouse_pos):
        dx = mouse_pos[0] - player_pos[0]
        dy = mouse_pos[1] - player_pos[1]
        angle = math.degrees(math.atan2(-dy, dx))
        return BoomerangDenture(player_pos, angle)