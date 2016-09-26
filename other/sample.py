import pygame, sys

pygame.init()
width, height = 720, 528
screen = pygame.display.set_mode((720, 528))
clock = pygame.time.Clock()

def main():
    deg = 0
    #anim = 0
    Imageorig = "test1.png"
    x = 50
    y = 50
    width = 66
    height = 66
    while True:
        screen.fill((255, 255, 255))
        """if getKey("space"):
            anim += 1
            if anim == 20:
                deg = 315
            elif anim == 35:
                deg = 337.5
            elif anim == 45:
                deg = 0
            elif anim == 55:
                deg = 337.5
            elif anim == 65:
                deg = 315
            elif anim == 75:
                deg = 292.5
            elif anim == 85:
                deg = 270
            elif anim == 95:
                deg = 247.5
            elif anim == 105:
                deg = 225
        if anim >= 150:
            anim = 0"""
        if getKey("space"):
            deg += 2
            print(x, y, deg)
            if deg >= 1 and deg <= 45:
                x -= 1
                y -= 1
            if deg >= 46 and deg <= 90:
                x += 1
                y += 1
            if deg >= 91 and deg <= 135:
                x -= 1
                y -= 1
            if deg >= 136 and deg <= 180:
                x += 1
                y += 1
            if deg >= 181 and deg <= 225:
                x -= 1
                y -= 1
            if deg >= 226 and deg <= 270:
                x += 1
                y += 1
            if deg >= 271 and deg <= 315:
                x -= 1
                y -= 1
            if deg >= 316 and deg <= 359:
                x += 1
                y += 1
        if deg >= 360:
            deg = 0
            x = 50
            y = 50
        Image = Imageorig
        newImage = rotateImage(Image, deg)
        screen.blit(newImage, (50, 50))
        pygame.display.update()
        clock.tick(40)
        eventHandler(pygame.event.get())

images = []
imageNames = []
def drawImage(imageName, position):
     #if loaded already, just draw it
     for i in range(len(imageNames)):
         if imageNames[i] == imageName:
             screen.blit(images[i], position)
             return
     #otherwise, load the image before drawing it
     images.append(pygame.image.load(imageName))
     imageNames.append(imageName)
     screen.blit(images[len(images) - 1], position) 

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
            elif event.key == pygame.K_KP_ENTER:
                setKey("enter", True)
            elif event.key == pygame.K_BACKSPACE:
                setKey("backspace", True)
            print (keyNames)
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
            elif event.key == pygame.K_KP_ENTER:
                setKey("enter", False)
            elif event.key == pygame.K_BACKSPACE:
                setKey("backspace", False)
            print (keyNames)

def rotateImage(Imagename, angle):
    Image = pygame.transform.rotate(pygame.image.load(Imagename), angle)
    return Image

if __name__ == '__main__':
    main()
