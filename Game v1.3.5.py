import pygame
import sys
import random
from math import *

pygame.init()
w, h = 720, 528
screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()
song = pygame.mixer.music
fps = 50
frame = 0
screenMode = "main menu"

def main():
    #CONSTRUCTORS
    global screenMode
    global frame
    #main menu
    mm_selector = 1
    mm_selected = ""
    #adventure mode
    locations = [ashburtonForest(), oakForest()]
    location = locations[0]
    characters = []
    charToDelete = 0
    enemies = []
    #sub menu
    sb_selector = 1
    sb_selected = "escape"
    sb_menuImages = ["ui/menu/sub characters.png", "ui/menu/sub inventory.png", "ui/menu/sub map.png", "ui/menu/sub options.png", "ui/menu/sub return.png"]
    sb_menuItems = ["Characters", "Inventory", "Map", "Options", "Return"]
    sb_buttons = []
    sb_oldPos = (0, 0)
    sb_mouse = False
    sb_oldSelector = 1
    for i in range(len(sb_menuItems)):
        sb_buttons.append(button((500, 200 + i * 52), sb_menuItems[i], sb_menuImages[i]))
    #action mode
    battle = True
    Prompt = BattlePrompt()
    ChainAttack = dChainAttack()
    BlueSpartan = cBlueSpartan()
    objectlist = [BlueSpartan]

    # MUSIC #
    song.load("media/still alive.mp3")
    song.play(-1)

    while True:
        # RESET #
        screen.fill((0, 0, 255))

        # MAIN MENU #
        if screenMode == "main menu":
            #user input
            if getKey("enter") or getKey("space"):
                if mm_selected != "enter":
                    if mm_selector == 1:
                        locations = [ashburtonForest(), oakForest()]
                        location = locations[0]
                        characters = [eElias((14, 35))]
                        i = 0
                        while i < len(location.npcs):
                            characters.append(location.npcs[i])
                            i += 1
                        charToDelete = 0
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
            menuItems = ["ui/menu/main new game.png", "ui/menu/main load game.png", "ui/menu/main options.png", "ui/menu/main exit.png"]
            
            drawImage("ui/menu/main menu.png", (0, 0))
            drawImage("ui/menu/menu borders.png", (471, 196))
            for i in range(len(menuItems)):
                if mm_selector - 1 == i:
                    drawImage("ui/menu/button selector.png", (500, 148 + mm_selector * 52))
                else:
                    drawImage("ui/menu/button background.png", (500, 200 + (i*52)))
                drawImage(menuItems[i], (500, 200 + (i*52)))

        # ADVENTURE MODE #
        if screenMode == "adventure mode":
            # <user input> escape sequence
            if getKey("escape"):
                if sb_selected != "escape":
                    screenMode = "sub menu"
                    sb_selected = "escape"
            elif not getKey("escape"):
                if sb_selected == "escape":
                    sb_selected = ""
            # object collision
            if charToDelete != 0:
                del(characters[charToDelete])
                charToDelete = 0
            i = len(characters) - 1
            while i > 0:
                if characters[0].collide(characters[i]):
                    screenMode = "battle mode"
                    charToDelete = i
                    enemies.append(characters[i])
                    break
                i -= 1
            # character and location movement (O(4))
            i = 0
            while i < len(characters):
                characters[i].move()
                if characters[i].msg_requireOpen:
                    direc = []
                    if location.isOpen("up", characters[i].getPos()) == True:
                        direc.append("up")
                    if location.isOpen("down", characters[i].getPos()) == True:
                        direc.append("down")
                    if location.isOpen("left", characters[i].getPos()) == True:
                        direc.append("left")
                    if location.isOpen("right", characters[i].getPos()) == True:
                        direc.append("right")
                    characters[i].sendDirec(direc)
                i += 1
            location.pos = characters[0].pos
            # location change, using tickets
            if characters[0].walking == False:
                if location.teleporter(characters[0].getPos()):
                    ticket = location.getTeleportTicket(characters[0].getPos())
                    for loc in locations:
                        if loc.name == ticket["to"]:
                            location = loc
                    characters[0].goToPosition(location.evalTicket(ticket))
                    characters = [characters[0]]
                    i = 0
                    while i < len(location.npcs):
                        characters.append(location.npcs[i])
                        i += 1

            # draw characters and location
            location.drawUnder(frame)
            i = len(characters) - 1
            while i >= 0:
                characters[i].draw(location.pos)
                i -= 1
            location.drawOver(frame)
            characters[0].drawGold()

        # Battle Mode #
        elif screenMode == "battle mode":
            #battle screen
            if battle == True:
                #draw Images
                drawImage("environment/maps/AshburtonForest_battlebackground.png", (0, 0))
                drawImage("ui/battle mode/battledisplay.png", (0, 378))
                drawImage("ui/battle mode/battlestatsally.png", (9, 387))
                drawImage("ui/battle mode/battlestatsenemy.png", (489, 387))
                characters[0].bmove()
                characters[0].bdraw()
                for obj in objectlist:
                    obj.bmove()
                    obj.bdraw()
                #user prompt
                if Prompt.ActionMode == "":
                    Prompt.display()
                    ChainAttack.defense = False
                if Prompt.ActionMode == "Action":
                    characters[0].Start = "Start" #initiates player movement
                    BlueSpartan.Start = "Nothing"
                    Prompt.ActionMode = "Nothing"
                if BlueSpartan.Start == "Finish":
                    Prompt.ActionMode = ""
                #if Elias.x >= BlueSpartan.x - BlueSpartan.weapon.x
                #chain attack
                if characters[0].Start == "Start":
                    ChainAttack.record()
                if characters[0].Stance == "Ready" or BlueSpartan.Stance == "Ready":
                    ChainAttack.display()
                if ChainAttack.defense == True:
                    if ChainAttack.Success == True:
                        ChainAttack.reset()
                        BlueSpartan.Stance = "Retreat"
                    elif ChainAttack.Success == False:
                        ChainAttack.reset()
                        BlueSpartan.Stance = "Attack"
                else:
                    if ChainAttack.Success == True:
                        ChainAttack.reset()
                        characters[0].Stance = "Attack"
                    elif ChainAttack.Success == False:
                        ChainAttack.reset()
                        characters[0].Stance = "Retreat"
                if ChainAttack.anim >= 360:
                    if ChainAttack.defense == True:
                        ChainAttack.reset()
                        ChainAttack.Success = False
                    else:
                        ChainAttack.reset()
                        characters[0].Stance = "Retreat"
                if characters[0].Stance == "Retreat":
                    ChainAttack.hitrecord = 0
                #updates health
                if characters[0].Dealt == True:
                    ChainAttack.hitrecord += 1
                    BlueSpartan.health = BlueSpartan.health - characters[0].weapon.dmg + BlueSpartan.armor
                    characters[0].Dealt = False
                if BlueSpartan.Dealt == True:
                    characters[0].health = characters[0].health - BlueSpartan.weapon.dmg + characters[0].armor
                    BlueSpartan.Dealt = False
                #initiates npc movement and resets player movement
                if characters[0].Start == "Finish":
                    BlueSpartan.Start = "Start"
                    characters[0].Start = "Nothing"
                    ChainAttack.defense = True
                #ends battle mode
                if characters[0].health <= 0:
                    screenMode = "main menu"
                if BlueSpartan.health <= 0:
                    battle = False
                if Prompt.Retreat == True:
                    Prompt.Retreat = False
                    screenMode = "adventure mode"
                    BlueSpartan.health = BlueSpartan.maxhealth
            #victory screen
            elif battle == False:
                drawImage("ui/battle mode/victory screen.png", (0, 0))
                characters[0].Start = "Nothing"
                characters[0].Stance = "Idle"
                BlueSpartan.health = BlueSpartan.maxhealth
                Prompt.ActionMode = ""
                ChainAttack.hitrecord = 0
                #characters[0].money = 
                if getKey("space"):
                    screenMode = "adventure mode"
                    battle = True

        # SUB MENU #
        elif screenMode == "sub menu":
            #user input
            if getKey("enter") or getKey("space"):
                if sb_selected != "enter":
                    if sb_selector == 5:
                        screenMode = "adventure mode"
                        sb_selector = 1
                        sb_mouse = False
            elif getKey("up") and not getKey("down"):
                if sb_selected != "up":
                    if sb_selector == 1:
                        sb_selector = 5
                    else:
                        sb_selector -= 1
                    sb_selected = "up"
                    sb_mouse = False
            elif not getKey("up") and getKey("down"):
                if sb_selected != "down":
                    if sb_selector == 5:
                        sb_selector = 1
                    else:
                        sb_selector += 1
                    sb_selected = "down"
                    sb_mouse = False
            elif getKey("escape"):
                if sb_selected != "escape":
                    screenMode = "adventure mode"
                    sb_selected = "escape"
                    sb_selector = 1
                    sb_mouse = False
            else:
                sb_selected = ""
            if getMousePos() != sb_oldPos:
                sb_mouse = True
                sb_oldPos = getMousePos()
            if sb_mouse:
                for i in range(len(sb_buttons)):
                    if sb_buttons[i].mouseOver():
                        sb_selector = i+1
                        if sb_buttons[i].mouseClicked():
                            if i == 4:
                                screenMode = "adventure mode"
                                sb_selector = 1
                                sb_mouse = False
            #draw
            location.drawUnder(frame)
            i = len(characters) - 1
            while i >= 0:
                characters[i].draw(location.pos)
                i -= 1
            location.drawOver(frame)

            drawImageOpaque("ui/menu/sub background.png", (0, 0), 127)
            drawImage("ui/menu/menu borders.png", (471, 196))
            for i in range(len(sb_buttons)):
                if i == sb_selector - 1:
                    sb_buttons[i].draw(True)
                else:
                    sb_buttons[i].draw(False)

        # DISPLAY, FRAME, EVENT #
        pygame.display.update()
        clock.tick(fps)
        frame += 1
        eventHandler(pygame.event.get())

