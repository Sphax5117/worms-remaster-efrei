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
        self.spritesheet = pygame.image.load('spritesheet.png')#load the entire sprite sheet with all the player positions
        self.image= Tool.split_image(self.spritesheet,0, 0, 16, 32)#we obtain the first image from the frame, ask Tom if the width and height are correct for one player
        self.position = [0,0]
        self.rect=pygame.Rect(0,0,16, 32)
        self.all_images = self.get_all_images()
    def update(self):
        self.check_move()
        self.rect.topleft = self.position

    def check_move(self):
        if self.keylistener.key_pressed(pygame.K_q):
            self.move_left()
        elif self.keylistener.key_released(pygame.K_d):
            self.move_right()
        elif self.keylistener.key_released(pygame.K_z):
            self.move_up()
        elif self.keylistener.key_released(pygame.K_s):
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

        for i in range (nombre de lignes dans l'image):
            for j, key in enumerate(images.keys()):
                images[key].append( Tool.split_image(self.spritesheet, i * 24, j*24, 16, 32))
        return images

""" import pygame
from spritesheet import Spritesheet"
class Player(pyagme.sprite.Sprite):"
    def _init_(self):"
        pygame.sprite.Sprite._init_(self)"
        self.LEFT_KEY, self.RIGHT_KEY, self. FACING8LEFT= False, False, False"
        self.is_jumping, self.on_ground=False, False"
        self.gravity, self.friction=.35, -.12"
        self.image=Spritesheet('spritesheet.png').parse_sprite('chick.png)"
        self.rect=self.image.get_rect()"
        self.position, self.velocity= pyagme.math.Vector2(0,0),pyagme.math.Vector2(0,0)"
        self.acceleration=pygame.math.Vector2(0,self.gravity)"
        "
        def draw(self, display):"
            display.blit(self.image.x, self.rect.y)"
            ""
        def update(self,dt,tiles):
            self.horizontal_movement(dt)
            self.checkCollisionx(tiles)
            self.vertical_movement(dt)
            self.checkColisiony(tiles)"
        "
        def horizontal_movement(self, dt)"
            self.acceleration.x=0"
            if self.LEFT_KEY:"
                self.acceleration.x-=.3"
            elif self.RIGHT KEY:""
                self.acceleration.x+=.3"
            self.acceleration.x+= self.velocity.x*self.friction"
            self.velocity.x+= selfself.acceleration.x*dt"
            "self.limit_velocity(4)"
            self.postion.x+= self.velocity.x * dt + (self.acceleration.x*.5)*(dt*dt)"
            "
            
        "
        def vertical_movement(self, dt):"
            self.velocity.y += self.acceleration.y*dt"
            if self.velocity.y > 7: self.velocity.y=7"
            self.postion.y+=self.velocity.x*dt + (self.acceleration.x * .5) * (dt*dt)"
            self.rect.bottom =self.postion.y"
            "
        def limit_velocity(self, max_vel):"
            self.velocity.x=min(-max_vel, max(self.velocity.x,max_vel))"
            if abs(self.veloxcity.x)<.01: self.velocity.x=0"
        "
        def jump(self):"
            if self.on ground:"
                self.is_jumping=True"
                self.velocity.y-=8"
                self.on_ground=False
 
        def gets_hits(self,tiles):
            hits=[]
            for tile in tiles:
                if self.rect.colliderect(tile):
                    hits.append(tile)
            return hits
        def checkCollisionx(self, tiles):
            collisions=self.get_hits(tiles)
            for tile in collisions:
                if self.velocity.x>0:
                    self.position.x=tile.rect.left-self.rect.w
                    self.rect.x=self.position.x
                elif self.velocity.x<0:
                    self.postion.x=tile.rect.right
                    self.rect.x=self.position.x"
                    ""
        def checkCollisionsy(self,tiles):
            self.on_ground=False
            self.rect.bottom +=1
            collisions=self.get_hits(tiles)
            for tile in collisions:
                if self.velocity.y>0:
                    self.on_ground=True
                    self.is_jump=False
                    self.velocity.y=0
                    self.position.y=tile.rect.top
                    self.rect.bottom=self.position.y
                elif self.velocity.y<0:
                    self.velocity.y=0
                    self.position.y=tile.rect.bottom + self.rect.h
                    self.rect.bottom=self.postion.y
