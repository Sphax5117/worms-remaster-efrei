import pygame
from sys import exit

#to handle the house in the middle of the house
class GroupeObjet(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

 
def testpygames():
    pygame.init

    #initialization of the screen
    screen = pygame.display.set_mode((1200, 600))
    pygame.display.set_caption('Worms.exe')

    #limit the game to 60 fps
    clock = pygame.time.Clock()

    #structure of the game, simples bridges
    bridge_surface = pygame.Surface((1500, 50))
    bridge_surface.fill('Brown')

    # Création des objets (maison + sous-sol) dans un groupe
    house_group = pygame.sprite.Group()
    house = GroupeObjet(115, 350, 260, 200, 'green')  # Maison
    basement = GroupeObjet(100, 440, 300, 60, 'green')  # Sous-sol
    house_group.add(house, basement)

    #backround surface 
    backround_image = pygame.image.load('first_test_to_test_possibility/backroundtest.png')
    backround_image = pygame.transform.scale(backround_image, (1200,600))

    #for the weapons and bullets
    bullet = pygame.image.load('assets/items/grenade_it.png').convert_alpha()
    #for the scale of the bullet
    bullet = pygame.transform.scale(bullet, (25,25))
    #to consider the bullet as a rectangle
    bullet_rect = bullet.get_rect()

    #players need to have a better well organised folder
    player1 = pygame.image.load('first_test_to_test_possibility/graphics_temp/players.png')
    player2 = pygame.image.load('first_test_to_test_possibility/graphics_temp/players.png')
    #for the scale of the player
    player1 = pygame.transform.scale(player1, (20,20))
    player2 = pygame.transform.scale(player1, (20,20))
    #con,sider the player as a rectangle for better positioning
    player1_rect = player1.get_rect(midbottom = (1000,500))
    player2_rect = player2.get_rect(midbottom = (800, 500))
    #for the gravity of the player

    player1_gravity = 0
    player2_gravity = 0

    #management for turns (1 or 2)
    player_turn = pygame.USEREVENT + 1
    pygame.time.set_timer(player_turn, 45000)
    current_player = 1


    bullets = []
    bullet_gravity = 0.3

    trajectory = []
    trajectory_show = True
    trajectory_color = (255,255,255)
    directionp1 = 1
    count = 0 


    while True:

        #to exit the windows
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            #pour les tours
            elif event.type == player_turn:
                if current_player == 1:
                    current_player = 2
                    count = 0
                elif current_player == 2:
                    current_player = 1
                    count = 0
            #pour les tirs
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a :
                    count += 1
                    if current_player == 1 and count <= 5:
                        x = player1_rect.centerx
                        y = player1_rect.centery
                        vx, vy = 10*directionp1, -10
                        bullets.append({"x":x, "y": y, "vx": vx, "vy": vy })

                    elif current_player == 2 and count <=  5:
                        x = player2_rect.centerx
                        y = player2_rect.centery
                        vx, vy = 10*directionp2, -10
                        bullets.append({"x":x, "y": y, "vx": vx, "vy": vy })
                
                if event.key == pygame.K_t :
                    trajectory_show = True
                    if current_player == 1 and count <= 5:
                        x = player1_rect.centerx
                        y = player1_rect.centery
                        vx, vy = 10*directionp1, -10

                    elif current_player == 2 and count <=  5:
                        x = player2_rect.centerx
                        y = player2_rect.centery
                        vx, vy = 10*directionp2, -10

                    #generate the trajectory of the bullet
                    trajectory.clear()
                    temp_x, temp_y, temp_vy = x, y ,vy

                    for i in range(100):
                        temp_x += vx
                        temp_y += temp_vy
                        temp_vy += bullet_gravity
                        if temp_y >= 470:
                            break
                        trajectory.append((int(temp_x), int(temp_y)))

                if event.key == pygame.K_h :
                    trajectory_show = False


        keys = pygame.key.get_pressed()
           
        if player1_rect.colliderect(player2_rect):
                if player1_rect.bottom > player2_rect.top and player1_rect.top < player2_rect.top:
                    player1_rect.bottom = player2_rect.top
                    player1_gravity = 0
                    if current_player == 1:
                        if keys[pygame.K_LEFT]:
                            player1_rect.x -= 5
                        if keys[pygame.K_RIGHT]:
                            player1_rect.x += 5
                        if keys[pygame.K_UP]:
                            player1_gravity = -9

        elif player2_rect.bottom > player1_rect.top and player2_rect.top < player1_rect.top:
                    player2_rect.bottom = player1_rect.top
                    player2_gravity = 0
                    if current_player == 2:
                        if keys[pygame.K_LEFT]:
                            player1_rect.x -= 5
                        if keys[pygame.K_RIGHT]:
                            player1_rect.x += 5
                        if keys[pygame.K_UP]:
                            player1_gravity = -9
        
        for obj in house_group:
            #gestion de la collision avec la maison 
            if player1_rect.colliderect(obj.rect):
                if player1_rect.bottom > obj.rect.top and player1_rect.top < obj.rect.top:
                    player1_rect.bottom = obj.rect.top
                    player1_gravity = 0
                    if current_player == 1:
                        if keys[pygame.K_LEFT]:
                            player1_rect.x -= 5
                        if keys[pygame.K_RIGHT]:
                            player1_rect.x += 5
                        if keys[pygame.K_UP]:
                            player1_gravity = -9

                elif player2_rect.bottom > obj.rect.top and player2_rect.top < obj.rect.top:
                    player2_rect.bottom = obj.rect.top
                    player2_gravity = 0
                    if current_player == 2:
                        if keys[pygame.K_LEFT]:
                            player1_rect.x -= 5
                        if keys[pygame.K_RIGHT]:
                            player1_rect.x += 5
                        if keys[pygame.K_UP]:
                            player1_gravity = -9
        

        #Players 1
        #pour les mouvements ici droite et gauche ou on prends on compte la collision entre deux joueur

        for obj in house_group:
            if current_player == 1:
                if keys[pygame.K_RIGHT]:
                    player1_rect.x += 2
                    directionp1 = 1
                    

                    if player1_rect.colliderect(player2_rect):
                        player1_rect.x -= 2
                    if player1_rect.colliderect(obj):
                        player1_rect.x -= 2
                
                if keys[pygame.K_LEFT]:
                    player1_rect.x -= 2
                    directionp1 = -1

                    if player1_rect.colliderect(player2_rect):
                        player1_rect.x += 2
                    if player1_rect.colliderect(obj):
                        player1_rect.x += 2
                if keys[pygame.K_UP] and player1_rect.bottom >= 470:
                    player1_gravity = -9



            elif current_player == 2:
                if keys[pygame.K_RIGHT]:
                    player2_rect.x += 2
                    directionp2 = 1

                    if player2_rect.colliderect(player1_rect):
                        player2_rect.x -= 2
                    if player2_rect.colliderect(obj.rect):
                        player2_rect.x -= 2
                
                if keys[pygame.K_LEFT]:
                    player2_rect.x -= 2
                    directionp2 = -1

                    if player2_rect.colliderect(player1_rect):
                        player2_rect.x += 2
                    if player2_rect.colliderect(obj):
                        player2_rect.x += 2
                
                if keys[pygame.K_UP] and player2_rect.bottom >= 470:
                    player2_gravity = -9

        #affiche la trajectoire
        if trajectory_show:
            for point in trajectory:
                pygame.draw.circle(screen, trajectory_color, point, 2)
            

        # Mise à jour des projectiles + la gravité
        bullet_remove = []
        for bullet_data in bullets:
            bullet_data["x"] += bullet_data["vx"]
            bullet_data["y"] += bullet_data["vy"]
            bullet_data["vy"] += bullet_gravity

            if bullet_data["y"] >= 470:
                bullet_remove.append(bullet_data)
            else:
               screen.blit(bullet, (int(bullet_data["x"]), int(bullet_data["y"])))

        for bullet_data in bullet_remove:
            bullets.remove(bullet_data)

        screen.blit(backround_image, (0,0))

        house_group.draw(screen)

        #display the brige on the screen 
        screen.blit(bridge_surface,(0,470))


        #screen for the backround
        #screen.blit(backround_image, (0,0))

                               

        #display the players1 + gravity
        player1_gravity += 0.5
        player1_rect.y += player1_gravity
        if player1_rect.bottom >= 470:
            player1_rect.bottom = 470
        if player1_rect.centerx >= 1190:
            player1_rect.centerx = 1190
        if player1_rect.centerx <= 10:
            player1_rect.centerx = 10
        screen.blit(player1, player1_rect)

        #display the players2 + gravity
        player2_gravity += 0.5
        player2_rect.y += player2_gravity
        if player2_rect.bottom >= 470:
            player2_rect.bottom = 470
        if player2_rect.centerx >= 1190:
            player2_rect.centerx = 1190
        if player2_rect.centerx <= 10:
            player2_rect.centerx = 10
        screen.blit(player2, player2_rect)

        #update everything
        pygame.display.update()

        #limit the game to 60 fps
        clock.tick(60)



            
testpygames()