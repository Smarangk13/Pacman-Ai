import time
import sys, pygame
import random
from Constants import Colors
from Constants import Properties
from Player import Player
from Shapes import Rectangle


class GamePlay:
    # Orb and powerup positions {coordinate : colledtedFlag} eg: '50x30y' : (50,30) or False
    orbs = {}
    powerups = {}

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode([Properties.WINDOWWIDTH, Properties.WINDOWHEIGHT])
        self.pacman = Player()

        self.max_wall_x = 0
        self.min_wall_y = Properties.WINDOWWIDTH
        self.min_wall_x = Properties.WINDOWHEIGHT
        self.max_wall_y = 0

        self.walls = []
        self.load_map()
        self.load_orbs()

    def load_map(self, map_Name='map1'):
        with open(map_Name) as f:
            walls = f.readlines()

        for wall in walls:
            wall.strip('\n')
            # print(eval(wall))
            wallBox = eval(wall)
            wallRect = Rectangle(wallBox[0], wallBox[1], wallBox[2], wallBox[3])

            if wallBox[0] > self.max_wall_x:
                self.max_wall_x = wallBox[0]

            elif wallBox[0] < self.min_wall_x:
                self.min_wall_x = wallBox[0]

            if wallBox[1] > self.max_wall_y:
                self.max_wall_y = wallBox[1]

            elif wallBox[1] < self.min_wall_y:
                self.min_wall_y = wallBox[1]

            self.walls.append(wallRect)

    # Unused
    def load_orbs(self):
        for wall in self.walls:
            if wall.x == self.max_wall_x or wall.y == self.max_wall_y:
                continue

            # Load y orbs
            end = wall.w + wall.x
            start = wall.x
            ypos = wall.y - Properties.ORBGAP
            xpos = start

            while xpos < end:
                xpos += Properties.ORBSPACING
                pos = str(xpos) + 'x' + str(ypos) + 'y'
                self.orbs[pos] = (xpos, ypos)

            # Load y orbs
            end = wall.h + wall.y
            start = wall.y
            xpos = wall.x - Properties.ORBSPACING
            ypos = start

            while ypos < end:
                ypos += Properties.ORBSPACING
                pos = str(xpos) + 'x' + str(ypos) + 'y'
                self.orbs[pos] = (xpos, ypos)

    def __key_action(self):
        key = pygame.key.get_pressed()
        pressed = [i for i, j in enumerate(key) if j == 1]
        # print(pressed)

        if Properties.UPARROW in pressed:
            self.pacman.turnUp()

        elif Properties.DOWNARROW in pressed:
            self.pacman.turnDown()

        if Properties.LEFTARROW in pressed:
            self.pacman.turnLeft()

        elif Properties.RIGHTARROW in pressed:
            self.pacman.turnRight()

    def move_player(self):
        # right left up down
        direction = self.pacman.get_direction()
        # print(direction)

        if direction == 0:
            self.pacman.x += self.pacman.playerSpeed

        elif direction == 1:
            self.pacman.x -= self.pacman.playerSpeed

        elif direction == 2:
            self.pacman.y -= self.pacman.playerSpeed

        elif direction == 3:
            self.pacman.y += self.pacman.playerSpeed

    def warp(self):
        # First check out of bounds
        if self.pacman.x > Properties.WINDOWWIDTH:
            self.pacman.x = 0

        if self.pacman.x < 0:
            self.pacman.x = Properties.WINDOWWIDTH

        if self.pacman.y > Properties.WINDOWHEIGHT:
            self.pacman.y = 0

        if self.pacman.y < 0:
            self.pacman.y = Properties.WINDOWHEIGHT

    def collisions(self):
        # Teleport if at edge
        self.warp()

        # pacman with walls
        playerbox = self.pacman.toBox()
        for wall in self.walls:
            if Rectangle.collision(playerbox, wall):
                direction = self.pacman.get_direction()

                if direction == 0:
                    self.pacman.x -= self.pacman.playerSpeed

                elif direction == 1:
                    self.pacman.x += self.pacman.playerSpeed

                elif direction == 2:
                    self.pacman.y += self.pacman.playerSpeed

                elif direction == 3:
                    self.pacman.y -= self.pacman.playerSpeed

        # enemy with walls

    def drawEnemies(self):
        pass

    def moveEnemies(self):
        pass

    def drawObjects(self):
        # Draw Objects
        # Draw player
        pygame.draw.circle(self.screen, Colors.YELLOW, self.pacman.get_pos(), Player.radius)

        # Draw walls
        for wall in self.walls:
            pygame.draw.rect(self.screen, Colors.BLUE, wall.get_dims(), 1)

        # Draw Orbs
        for orb in self.orbs:
            if self.orbs[orb]:
                pygame.draw.circle(self.screen, Colors.YELLOW, self.orbs[orb], Properties.ORBSIZE)

        # Draw Orbs
        for powerup in self.powerups:
            if self.powerups[powerup]:
                pygame.draw.circle(self.screen, Colors.YELLOW, self.powerups[powerup], Properties.POWERUPSIZE)

        self.drawEnemies()

    def gameLoop(self):
        while (1):
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    self.__key_action()

            self.drawObjects()

            self.move_player()
            self.moveEnemies()
            self.collisions()

            pygame.display.flip()
            self.screen.fill(Colors.BLACK)


    def updateData(self):
        pass

if __name__ == '__main__':
    game = GamePlay()
    game.gameLoop()
