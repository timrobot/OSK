import pygame
import sys
import random
import math

pygame.init()
w, h = 720, 528
screen = pygame.display.set_mode((w, h))
fps = 40
clock = pygame.time.Clock()

def main():
    #CONSTRUCTORS
    #game
    screenMode = "main menu"
    frame = 0
    #main menu
    mm_selector = 1
    mm_selected = ""
    #adventure mode
    locations = []
    locations.append(ashburtonForest())
    location = locations[0]
    locSwitch = True
    characters = []
    char = eElias()
    characters.append(char)
    for c in xrange(len(location.npcs)):
        characters.append(location.npcs[c])
    #sub menu
    sm_selector = 1
    sm_selected = ""
    #action mode
    Prompt = BattlePrompt()
    Elias = cElias()
    BlueSpartan = cBlueSpartan()
    objectlist = [Elias, BlueSpartan]

    while True:
        """RESET"""
        screen.fill((255, 255, 255))

        """GAME LOGIC"""
        # Main menu #
        if screenMode == "main menu":
            #user input
            if getKey("enter") or getKey("space"):
                if mm_selected != "enter":
                    if mm_selector == 1:
                        screenMode = "adventure mode"
                    elif mm_selector == 4:
                        pygame.quit()
                        sys.exit()
            elif getKey("up") and not getKey("down"):
                if mm_selected != "up":
                    if mm_selector == 1:
                        mm_selector = 4
                    else:
                        mm_selector -= 1
                    mm_selected = "up"
            elif not getKey("up") and getKey("down"):
                if mm_selected != "down":
                    if mm_selector == 4:
                        mm_selector = 1
                    else:
                        mm_selector += 1
                    mm_selected = "down"
            else:
                mm_selected = ""
            #draw
            drawImage("Images\main menu.png", (0, 0))
            drawImage("Images\main new game.png", (500, 200))
            drawImage("Images\main load game.png", (500, 255))
            drawImage("Images\main options.png", (500, 310))
            drawImage("Images\main exit.png", (500, 365))
            drawImage("Images\main selector.png", (460, 145 + mm_selector * 55))

        # Adventure mode #
        elif screenMode == "adventure mode":
            i = len(characters) -1
            while i > 0:
                if char.collide(characters[i], location.pos):
                    screenMode = "action mode"
                    del(characters[i])
                i -= 1
            # <user input>
            if getKey("escape"):
                screenMode = "sub menu"
            if not char.walking:
                if getKey("up") or getKey("down") or getKey("left") or getKey("right"):
                    i = len(keyNames) - 1
                    while i >= 0:
                        if keyNames[i] == "up":
                            char.vector = "up"
                            break
                        elif keyNames[i] == "down":
                            char.vector = "down"
                            break
                        elif keyNames[i] == "left":
                            char.vector = "left"
                            break
                        elif keyNames[i] == "right":
                            char.vector = "right"
                            break
                        i -= 1
                    if location.open(char.vector, location.pos):
                        char.walking = True
            # <no user input>
            if char.walking:
                if char.vector == "left":
                    location.pos = (location.pos[0] - char.speed, location.pos[1])
                elif char.vector == "right":
                    location.pos = (location.pos[0] + char.speed, location.pos[1])
                elif char.vector == "up":
                    location.pos = (location.pos[0], location.pos[1] - char.speed)
                elif char.vector == "down":
                    location.pos = (location.pos[0], location.pos[1] + char.speed)
                char.steps += 1
                if char.steps == 48 / char.speed:
                    char.steps = 0
                    char.walking = False

            for i in xrange(1, len(characters)):
                characters[i].move()
                if characters[i].walking:
                    direc = []
                    if location.open("up", characters[i].pos):
                        direc.append("up")
                    if location.open("down", characters[i].pos):
                        direc.append("down")
                    if location.open("left", characters[i].pos):
                        direc.append("left")
                    if location.open("right", characters[i].pos):
                        direc.append("right")
                    characters[i].vector = direc[random.randint(0, len(direc) - 1)]
                    characters[i].walking = False

            location.drawUnder(frame)
            for i in xrange(len(characters)):
                characters[i].draw(location.pos)
            location.drawOver(frame)

        # Action Mode #
        elif screenMode == "action mode":
            drawImage("AshburtonForest_battlebackground.png", (0, 0))
            drawImage("battledisplay.png", (0, 378))
            drawImage("battlestatsally.png", (9, 387))
            drawImage("battlestatsenemy.png", (489, 387))
            if Prompt.ActionMode == "":
                Prompt.display()
            if Prompt.ActionMode == "Action":
                Elias.Start = "Start"
                BlueSpartan.Start = "Nothing"
                Prompt.ActionMode = "Nothing"
            if Elias.Start == "Start":
                ChainAttack.record()
            if ChainAttack.Success == True:
                    ChainAttack.reset()
                    Elias.Stance = "Attack"
            elif ChainAttack.Success == False:
                    ChainAttack.reset()
                    Elias.Stance = "Retreat"
            if ChainAttack.anim >= 360:
                ChainAttack.reset()
                Elias.Stance = "Retreat"
            if Elias.Stance == "Ready":
                ChainAttack.display()
            if Elias.Dealt == True:
                ChainAttack.hitrecord += 1
                BlueSpartan.health = BlueSpartan.health - Elias.weapon.dmg + BlueSpartan.armor
                Elias.Dealt = False
            if BlueSpartan.Dealt == True:
                Elias.health = Elias.health - BlueSpartan.weapon.dmg + Elias.armor
                BlueSpartan.Dealt = False
            if Elias.Stance == "Retreat":
                ChainAttack.hitrecord = 0
            if Elias.Start == "Finish":
                BlueSpartan.Start = "Start"
                Elias.Start = "Nothing"
            if BlueSpartan.Start == "Finish":
                Prompt.ActionMode = ""
            if Elias.health == 0:
                screenMode = "adventure mode"
            if BlueSpartan.health == 0:
                screenMode = "adventure mode"
            for obj in objectlist:
                obj.move()
                obj.draw()

        """# Sub Menu #
        elif screenMode == "sub menu":
            #user input
            if getKey("enter") or getKey("space"):
                if sb_selected != "enter":
                    if sb_selector == 5:
                        screenMode = "adventure mode"
            elif getKey("up") and not getKey("down"):
                if sb_selected != "up":
                    if sb_selector == 1:
                        sb_selector = 5
                    else:
                        sb_selector -= 1
                    sb_selected = "up"
            elif not getKey("up") and getKey("down"):
                if sb_selected != "down":
                    if sb_selector == 5:
                        sb_selector = 1
                    else:
                        sb_selector += 1
                    sb_selected = "down"
            else:
                mm_selected = ""
            #draw
            screen.fill((96, 60, 40))
            drawImage("Images\sub characters.png", ())
            drawImage("Images\sub inventory.png")
            drawImage("Images\sub map.png")
            drawImage("Images\sub options.png")
            drawImage("Images\sub return.png")"""

        """DISPLAY, FRAME, EVENT"""
        pygame.display.update()
        clock.tick(fps)
        frame += 1
        eventHandler(pygame.event.get())


