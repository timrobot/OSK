import pygame
import sys
import random
import math

pygame.init()
w, h = 720, 528
screen = pygame.display.set_mode((w, h))
fps = 40
frame = 0
screenMode = "main menu"
clock = pygame.time.Clock()
    
def iterFrame():
    global frame
    frame += 1

def main():
    global frame
    global screenMode
    global mouseMoved
    global mouse
    global mouseClicked
    #CONSTRUCTORS
    #main menu
    mm_selector = 1
    mm_selected = ""
    #adventure mode
    locations = []
    locations.append(ashburtonForest())
    location = locations[0]
    locSwitch = True
    characters = []
    characters.append(eElias((14 * 48, 35 * 48)))
    for c in range(len(location.npcs)):
        characters.append(location.npcs[c])
    #sub menu
    sm_selector = 1
    sm_selected = ""
    #battle mode
    Prompt = BattlePrompt()
    ChainAttack = dChainAttack()
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
                mouseMoved = False
                if mm_selected != "enter":
                    mouseMoving = False
                    if mm_selector == 1:
                        screenMode = "adventure mode"
                    elif mm_selector == 4:
                        pygame.quit()
                        sys.exit()
            elif getKey("up") and not getKey("down"):
                mouseMoved = False
                if mm_selected != "up":
                    if mm_selector == 1:
                        mm_selector = 4
                    else:
                        mm_selector -= 1
                    mm_selected = "up"
            elif not getKey("up") and getKey("down"):
                mouseMoved = False
                if mm_selected != "down":
                    if mm_selector == 4:
                        mm_selector = 1
                    else:
                        mm_selector += 1
                    mm_selected = "down"
            else:
                if mouseMoved:
                    if(mouse[0] >= 500 and mouse[0] <= 700) and (mouse[1] >= 200 and mouse[1] <= 389):
                        if mouse[1] >= 200 and mouse[1] <= 224:
                            mm_selector = 1
                        elif mouse[1] >= 255 and mouse[1] <= 279:
                            mm_selector = 2
                        elif mouse[1] >= 310 and mouse[1] <= 334:
                            mm_selector = 3
                        elif mouse[1] >= 365 and mouse[1] <= 389:
                            mm_selector = 4
                if mouseClicked:
                    if mm_selector == 1:
                        screenMode = "adventure mode"
                    elif mm_selector == 4:
                        pygame.quit()
                        sys.exit()
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
                if characters[0].collide(characters[i]):
                    screenMode = "battle mode"
                    del(characters[i])
                i -= 1
            # <user input>
            if getKey("escape"):
                screenMode = "sub menu"
            for i in range(len(characters)):
                characters[i].loc = location
            characters[0].move()

            location.pos = characters[0].pos
            location.drawUnder(frame)
            for i in range(len(characters)):
                characters[i].draw()
            location.drawOver(frame)

        # Battle Mode #
        elif screenMode == "battle mode":
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
            #if Elias.x >= BlueSpartan.x - BlueSpartan.weapon.x
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
            if Elias.health <= 0:
                screenMode = "main menu"
            if BlueSpartan.health <= 0:
                screenMode = "adventure mode"
                BlueSpartan.health = BlueSpartan.maxhealth
            if Prompt.Retreat == True:
                Prompt.Retreat = False
                screenMode = "adventure mode"
                BlueSpartan.health = BlueSpartan.maxhealth
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
        iterFrame()
        eventHandler(pygame.event.get())


"""@Images and @Keys"""

mouse = (0, 0)
mouseClicked = False
mouseMoved = False
    
images = []
imageNames = []
def drawImage(imageName, position):
    for i in range(len(imageNames)):
        if imageNames[i] == imageName:
            screen.blit(images[i], position)
            return
    images.append(pygame.image.load(imageName))
    imageNames.append(imageName)
    screen.blit(images[len(images) - 1], position)

