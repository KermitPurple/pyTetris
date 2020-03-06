import pygame
from coord import coord
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
        p = peice(self.screen, self.scl, self.grid, coord(4,0))
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.unicode == 'a':
                        p.move(coord(-1,0))
                    elif event.unicode == 's':
                        p.move(coord(0,1))
                    elif event.unicode == 'd':
                        p.move(coord(1,0))
            self.screen.fill((0,0,0)) #clear screen
            p.printpeice()
            pygame.display.update()
            sleep(0.02)
