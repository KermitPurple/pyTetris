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

    def __init__(self, screen, scl, grid, pos=coord(0,0)):
        self.screen = screen
        self.pos = pos
        self.scl = scl
        self.grid = grid
        self.peice = [
                "IIII",
                "IIII",
                "IIII",
                "IIII",
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

    def colision(self):
        if self.pos.x < -2 or self.pos.x > 8 or self.pos.y > 18:
            return True
        else:
            return False

    def move(self, change):
        self.pos.x += change.x
        self.pos.y += change.y
        if self.colision():
            self.pos.x -= change.x
            self.pos.y -= change.y