#@Images and @Keys#

images = []
imageNames = []
def drawImage(imageName, position):
    i = 0
    while i < len(imageNames):
        if imageNames[i] == imageName:
            screen.blit(images[i], position)
            return
        i += 1
    images.append(pygame.Surface.convert_alpha(pygame.image.load(imageName)))
    imageNames.append(imageName)
    screen.blit(images[len(images) - 1], position)

def drawImageOrigin(imageName, position):
    drawImage(imageName, (position[0] + w/2 - 24, position[1] + h/2 - 24))

def drawImageOpaque(imageName, position, opacity):
    i = 0
    while i < len(imageNames):
        if imageNames[i] == imageName:
            images[i].set_alpha(opacity, pygame.RLEACCEL)
            screen.blit(images[i], position)
            return
        i += 1
    images.append(pygame.image.load(imageName))
    imageNames.append(imageName)
    images[len(images) - 1].set_alpha(opacity, pygame.RLEACCEL)
    screen.blit(images[len(images) - 1], position)

def drawImageScaled(imageName, position, size):
    i = 0
    while i < len(imageNames):
        if imageNames[i] == imageName:
            screen.blit(pygame.transform.scale(images[i], size), position)
            return
        i += 1
    images.append(pygame.Surface.convert_alpha(pygame.image.load(imageName)))
    imageNames.append(imageName)
    screen.blit(pygame.transform.scale(images[len(images) - 1], size), position)

