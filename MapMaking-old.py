import sys
import pygame
from Constants import Colors
from Constants import Properties
from Player import Player

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode([Properties.WINDOWWIDTH, Properties.WINDOWHEIGHT])

startx = 0
starty = 0
startlen = 0
startheight = 0

wallWidth = 20
mousedown = False
walls = []
mapNum = 0

def close(a,b,target):
    if abs(target - a) < abs(target - b):
        return 1
    return 2


def wall_cleaning(walls):
    gap = Properties.WALLGAP
    # print(gap)

    for wall in walls:
        wallx = wall[0]
        wally = wall[1]

        closeUp = wally//gap * gap
        closeDown = wally//gap * gap + gap

        closeRight = wallx//gap * gap
        closeLeft = wallx//gap * gap + gap

        if close(closeUp,closeDown,wally) == 1:
            wall[1] = closeUp

        else:
            wall[1] = closeDown

        if close(closeRight, closeLeft, wallx) == 1:
            wall[0] = closeRight

        else:
            wall[0] = closeLeft

    return walls


while (1):
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        mousePosX, mousePosY = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mousedown = True
            startx, starty = mousePosX, mousePosY

        if event.type == pygame.MOUSEBUTTONUP:
            mousedown = False
            x = min(startx, mousePosX)
            y = min(starty, mousePosY)
            l = abs(mousePosX - startx)
            h = abs(mousePosY - starty)

            if close(l,h, wallWidth) == 1:
                l = wallWidth
            else:
                h = wallWidth

            walls.append([x,y,l,h])

        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            pressed = [i for i, j in enumerate(key) if j == 1]

            # C- clean
            if pressed[0] == 6:
                wall_cleaning(walls)

            # S- save
            elif pressed[0] == 22:
                mapFile = 'map' + str(mapNum)
                writer = open(mapFile,'w')
                for wall in walls:
                    writer.write(str(wall))
                    writer.write('\n')
                writer.close()

        if mousedown:
            x = min(startx, mousePosX)
            y = min(starty, mousePosY)
            l = abs(mousePosX - startx)
            h = abs(mousePosY - starty)
            pygame.draw.rect(screen, Colors.LIGHTBLUE, [x,y,l,h])

        for wall in walls:
            pygame.draw.rect(screen, Colors.BLUE, wall)

        pygame.display.flip()
        screen.fill(Colors.BLACK)