"""@Images and @Keys"""

images = []
imageNames = []
def drawImage(imageName, position):
    for i in xrange(len(imageNames)):
        if imageNames[i] == imageName:
            screen.blit(images[i], position)
            return
    images.append(pygame.image.load(imageName))
    imageNames.append(imageName)
    screen.blit(images[len(images) - 1], position)

PI = 3.14159265359
def drawRadial(color, pos, radius, deg, speed=1):
    radius = float(radius)
    circumference = radius * 2 * PI
    parts = deg * circumference / 360
    part = float(0)
    while part < parts:
        for i in range(speed):
            pygame.draw.line(screen, color, (pos[0], pos[1]), (pos[0] + int(math.sin(float(part) / float(radius)) * float(radius)), pos[1] + int(-math.cos(float(part) / float(radius)) * float(radius))), 3)
            part += 1

def drawImageOrigin(imageName, position):
    drawImage(imageName, (position[0] + w/2 - 24, position[1] + h/2 - 24))

keyNames = []
def setKey(keyName, state):
    if state == True:
        keyNames.append(keyName)
    else:
        for i in xrange(len(keyNames)):
            if keyNames[i] == keyName:
                del(keyNames[i])
                return

def getKey(keyName):
    for i in xrange(len(keyNames)):
        if keyNames[i] == keyName:
            return True
    return False

