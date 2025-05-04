import pygame as pg
import math
import random

soup_img = pg.image.load("assets/items/soup.png")
pill_img = pg.image.load("assets/items/pill.png")
grenade_img =pg.image.load("assets/items/grenade_it.png")
pill_img = pg.transform.scale(pill_img, (40,40))
soup_img = pg.transform.scale(soup_img, (40,40))
grenade_img = pg.transform.scale(grenade_img, (40,40))

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
        if self.rect.top > 1000 or self.rect.left > 3000 or self.rect.right < 0:
            self.kill()

    def on_impact(self):
        self.kill()


class ExplodingSlipper(ThrowableWeapon):
    def __init__(self, pos, angle, puissance):
        super().__init__(pos, angle, puissance, gravite=0.6, degats=25)
        self.image = pill_img
        self.rect = self.image.get_rect(center=self.pos)

    def on_impact(self):
        self.kill()

    @staticmethod
    def fire(player_pos, mouse_pos):
        distance = 115
        dx = mouse_pos[0] - player_pos[0]
        dy = mouse_pos[1] - player_pos[1]
        angle = math.degrees(math.atan2(-dy, dx))
        offset_x = distance * math.cos(math.radians(angle))
        offset_y = -distance * math.sin(math.radians(angle))
        spawn_pos = (player_pos[0] + offset_x, player_pos[1] + offset_y)
        return ExplodingSlipper(spawn_pos, angle, puissance=15)



class BurningSoup(ThrowableWeapon):
    def __init__(self, pos, angle, puissance):
        super().__init__(pos, angle, puissance, gravite=0.5, degats=10)
        self.image = grenade_img
        self.rect = self.image.get_rect(center =pos)

    def on_impact(self):
        print("Soupe brûlante sur le sol")
        flaque = SoupPuddle(self.rect.center)
        self.groups()[0].add(flaque)
        self.kill()

    @staticmethod
    def fire(player_pos, mouse_pos):
        distance = 115
        dx = mouse_pos[0] - player_pos[0]
        dy = mouse_pos[1] - player_pos[1]
        angle = math.degrees(math.atan2(-dy, dx))
        offset_x = distance * math.cos(math.radians(angle))
        offset_y = -distance * math.sin(math.radians(angle))
        spawn_pos = (player_pos[0] + offset_x, player_pos[1] + offset_y)
        return BurningSoup(spawn_pos, angle, puissance=15)



class SoupPuddle(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pg.Surface((40, 20), pg.SRCALPHA)
        self.image.fill((100, 255, 100, 180))  #vert clair sah
        self.rect = self.image.get_rect(center=pos)
        self.timer = 5.0  #durée de vie (secondes)

    def update(self, *args):
        # supprime la flaque au bout d'un certain temps (erwann t un bg)
        dt = 1 / 60.0
        self.timer -= dt
        if self.timer <= 0:
            self.kill()


class ToiletPaperRoll(pg.sprite.Sprite):
    def __init__(self, pos, angle, vitesse=10, degats=5):
        super().__init__()
        self.image = pg.Surface((8, 8))
        self.image.fill((255, 255, 255))  #blanc
        self.rect = self.image.get_rect(center=pos)
        self.pos = pg.Vector2(pos)

        #mouvement linear
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

        if self.rect.top > 1000 or self.rect.left > 3000 or self.rect.right < 0:
            self.kill()

    def on_impact(self):
        self.kill()


    @staticmethod
    def fire(player_pos, mouse_pos):
        dx = mouse_pos[0] - player_pos[0]
        dy = mouse_pos[1] - player_pos[1]
        angle = math.degrees(math.atan2(-dy, dx))
        rouleaux = []
        distance = 30  #distance in pixels in front of the player

        for _ in range(5):  #rouleaux envoyés avec écart
            offset = random.uniform(-5, 5)
            effective_angle = angle + offset
            offset_x = distance * math.cos(math.radians(effective_angle))
            offset_y = -distance * math.sin(math.radians(effective_angle))
            spawn_pos = (player_pos[0] + offset_x, player_pos[1] + offset_y)
            proj = ToiletPaperRoll(spawn_pos, effective_angle)
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
        self.portee_max = 350
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
        
        if self.en_retour == True and distance <= 10:
            self.kill()

        for obstacle in obstacles_group:
            if pg.sprite.collide_mask(self, obstacle):
                self.on_impact()
                break

        if self.rect.top > 1000 or self.rect.left > 3000 or self.rect.right < 0:
            self.kill()

    def on_impact(self):
        self.kill()


    @staticmethod
    def fire(player_pos, mouse_pos):
        distance = 120
        dx = mouse_pos[0] - player_pos[0]
        dy = mouse_pos[1] - player_pos[1]
        angle = math.degrees(math.atan2(-dy, dx))
        offset_x = distance * math.cos(math.radians(angle))
        offset_y = -distance * math.sin(math.radians(angle))
        spawn_pos = (player_pos[0] + offset_x, player_pos[1] + offset_y)
        return BoomerangDenture(spawn_pos, angle)