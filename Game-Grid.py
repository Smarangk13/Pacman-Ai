import time
import sys, pygame
import random
from Constants import Colors
from Constants import Properties
from Player import Player
from Shapes import Rectangle
from Map_Standard import BetterMaps as GameMap


class GamePlay:
    # Orb and powerup positions {coordinate : colledtedFlag} eg: '50x30y' : (50,30) or False
    orbs = {}
    powerups = {}

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode([Properties.WINDOWWIDTH, Properties.WINDOWHEIGHT])
        self.pacman = Player()

        self.game_font = pygame.font.SysFont('Terminal', 45)

        self.score = 0

        self.map = GameMap()
        self.map.load_map()
        self.map.drawGrid()
        self.map.color_grid()
        self.player_pos = self.map.player_start
        self.pacman.x = self.player_pos[0]
        self.pacman.y = self.player_pos[1]

        # Make Pacman spot on map an Open
        player_X = self.player_pos[0]
        player_Y = self.player_pos[1]
        player_grid_X, player_grid_Y = self.map.find_grid(player_X, player_Y)
        self.map.grid[player_grid_Y][player_grid_X] = 'O'

    def __key_action(self):
        key = pygame.key.get_pressed()
        pressed = [i for i, j in enumerate(key) if j == 1]
        # print(pressed)

        if Properties.UPARROW in pressed:
            self.pacman.next_turn = 'Up'

        elif Properties.DOWNARROW in pressed:
            self.pacman.next_turn = 'Down'

        if Properties.LEFTARROW in pressed:
            self.pacman.next_turn = 'Left'

        elif Properties.RIGHTARROW in pressed:
            self.pacman.next_turn = 'Right'

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

    def get_next(self, row, col, direction):
        next_row = row
        next_col = col

        if direction == 'Right':
            next_row = row
            next_col = col + 1

        elif direction == 'Left':
            next_row = row
            next_col = col - 1

        elif direction == 'Down':
            next_row = row + 1
            next_col = col

        elif direction == 'Up':
            next_row = row - 1
            next_col = col

        if next_row >= len(self.map.grid):
            next_row -= 1

        if next_col >= len(self.map.grid[0]):
            next_col -= 1

        return self.map.grid[next_row][next_col]

    # Check collisions with walls for current path and turns
    def collisions(self):
        # Teleport if at edge
        self.warp()
        player_X = self.pacman.x
        player_Y = self.pacman.y

        col, row = self.map.find_grid(player_X, player_Y)
        direction = self.pacman.direction

        next_tile = self.get_next(row, col, direction)
        if next_tile == 'W':
            self.pacman.stop_movement()
        else:
            self.pacman.start_movement()

        # For turns
        next_tile =self.get_next(row, col, self.pacman.next_turn)
        if next_tile != 'W':
            self.pacman.makeTurn()

    # Remove tokens and update score
    def update_map(self):
        player_X = self.pacman.x
        player_Y = self.pacman.y
        col, row = self.map.find_grid(player_X, player_Y)
        current_tile = self.map.grid[row][col]

        if current_tile == 'T':
            self.map.grid[row][col] = 'O'
            self.score += Properties.TOKEN_SCORE


    def drawEnemies(self):
        pass

    def moveEnemies(self):
        pass

    def drawObjects(self):
        # Draw Objects
        # Draw player
        player_X = self.pacman.x
        player_Y = self.pacman.y
        pos = [player_X, player_Y]
        pygame.draw.circle(self.screen, Colors.YELLOW, pos, Player.radius)

        # Draw map

        self.map.drawGrid()
        self.map.color_grid()

        self.drawEnemies()

    def show_HUD(self):
        score_val = '0' * (6 - len(str(self.score))) + str(self.score)
        score_display = self.game_font.render(score_val, False, Colors.WHITE)
        score_text = self.game_font.render('SCORE', False, Colors.WHITE)
        self.screen.blit(score_display, Properties.SCORE_NUMS)
        self.screen.blit(score_text, Properties.SCORE_TEXT)

    def gameLoop(self):
        while (1):
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    self.__key_action()

                if event.type == pygame.MOUSEBUTTONUP:
                    mousePosX, mousePosY = pygame.mouse.get_pos()
                    gridPosX, gridPosY = self.map.find_grid(mousePosX, mousePosY)

                    print(gridPosY, gridPosX)
                    player_X = self.pacman.x
                    player_Y = self.pacman.y

                    row, col = self.map.find_grid(player_X, player_Y)
                    print(row, col)
                    print('map = ', self.map.grid[gridPosY][gridPosX])
                    print('player=', self.map.grid[row][col])

            self.drawObjects()
            self.move_player()
            self.collisions()
            self.update_map()
            self.show_HUD()

            pygame.display.flip()
            self.screen.fill(Colors.BLACK)

    def updateData(self):
        pass


if __name__ == '__main__':
    game = GamePlay()
    game.gameLoop()