def eventHandler(eventList):
    for event in eventList:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                setKey("down", True)
            elif event.key == pygame.K_UP:
                setKey("up", True)
            elif event.key == pygame.K_LEFT:
                setKey("left", True)
            elif event.key == pygame.K_RIGHT:
                setKey("right", True)
            elif event.key == pygame.K_SPACE:
                setKey("space", True)
            elif event.key == pygame.K_RETURN:
                setKey("enter", True)
            elif event.key == pygame.K_BACKSPACE:
                setKey("backspace", True)
            elif event.key == pygame.K_ESCAPE:
                setKey("escape", True)
            print "DK: " + str(keyNames)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                setKey("down", False)
            elif event.key == pygame.K_UP:
                setKey("up", False)
            elif event.key == pygame.K_LEFT:
                setKey("left", False)
            elif event.key == pygame.K_RIGHT:
                setKey("right", False)
            elif event.key == pygame.K_SPACE:
                setKey("space", False)
            elif event.key == pygame.K_RETURN:
                setKey("enter", False)
            elif event.key == pygame.K_BACKSPACE:
                setKey("backspace", False)
            elif event.key == pygame.K_ESCAPE:
                setKey("escape", False)
            print "UK: " + str(keyNames)


"""@Maps"""

class npc():
    pos = (0, 0)
    adventureImage = ""
    name = ""
    speed = 0
    steps = 0
    walking = False
    vector = "down"
    def move(self):
        pass
    def draw(self, pos):
        drawImageOrigin(self.adventureimage, self.pos)

class eElias(npc):
    def __init__(self):
        self.name = "Elias"
        self.adventureimage = "Images\characters\char.png"
        self.speed = 6
    def collide(self, char, pos):
        if char.pos[0] - pos[0] == self.pos[0]:
            if char.pos[1] - pos[1] == self.pos[1] + 48:
                return True
            if char.pos[1] - pos[1] + 48 == self.pos[1]:
                return True
        if char.pos[1] - pos[1] == self.pos[1]:
            if char.pos[0] - pos[0] == self.pos[0] + 48:
                return True
            if char.pos[0] - pos[0] + 48 == self.pos[0]:
                return True
        return False

class spartan(npc):
    wait = 0
    def move(self):
        if self.wait < 50:
            self.wait += 1
        elif self.wait == 50:
            self.walking = True
            self.wait += 1
        elif self.wait > 50:
            if self.vector == "left":
                self.pos = (self.pos[0] - self.speed, self.pos[1])
            elif self.vector == "right":
                self.pos = (self.pos[0] + self.speed, self.pos[1])
            elif self.vector == "up":
                self.pos = (self.pos[0], self.pos[1] - self.speed)
            elif self.vector == "down":
                self.pos = (self.pos[0], self.pos[1] + self.speed)
            self.steps += 1
            if self.steps == 48 / self.speed:
                self.steps = 0
                self.wait = 0
    def draw(self, pos):
        drawImageOrigin(self.adventureimage, (self.pos[0] - pos[0], self.pos[1] - pos[1]))

class redSpartan(spartan):
    def __init__(self):
        self.name = "red spartan"
        self.adventureimage = "Images\characters\@red spartan.png"
        self.speed = 6