def drawImageRotated(imageName, centerPos, angle):
    image = None
    i = 0
    while i < len(imageNames):
        if imageNames[i] == imageName:
            image = images[i]
            break
        i += 1
    if image == None:
        images.append(pygame.Surface.convert_alpha(pygame.image.load(imageName)))
        imageNames.append(imageName)
        image = images[len(images) - 1]
    w = image.get_width()
    h = image.get_height()
    l = sqrt(w*w + h*h)
    thetaA = atan(h/w)
    phiA = thetaA + angle
    hA = fabs(sin(phiA)*l)
    wA = fabs(cos(phiA)*l)
    beta = 90  - angle
    phiB = thetaA + beta
    hB = fabs(sin(phiB)*l)
    wB = fabs(cos(phiB)*l)
    H = hA
    if hB > hA:
        H = hB
    W = wA
    if wB > wA:
        W = wB
    newPos = (centerPos[0] - H/2, centerPos[1] - W/2)
    screen.blit(pygame.transform.rotate(image, -angle), newPos)

def drawString(string, pos, font = "agency fb", size = 21, color = (0, 0, 0), space = 2):
    charShift = 0
    uppercase = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z")
    upperwidth = (26, 24, 24, 26, 19, 18, 24, 26, 5, 23, 24, 18, 30, 26, 26, 24, 29, 24, 24, 22, 26, 24, 38, 26, 25, 24)
    lowercase = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")
    lowerheight = (63, 63, 63, 63, 63, 63, 78, 63, 63, 78, 63, 63, 63, 63, 63, 63, 78, 72, 63, 63, 63, 63, 63, 63, 77, 63)
    lowerwidth = (21, 21, 21, 21, 21, 14, 21, 21, 5, 10, 20, 5, 37, 21, 21, 21, 21, 20, 21, 13, 21, 22, 34, 22, 22, 21)
    for i in range(len(string)):
        upper = False
        for n in range(26):
            if uppercase[n] == string[i]:
                upper = True
                drawImageScaled("font/agency fb/upper/" + string[i] + ".png", (pos[0] + charShift, pos[1]), (int(upperwidth[n] * size / 63), size))
                charShift += int(upperwidth[n] * size / 63) + space
                break
        if not upper:
            for n in range(len(lowercase)):
                if lowercase[n] == string[i]:
                    drawImageScaled("font/agency fb/" + string[i] + ".png", (pos[0] + charShift, pos[1]), (int(lowerwidth[n] * size / 63), int(lowerheight[n] * size / 63)))
                    charShift += int(lowerwidth[n] * size / 63) + space
                    break