PI = 3.14159265359
def drawRadial(color, pos, radius, deg):
    radius = float(radius)
    circumference = radius * 2 * PI
    parts = deg * circumference / 360
    part = float(0)
    while part < parts:
        pygame.draw.line(screen, color, (pos[0], pos[1]), (pos[0] + int(math.sin(part / radius) * radius), pos[1] + int(-math.cos(part / radius) * radius)), 3)
        part += 1

def drawImageOrigin(imageName, position):
    drawImage(imageName, (position[0] + w/2 - 24, position[1] + h/2 - 24))

keyNames = []
def setKey(keyName, state):
    if state == True:
        keyNames.append(keyName)
    else:
        for i in range(len(keyNames)):
            if keyNames[i] == keyName:
                del(keyNames[i])
                return

def getKey(keyName):
    for i in range(len(keyNames)):
        if keyNames[i] == keyName:
            return True
    return False

def eventHandler(eventList):
    global mouse
    global mouseClicked
    global mouseMoved
    for event in eventList:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouseClicked = True
            mouse = event.pos
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouseClicked = False
        elif event.type == pygame.MOUSEMOTION:
            mouse = event.pos
            mouseMoved = True
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
            elif event.key == pygame.K_0:
                setKey("0", True)
            elif event.key == pygame.K_1:
                setKey("1", True)
            elif event.key == pygame.K_2:
                setKey("2", True)
            elif event.key == pygame.K_3:
                setKey("3", True)
            elif event.key == pygame.K_4:
                setKey("4", True)
            elif event.key == pygame.K_5:
                setKey("5", True)
            elif event.key == pygame.K_6:
                setKey("6", True)
            elif event.key == pygame.K_7:
                setKey("7", True)
            elif event.key == pygame.K_8:
                setKey("8", True)
            elif event.key == pygame.K_9:
                setKey("9", True)
            elif event.key == pygame.K_A:
                setKey("a", True)
            elif event.key == pygame.K_B:
                setKey("b", True)
            elif event.key == pygame.K_C:
                setKey("c", True)
            elif event.key == pygame.K_D:
                setKey("d", True)
            elif event.key == pygame.K_E:
                setKey("e", True)
            elif event.key == pygame.K_F:
                setKey("f", True)
            elif event.key == pygame.K_G:
                setKey("g", True)
            elif event.key == pygame.K_H:
                setKey("h", True)
            elif event.key == pygame.K_I:
                setKey("i", True)
            elif event.key == pygame.K_J:
                setKey("j", True)
            elif event.key == pygame.K_K:
                setKey("k", True)
            elif event.key == pygame.K_L:
                setKey("l", True)
            elif event.key == pygame.K_M:
                setKey("m", True)
            elif event.key == pygame.K_N:
                setKey("n", True)
            elif event.key == pygame.K_O:
                setKey("o", True)
            elif event.key == pygame.K_P:
                setKey("p", True)
            elif event.key == pygame.K_Q:
                setKey("q", True)
            elif event.key == pygame.K_R:
                setKey("r", True)
            elif event.key == pygame.K_S:
                setKey("s", True)
            elif event.key == pygame.K_T:
                setKey("t", True)
            elif event.key == pygame.K_U:
                setKey("u", True)
            elif event.key == pygame.K_V:
                setKey("v", True)
            elif event.key == pygame.K_W:
                setKey("w", True)
            elif event.key == pygame.K_X:
                setKey("x", True)
            elif event.key == pygame.K_Y:
                setKey("y", True)
            elif event.key == pygame.K_Z:
                setKey("z", True)
            #print "DK: " + str(keyNames)
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
            elif event.key == pygame.K_0:
                setKey("0", False)
            elif event.key == pygame.K_1:
                setKey("1", False)
            elif event.key == pygame.K_2:
                setKey("2", False)
            elif event.key == pygame.K_3:
                setKey("3", False)
            elif event.key == pygame.K_4:
                setKey("4", False)
            elif event.key == pygame.K_5:
                setKey("5", False)
            elif event.key == pygame.K_6:
                setKey("6", False)
            elif event.key == pygame.K_7:
                setKey("7", False)
            elif event.key == pygame.K_8:
                setKey("8", False)
            elif event.key == pygame.K_9:
                setKey("9", False)
            elif event.key == pygame.K_A:
                setKey("a", False)
            elif event.key == pygame.K_B:
                setKey("b", False)
            elif event.key == pygame.K_C:
                setKey("c", False)
            elif event.key == pygame.K_D:
                setKey("d", False)
            elif event.key == pygame.K_E:
                setKey("e", False)
            elif event.key == pygame.K_F:
                setKey("f", False)
            elif event.key == pygame.K_G:
                setKey("g", False)
            elif event.key == pygame.K_H:
                setKey("h", False)
            elif event.key == pygame.K_I:
                setKey("i", False)
            elif event.key == pygame.K_J:
                setKey("j", False)
            elif event.key == pygame.K_K:
                setKey("k", False)
            elif event.key == pygame.K_L:
                setKey("l", False)
            elif event.key == pygame.K_M:
                setKey("m", False)
            elif event.key == pygame.K_N:
                setKey("n", False)
            elif event.key == pygame.K_O:
                setKey("o", False)
            elif event.key == pygame.K_P:
                setKey("p", False)
            elif event.key == pygame.K_Q:
                setKey("q", False)
            elif event.key == pygame.K_R:
                setKey("r", False)
            elif event.key == pygame.K_S:
                setKey("s", False)
            elif event.key == pygame.K_T:
                setKey("t", False)
            elif event.key == pygame.K_U:
                setKey("u", False)
            elif event.key == pygame.K_V:
                setKey("v", False)
            elif event.key == pygame.K_W:
                setKey("w", False)
            elif event.key == pygame.K_X:
                setKey("x", False)
            elif event.key == pygame.K_Y:
                setKey("y", False)
            elif event.key == pygame.K_Z:
                setKey("z", False)
            #print "UK: " + str(keyNames)

