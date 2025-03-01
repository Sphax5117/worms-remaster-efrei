import pygame as pg


class Weapon:
    def __init__(self, name, damage, fire_range, ammo, sprite_path):
        self.name = name
        self.damage = damage
        self.fire_range = fire_range
        self.ammo = ammo
        self.sprite = pg.image.load(sprite_path)
        self.sprite = pg.transform.scale(self.sprite, (50, 50))  # optional resize

    def fire(self, pos, direction):
        """gun fire method, to define as function of the weapons that we will set up"""
        if self.ammo > 0:
            self.ammo -= 1
            print(f"{self.name} a tiré! Munitions restantes: {self.ammo}")
        else:
            print(f"{self.name} n'a plus de munitions!")

    def reload(self, amnt):
        """reload method with a specific amount"""
        self.ammo += amnt
        print(f"{self.name} rechargé avec {amnt} munitions.")

    def draw(self, screen, position):
        """Display the weapons on the screen"""
        screen.blit(self.sprite, position)


class Bullet:
    def __init__(self, pos, direction, speed=10, damage=5):
        self.pos = pg.Vector2(pos)
        self.direction = direction
        self.speed = speed
        self.damage = damage
        sel.alive = True

        def update(self):
            """update the position of the bullet"""
            self.pos += self.direction * self.speed

            if self.pos.x < 0 or self.pos.x > 800 or self.pos.y < 0 or self.pos.y > 600:
                self.alive = False

        def draw(self, screen):
            """draw the bullet"""
            pg.draw.circle(screen, (255, 0, 0), (int(self.pos.x), int(self.pos.y)),5)

'''ARME DE TEST !!!!'''

class shotgun(Weapon):
    def __init__(self):
        super().__init__("shotgun",damage = 5, fire_range=200, ammo=6, sprite_path="shotgun.png")
        self.pellets = 6 # number of bullet per shot

    def fire(self, pos, direction, bullets_list):
        if self.ammo > 0:
            self.ammo -= 1
            for _ in range(self.pellets):

                angle_offset = random.uniform(-15, 15)
                angle_rad = math.radians(angle_offset)
                new_dir = pg.Verctor2(
                    math.cos(angle_rad) * direction.x - math.sin(angle_rad) * direction.y,
                    math.sin(angle_rad) * direction + math.cos(angle_rad) * direction.y
                ).normalize()

                bullets_list.append(Bullet(pos, new_dir))