class blueSpartan(spartan):
    def __init__(self):
        self.name = "blue spartan"
        self.adventureimage = "Images\characters\@blue spartan.png"
        self.speed = 6

class map():
    name = ""
    layout = []
    image = ""
    pos = (0, 0)
    npcs = []
    def draw(self, pos):
        self.pos = pos
        drawImageOrigin(self.image, (-self.pos[0], -self.pos[1] + 16))
    def open(self, vector, pos):
        blockPos = (pos[0]/48, pos[1]/48)
        if vector == "up" and blockPos[1] - 1 >= 0:
            return (self.layout[blockPos[1] - 1][blockPos[0]] != 0)
        elif vector == "down" and blockPos[1] + 1 < len(self.layout):
            return (self.layout[blockPos[1] + 1][blockPos[0]] != 0)
        elif vector == "left" and blockPos[0] - 1 >= 0:
            return (self.layout[blockPos[1]][blockPos[0] - 1] != 0)
        elif vector == "right" and blockPos[0] + 1 < len(self.layout[0]):
            return (self.layout[blockPos[1]][blockPos[0] + 1] != 0)

class ashburtonForest(map):
    def __init__(self):
        self.name = "Ashburton Forest"
        self.image = "Images\environment\maps\Ashburton Forest.png"
        self.pos = (14 * 48, 35 * 48)
        self.npcs = [redSpartan(), blueSpartan()]
        self.npcs[0].pos = (23 * 48, 23 * 48)
        self.npcs[1].pos = (30 * 48, 50 * 48)
        #layout
        self.layout = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],

        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2, 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0, 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0, 2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0, 0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1, 1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1, 1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1,1,1, 1,1,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1,1, 1,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1, 1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2, 2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],

        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1, 1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0, 1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2, 2,1,1,1,0,0,1,1,1,1,2,2,2,2,2,2,2,2,1,2, 2,2,2,2,2,2,2,2,2,2,1,0,0,0,0,0,0,0,0,0, 1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0, 0,1,1,1,0,0,1,1,1,2,0,0,0,0,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0, 1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0, 0,1,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0, 1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0, 0,1,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0, 1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0, 0,1,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,1, 1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0, 0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0, 0,1,1,1,0,0,2,2,2,0,0,0,0,0,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,2,1,2,2,2,2,2,1,1,1, 1,1,1,1,1,1,2,2,2,2,2,2,2,0,0,0,0,0,0,0],

        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0, 0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,2,2,2, 1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0, 0,1,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0, 1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0, 0,1,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0, 1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0, 0,1,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0, 1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0, 0,1,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0, 1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0, 0,1,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0, 1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0, 0,1,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0, 2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0, 0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,2,2,2,0,0,2,2,2,0,0,0,0,0,2,2,2,2,2,0, 0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],

        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 1,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 1,1,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 1,1,1,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 1,1,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,0,0,0,0,0,1,1,1,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,0,0,0,0,1,1,1,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],

        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,2,2,2,2,2,2,1,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 1,1,1,1,1,1,2,0,0,0,0,0,0,1,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 1,1,1,1,1,2,0,0,0,0,0,0,0,1,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 1,1,1,1,2,0,0,0,0,0,0,0,0,1,1,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 1,1,1,2,0,0,0,0,0,0,0,0,0,2,1,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 1,1,2,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1, 1,2,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1, 2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2, 2,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,2, 0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0, 0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,2,0, 0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],

        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0, 0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2, 2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],

        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    def drawUnder(self, frame):
        for i in xrange(80):
            drawImageOrigin("Images\environment\water.png", (-self.pos[0] + 24*48, -self.pos[1] + 16 + i*48 + frame%48))
            drawImageOrigin("Images\environment\water.png", (-self.pos[0] + 25*48, -self.pos[1] + 16 + i*48 + frame%48))
        drawImageOrigin(self.image, (-self.pos[0], -self.pos[1] + 16))
    def drawOver(self, frame):
        for y in xrange(80):
            for x in xrange(80):
                if self.layout[y][x] == 2 and (x != self.pos[0]/48 or (y != self.pos[1]/48-1)):
                    drawImageOrigin("Images\environment\@treetop.png", (-self.pos[0] + x*48, -self.pos[1] + y*48 + 16))

