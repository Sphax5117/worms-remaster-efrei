import pygame

#definition of function of the ready screen used before the fame start
def readyscreen(screen, screensize, countdown):

    #usefull variables
    font_big = pygame.font.SysFont(None, 150)
    clock = pygame.time.Clock()
    running = True
    last_tick = pygame.time.get_ticks()
    curr_count = countdown
    show_go = False
    go_time = 0
    rect1 = text1.get_rect(center=(screensize[0]//2, screensize[1]//2 - 80))
    rect2 = text.get_rect(center=(screensize[0]//2, screensize[1]//2 + 70))

    #the big loop to dsiplay the ready screen
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        now = pygame.time.get_ticks()

        if not show_go:
            #check if one second has passed
            if now - last_tick >= 1000:
                curr_count -= 1
                last_tick = now

            if curr_count <= 0:
                show_go = True
                go_time = now
        else:
            #show go for 1 second
            if now - go_time > 1000:
                running = False

        #render texts + display the message
        screen.fill((255,255,255))
        text1 = font_big.render("Are you ready ?", True, (0,0,0))
        if not show_go:
            text = font_big.render(str(curr_count), True, (255,0,0))
        else:
            text = font_big.render("GO!", True, (0,200,0)) 
        screen.blit(text1, rect1)
        screen.blit(text, rect2)

        #udpate and countdown + limit fps every times
        pygame.display.flip()
        clock.tick(60)
