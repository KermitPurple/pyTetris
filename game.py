import pygame
from peice import peice
from time import sleep

class game:
    def __init__(self, sz=(300,600), scl=30):
        pygame.display.init()
        self.screen = pygame.display.set_mode(size=sz)
        self.running = True
        self.scl = scl
        grid = [
                "..........",
                "..........",
                "..........",
                "..........",
                "..........",
                "..........",
                "..........",
                "..........",
                "..........",
                "..........",
                "..........",
                "..........",
                "..........",
                "..........",
                "..........",
                "..........",
                "..........",
                "..........",
                "..........",
                "..........",
                ]

    def play(self):
        #game loop
        x = 0
        pygame.key.set_repeat(40)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.unicode == 'a':
                        x -= self.scl
                    elif event.unicode == 'd':
                        x += self.scl
            self.screen.fill((0,0,0)) #clear screen
            pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(x, 0, 30, 30))    
            pygame.display.update()
            sleep(0.02)