keyNames = []
def setKey(keyName, state):
    if state == True:
        keyNames.append(keyName)
    else:
        i = 0
        while i < len(keyNames):
            if keyNames[i] == keyName:
                del(keyNames[i])
                return
            i += 1

def getKey(keyName):
    i = 0
    while i < len(keyNames):
        if keyNames[i] == keyName:
            return True
        i += 1
    return False

mouseClicked = False
def setMouseClick(var):
    global mouseClicked
    mouseClicked = var
mousePosition = (0, 0)
def setMousePos(pos):
    global mousePosition
    mousePosition = pos
def getMouseClick():
    global mouseClicked
    return mouseClicked
def getMousePos():
    global mousePosition
    return mousePosition

def eventHandler(eventList):
    try:
        for event in eventList:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                setMousePos(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                setMouseClick(True)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                setMouseClick(False)
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
    except:
        pass

def rotateImage(Imagename, angle, pos):
    Image = pygame.transform.rotate(pygame.image.load(Imagename), angle)
    screen.blit(Image, pos)

#@Game#
class div():
    pos = (0, 0)
    size = (0, 0)
    def __init__(self, size, pos):
        self.pos = pos
        self.size = size
    def mouseOver(self):
        pos = getMousePos()
        if pos[0] >= self.pos[0] and pos[0] <= (self.pos[0] + self.size[0]):
            if pos[1] >= self.pos[1] and pos[1] <= (self.pos[1] + self.size[1]):
                return True
        return False
    def mouseClicked(self):
        if getMouseClick() and self.mouseOver():
                return True
        return False

class button(div):
    text = ""
    icon = ""
    def __init__(self, pos, text, icon):
        self.text = text
        self.icon = icon
        self.size = (175, 50)
        self.pos = pos
    def draw(self, highlighted):
        drawImage("ui/menu/button background.png", self.pos)
        if highlighted:
            drawImage("ui/menu/button selector.png", self.pos)
        drawImage(self.icon, self.pos)

#@Maps#

class npc():
    pos = (0, 0)
    adventureImage = ""
    name = ""
    speed = 0
    steps = 0
    walking = False
    vector = "down"
    wait = 0
    waitTime = 50

    msg_requireOpen = False

    #Battle Mode
    Stance = "Idle"
    Start = ""
    #turn = False (this is to replace "Start")
    Dealt = False
    x = 0
    y = 0
    width = 0
    height = 0
    v_x = 10
    battleImage = ""

    #Stats
    health = 0
    maxhealth = 0
    exhaustion = 0
    weapon = ""
    armor = 0 #change to string in future
    
    def move(self, incr = True):
        if incr:
            if self.wait <= self.waitTime:
                self.wait += 1
            if self.wait == self.waitTime:
                self.msg_requireOpen = True
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
    def sendDirec(self, direc):
        self.msg_requireOpen = False
        try:
            self.vector = direc[random.randint(0, len(direc) - 1)]
            self.walking = True
            self.move(False)
        except:
            print ("Failed to calculate random number")
            print ("Check character " + self.name + " at " + self.pos)
    def draw(self, pos):
        drawImageOrigin(self.adventureImage, (self.pos[0] - pos[0], self.pos[1] - pos[1]))
    def left(self):
        return self.pos[0]
    def right(self):
        return self.pos[0] + 48
    def bottom(self):
        return self.pos[1] + 48
    def top(self):
        return self.pos[1]
    def getPos(self):
        return (self.pos[0]/48, self.pos[1]/48)
    def setPos(self, pos):
        self.pos = (pos[0]*48, pos[1]*48)

class eElias(npc):
    def __init__(self, pos):
        self.name = "Elias"
        self.adventureImage = "characters/elias/elias d s.png"
        self.speed = 6
        self.setPos(pos)
        self.money = 0

        #battle mode
        self.Stance = "Idle"
        self.Start = ""
        self.Dealt = False
        self.x = 96
        self.y = 240
        self.width = 29
        self.height = 84
        self.v_x = 10
        self.Image = "characters/playertest.png"

        #stats
        self.health = 800
        self.maxhealth = 800
        self.exhaustion = 0
        self.weapon = wFriendlyWeapon()
        self.armor = 10
        
    def collide(self, char):
        margin = 8
        #case analysis:
        if ((char.top() <= self.top() and self.top() <= char.bottom()) or (char.top() <= self.bottom() and self.bottom() <= char.bottom())) and ((char.left() <= self.left() and self.left() <= char.right()) or (char.left() <= self.right() and self.right() <= char.right())):
                ##if (self.bottom() - char.top() <= margin):
                    ##if (self.left() - char.left() <= margin):
                        ##return True
                    ##if (right - r <= margin):
                ##if (bottom - b <= margin or t - top <= margin) and (r - left <= margin or right - l <= margin):
                    ##return True
                ###if top or bottom is within area and left or right is within area
                ##if ((sT + delta <= cB and cT + delta <= sT) or (cT + delta <= sB and sB + delta <= cB)) and ((cL + delta <= sR and sR + delta <= cR) or (sL + delta <= cR and cL + delta <= sL)):
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
                self.adventureImage = self.adventureImage[:-7] + self.vector[0] + " s.png"
                self.msg_requireOpen = True
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
            ##if self.steps >= 1 and self.steps < 48/(self.speed*2):
                ##self.adventureImage = self.adventureImage[:-5] + "l.png"
            ##elif self.steps >= 48/(self.speed*2) and self.steps < 48/self.speed:
                ##self.adventureImage = self.adventureImage[:-5] + "r.png"
            if self.steps == 48 / self.speed:
                ##self.adventureImage = self.adventureImage[:-5] + "s.png"
                self.steps = 0
                self.wait = 0
                self.walking = False
    def sendDirec(self, direc):
        self.msg_requireOpen = False
        for direction in direc:
            if direction == self.vector:
                self.walking = True
                self.move()
    def draw(self, pos):
        if screenMode == "adventure mode" or screenMode == "sub menu":
            drawImageOrigin(self.adventureImage, (13, 6))
        elif screenMode == "battle mode":
            drawImage(self.Image, (self.x, self.y))
    def goToPosition(self, env):
        self.setPos(env[0])
        self.vector = env[1]
        self.walking = True
    def drawGold(self):
        drawImage("ui/adventure mode/gold icon.png", (10, h-34))
        digits = 0
        money = self.money
        yellow = (255, 255, 50)
        i = 0
        while i < money:
            pygame.draw.line(screen, yellow, (40+i, h-30), (40+i, h-15))
            i += 1



    # ------ BATTLE MODE ------- #
    
    def bdraw(self):
        if self.Stance == "Idle":
            self.x = 96
            self.y = 240
            Image = "characters/playertest.png"
            self.weapon.update(self.Stance, self.x, self.y, self.width, self.height)
        for i in range(int(self.health * 100 / self.maxhealth)):
            pygame.draw.line(screen, (0, 255, 0), (i + 14, 409), (i + 14, 422))
        drawImage(self.Image, (self.x, self.y))
    def bmove(self):
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

    # ------ BATTLE MODE ------- #
    

class redSpartan(npc):
    def __init__(self, pos):
        self.name = "red spartan"
        self.adventureImage = "characters/red spartan.png"
        self.speed = 6
        self.setPos(pos)

class blueSpartan(npc):
    def __init__(self, pos):
        self.name = "blue spartan"
        self.adventureImage = "characters/blue spartan.png"
        self.speed = 6
        self.setPos(pos)

class area():
    name = ""
    layout = []
    image = ""
    pos = (0, 0)
    npcs = []
    def draw(self, pos):
        self.pos = pos
        drawImageOrigin(self.image, (-self.pos[0], -self.pos[1] + 16))
    def isOpen(self, vector, pos):
        num = 0
        if vector == "up" and pos[1] - 1 >= 0:
            num = self.layout[int(pos[1] - 1)][int(pos[0])]
        elif vector == "down" and pos[1] + 1 < len(self.layout):
            num = self.layout[int(pos[1] + 1)][int(pos[0])]
        elif vector == "left" and pos[0] - 1 >= 0:
            num = self.layout[int(pos[1])][int(pos[0] - 1)]
        elif vector == "right" and pos[0] + 1 < len(self.layout[0]):
            num = self.layout[int(pos[1])][int(pos[0] + 1)]
        if num == 1:
            return True
        else:
            return self.evalOpen(num)
    def evalOpen(self, num):
        return False

class ashburtonForest(area):
    def __init__(self):
        self.name = "Ashburton Forest"
        self.image = "environment/maps/Ashburton Forest.png"
        self.npcs = [redSpartan((23, 23)), blueSpartan((30, 50)), redSpartan((27, 23))]
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
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0, 0,1,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0, 2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0, 0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,2,2,2,0,0,2,2,2,0,0,0,0,0,2,2,2,2,2,0, 0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],

        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,9,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
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
    def evalOpen(self, num):
        return (num == 2 or num == 9 or num == 8)
    def teleporter(self, pos):
        num = self.layout[int(pos[1])][int(pos[0])]
        return (num == 9 or num == 8)
    def getTeleportTicket(self, pos):
        num = self.layout[int(pos[1])][int(pos[0])]
        if num == 9:
            return {"from":"Ashburton Forest", "to":"Oak Forest", "node":"outbound"}
        if num == 8:
            return {"from":"Ashburton Forest", "to":"Oak Forest", "node":"inbound"}
    def evalTicket(self, ticket):
        if ticket["from"] == "Oak Forest":
            if ticket["node"] == "outbound":
                return ((14, 36), "up")
            elif ticket["node"] == "inbound":
                return ((58, 41), "down")
    def drawUnder(self, frame):
        i = 0
        while i < 80:
            drawImageOrigin("environment/water.png", (-self.pos[0] + 24*48, -self.pos[1] + 16 + i*48 + frame%48))
            drawImageOrigin("environment/water.png", (-self.pos[0] + 25*48, -self.pos[1] + 16 + i*48 + frame%48))
            i += 1
        drawImageOrigin(self.image, (-self.pos[0], -self.pos[1] + 16))
    def drawOver(self, frame):
        y = 0
        while y < 80:
            x = 0
            while x < 80:
                if self.layout[y][x] == 8 or (self.layout[y][x] == 2 and (x != self.pos[0]/48 or (y != self.pos[1]/48-1))):
                    drawImageOrigin("environment/treetop.png", (-self.pos[0] + x*48, -self.pos[1] + y*48 + 16))
                x += 1
            y += 1