def rotateImage(Imagename, angle, pos):
    Image = pygame.transform.rotate(pygame.image.load(Imagename), angle)
    screen.blit(Image, pos)

"""@Maps"""

class area():
    name = ""
    layout = []
    image = ""
    pos = (0, 0)
    npcs = []
    def draw(self, pos):
        self.pos = pos
        drawImageOrigin(self.image, (-self.pos[0], -self.pos[1] + 16))
    def isopen(self, vector, pos):
        blockPos = (int(pos[0]/48), int(pos[1]/48))
        if vector == "up" and blockPos[1] - 1 >= 0:
            return (self.layout[blockPos[1] - 1][blockPos[0]] != 0)
        elif vector == "down" and blockPos[1] + 1 < len(self.layout):
            return (self.layout[blockPos[1] + 1][blockPos[0]] != 0)
        elif vector == "left" and blockPos[0] - 1 >= 0:
            return (self.layout[blockPos[1]][blockPos[0] - 1] != 0)
        elif vector == "right" and blockPos[0] + 1 < len(self.layout[0]):
            return (self.layout[blockPos[1]][blockPos[0] + 1] != 0)

class npc():
    pos = (0, 0)
    adventureImage = ""
    name = ""
    speed = 0
    steps = 0
    walking = False
    vector = "down"
    loc = area()
    wait = 0
    waitTime = 50
    def move(self, auto = True):
        if auto:
            if self.wait < self.waitTime:
                self.wait += 1
            elif self.wait == self.waitTime:
                self.walking = True
                direc = []
                if self.loc.isopen("up", self.pos) == True:
                    direc.append("up")
                if self.loc.isopen("down", self.pos) == True:
                    direc.append("down")
                if self.loc.isopen("left", self.pos) == True:
                    direc.append("left")
                if self.loc.isopen("right", self.pos) == True:
                    direc.append("right")
                index = -1
                try:
                    index = random.randint(0, len(direc) - 1)
                    #print "index: " + str(index)
                except:
                    pass
                    #print "failed to calculate random number"
                if not index == -1:
                    self.vector = direc[index]
                    self.walking = False
        if self.walking:
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
                self.walking = False
    def draw(self):
        drawImageOrigin(self.adventureimage, (self.pos[0] - self.loc.pos[0], self.pos[1] - self.loc.pos[1]))

