import pygame
import pygame as pg


# Player:
class Player:
    # definition of Player class
    def __init__(self, color, nb, x_pos, y_pos):
        # sprite variables:
        #self.sprite = pg.image.load("assets/players/blob.png").convert_alpha()
        self.sprite_sheet = pg.Rect(color*72, 0*90, 72, 90)
        self.animation_time = 0
        self.rainbow_time = 17.5 ### on garde le raimbow ???
        # players number:
        self.nb = nb
        # position/movement variables:
        self.pos = [x_pos, y_pos]
        self.is_jumping = False
        self.jump_height = 20
        self.y_velocity = self.jump_height
        # hit box:
        self.hit_box = pg.Rect(x_pos + 9, y_pos + 12, 54, 78)

    # methode to get the players movements
    def player_input(self):
        keys = pg.key.get_pressed()
        is_moving = False
        if (keys[pg.K_q] is True and self.nb == 1) or (keys[pg.K_LEFT] is True and self.nb == 2):
            is_moving = True
            if self.pos[0] <= -9:
                self.pos[0] = -9
            if self.hit_box.left <= 408 and self.hit_box.right >= 400:
                self.pos[0] = 399
            else:
                self.pos[0] = self.pos[0] - 7.5
            self.hit_box[0] = self.pos[0] + 9
        if (keys[pg.K_d] is True and self.nb == 1) or (keys[pg.K_RIGHT] is True and self.nb == 2):
            is_moving = True
            if self.hit_box.right >= 800:
                self.pos[0] = 737
            if self.hit_box.right >= 392 and self.hit_box.left <= 400:
                self.pos[0] = 329
            else:
                self.pos[0] = self.pos[0] + 7.5
            self.hit_box[0] = self.pos[0] + 9
        if (keys[pg.K_z] is True and self.nb == 1) or (keys[pg.K_UP] is True and self.nb == 2):
            self.is_jumping = True
        if self.is_jumping is True:
            self.pos[1] = self.pos[1] - self.y_velocity
            self.hit_box[1] = self.pos[1] + 12
            self.y_velocity = self.y_velocity - gravity
            if self.y_velocity < -self.jump_height:
                self.is_jumping = False
                self.y_velocity = self.jump_height
        if is_moving is True and self.hit_box.bottom == 400:
            self.sprite_sheet[1] = (self.animation_time//8)*90
            if self.animation_time == 23:
                self.animation_time = 0
            else:
                self.animation_time = self.animation_time + 1
        else:
            self.sprite_sheet[1] = 0*90
            self.animation_time = 0

    # methode to make the players change color each 16 frame (I did it because it is cool)
    def rainbow(self):
        if self.rainbow_time == 0:
            if self.sprite_sheet[0] != 8*72:
                self.sprite_sheet[0] = self.sprite_sheet[0] + 72
            else:
                self.sprite_sheet[0] = 0
            self.rainbow_time = 15
        else:
            self.rainbow_time = self.rainbow_time - 1


'''Mettre les joueurs a des positions aléatoires au début de la partie (tout en restant sur la map)'''
# players:
player1 = Player(2, 1, 128, 310)
player2 = Player(1, 2, 600, 310)

class Playe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image= pygame.image.load('assets/characters/granny.png').convert_alpha
        self.rect = self.image.get_rect(midbottom = (200,300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300 :
            self.gravity= -20
    
    def apply_gravity(self):
        self.gravity +=1
        self.rect.y += self.gravity
        if self.rect.bottom >=300:
            self.rect.bottom = 300

    def update(self):
        self.player_input()
        self.apply_gravity()




player = pygame.sprite.GroupSingle()
player.add(Player())