class oakForest(area):
    def __init__(self):
        self.name = "Oak Forest"
        self.image = "environment/maps/Ashburton Forest.png"
        self.npcs = [blueSpartan((23, 23)), redSpartan((30, 50)), blueSpartan((27, 23))]
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
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0, 0,1,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,0, 0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0, 2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0, 0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,2,2,2,0,0,2,2,2,0,0,0,0,0,2,2,2,2,2,0, 0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],

        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,9,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
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
    def evalOpen(self, num):
        return (num == 2 or num == 9 or num == 8)
    def teleporter(self, pos):
        num = self.layout[int(pos[1])][int(pos[0])]
        return (num == 9 or num == 8)
    def getTeleportTicket(self, pos):
        num = self.layout[int(pos[1])][int(pos[0])]
        if num == 9:
            return {"from":"Oak Forest", "to":"Ashburton Forest", "node":"outbound"}
        if num == 8:
            return {"from":"Oak Forest", "to":"Ashburton Forest", "node":"inbound"}
    def evalTicket(self, ticket):
        if ticket["from"] == "Ashburton Forest":
            if ticket["node"] == "outbound":
                return ((14, 36), "up")
            elif ticket["node"] == "inbound":
                return ((58, 41), "down")
    def drawUnder(self, frame):
        i = 0
        while i < 80:
            drawImageOrigin("environment/water.png", (-self.pos[0] + 24*48, -self.pos[1] + 16 + i*48 + frame%48))
            drawImageOrigin("environment/water.png", (-self.pos[0] + 25*48, -self.pos[1] + 16 + i*48 + frame%48))
            i += 1
        drawImageOrigin(self.image, (-self.pos[0], -self.pos[1] + 16))
    def drawOver(self, frame):
        y = 0
        while y < 80:
            x = 0
            while x < 80:
                if self.layout[y][x] == 8 or (self.layout[y][x] == 2 and (x != self.pos[0]/48 or (y != self.pos[1]/48-1))):
                    drawImageOrigin("environment/treetop.png", (-self.pos[0] + x*48, -self.pos[1] + y*48 + 16))
                x += 1
            y += 1

