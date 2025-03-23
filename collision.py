import pygame,csv,os 


class Tile(pygame.sprite.Sprite):
    def _init_(self, image,x,y, spritesheet):
        pygame.sprite.Sprite._init_(self)
        self.image=spritesheet.parse_sprite(image)
        self.rect=self.image.get_rect()
        self.rect.x,self.rect.y=x,y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class TileMap():
    def _init_(self,filename,spritesheet):
        self.tile_size=16
        self.start_x,self.start_y=0,0
        self.spritesheet=spritesheet
        self.tiles=self.load_tiles(filename)
        self.map_surface=pygame.Surface((self.map_w,self.map_h))
        self.map_surface.set_colorkey((0,0,0))
        self.load_map()

    def draw_map(self,surface):
        surface.blit(self.map_surface,(0,0))

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)


    def read_cvs(self, filename):
        map=[]
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map
    
    def load_tiles(self, filename):
        tiles=[]
        map= self.read_cvs(filename)
        x, y =0, 0
        for row in map:
            x=0
            for tile in row:
                if tile == '0':
                    self.start_x, self.start_y= x * self.tile_size, y * self.tile_size
                elif tile== '1':
                    tiles.append(Tile('png',x*self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile== '2':
                    tiles.append(Tile('png',x*self.tile_size, y * self.tile_size, self.spritesheet))
                
                x+=1
            y+=1

        self.map_w,self.map_h=x*self.tile_size, y*self.tile_size
        return tiles


#class player#
def update(self,dt,tiles):
    self.horizontal_movement(dt)
    self.checkCollisionx(tiles)
    self.vertical_movement(dt)
    self.checkColisiony(tiles)

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
            self.rect.x=self.position.x

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


#main#
map=TileMap('testlevel.csv', spritesheet)
player_rect.x, player_rect.y=map.start_x, map.start_y


player.update(dt,map.tiles)           