class eElias(npc):
    def __init__(self, pos):
        self.name = "Elias"
        self.adventureimage = "Images\characters\char.png"
        self.speed = 6
        self.pos = pos
    def collide(self, char):
        if char.pos[0] == self.pos[0]:
            if char.pos[1] == self.pos[1] + 48:
                return True
            if char.pos[1] + 48 == self.pos[1]:
                return True
        if char.pos[1] == self.pos[1]:
            if char.pos[0] == self.pos[0] + 48:
                return True
            if char.pos[0] + 48 == self.pos[0]:
                return True
        return False
    def move(self):
        if not self.walking:
            if getKey("up") or getKey("down") or getKey("left") or getKey("right"):
                i = len(keyNames) - 1
                while i >= 0:
                    if keyNames[i] == "up":
                        self.vector = "up"
                        break
                    elif keyNames[i] == "down":
                        self.vector = "down"
                        break
                    elif keyNames[i] == "left":
                        self.vector = "left"
                        break
                    elif keyNames[i] == "right":
                        self.vector = "right"
                        break
                    i -= 1
                if self.loc.isopen(self.vector, self.pos):
                    self.walking = True
        if self.walking:
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
                self.walking = False
                        
class redSpartan(npc):
    def __init__(self, pos):
        self.name = "red spartan"
        self.adventureimage = "Images\characters\@red spartan.png"
        self.speed = 6
        self.pos = pos

class blueSpartan(npc):
    def __init__(self, pos):
        self.name = "blue spartan"
        self.adventureimage = "Images\characters\@blue spartan.png"
        self.speed = 6
        self = pos

class ashburtonForest(area):
    def __init__(self):
        self.name = "Ashburton Forest"
        self.image = "Images\environment\maps\Ashburton Forest.png"
        self.npcs = [redSpartan((23 * 48, 23 * 48)), blueSpartan((30 * 48, 50 * 48))]
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
        for i in range(80):
            drawImageOrigin("Images\environment\water.png", (-self.pos[0] + 24*48, -self.pos[1] + 16 + i*48 + frame%48))
            drawImageOrigin("Images\environment\water.png", (-self.pos[0] + 25*48, -self.pos[1] + 16 + i*48 + frame%48))
        drawImageOrigin(self.image, (-self.pos[0], -self.pos[1] + 16))
    def drawOver(self, frame):
        for y in range(80):
            for x in range(80):
                if self.layout[y][x] == 2 and (x != self.pos[0]/48 or (y != self.pos[1]/48-1)):
                    drawImageOrigin("Images\environment\@treetop.png", (-self.pos[0] + x*48, -self.pos[1] + y*48 + 16))

