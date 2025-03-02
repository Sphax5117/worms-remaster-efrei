import pygame


my_rect

class collision_map,
    while True:
        if event.type==pygame.MOUSEMOTION:
            if self.colliderect(event.pos):


def check_wall_collision(self, dx, dy, map_walls):
    temp_rect = self.rect.move(dx, dy)
    for wall in map_walls:
        if temp_rect.colliderect(wall):
            return True
    return False


def check_element_collision(self, map_elements):
    for element in map_elements:
        if self.rect.colliderect(element.rect):
            element.interact(self)



