import pygame
from peice import peice
from time import sleep

class game:
    def __init__(self, sz=(300,600), scl=30):
        pygame.display.init()
        self.screen = pygame.display.set_mode(size=sz)
        self.running = True
        self.scl = scl
        self.grid = [
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
        p = peice(self.screen, self.scl, self.grid)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.unicode == 'a':
                        p.pos.x -= 1
                    elif event.unicode == 'd':
                        p.pos.x += 1
                    elif event.unicode == 'w':
                        p.pos.y -= 1
                    elif event.unicode == 's':
                        p.pos.y += 1
            self.screen.fill((0,0,0)) #clear screen
            p.printpeice()
            pygame.display.update()
            sleep(0.02)