"""@ACTION MODE"""
class BattlePrompt():
    ActionMode = ""
    bp_selector = 1
    bp_selected = ""
    x = 285
    y = 378
    Image = "battleprompt.png"
    def display(self):
        drawImage(self.Image, (self.x, self.y))
        drawImage("main selector.png", (308, 368 + self.bp_selector * 31))
        if self.bp_selector == 1:
            drawImage("battleprompt_attack_dscrp.png", (self.x + 12, self.y + 91))
        elif self.bp_selector == 2:
            drawImage("battleprompt_retreat_dscrp.png", (self.x + 12, self.y + 91))
        if getKey("space"):
                if self.bp_selector == 1:
                    self.ActionMode = "Action"
                elif self.bp_selector == 2:
                    screenMode = "adventure mode"
        elif getKey("up") and not getKey("down"):
            if self.bp_selected != "up":
                if self.bp_selector == 1:
                   self.bp_selector = 2
                else:
                   self.bp_selector -= 1
                self.bp_selected = "up"
        elif not getKey("up") and getKey("down"):
            if self.bp_selected != "down":
                if self.bp_selector == 2:
                   self.bp_selector = 1
                else:
                   self.bp_selector += 1
                self.bp_selected = "down"
        else:
            self.bp_selected = ""

class dChainAttack():
    Success = ""
    limit1 = ""
    limit2 = ""
    hitrecord = 0
    recordx = 0
    recordy = 0
    spacingx = 45
    spacingy = 45
    x = 310
    y = 214
    indicator = ""
    Imagedef = "circlex.png"
    Imagebackground = "circletemplate.png"
    Image1 = "circle1.png"
    Image2 = "circle2.png"
    Image3 = "circle3.png"
    Image4 = "circle4.png"
    Image5 = "circle5.png"
    Image6 = "circle6.png"
    Image7 = "circle7.png"
    Image8 = "circle8.png"
    Imagehit = "hitrecord.png"
    anim = 0
    randindct = 0
    def reset(self):
        self.anim = 0
        self.Success = ""
        self.limit1 = ""
        self.limit2 = ""
        self.randindct = 0
    def record(self):
        if self.hitrecord >= 1:
            drawImage(self.Imagehit, (self.recordx + (self.spacingx * 0), self.recordy))
        if self.hitrecord >= 2:
            drawImage(self.Imagehit, (self.recordx + (self.spacingx * 1), self.recordy))
        if self.hitrecord >= 3:
            drawImage(self.Imagehit, (self.recordx + (self.spacingx * 2), self.recordy))
        if self.hitrecord >= 4:
            drawImage(self.Imagehit, (self.recordx + (self.spacingx * 3), self.recordy))
        if self.hitrecord >= 5:
            drawImage(self.Imagehit, (self.recordx + (self.spacingx * 4), self.recordy))
        if self.hitrecord >= 6:
            drawImage(self.Imagehit, (self.recordx + (self.spacingx * 5), self.recordy))
        if self.hitrecord >= 7:
            drawImage(self.Imagehit, (self.recordx + (self.spacingx * 0), self.recordy + self.spacingy))
        if self.hitrecord >= 8:
            drawImage(self.Imagehit, (self.recordx + (self.spacingx * 1), self.recordy + self.spacingy))
        if self.hitrecord >= 9:
            drawImage(self.Imagehit, (self.recordx + (self.spacingx * 2), self.recordy + self.spacingy))
        if self.hitrecord >= 10:
            drawImage(self.Imagehit, (self.recordx + (self.spacingx * 3), self.recordy + self.spacingy))
        if self.hitrecord >= 11:
            drawImage(self.Imagehit, (self.recordx + (self.spacingx * 4), self.recordy + self.spacingy))
        if self.hitrecord >= 12:
            drawImage(self.Imagehit, (self.recordx + (self.spacingx * 5), self.recordy + self.spacingy))
        if self.hitrecord >= 13:
            drawImage(self.Imagehit, (self.recordx + (self.spacingx * 0), self.recordy + (self.spacingy * 2)))
    def display(self):
        self.anim += 6
        if self.anim == 6:
            if self.hitrecord >= 1 and self.hitrecord <= 3:
                self.randindct = random.randint(4,7)
            elif self.hitrecord >= 4 and self.hitrecord <= 7:
                self.randindct = random.randint(3,7)
            elif self.hitrecord >= 8 and self.hitrecord <= 11:
                self.randindct = random.randint(2,5)
            elif self.hitrecord >= 12:
                self.randindct = random.randint(1,3)
            else: 
                self.randindct = random.randint(6,8)
        drawImage(self.Imagebackground, (self.x, self.y))
        if self.randindct == 1:
            self.indicator = self.Image1
            self.limit1 = 2
            self.limit2 = 44
        if self.randindct == 2:
            self.indicator = self.Image2
            self.limit1 = 46
            self.limit2 = 89
        if self.randindct == 3:
            self.indicator = self.Image3
            self.limit1 = 91
            self.limit2 = 134
        if self.randindct == 4:
            self.indicator = self.Image4
            self.limit1 = 136
            self.limit2 = 179
        if self.randindct == 5:
            self.indicator = self.Image5
            self.limit1 = 181
            self.limit2 = 224
        if self.randindct == 6:
            self.indicator = self.Image6
            self.limit1 = 226
            self.limit2 = 269
        if self.randindct == 7:
            self.indicator = self.Image7
            self.limit1 = 271
            self.limit2 = 314
        if self.randindct == 8:
            self.indicator = self.Image8
            self.limit1 = 316
            self.limit2 = 358
        drawImage(self.indicator, (self.x, self.y))
        if self.hitrecord >= 1 and self.hitrecord <= 3:
            drawRadial((0, 0, 255), (self.x + 50, self.y + 50), 47, (self.anim), 6)
        elif self.hitrecord >= 4 and self.hitrecord <= 7:
            drawRadial((0, 0, 255), (self.x + 50, self.y + 50), 47, (self.anim), 8)
        elif self.hitrecord >= 8 and self.hitrecord <= 11:
            drawRadial((0, 0, 255), (self.x + 50, self.y + 50), 47, (self.anim), 10)
        elif self.hitrecord >= 12:
            drawRadial((0, 0, 255), (self.x + 50, self.y + 50), 47, (self.anim), 12)
        else: 
            drawRadial((0, 0, 255), (self.x + 50, self.y + 50), 47, (self.anim), 4)
        if self.anim >= 360:
            drawRadial((0, 0, 255), (self.x + 50, self.y + 50), 47, 360)
        drawImage(self.Imagedef, (self.x, self.y))
        if getKey("space"):
            if self.anim >= self.limit1 and self.anim <= self.limit2:
                self.Success = True
            elif (self.anim >= 1 and self.anim <= (self.limit1 - 1)) or (self.anim >= (self.limit2 + 1) and self.anim <= 359):
                self.Success = False

