import pygame
from os import system
from coord import coord
from time import sleep
from random import choice, randrange

class game:

    configPath = "config.txt"
    try:
        open(configPath)
    except:
        configPath = "C:\\Users\\Shane\\Dropbox\\Desktop\\Coding\\python\\pyTetris\\config.txt" #custom path if u want to run outside its folder

    peices = [
    [
        "....",
        "IIII",
        "....",
        "....",
    ],
    [
        "S..",
        "SS.",
        ".S.",
    ],
    [
        "..Z",
        ".ZZ",
        ".Z.",
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

    def __init__(self):
        pygame.display.init()
        pygame.font.init()
        pygame.display.set_caption('PyTetris')
        self.tiks = 1
        self.sz = 550,640
        self.screen = pygame.display.set_mode(size=self.sz)
        self.running = True
        self.scl = 30
        self.pos = coord(4,0)
        self.holdready = True
        self.lockrate = 0
        self.level = 0
        self.speed = self.get_speed()
        self.offset = coord(150, 40)
        self.score = 0
        self.locktries = 0
        self.paused = False
        self.chain = 0
        self.grabBag = True
        self.record = [0] * 7
        self.remainingPeices = self.peices.copy()
        self.peice = self.getrandpeice()
        self.updateRecord()
        self.peiceLength = len(self.peice)
        self.gameover = False
        self.hold = self.matrix(4)
        self.grid = self.matrix(10, 20)
        self.queue = [self.matrix(4) for i in range(0, 5)]
        pygame.key.set_repeat(80)
        self.fillqueue()
        self.linesCleared = 0
        self.numOfTetris = 0
        self.numOfClears = 0
        self.shadowOn = True
        self.level_up_goal = 10
        self.instant_lock = False
        self.readSettingsFromFile()

    def realpos(self, x=0, y=0):
        return coord((self.pos.x + x) * self.scl, (self.pos.y + y) * self.scl + self.offset.y)

    def printblock(self, real, color, scl = None, shadow = False):
        if scl == None:
            scl = self.scl
        if shadow:
            detail_color = color + pygame.Color(40, 40, 40)
        else:
            detail_color = color + pygame.Color(100, 100, 100)
        pygame.draw.rect(self.screen, color, pygame.Rect(real.x, real.y, scl, scl))    
        pygame.draw.line(self.screen, detail_color, (real.x + scl/10, real.y + scl/10), (real.x + scl/10, real.y + 9*scl/10), 2)
        pygame.draw.line(self.screen, detail_color, (real.x + scl/10, real.y + scl/10), (real.x + 9*scl/10, real.y + scl/10), 2)

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

    def move(self, change, auto = False, nolock = False):
        down = False
        if change == coord(0,1):
            down = True
        self.pos.x += change.x
        self.pos.y += change.y
        if self.collision():
            self.pos.x -= change.x
            self.pos.y -= change.y
            if nolock:
                return False
            if down:
                if not auto:
                    self.lock()
                elif self.locktries >= self.lockrate or self.instant_lock:
                    self.lock()
                    self.locktries = 0
                else:
                    self.locktries += 1
            return False
        return True

    def rotate(self, ch, recur=True):
        if self.peiceLength == 2:
            return
        valid_directions = [
                coord(1, 1),
                coord(-1, 1),
                coord(1, 0),
                coord(-1, 0),
                coord(0, 1),
                coord(0, -1),
                ]
        temp = self.matrix(self.peiceLength)
        if ch == 'r':
            for i in range(self.peiceLength):
                for j in range(self.peiceLength):
                    temp[i][j] = self.peice[self.peiceLength - 1 - j][i]
            self.peice = temp
            if self.collision() and recur:
                for direction in valid_directions:
                    if self.move(direction, False, True):
                        return
                self.rotate('l', False)
        elif ch == 'l':
            for i in range(self.peiceLength):
                for j in range(self.peiceLength):
                    temp[i][j] = self.peice[j][self.peiceLength - 1 - i]
            self.peice = temp
            if self.collision() and recur:
                for direction in valid_directions:
                    if self.move(direction, False, True):
                        return
                self.rotate('r', False)

    def getnextpeice(self):
        self.peice = self.queue.pop(0)
        self.peiceLength = len(self.peice)
        self.queue.append(self.getrandpeice())

    def getrandpeice(self):
        if not self.grabBag:
            return choice(self.peices)
        if len(self.remainingPeices) == 0:
            self.remainingPeices = self.peices.copy()
        return self.remainingPeices.pop(randrange(0, len(self.remainingPeices)))
    
    def fillqueue(self):
        self.queue = [self.getrandpeice() for item in self.queue]

    def lock(self):
        self.holdready = True
        for i, line in enumerate(self.peice):
            for j, ch in enumerate(line):
                if ch != '.':
                    self.grid[i + self.pos.y][j + self.pos.x] = ch
        self.getnextpeice()
        self.updateRecord()
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
            return pygame.Color(64, 207, 255)
        elif ch == 'S':
            return pygame.Color(4, 255, 0)
        elif ch == 'Z':
            return pygame.Color(255, 0, 0)
        elif ch == 'T':
            return pygame.Color(174, 0, 255)
        elif ch == 'O':
            return pygame.Color(238, 255, 0)
        elif ch == 'L':
            return pygame.Color(255, 153, 0)
        elif ch == 'J':
            return pygame.Color(0, 13, 255)
        return pygame.Color(0, 0, 0)

    def instadrop(self):
        while self.move(coord(0,1)):
            self.score += 5

    def printqueue(self):
        queuescl = 20
        pygame.draw.line(self.screen, (255,255,255), (300, self.offset.y), (300,600+ self.offset.y), 3)
        for n, item in enumerate(self.queue):
            for i, line in enumerate(item):
                for j, ch in enumerate(line):
                    if ch != '.':
                        lengthOffset = queuescl * (3 - len(item)) / 2
                        point = coord(lengthOffset + 345 + j * queuescl ,queuescl + 150 + 90 * n + i * queuescl + self.offset.y + lengthOffset)
                        color = self.selectcolor(ch)
                        self.printblock(point, color,queuescl)

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
                if ch != '.':
                    lengthOffset = self.scl * (4 - len(line)) / 2
                    point = coord(lengthOffset + 315 + j * self.scl,14 + i * self.scl + self.offset.y + lengthOffset)
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
                self.grid.insert(0, ['.' for _ in range(0, 10)])
                cleared += 1
        if cleared > 0:
            self.linesCleared += cleared
            self.numOfClears += 1
            self.chain += 1
            if cleared == 1:
                self.score += 100 * self.chain
            elif cleared == 2:
                self.score += 400 * self.chain
            elif cleared == 3:
                self.score += 800 * self.chain
            elif cleared == 4:
                self.score += 1600 * self.chain
                self.numOfTetris += 1
        else:
            self.chain = 0

    def tik(self):
        self.tiks += 1
        if self.tiks > 100000:
            self.tiks = 0
        sleep(0.0005)

    def printtop(self):
        #Top line
        pygame.draw.line(self.screen, (255,255,255), (0, self.offset.y), (self.sz[0], self.offset.y),3)
        # Score
        txt = pygame.font.SysFont("Arial", 20).render("Score: " + str(self.score), True, (255,255,255))
        self.screen.blit(txt, (5,8))
        # Hold
        txt = pygame.font.SysFont("Arial", 30).render("HOLD", True, (255,255,255))
        self.screen.blit(txt, (345,3))
        # Level
        txt = pygame.font.SysFont("Arial", 20).render("Level: " + str(self.level), True, (255,255,255))
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
                    color = color // pygame.Color(3, 3, 3)
                    self.printblock(coord(real.x, real.y), color, None, True)

    def pause(self):
        self.paused = not self.paused
        self.drawPause()

    def coverBoard(self):
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(0, self.offset.y, self.scl * 10, self.scl * 20))

    def drawPause(self):
        self.coverBoard()
        txt = pygame.font.SysFont("Arial", 60).render("PAUSED", True, (255,255,255))
        self.screen.blit(txt, (205 - self.offset.x, 200))
        txt = pygame.font.SysFont("Arial", 30).render("Press 'q' to exit", True, (255,255,255))
        self.screen.blit(txt, (215 - self.offset.x, 265))
        txt = pygame.font.SysFont("Arial", 30).render("Press 'r' to restart", True, (255,255,255))
        self.screen.blit(txt, (203 - self.offset.x , 295))
        txt = pygame.font.SysFont("Arial", 28).render("Press <ESC> or 'p' to resume", True, (255,255,255))
        self.screen.blit(txt, (0, 325))
        # grabbag
        txt = pygame.font.SysFont("Arial", 28).render("Press 'g' to toggle grabbag", True, (0,255,0) if self.grabBag else (255,0,0))
        self.screen.blit(txt, (15, 355))
        # shadow
        txt = pygame.font.SysFont("Arial", 28).render("Press 's' to toggle shadow", True, (0,255,0) if self.shadowOn else (255,0,0))
        self.screen.blit(txt, (18, 385))
        # instant lock
        txt = pygame.font.SysFont("Arial", 28).render("Press 'l' to toggle instant lock", True, (0,255,0) if self.instant_lock else (255,0,0))
        self.screen.blit(txt, (6, 415))


    def increasespeed(self):
        if self.linesCleared >= self.level_up_goal:
            self.level += 1
            self.speed = self.get_speed()
            self.level_up_goal += 10

    def endgame(self):
        self.render()
        txt = pygame.font.SysFont("Arial", 60).render("GAME OVER", True, (255,255,255))
        self.screen.blit(txt, (150 - self.offset.x, 200))
        txt = pygame.font.SysFont("Arial", 30).render("Press 'q' to exit", True, (255,255,255))
        self.screen.blit(txt, (215 - self.offset.x, 265))
        txt = pygame.font.SysFont("Arial", 30).render("Press 'r' to restart", True, (255,255,255))
        self.screen.blit(txt, (203 - self.offset.x, 295))
        self.gameover = True

    def play(self):
        #game loop
        while self.running:
            if not self.paused and not self.gameover:
                self.clearlines()
                if self.tiks % self.speed == 0:
                    self.move(coord(0,1), True)
                if not self.gameover:
                    self.render()
            pygame.display.update()
            self.tik()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.kbin(event)
        pygame.display.quit()

    def printcontrols(self):
        print("W - Instant drop")
        print("A - Move left")
        print("S - Move down")
        print("D - Move right")
        print("Q - rotate left")
        print("E - rotate right")
        print("<SPACE> - Swap hold")
        print("<ESC>, P - Pause / unPause")

    def render(self):
        self.screen.fill((0,0,0)) #clear screen
        self.printtop()
        self.printgrid()
        self.printqueue()
        self.printStats()
        self.printhold()
        if self.shadowOn:
            self.printshadow()
        self.printpeice()
        self.printgridlines()
        self.increasespeed()

    def kbin(self, event):
        if self.paused:
            if event.unicode.lower() == 'p' or event.unicode.lower() == '\x1b':
                self.pause()
            elif event.unicode.lower() == 'q':
                self.running = False
            elif event.unicode.lower() == 'r':
                self.__init__()
            elif event.unicode.lower() == 'g':
                self.grabBag = not self.grabBag
                self.WriteSettingsToFile()
                self.render()
                self.drawPause()
            elif event.unicode.lower() == 's':
                self.shadowOn = not self.shadowOn
                self.WriteSettingsToFile()
                self.render()
                self.drawPause()
            elif event.unicode.lower() == 'l':
                self.instant_lock = not self.instant_lock
                self.WriteSettingsToFile()
                self.render()
                self.drawPause()
        elif self.gameover:
            if event.unicode.lower() == '\x1b' or event.unicode.lower() == 'q':
                self.running = False
            elif event.unicode.lower() == 'r':
                self.__init__()
        else:
            if event.unicode.lower() == 'p' or event.unicode.lower() == '\x1b':
                self.pause()
            if event.unicode.lower() == 'w':
                self.instadrop()
            elif event.unicode.lower() == 'a':
                self.move(coord(-1,0))
            elif event.unicode.lower() == 's':
                self.move(coord(0,1))
                self.score += 5
            elif event.unicode.lower() == 'd':
                self.move(coord(1,0))
            elif event.unicode.lower() == 'q':
                self.rotate('l')
            elif event.unicode.lower() == 'e':
                self.rotate('r')
            elif event.unicode.lower() == ' ':
                self.swaphold()

    def matrix(self, w, h=None):
        if h == None:
            h = w
        return [['.' for j in range(0, w)] for i in range(0, h)]

    def printStats(self):
        statScale = 10
        pygame.draw.line(self.screen, (255,255,255), (450, self.offset.y), (450, 600 + self.offset.y), 3)
        txt = pygame.font.SysFont("Arial", 20).render("Statistics", True, (255,255,255))
        self.screen.blit(txt, (470, 10))
        txt = pygame.font.SysFont("Arial", 20).render("Lines: " + str(self.linesCleared), True, (255,255,255))
        self.screen.blit(txt, (460, 50))
        txt = pygame.font.SysFont("Arial", 20).render("Tetris Rate:", True, (255,255,255))
        self.screen.blit(txt, (460, 100))
        if self.linesCleared != 0:
            txt = pygame.font.SysFont("Arial", 20).render(str(int(self.numOfTetris * 100 / self.numOfClears)) + "%", True, (255,255,255))
        else:
            txt = pygame.font.SysFont("Arial", 20).render("100%", True, (255,255,255))
        self.screen.blit(txt, (470, 130))
        for n, item in enumerate(self.peices):
            txt = pygame.font.SysFont("Arial", 20).render(str(self.record[n]), True, (255,255,255))
            self.screen.blit(txt, (480, 193 + 70 * n))
            for i, line in enumerate(item):
                for j, ch in enumerate(line):
                    if ch != '.':
                        lengthOffset = statScale * (3 - len(item)) / 2
                        point = coord(lengthOffset + 480 + j * statScale , 120 + 70 * n + i * statScale + self.offset.y + lengthOffset)
                        color = self.selectcolor(ch)
                        self.printblock(point, color,statScale)
    
    def updateRecord(self):
        indexes = {
                'I': 0,
                'S': 1,
                'Z': 2,
                'T': 3,
                'O': 4,
                'L': 5,
                'J': 6,
                }
        for line in self.peice:
            for ch in line:
                if ch != '.':
                    index = indexes[ch]
                    self.record[index] += 1
                    return

    def readSettingsFromFile(self):
        values = []
        with open(self.configPath) as f:
            for line in f:
                values.append(int(line[:-1]))
        try:
            self.grabBag = bool(values[0])
            self.shadowOn = bool(values[1])
            self.shadowOn = bool(values[2])
        except:
            self.WriteSettingsToFile()

    def WriteSettingsToFile(self):
        with open(self.configPath, 'w') as f:
            f.write(str(int(self.grabBag)) + '\n')
            f.write(str(int(self.shadowOn)) + '\n')
            f.write(str(int(self.instant_lock)) + '\n')

    def get_speed(self):
        if self.level == 0:
            return 48
        elif self.level == 1:
            return 43
        elif self.level == 2:
            return 38
        elif self.level == 3:
            return 33
        elif self.level == 4:
            return 28
        elif self.level == 5:
            return 23
        elif self.level == 6:
            return 18
        elif self.level == 7:
            return 13
        elif self.level == 8:
            return 8
        elif self.level == 9:
            self.lockrate = 2
            return 6
        elif self.level >= 10 and self.level <= 12:
            self.lockrate = 3
            return 5
        elif self.level >= 13 and self.level <= 15:
            self.lockrate = 4
            return 4
        elif self.level >= 16 and self.level <= 18:
            self.lockrate = 5
            return 3
        elif self.level >= 19 and self.level <= 28:
            self.lockrate = 6
            return 2
        elif self.level >= 29:
            self.lockrate = 7
            return 1
