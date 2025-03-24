import pygame

class Keylistener:
    def __init__(self):
        self.keys = []

    def add_key(self, key):
        if key not in self.keys:
            self.keys.append(key)

    def remove_key(self, key):
        if key in self.keys:
            self.keys.remove(key)

    def key_pressed(self, key):
        return key in self.keys

    def clear(self):
        self.keys.clear()

class Entity(pygame.sprite.Sprite):
    def __init__(self, keylistener: Keylistener):
        super().__init__()
        self.keylistener = keylistener
        
        # Chargement des images individuelles au lieu d'une spritesheet
        self.images = {
            "down": pygame.image.load("frame grand mère/tile132.png"),
            "left": pygame.image.load("frame grand mère/tile019.png"),
            "right": pygame.image.load("frame grand mère/tile041.png"),
            "up": pygame.image.load("frame grand mère/tile132.png")
        }
        
        self.image = self.images["down"]
        self.position = [100, 100]
        self.rect = self.image.get_rect(topleft=self.position)

    def update(self):
        self.check_move()
        self.rect.topleft = self.position

    def check_move(self):
        if self.keylistener.key_pressed(pygame.K_q):
            self.move_left()
        elif self.keylistener.key_pressed(pygame.K_d):
            self.move_right()
        elif self.keylistener.key_pressed(pygame.K_z):
            self.move_up()
        elif self.keylistener.key_pressed(pygame.K_s):
            self.move_down()

    def move_left(self):
        self.position[0] -= 5
        self.image = self.images["left"]

    def move_right(self):
        self.position[0] += 5
        self.image = self.images["right"]

    def move_up(self):
        self.position[1] -= 5
        self.image = self.images["up"]

    def move_down(self):
        self.position[1] += 5
        self.image = self.images["down"]