class wFalchion():
    x = 118
    y = 241
    dmg = 50
    Imagedefally = "m_falchion_45.png"
    Imagedefenmy = "m_falchion_135.png"
    #From order of appearance in animation, friendly attack
    Image90 = "m_falchion_90.png"
    Image67_5 = "m_falchion_67_5.png"
    Image45 = "m_falchion_45.png"
    Image22_5 = "m_falchion_22_5.png"
    Image0 = "m_falchion_0.png"
    Image337_5 = "m_falchion_337_5.png"
    Image315 = "m_falchion_315.png"
    #From order of appearance in animation, enemy attack
    Image90r = "m_falchion_90r.png"
    Image112_5 = "m_falchion_112_5.png"
    Image135 = "m_falchion_135.png"
    Image157_5 = "m_falchion_157_5.png"
    Image180 = "m_falchion_180.png"
    Image202_5 = "m_falchion_202_5.png"
    Image225 = "m_falchion_225.png"

class wFriendlyWeapon():
    weapon = wFalchion()
    anim = 0
    x = weapon.x
    y = weapon.y
    dmg = weapon.dmg
    def update(self, Stance, x, y):
        if Stance == "Default":
            self.x = x + 22
            self.y = y + 1
            self.Image = self.weapon.Imagedefally
        if Stance == "Attack":
            self.anim += 1
            if self.anim == 2:
                self.x = x
                self.y = y - 48
                self.Image = self.weapon.Image90
            elif self.anim == 3:
                self.x = x + 21
                self.y = y + 1
                self.Image = self.weapon.Image67_5
            elif self.anim == 4:
                self.x = x + 22
                self.y = y + 1
                self.Image = self.weapon.Image45
            elif self.anim == 5:
                self.x = x + 22
                self.y = y + 2
                self.Image = self.weapon.Image22_5
            elif self.anim == 6:
                self.x = x + 22
                self.y = y + 24
                self.Image = self.weapon.Image0
            elif self.anim == 7:
                self.x = x + 21
                self.y = y + 47
                self.Image = self.weapon.Image337_5
            elif self.anim == 8:
                self.x = x + 22
                self.y = y + 44
                self.Image = self.weapon.Image315
        if Stance == "Retreat":
            self.x = x + 22
            self.y = y + 44
            self.Image = self.weapon.Image315
        if Stance == "Charge":
            self.x = x
            self.y = y - 48
            self.Image = self.weapon.Image90
        if Stance == "NotReady":
            self.anim += 1
            if self.anim == 2:
                self.x = x + 22
                self.y = y + 44
                self.Image = self.weapon.Image315
            elif self.anim == 3:
                self.x = x + 21
                self.y = y + 47
                self.Image = self.weapon.Image337_5
            elif self.anim == 4:
                self.x = x + 22
                self.y = y + 24
                self.Image = self.weapon.Image0
            elif self.anim == 5:
                self.x = x + 22
                self.y = y + 2
                self.Image = self.weapon.Image22_5
            elif self.anim == 6:
                self.x = x + 22
                self.y = y + 1
                self.Image = self.weapon.Image45
            elif self.anim == 7:
                self.x = x + 21
                self.y = y + 1
                self.Image = self.weapon.Image67_5
            elif self.anim == 8:
                self.x = x
                self.y = y - 48
                self.Image = self.weapon.Image90
        drawImage(self.Image, (self.x, self.y))

