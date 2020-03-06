import pygame
pygame.display.init()
screen = pygame.display.set_mode(size=(300,600))

running = True

#game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,0,0)) #clear screen
    pygame.draw.rect(screen, (255,255,255), pygame.Rect(0, 0, 30, 30))    
    pygame.display.update()
