import pygame


from pathlib import Path

# Get the absolute path to the `menu.py` file
base_path = Path(__file__).resolve().parent

grand_mere_down =  base_path / '..' / 'frame grand mère' / 'tile132.png'
grand_mere_left =  base_path / '..' / 'frame grand mère' / 'tile019.png'
grand_mere_right =  base_path / '..' / 'frame grand mère' / 'tile041.png'
grand_mere_up =  base_path / '..' / 'frame grand mère' / 'tile132.png'
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
            "down": pygame.image.load(str(grand_mere_down)),
            "left": pygame.image.load(str(grand_mere_left)),
            "right": pygame.image.load(str(grand_mere_right)),
            "up": pygame.image.load(str(grand_mere_up))
        }
        
        self.image = self.images["down"]
        self.position = [100, 100]
        self.rect = self.image.get_rect(topleft=self.position)
        self.lives = 3
        self.health= 5

    def update(self):
        self.check_move()
        self.rect.topleft = self.position

    def check_move(self):
        if self.keylistener.key_pressed(pygame.K_LEFT):
            self.move_left()
        elif self.keylistener.key_pressed(pygame.K_RIGHT):
            self.move_right()
        elif self.keylistener.key_pressed(pygame.K_UP):
            self.move_up()
        elif self.keylistener.key_pressed(pygame.K_DOWN):
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

    def update_lives(self):
        if self.health == 0 and self.lives >1 :
            self.health =5
            self.lives -=1
        if self.health >1 and #collision:
            self.health -= 1
        elif self.health == 1 and collision :
            #run final animation : explosion
            

                
    