#@BATTLE MODE#
PI = 3.14159265359
def drawRadial(color, pos, radius, deg):
    radius = float(radius)
    circumference = radius * 2 * PI
    parts = deg * circumference / 360
    part = float(0)
    while part < parts:
        pygame.draw.line(screen, color, (pos[0], pos[1]), (pos[0] + int(sin(part / radius) * radius), pos[1] + int(-cos(part / radius) * radius)), 3)
        part += 1

class BattlePrompt():
    Retreat = False
    ActionMode = ""
    bp_selector = 1
    bp_selected = ""
    x = 285
    y = 378
    Image = "ui/battle mode/battleprompt.png"
    def display(self):
        drawImage(self.Image, (self.x, self.y))
        drawImage("ui/menu/main selector.png", (308, 368 + self.bp_selector * 31))
        if self.bp_selector == 1:
            drawImage("ui/battle mode/battleprompt_attack_dscrp.png", (self.x + 12, self.y + 91))
        elif self.bp_selector == 2:
            drawImage("ui/battle mode/battleprompt_retreat_dscrp.png", (self.x + 12, self.y + 91))
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
    Imagedef = "ui/battle mode/circlex.png"
    Imagebackground = "ui/battle mode/circletemplate.png"
    Image1 = "ui/battle mode/circle1.png"
    Image2 = "ui/battle mode/circle2.png"
    Image3 = "ui/battle mode/circle3.png"
    Image4 = "ui/battle mode/circle4.png"
    Image5 = "ui/battle mode/circle5.png"
    Image6 = "ui/battle mode/circle6.png"
    Image7 = "ui/battle mode/circle7.png"
    Image8 = "ui/battle mode/circle8.png"
    Imagehit = "ui/battle mode/hitrecord.png"
    anim = 0
    randindct = 0
    defense = False
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
        #generates random integer based on number of successful hits already made
        if self.anim == 6:
            if self.defense == True:
                self.randindct = random.randint(1,8)
            elif self.defense == False:
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
        #displays indicator based on random integer generated
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
        #draws radial (controls radial speed- dependent on number of hits already made)
        if self.anim <= 359:
            if self.hitrecord >= 1 and self.hitrecord <= 3:
                self.anim += 0
            elif self.hitrecord >= 4 and self.hitrecord <= 7:
                self.anim += 2
            elif self.hitrecord >= 8 and self.hitrecord <= 11:
                self.anim += 4
            elif self.hitrecord >= 12:
                self.anim += 6
            else:
                if self.defense == True:
                    self.anim += 0
                else:
                    self.anim -= 2
            drawRadial((0, 0, 255), (self.x + 50, self.y + 50), 47, (self.anim))
        #resets radial (never used- chainattack.display is closed when self.anim == 360)
        elif self.anim >= 360:
            drawRadial((0, 0, 255), (self.x + 50, self.y + 50), 47, 360)
        drawImage(self.Imagedef, (self.x, self.y))
        #user input
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
    wpntype = "sword"
    dmg = 50
    Image0 = "items/m_falchion_0.png"
    Image45 = "items/m_falchion_45.png"
    Imagedefenmy = "items/m_falchion_135.png"
    #From order of appearance in animation, enemy attack
    Image90r = "items/m_falchion_90r.png"
    Image112_5 = "items/m_falchion_112_5.png"
    Image135 = "items/m_falchion_135.png"
    Image157_5 = "items/m_falchion_157_5.png"
    Image180 = "items/m_falchion_180.png"
    Image202_5 = "items/m_falchion_202_5.png"
    Image225 = "items/m_falchion_225.png"
    #def flip(self):

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
            elif self.anim >= 67.5 and self.anim <= 112.5:
                rotateImage(self.Image0, self.anim, (self.x, self.y))
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
    wpntype = weapon.wpntype
    Image135 = weapon.Image135
    Image180 = weapon.Image180
    anim = 0
    x = weapon.x
    y = weapon.y
    width = weapon.width
    height = weapon.height
    deg = 0
    dmg = weapon.dmg
    def update(self, Stance, x, y, width, height):
        self.x = x - 48
        self.y = y
        if self.anim >= 360:
            self.anim = 10
        if Stance == "Idle":
            rotateImage(self.Image135, 0, (self.x, self.y))
        if Stance == "Prepare":
            self.anim -= 10
            if self.anim <= 0 and self.anim >= -22.5:
                rotateImage(self.Image180, self.anim, (self.x, self.y))
            elif self.anim <= -22.5 and self.anim >= -67.5:
                rotateImage(self.Image135, self.anim + 45, (self.x, self.y))
            elif self.anim <= -67.5 and self.anim >= -112.5:
                rotateImage(self.Image180, self.anim, (self.x, self.y))
        if Stance == "Charge":
            rotateImage(self.Image180, -90, (self.x, self.y))
        if Stance == "Ready":
            rotateImage(self.Image180, -90, (self.x, self.y))
        if Stance == "Attack":
            self.anim += 10
            if (self.anim >= 0 and self.anim <= 22.5) or (self.anim <= 0 and self.anim >= -22.5):
                rotateImage(self.Image180, self.anim, (self.x, self.y))
            elif self.anim <= -22.5 and self.anim >= -67.5:
                rotateImage(self.Image135, self.anim + 45, (self.x, self.y))
            elif self.anim <= -67.5 and self.anim >= -112.5:
                rotateImage(self.Image180, self.anim, (self.x, self.y))
            elif self.anim <= 67.5 and self.anim >= 22.5:
                rotateImage(self.Image135, self.anim + 45, (self.x, self.y))
            elif self.anim <= 112.5 and self.anim >= 67.5:
                rotateImage(self.Image180, self.anim, (self.x, self.y))
        if Stance == "NotReady":
            self.anim -= 10
            if (self.anim >= 0 and self.anim <= 22.5) or (self.anim <= 0 and self.anim >= -22.5):
                rotateImage(self.Image180, self.anim, (self.x, self.y))
            elif self.anim <= -22.5 and self.anim >= -67.5:
                rotateImage(self.Image135, self.anim + 45, (self.x, self.y))
            elif self.anim <= -67.5 and self.anim >= -112.5:
                rotateImage(self.Image180, self.anim, (self.x, self.y))
            elif self.anim <= 67.5 and self.anim >= 22.5:
                rotateImage(self.Image135, self.anim + 45, (self.x, self.y))
            elif self.anim <= 112.5 and self.anim >= 67.5:
                rotateImage(self.Image180, self.anim, (self.x, self.y))
        if Stance == "Retreat":
            rotateImage(self.Image135, self.anim + 90, (self.x, self.y))
        if Stance == "Reset":
            self.anim -= 10
            if (self.anim >= 0 and self.anim <= 22.5) or (self.anim <= 0 and self.anim >= -22.5):
                rotateImage(self.Image180, self.anim, (self.x, self.y))
            elif self.anim <= -22.5 and self.anim >= -67.5:
                rotateImage(self.Image135, self.anim + 45, (self.x, self.y))
            elif self.anim <= -67.5 and self.anim >= -112.5:
                rotateImage(self.Image180, self.anim, (self.x, self.y))
            elif self.anim <= 67.5 and self.anim >= 22.5:
                rotateImage(self.Image135, self.anim + 45, (self.x, self.y))
            elif self.anim <= 112.5 and self.anim >= 67.5:
                rotateImage(self.Image180, self.anim, (self.x, self.y))

