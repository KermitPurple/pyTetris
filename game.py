import pygame
from os import system
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
		".T.",
		"TT.",
		".T.",
	],
	[
		"OO",
		"OO",
	],
	[
		".L.",
		".L.",
		".LL",
	],
	[
		".J.",
		".J.",
		"JJ.",
	],
]

	def __init__(self, sz=(450,640), scl=30):
		pygame.display.init()
		pygame.font.init()
		self.tiks = 0
		self.screen = pygame.display.set_mode(size=sz)
		self.running = False
		self.sz = sz
		self.scl = scl
		self.pos = coord(4,0)
		self.holdready = True
		self.speed = 21 # will actually be twenty because it tiks down immedately by one
		self.offset = coord(150, 40)
		self.score = 0
		self.level = 1
		self.lockrate = 0
		self.locktries = 0
		self.paused = False
		self.chain = 0
		self.peice = self.getrandpeice()
		self.peiceLength = len(self.peice)
		self.hold = [
				['.','.','.','.'],
				['.','.','.','.'],
				['.','.','.','.'],
				['.','.','.','.'],
				]
		self.grid = [
				['.','.','.','.','.','.','.','.','.','.'],
				['.','.','.','.','.','.','.','.','.','.'],
				['.','.','.','.','.','.','.','.','.','.'],
				['.','.','.','.','.','.','.','.','.','.'],
				['.','.','.','.','.','.','.','.','.','.'],
				['.','.','.','.','.','.','.','.','.','.'],
				['.','.','.','.','.','.','.','.','.','.'],
				['.','.','.','.','.','.','.','.','.','.'],
				['.','.','.','.','.','.','.','.','.','.'],
				['.','.','.','.','.','.','.','.','.','.'],
				['.','.','.','.','.','.','.','.','.','.'],
				['.','.','.','.','.','.','.','.','.','.'],
				['.','.','.','.','.','.','.','.','.','.'],
				['.','.','.','.','.','.','.','.','.','.'],
				['.','.','.','.','.','.','.','.','.','.'],
				['.','.','.','.','.','.','.','.','.','.'],
				['.','.','.','.','.','.','.','.','.','.'],
				['.','.','.','.','.','.','.','.','.','.'],
				['.','.','.','.','.','.','.','.','.','.'],
				['.','.','.','.','.','.','.','.','.','.'],
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
		return coord((self.pos.x + x) * self.scl, (self.pos.y + y) * self.scl + self.offset.y)

	def printblock(self, real, color, scl = None):
		if scl == None:
			scl = self.scl
		pygame.draw.rect(self.screen, color, pygame.Rect(real.x, real.y, scl, scl))    

	def printpeice(self):
		for i, line in enumerate(self.peice):
			for j, ch in enumerate(line):
				if ch != '.':
					real = self.realpos(j, i)
					color = self.selectcolor(ch)
					self.printblock(coord(real.x, real.y), color)

	def collision(self, pos=None):
		if pos is None:
			pos = self.pos
		for i, line in enumerate(self.peice):
			for j, ch in enumerate(line):
				if ch != '.':
					if pos.x + j < 0 or pos.x + j > 9 or pos.y + i > 19:
						return True
					elif self.grid[pos.y + i][pos.x + j] != '.':
						return True
		return False

	def move(self, change, auto = False):
		down = False
		if change == coord(0,1):
			down = True
		self.pos.x += change.x
		self.pos.y += change.y
		if self.collision():
			self.pos.x -= change.x
			self.pos.y -= change.y
			if down:
				if not auto:
					self.lock()
				elif self.locktries >= self.lockrate:
					self.lock()
					self.locktries = 0
				else:
					self.locktries += 1
			return False
		return True

	def rotate(self, ch, recur=True):
		if self.peiceLength == 4:
			temp = [
					['.','.','.','.'],
					['.','.','.','.'],
					['.','.','.','.'],
					['.','.','.','.'],
					]
		elif self.peiceLength == 3:
			temp = [
					['.','.','.'],
					['.','.','.'],
					['.','.','.'],
					]
		else:
			return
		if ch == 'r':
			for i in range(self.peiceLength):
				for j in range(self.peiceLength):
					temp[i][j] = self.peice[self.peiceLength - 1 - j][i]
			self.peice = temp
			if self.collision() and recur:
				self.rotate('l', False)
		elif ch == 'l':
			for i in range(self.peiceLength):
				for j in range(self.peiceLength):
					temp[i][j] = self.peice[j][self.peiceLength - 1 - i]
			self.peice = temp
			if self.collision() and recur:
				self.rotate('r', False)

	def getnextpeice(self):
		self.peice = self.queue.pop(0)
		self.peiceLength = len(self.peice)
		self.queue.append(self.getrandpeice())

	def getrandpeice(self):
		return self.peices[randint(0,6)]                
	
	def fillqueue(self):
		new_queue = []
		for item in self.queue:
			 new_queue.append(self.getrandpeice())
		self.queue = new_queue

	def lock(self):
		self.holdready = True
		for i, line in enumerate(self.peice):
			for j, ch in enumerate(line):
				if ch != '.':
					self.grid[i + self.pos.y][j + self.pos.x] = ch
		self.getnextpeice()
		self.pos = coord(4,0)
		if self.collision():
			self.endgame()

	def printgrid(self):
		for i, line in enumerate(self.grid):
			for j, ch in enumerate(line):
				if ch != '.':
					color = self.selectcolor(ch)
					self.printblock(coord(j * self.scl, i* self.scl + self.offset.y), color)

	def selectcolor(self, ch):
		if ch == 'I':
			return (64, 207, 255)
		elif ch == 'S':
			return (4, 255, 0)
		elif ch == 'Z':
			return (255, 0, 0)
		elif ch == 'T':
			return (174, 0, 255)
		elif ch == 'O':
			return (238, 255, 0)
		elif ch == 'L':
			return (255, 153, 0)
		elif ch == 'J':
			return (0, 13, 255)
		return (0, 0, 0)

	def instadrop(self):
		while self.move(coord(0,1)):
			self.score += 5

	def printqueue(self):
		pygame.draw.line(self.screen, (255,255,255), (300, self.offset.y), (300,600+ self.offset.y), 3)
		for n, item in enumerate(self.queue):
			for i, line in enumerate(item):
				for j, ch in enumerate(line):
					if ch != '.':
						point = coord(345 + j * 15 ,15 + 150 + 90 * n + i * 15 + self.offset.y)
						color = self.selectcolor(ch)
						self.printblock(point, color,15)

	def swaphold(self):
		if self.holdready:
			self.peice, self.hold = self.hold, self.peice
			self.pos = coord(4,0)
			self.holdready = False
			empty = True
			for line in self.peice:
				for ch in line:
					if ch != '.':
						empty = False
			if empty:
				self.getnextpeice()
			self.peiceLength = len(self.peice)

	def printhold(self):
		pygame.draw.line(self.screen, (255,255,255), (300, 135 + self.offset.y), (450, 135 + self.offset.y), 3)
		for i, line in enumerate(self.hold):
			for j, ch in enumerate(line):
				point = coord(315 + j * self.scl,14 + i * self.scl + self.offset.y)
				color = self.selectcolor(ch)
				self.printblock(point, color)

	def clearlines(self):
		cleared = 0
		for i, line in enumerate(self.grid):
			full = True            
			for ch in line:
				if ch == '.':
					full = False
			if full:
				_ = self.grid.pop(i)
				self.grid.insert(0, ['.','.','.','.','.','.','.','.','.','.',])
				cleared += 1
			if cleared > 0:
				self.chain += 1
				if cleared == 1:
					self.score += 100 * self.chain
				elif cleared == 2:
					self.score += 400 * self.chain
				elif cleared == 3:
					self.score += 800 * self.chain
				elif cleared == 4:
					self.score += 1600 * self.chain
			else:
				self.chain = 0

	def tik(self):
		self.tiks += 1
		if self.tiks > 100000:
			self.tiks = 0
		sleep(0.02)

	def printtop(self):
		#Top line
		pygame.draw.line(self.screen, (255,255,255), (0, self.offset.y), (self.sz[0], self.offset.y),3)
		# Score
		txt = pygame.font.SysFont("Arial", 20).render("Score: " + str(self.score), True, (255,255,255))
		self.screen.blit(txt, (5,8))
		# Hold
		txt = pygame.font.SysFont("Arial", 30).render("HOLD", True, (255,255,255))
		self.screen.blit(txt, (345,3))
		# speed
		txt = pygame.font.SysFont("Arial", 20).render("Speed: " + str(self.speed), True, (255,255,255))
		self.screen.blit(txt, (150,8))

	def printgridlines(self):
		#grid lines
		for i in range(1,10):
			pygame.draw.line(self.screen, (100,100,100), (i * self.scl, self.offset.y), (i * self.scl, self.sz[1]))
			pygame.draw.line(self.screen, (100,100,100), (0, i * self.scl + self.offset.y), (10 * self.scl, i * self.scl + self.offset.y))
			pygame.draw.line(self.screen, (100,100,100), (0, (i+9) * self.scl + self.offset.y), (10 * self.scl, (i + 9) * self.scl + self.offset.y))
		pygame.draw.line(self.screen, (100,100,100), (0, 19 * self.scl + self.offset.y), (10 * self.scl, 19 * self.scl + self.offset.y))
		#outline
		pygame.draw.line(self.screen, (255,255,255), (0, self.offset.y), (10 * self.scl, self.offset.y),3)
		pygame.draw.line(self.screen, (255,255,255), (0, self.sz[1]), (10 * self.scl, self.sz[1]),3)
		pygame.draw.line(self.screen, (255,255,255), (0, self.offset.y), (0, self.sz[1]),3)

	def printshadow(self):
		shadowpos = coord(self.pos.x, self.pos.y)
		while 1:
			shadowpos.y += 1
			if self.collision(shadowpos):
				shadowpos.y -= 1
				break
		for i, line in enumerate(self.peice):
			for j, ch in enumerate(line):
				if ch != '.':
					real = coord((shadowpos.x + j) * self.scl, (shadowpos.y + i ) * self.scl + self.offset.y)
					color = self.selectcolor(ch)
					color = (color[0]/3, color[1]/3, color[2]/3,)
					self.printblock(coord(real.x, real.y), color)

	def pause(self):
		self.paused = not self.paused
		txt = pygame.font.SysFont("Arial", 60).render("PAUSED", True, (255,255,255))
		txtwidth = txt.get_width()
		self.screen.blit(txt, (self.sz[0]/2 - self.offset.x - 20,300))

	def increasespeed(self):
		if self.tiks % 1500 == 0:
			self.speed -= 1
			if self.speed <= 1:
				self.speed = 1
			if self.speed >= 5:
				self.lockrate = 2
			else:
				if self.speed == 4:
					self.lockrate = 5
				elif self.speed == 3:
					self.lockrate = 7
				elif self.speed == 2:
					self.lockrate = 10
				elif self.speed == 1:
					self.lockrate = 20

	def endgame(self):
		print(60 * "=")
		print("FINAL SCORE:",self.score)
		self.running = False

	def play(self):
		#game loop
		pygame.key.set_repeat(80)
		self.fillqueue()
		self.running = True
		self.paused = False
		self.score = 0
		self.level = 1
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.endgame()
				elif event.type == pygame.KEYDOWN:
					if event.unicode == 'p' or event.unicode == '\x1b':
						self.pause()
					if not self.paused:
						if event.unicode == 'w':
							self.instadrop()
						elif event.unicode == 'a':
							self.move(coord(-1,0))
						elif event.unicode == 's':
							self.move(coord(0,1))
							self.score += 5
						elif event.unicode == 'd':
							self.move(coord(1,0))
						elif event.unicode == 'q':
							self.rotate('l')
						elif event.unicode == 'e':
							self.rotate('r')
						elif event.unicode == ' ':
							self.swaphold()
			if not self.paused:
				self.screen.fill((0,0,0)) #clear screen
				if self.tiks % self.speed == 0:
					self.move(coord(0,1), True)
				self.clearlines()
				self.printtop()
				self.printgrid()
				self.printqueue()
				self.printhold()
				self.printshadow()
				self.printpeice()
				self.printgridlines()
				self.increasespeed()
			pygame.display.update()
			self.tik()
		pygame.display.quit()

	def printcontrols(self):
		print("W - Instant drop")
		print("A - Move left")
		print("S - Move down")
		print("D - Move right")
		print("Q - rotate left")
		print("E - rotate right")
		print("<SPACE> - Swap hold")