class wEnemyWeapon():
    weapon = wFalchion()
    anim = 0
    x = weapon.x
    y = weapon.y
    dmg = weapon.dmg
    def update(self, Stance, x, y):
        if Stance == "Default":
            self.x = x - 44
            self.y = y + 1
            self.Image = self.weapon.Image135
        if Stance == "Attack":
            self.anim += 1
            if self.anim == 2:
                self.x = x - 26
                self.y = y - 48
                self.Image = self.weapon.Image90r
            elif self.anim == 3:
                self.x = x - 43
                self.y = y + 1
                self.Image = self.weapon.Image112_5
            elif self.anim == 4:
                self.x = x - 44
                self.y = y + 1
                self.Image = self.weapon.Image135
            elif self.anim == 5:
                self.x = x - 44
                self.y = y + 2
                self.Image = self.weapon.Image157_5
            elif self.anim == 6:
                self.x = x - 44
                self.y = y + 24
                self.Image = self.weapon.Image180
            elif self.anim == 7:
                self.x = x - 43
                self.y = y + 47
                self.Image = self.weapon.Image202_5
            elif self.anim == 8:
                self.x = x - 44
                self.y = y + 44
                self.Image = self.weapon.Image225
        if Stance == "Retreat":
            self.x = x - 44
            self.y = y + 44
            self.Image = self.weapon.Image225
        if Stance == "Charge":
            self.x = x - 26
            self.y = y - 48
            self.Image = self.weapon.Image90r
        drawImage(self.Image, (self.x, self.y))