"""@BATTLE MODE"""
class BattlePrompt():
    Retreat = False
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
                    self.Retreat = True
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
    recordx = 250
    recordy = 390
    spacingx = 38
    spacingy = 33
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
            drawRadial((0, 0, 255), (self.x + 50, self.y + 50), 47, (self.anim))
        elif self.hitrecord >= 4 and self.hitrecord <= 7:
            self.anim += 2
            drawRadial((0, 0, 255), (self.x + 50, self.y + 50), 47, (self.anim))
        elif self.hitrecord >= 8 and self.hitrecord <= 11:
            self.anim += 4
            drawRadial((0, 0, 255), (self.x + 50, self.y + 50), 47, (self.anim))
        elif self.hitrecord >= 12:
            self.anim += 6
            drawRadial((0, 0, 255), (self.x + 50, self.y + 50), 47, (self.anim))
        else:
            self.anim -= 2
            drawRadial((0, 0, 255), (self.x + 50, self.y + 50), 47, (self.anim))
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
    width = 48
    height = 48
    wpntype = sword
    dmg = 30
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
    wpntype = weapon.wpntype
    Image45 = weapon.Image45
    Image0 = weapon.Image0
    anim = 0
    x = weapon.x
    y = weapon.y
    width = weapon.width
    height = weapon.height
    deg = 0
    dmg = weapon.dmg
    def update(self, Stance, x, y, width, height):
        self.x = x - 24
        self.y = y
        if self.anim >= 360:
            self.anim = 10
        if Stance == "Idle":
            rotateImage(self.Image45, 0, (self.x, self.y))
        if Stance == "Prepare":
            self.anim += 10
            if (self.anim >= 0 and self.anim <= 22.5) or (self.anim >= 337.5 and self.anim <= 360):
                rotateImage(self.Image0, self.anim, (self.x, self.y))
            elif self.anim >= 22.5 and self.anim <= 67.5:
                rotateImage(self.Image45, self.anim - 45, (self.x, self.y))
        if Stance == "Charge":
            rotateImage(self.Image0, 90, (self.x, self.y))
        if Stance == "Ready":
            rotateImage(self.Image0, 90, (self.x, self.y))
        if Stance == "Attack":
            self.anim -= 10
            if (self.anim >= 0 and self.anim <= 22.5) or (self.anim >= 337.5 and self.anim <= 360):
                rotateImage(self.Image0, self.anim, (self.x, self.y))
            elif self.anim >= 22.5 and self.anim <= 67.5:
                rotateImage(self.Image45, self.anim - 45, (self.x, self.y))
            elif self.anim >= 67.5 and self.anim <= 112.5:
                rotateImage(self.Image0, self.anim, (self.x, self.y))
            elif self.anim >= -67.5 and self.anim <= -22.5:
                rotateImage(self.Image45, self.anim - 45, (self.x, self.y))
            elif self.anim >= -22.5 and self.anim <= 0:
                rotateImage(self.Image0, self.anim, (self.x, self.y))
        if Stance == "NotReady":
            self.anim += 10
            if (self.anim >= 0 and self.anim <= 22.5) or (self.anim >= 337.5 and self.anim <= 360):
                rotateImage(self.Image0, self.anim, (self.x, self.y))
            elif self.anim >= 22.5 and self.anim <= 67.5:
                rotateImage(self.Image45, self.anim - 45, (self.x, self.y))
            elif self.anim >= 67.5 and self.anim <= 112.5:
                rotateImage(self.Image0, self.anim, (self.x, self.y))
            elif self.anim >= -67.5 and self.anim <= -22.5:
                rotateImage(self.Image45, self.anim - 45, (self.x, self.y))
            elif self.anim >= -22.5 and self.anim <= 0:
                rotateImage(self.Image0, self.anim, (self.x, self.y))
        if Stance == "Retreat":
            rotateImage(self.Image45, self.anim - 90, (self.x, self.y))
        if Stance == "Reset":
            self.anim += 10
            if (self.anim >= 0 and self.anim <= 22.5) or (self.anim >= 337.5 and self.anim <= 360):
                rotateImage(self.Image0, self.anim, (self.x, self.y))
            elif self.anim >= 22.5 and self.anim <= 67.5:
                rotateImage(self.Image45, self.anim - 45, (self.x, self.y))
            elif self.anim >= 67.5 and self.anim <= 112.5:
                rotateImage(self.Image0, self.anim, (self.x, self.y))
            elif self.anim >= -67.5 and self.anim <= -22.5:
                rotateImage(self.Image45, self.anim - 45, (self.x, self.y))
            elif self.anim >= -22.5 and self.anim <= 0:
                rotateImage(self.Image0, self.anim, (self.x, self.y))

