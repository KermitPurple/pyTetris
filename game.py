import pygame
from coord import coord
from time import sleep
from random import randint

class game:

    peices = [
	[
		".I..",
		".I..",
		".I..",
		".I..",
	],
	[
		".S..",
		".SS.",
		"..S.",
		"....",
	],
	[
		"..Z.",
		".ZZ.",
		".Z..",
		"....",
	],
	[
		"..T.",
		".TT.",
		"..T.",
		"....",
	],
	[
		"....",
		".OO.",
		".OO.",
		"....",
	],
	[
		".L..",
		".L..",
		".LL.",
		"....",
	],
	[
		"..J.",
		"..J.",
		".JJ.",
		"....",
	],
        ]

    def __init__(self, sz=(300,600), scl=30):
        pygame.display.init()
        self.screen = pygame.display.set_mode(size=sz)
        self.running = True
        self.scl = scl
        self.pos = coord(4,0)
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
        self.peice = [
                ".T..",
                ".TT.",
                ".T..",
                "....",
                ]
        self.queue = [
            [
                    "....",
                    "....",
                    "....",
                    "....",
            ],
            [
                    "....",
                    "....",
                    "....",
                    "....",
            ],
            [
                    "....",
                    "....",
                    "....",
                    "....",
            ],
            [
                    "....",
                    "....",
                    "....",
                    "....",
            ],
            [
                    "....",
                    "....",
                    "....",
                    "....",
            ],
            ]

    def realpos(self, x=0, y=0):
        return coord((self.pos.x + x) * self.scl, (self.pos.y + y) * self.scl)

    def printblock(self, real):
        pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(real.x, real.y, self.scl, self.scl))    

    def printpeice(self):
        for i, line in enumerate(self.peice):
            for j, ch in enumerate(line):
                if ch != '.':
                    real = self.realpos(j, i)
                    self.printblock(coord(real.x, real.y))

    def collision(self):
        for i, line in enumerate(self.peice):
            for j, ch in enumerate(line):
                if ch != '.':
                    if self.pos.x + j < 0 or self.pos.x + j > 9 or self.pos.y + i > 19:
                        return True
                    elif self.grid[self.pos.y + i][self.pos.x + j] != '.':
                        return True
        return False

    def move(self, change):
        self.pos.x += change.x
        self.pos.y += change.y
        if self.collision():
            self.pos.x -= change.x
            self.pos.y -= change.y

    def rotate(self, ch):
        temp = [
                ['.','.','.','.'],
                ['.','.','.','.'],
                ['.','.','.','.'],
                ['.','.','.','.'],
                ]
        if ch == 'r':
            for i in range(4):
                for j in range(4):
                    temp[i][j] = self.peice[3 - j][i]
            self.peice = temp
            if self.collision():
                self.rotate('l')
        elif ch == 'l':
            for i in range(4):
                for j in range(4):
                    temp[i][j] = self.peice[j][3 - i]
            self.peice = temp
            if self.collision():
                self.rotate('r')

    def getnextpeice(self):
        self.peice = self.queue.pop(0)
        self.queue.append(self.getrandpeice())

    def getrandpeice(self):
        return self.peices[randint(0,6)]                
    
    def fillqueue(self):
        new_queue = []
        for item in self.queue:
             new_queue.append(self.getrandpeice())
        self.queue = new_queue

    def lock(self):
        for i, line in enumerate(self.peice):
            for j, ch in enumerate(line):
                if ch != '.':
                    self.grid[i + self.pos.y][j + self.pos.x] = ch
        self.getnextpeice()

    def play(self):
        #game loop
        pygame.key.set_repeat(80)
        self.fillqueue()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.unicode == 'a':
                        self.move(coord(-1,0))
                    elif event.unicode == 's':
                        self.move(coord(0,1))
                    elif event.unicode == 'd':
                        self.move(coord(1,0))
                    elif event.unicode == 'q':
                        self.rotate('l')
                    elif event.unicode == 'e':
                        self.rotate('r')
                    elif event.unicode == 'g':
                        self.getnextpeice()
            self.screen.fill((0,0,0)) #clear screen
            self.printpeice()
            pygame.display.update()
            sleep(0.02)