class cElias():
    Stance = "Default"
    Start = ""
    Dealt = False
    x = 96
    y = 240
    v_x = 10
    Image = "playertest.png"
    health = 800
    maxhealth = 800
    exhaustion = 0
    weapon = wFriendlyWeapon()
    armor = 10
    def draw(self):
        if self.Stance == "Default":
            self.x = 96
            self.y = 240
            Image = "playertest.png"
            self.weapon.update(self.Stance, self.x, self.y)
        for i in range(int(self.health * (100/self.maxhealth))):
            pygame.draw.line(screen, (0, 255, 0), (i + 14, 409), (i + 14, 422))
        drawImage(self.Image, (self.x, self.y))
    def move(self):
        if self.Start == "Start":
            if self.Stance == "Attack":
                 self.weapon.update(self.Stance, self.x, self.y)
                 if self.weapon.anim == 10:
                     self.weapon.anim = 0
                     self.Dealt = True
                     self.Stance = "NotReady"
            elif self.Stance == "Retreat":
                 self.x -= self.v_x
                 self.weapon.update(self.Stance, self.x, self.y)
                 if self.x <= 96:
                     self.x = 96
                     self.Stance = "Default"
                     self.Start = "Finish"
            elif self.Stance == "Ready":
                 self.x = self.x
                 self.y = self.y
                 self.weapon.update(self.Stance, self.x, self.y)
            elif self.Stance == "NotReady":
                 self.x = self.x
                 self.y = self.y
                 self.weapon.update(self.Stance, self.x, self.y)
                 if self.weapon.anim == 10:
                     self.weapon.anim = 0
                     self.Stance = "Ready"
            else:
                 self.Stance = "Charge"
                 self.x += self.v_x
                 self.weapon.update(self.Stance, self.x, self.y)
                 if self.x >= 528:
                     self.Stance = "Ready"

class cBlueSpartan():
    Stance = "Default"
    Start = ""
    Dealt = False
    x = 594
    y = 240
    v_x = 10
    Image = "npctest.png"
    health = 800
    maxhealth = 1600
    exhaustion = 0
    weapon = wEnemyWeapon()
    armor = 5
    def draw(self):
        if self.Stance == "Default":
            self.x = 594
            self.y = 240
            Image = "npctest.png"
            self.weapon.update(self.Stance, self.x, self.y)
        for i in range(int(self.health * (100/self.maxhealth))):
            pygame.draw.line(screen, (0, 255, 0), (i + 494, 409), (i + 494, 422))
        drawImage(self.Image, (self.x, self.y))
    def move(self):
        if self.Start == "Start":
            if self.Stance == "Attack":
                 self.weapon.update(self.Stance, self.x, self.y)
                 if self.weapon.anim == 10:
                     self.Stance = "Retreat"
                     self.weapon.anim = 0
                     self.Dealt = True
            elif self.Stance == "Retreat":
                 self.x += self.v_x
                 self.weapon.update(self.Stance, self.x, self.y)
                 if self.x >= 548:
                     self.x = 548
                     self.Stance = "Default"
                     self.Start = "Finish"
            else:
                 self.Stance = "Charge"
                 self.x -= self.v_x
                 self.weapon.update(self.Stance, self.x, self.y)
                 if self.x <= 116:
                     self.Stance = "Attack"


if __name__ == '__main__':
    main()