class cBlueSpartan():
    Stance = "Idle"
    Start = ""
    Dealt = False
    x = 594
    y = 240
    width = 30
    height = 84
    v_x = 10
    Image = "characters/npctest.png"
    health = 800
    maxhealth = 800
    exhaustion = 0
    weapon = wEnemyWeapon()
    armor = 0
    def bdraw(self):
        if self.Stance == "Idle":
            self.x = 594
            self.y = 240
            Image = "characters/npctest.png"
            self.weapon.update(self.Stance, self.x, self.y, self.width, self.height)
        for i in range(int(self.health * 100 / self.maxhealth)):
            pygame.draw.line(screen, (0, 255, 0), (i + 494, 409), (i + 494, 422))
        drawImage(self.Image, (self.x, self.y))
    def bmove(self):
        if self.Start == "Start":
            #if wpntype == "melee":
            #skill sequence
            if self.Stance == "Skill":
                 self.weapon.update(self.Stance, self.x, self.y, self.width, self.height)
            #normal attack sequence
            elif self.Stance == "Charge":
                self.x -= self.v_x
                self.weapon.update(self.Stance, self.x, self.y, self.width, self.height)
                if self.x <= 200:
                    self.Stance = "Ready"
            elif self.Stance == "Ready":
                 self.x = self.x
                 self.y = self.y
                 self.weapon.update(self.Stance, self.x, self.y, self.width, self.height)
            elif self.Stance == "Attack":
                 self.weapon.update(self.Stance, self.x, self.y, self.width, self.height)
                 if self.weapon.anim >= 45:
                     self.Dealt = True
                     self.Stance = "NotReady"
            elif self.Stance == "NotReady":
                 self.x = self.x
                 self.y = self.y
                 self.weapon.update(self.Stance, self.x, self.y, self.width, self.height)
                 if self.weapon.anim <= -90:
                     self.Stance = "Ready"
            elif self.Stance == "Retreat":
                 self.x += self.v_x
                 self.weapon.update(self.Stance, self.x, self.y, self.width, self.height)
                 if self.x >= 594:
                     self.x = 594
                     self.Stance = "Reset"
            elif self.Stance == "Reset":
                 self.weapon.update(self.Stance, self.x, self.y, self.width, self.height)
                 if self.weapon.anim <= -45:
                      self.Stance = "Idle"
                      self.Start = "Finish"
            else:
                self.Stance = "Prepare"
                self.weapon.update(self.Stance, self.x, self.y, self.width, self.height)
                if self.weapon.anim <= -90:
                    self.Stance = "Charge"

if __name__ == '__main__':
    main()