class wEnemyWeapon():
    weapon = wFalchion()
    anim = 0
    x = weapon.x
    y = weapon.y
    width = weapon.width
    height = weapon.height
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
    Stance = "Idle"
    Start = ""
    Dealt = False
    x = 96
    y = 240
    width = 29
    height = 84
    v_x = 10
    Image = "playertest.png"
    health = 800
    maxhealth = 800
    exhaustion = 0
    weapon = wFriendlyWeapon()
    armor = 10
    def draw(self):
        if self.Stance == "Idle":
            self.x = 96
            self.y = 240
            Image = "playertest.png"
            self.weapon.update(self.Stance, self.x, self.y, self.width, self.height)
        for i in range(int(self.health * 100 / self.maxhealth)):
            pygame.draw.line(screen, (0, 255, 0), (i + 14, 409), (i + 14, 422))
        drawImage(self.Image, (self.x, self.y))
    def move(self):
        if self.Start == "Start":
            #if wpntype == "melee":
            #skill sequence
            if self.Stance == "Skill":
                 self.weapon.update(self.Stance, self.x, self.y, self.width, self.height)
            #normal attack sequence
            elif self.Stance == "Charge":
                self.x += self.v_x
                self.weapon.update(self.Stance, self.x, self.y, self.width, self.height)
                if self.x >= 528:
                    self.Stance = "Ready"
            elif self.Stance == "Ready":
                 self.x = self.x
                 self.y = self.y
                 self.weapon.update(self.Stance, self.x, self.y, self.width, self.height)
            elif self.Stance == "Attack":
                 self.weapon.update(self.Stance, self.x, self.y, self.width, self.height)
                 if self.weapon.anim <= -45:
                     self.Dealt = True
                     self.Stance = "NotReady"
            elif self.Stance == "NotReady":
                 self.x = self.x
                 self.y = self.y
                 self.weapon.update(self.Stance, self.x, self.y, self.width, self.height)
                 if self.weapon.anim >= 90:
                     self.Stance = "Ready"
            elif self.Stance == "Retreat":
                 self.x -= self.v_x
                 self.weapon.update(self.Stance, self.x, self.y, self.width, self.height)
                 if self.x <= 96:
                     self.x = 96
                     self.Stance = "Reset"
            elif self.Stance == "Reset":
                 self.weapon.update(self.Stance, self.x, self.y, self.width, self.height)
                 if self.weapon.anim >= 45:
                      self.Stance = "Idle"
                      self.Start = "Finish"
            else:
                self.Stance = "Prepare"
                self.weapon.update(self.Stance, self.x, self.y, self.width, self.height)
                if self.weapon.anim >= 90:
                    self.Stance = "Charge"


class cBlueSpartan():
    Stance = "Default"
    Start = ""
    Dealt = False
    x = 594
    y = 240
    v_x = 10
    Image = "npctest.png"
    health = 1600
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
        for i in range(int(self.health * 100 / self.maxhealth)):
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

