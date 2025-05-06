import pygame as pg
import math
import random
from pathlib import Path

#the sprite needed to the calsses
base_path = Path(__file__).resolve().parent
pill = base_path / '..' / 'assets' / 'items' / 'pill.png'
grenade = base_path / '..' / 'assets' / 'items' / 'grenade_it.png'
glasses = base_path / '..' / 'assets' / 'items' / 'glasses.png'
toiletp = base_path / '..' / 'assets' / 'items' / 'toilet_paper.png'

#ajust and load the images
pill_img = pg.image.load(pill)
grenade_img =pg.image.load(grenade)
glasses_img = pg.image.load(glasses)
toiletp_img = pg.image.load(toiletp)
pill_img = pg.transform.scale(pill_img, (40,40))
grenade_img = pg.transform.scale(grenade_img, (40,40))
glasses_img = pg.transform.scale(glasses_img, (50,50))
toiletp_img = pg.transform.scale(toiletp_img, (20,20))

#the main class that is use on all functions
class ThrowableWeapon(pg.sprite.Sprite):
    def __init__(self, pos, angle, puissance, gravite=0.5, degats=10):
        super().__init__()
        self.image = pg.Surface((10, 10))
        self.image.fill((255, 255, 0)) 
        self.rect = self.image.get_rect(center=pos)
        self.pos = pg.Vector2(pos)

        #speed initial of the prohjectil
        self.vitesse_vecteur = pg.Vector2(
            puissance * math.cos(math.radians(angle)),
            -puissance * math.sin(math.radians(angle))
        )
        self.gravite = gravite
        self.degats = degats

    def update(self, obstacles_group):
        #collision ang gravity handle
        self.vitesse_vecteur.y += self.gravite
        self.pos += self.vitesse_vecteur
        self.rect.center = self.pos

        #verify the colision
        for obstacle in obstacles_group:
            if pg.sprite.collide_mask(self, obstacle):
                self.on_impact()
                break

        #checks for the out of the screen
        if self.rect.top > 2000 or self.rect.left > 3000 or self.rect.right < 0:
            self.kill()

    def on_impact(self):
        self.kill()

#class for the first weapon slipper 
class ExplodingSlipper(ThrowableWeapon):
    def __init__(self, pos, angle, puissance):
        super().__init__(pos, angle, puissance, gravite=0.6, degats=25)
        self.image = pill_img
        self.rect = self.image.get_rect(center=self.pos)

    def on_impact(self):
        self.kill()

    #for no self method
    @staticmethod
    def fire(player_pos, mouse_pos):
        dx = mouse_pos[0] - player_pos[0]
        dy = mouse_pos[1] - player_pos[1]
        angle = math.degrees(math.atan2(-dy, dx))
        spawn_pos = (player_pos[0] , player_pos[1])
        return ExplodingSlipper(spawn_pos, angle, puissance=15)


#class for the scond weapon the burning soup 
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

    #for no self method
    @staticmethod
    def fire(player_pos, mouse_pos):
        dx = mouse_pos[0] - player_pos[0]
        dy = mouse_pos[1] - player_pos[1]
        angle = math.degrees(math.atan2(-dy, dx))
        spawn_pos = (player_pos[0], player_pos[1])
        return BurningSoup(spawn_pos, angle, puissance=15)

#class for the rest of the soup
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

#class for the third weapon toilet paper roll
class ToiletPaperRoll(pg.sprite.Sprite):
    def __init__(self, pos, angle, vitesse=10, degats=5):
        super().__init__()
        self.image = toiletp_img
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

        if self.rect.top > 2000 or self.rect.left > 3000 or self.rect.right < 0:
            self.kill()

    def on_impact(self):
        self.kill()

    #for no self method
    @staticmethod
    def fire(player_pos, mouse_pos):
        dx = mouse_pos[0] - player_pos[0]
        dy = mouse_pos[1] - player_pos[1]
        angle = math.degrees(math.atan2(-dy, dx))
        rouleaux = []

        for _ in range(5):  #rouleaux envoyés avec écart
            offset = random.uniform(-5, 5)
            effective_angle = angle + offset
            spawn_pos = (player_pos[0] , player_pos[1] )
            proj = ToiletPaperRoll(spawn_pos, effective_angle)
            rouleaux.append(proj)
        return rouleaux


#class for the fourth weapon the boomrang
class BoomerangDenture(pg.sprite.Sprite):
    def __init__(self, pos, angle, vitesse=8, degats=20):
        super().__init__()
        self.image = glasses_img
        self.rect = self.image.get_rect(center=pos)
        self.start_pos = pg.Vector2(pos)
        self.pos = pg.Vector2(pos)

        self.vitesse_vecteur = pg.Vector2(
            vitesse * math.cos(math.radians(angle)),
            -vitesse * math.sin(math.radians(angle))
        )
        self.portee_max = 350
        self.en_retour = False
        self.degats = degats

    def update(self, obstacles_group):
        self.pos += self.vitesse_vecteur
        self.rect.center = self.pos

        distance = self.pos.distance_to(self.start_pos)
        if distance >= self.portee_max and not self.en_retour:
            self.vitesse_vecteur *= -1
            self.en_retour = True
        
        if self.en_retour == True and distance == 0:
            self.kill()

        for obstacle in obstacles_group:
            if pg.sprite.collide_mask(self, obstacle):
                self.on_impact()
                break

        if self.rect.top > 2000 or self.rect.left > 3000 or self.rect.right < 0:
            self.kill()

    def on_impact(self):
        self.kill()

    #for no self method
    @staticmethod
    def fire(player_pos, mouse_pos):
        dx = mouse_pos[0] - player_pos[0]
        dy = mouse_pos[1] - player_pos[1]
        angle = math.degrees(math.atan2(-dy, dx))
        spawn_pos = (player_pos[0], player_pos[1])
        return BoomerangDenture(spawn_pos, angle)