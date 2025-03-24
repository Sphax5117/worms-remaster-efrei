import pygame

#TO DO /
#créer un perso dans le main ou le game pour tester si ça fonctionne

class Tool:
    def split_image(spritesheet : pygame.Surface , x : int, y, width : int, height : int):
        return spritesheet.subsurface(pygame.Rect(x, y, width, height))


class Keylistener:
    def __init__(self):
        self.keys : list[int] = []
    def add_key(self, key : int):
        if key not in self.keys :
            self.keys.append(key)
    def remove_key(self, key : int):
        if key in self.keys :
            self.keys.remove(key)
    def key_pressed(self,key):
        return key in self.keys
    def clear(self):
        self.keys.clear()

class Entity(pygame.sprite.Sprite):
    def __init__(self, keylistener : Keylistener):
        super().__init__()
        self.keylistener = keylistener
        self.spritesheet = pygame.image.load('assets/characters/granny.png')#load the entire sprite sheet with all the player positions
        self.image= Tool.split_image(self.spritesheet,0, 0, 16, 32)#we obtain the first image from the frame, ask Tom if the width and height are correct for one player
        self.position = [100,100]
        self.rect=pygame.Rect(0,0,16, 32)
        self.all_images = self.get_all_images()
        print("Taille de la spritesheet :", self.spritesheet.get_size())
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
        self.position[0] -=1
        self.image = self.all_images["left"][0]
    def move_right(self):
        self.position[0]+=1
        self.image = self.all_images["right"][0]
    def move_up(self):
        self.position[1] -=1
        self.image = self.all_images["up"][0]
    def move_down(self):
        self.position[1]+=1
        self.image = self.all_images["down"][0]

    def get_all_images(self):
        images = {
            "down":[],
            "left":[],
            "right":[],
            "up":[]
        }

        for i in range (3):
            for j, key in enumerate(images.keys()):
                images[key].append( Tool.split_image(self.spritesheet, i * 24, j*24, 16, 32))
        return images