"""def drawstring(string, pos, color = (0, 0, 0), size = 4):
    for i in range(len(string)):
        letters[string[i]]((pos[0] + (size * i * 8), pos[1]), color, size)

def drawA(pos, color, size):
    pygame.draw.line(screen, color, (pos[0] + 3 * size, pos[1] + 0 * size), (pos[0] + 0 * size, pos[1] + 7 * size), 1 * size)
    pygame.draw.line(screen, color, (pos[0] + 3 * size, pos[1] + 0 * size), (pos[0] + 6 * size, pos[1] + 7 * size), 1 * size)
    pygame.draw.line(screen, color, (pos[0] + 1 * size, pos[1] + 5 * size), (pos[0] + 5 * size, pos[1] + 5 * size), 1 * size)
def drawB(pos, color, size):
    pygame.draw.line(screen, color, (pos[0] + 0 * size, pos[1] + 0 * size), (pos[0] + 0 * size, pos[1] + 7 * size), 1 * size)
    pygame.draw.line(screen, color, (pos[0] + 0 * size, pos[1] + 0 * size), (pos[0] + 3 * size, pos[1] + 0 * size), 1 * size)
    pygame.draw.line(screen, color, (pos[0] + 0 * size, pos[1] + 3 * size), (pos[0] + 3 * size, pos[1] + 3 * size), 1 * size)
    pygame.draw.line(screen, color, (pos[0] + 3 * size, pos[1] + 0 * size), (pos[0] + 3 * size, pos[1] + 3 * size), 1 * size)
    pygame.draw.line(screen, color, (pos[0] + 0 * size, pos[1] + 7 * size), (pos[0] + 3 * size, pos[1] + 7 * size), 1 * size)
    pygame.draw.line(screen, color, (pos[0] + 4 * size, pos[1] + 4 * size), (pos[0] + 4 * size, pos[1] + 6 * size), 1 * size)
def drawC(pos, color, size):
    pygame.draw.line(screen, color, (pos[0] + 0 * size, pos[1] + 2 * size), (pos[0] + 0 * size, pos[1] + 5 * size), 1 * size)
    pygame.draw.line(screen, color, (pos[0] + 0 * size, pos[1] + 1 * size), (pos[0] + 1 * size, pos[1] + 1 * size), 1 * size)
    pygame.draw.line(screen, color, (pos[0] + 0 * size, pos[1] + 6 * size), (pos[0] + 1 * size, pos[1] + 6 * size), 1 * size)
    pygame.draw.line(screen, color, (pos[0] + 1 * size, pos[1] + 1 * size), (pos[0] + 1 * size, pos[1] + 0 * size), 1 * size)
    pygame.draw.line(screen, color, (pos[0] + 1 * size, pos[1] + 6 * size), (pos[0] + 1 * size, pos[1] + 7 * size), 1 * size)
    pygame.draw.line(screen, color, (pos[0] + 1 * size, pos[1] + 0 * size), (pos[0] + 3 * size, pos[1] + 0 * size), 1 * size)
    pygame.draw.line(screen, color, (pos[0] + 1 * size, pos[1] + 7 * size), (pos[0] + 3 * size, pos[1] + 7 * size), 1 * size)
    pygame.draw.line(screen, color, (pos[0] + 3 * size, pos[1] + 0 * size), (pos[0] + 3 * size, pos[1] + 1 * size), 1 * size)
    pygame.draw.line(screen, color, (pos[0] + 3 * size, pos[1] + 7 * size), (pos[0] + 3 * size, pos[1] + 6 * size), 1 * size)
def drawD(pos, color, size):
    pygame.draw.line(screen, color, (pos[0] + 0 * size, pos[1] + 0 * size), (pos[0] + 0 * size, pos[1] + 7 * size), 1 * size)
    pygame.draw.line(screen, color, (pos[0] + 0 * size, pos[1] + 0 * size), (pos[0] + 3 * size, pos[1] + 0 * size), 1 * size)
    pygame.draw.line(screen, color, (pos[0] + 0 * size, pos[1] + 7 * size), (pos[0] + 3 * size, pos[1] + 7 * size), 1 * size)
    pygame.draw.line(screen, color, (pos[0] + 4 * size, pos[1] + 1 * size), (pos[0] + 4 * size, pos[1] + 2 * size), 1 * size)
    pygame.draw.line(screen, color, (pos[0] + 4 * size, pos[1] + 6 * size), (pos[0] + 4 * size, pos[1] + 5 * size), 1 * size)
    pygame.draw.line(screen, color, (pos[0] + 5 * size, pos[1] + 3 * size), (pos[0] + 5 * size, pos[1] + 4 * size), 1 * size)
letters = {"A":drawA, "B":drawB, "C":drawC, "D":drawD}"""

if __name__ == '__main__':
    main()
