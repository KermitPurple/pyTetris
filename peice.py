import pygame
from coord import coord

class peice:
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

    def __init__(self, screen, scl, grid, queue,pos=coord(0,0)):
        self.screen = screen
        self.pos = pos
        self.scl = scl
        self.grid = grid
        self.queue = queue
        self.peice = [
                ".T..",
                ".TT.",
                ".T..",
                "....",
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
        pass

    def getrandpeice(self):
        pass
    
    def fillqueue(self):
        empty = [
		"....",
		"....",
		"....",
		"....",
                ]
        for item in self.queue:
            if item != empty:
                item = self.getrandpeice()
