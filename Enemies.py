from Shapes import Circle
from Constants import Properties
from Player import Player
from searcher import finder

class Enemy(Player):
    movement_speed = Properties.ENEMYSPEED
    speed = Properties.ENEMYSPEED
    mode = 'Chase'
    sleeptime = 0
    start_pos = [1,1]

    def __init__(self, type = 'Inky'):
        radius = Properties.CHARACTERRADIUS
        self.name = type
        super().__init__()
        self.behaviour()

    def behaviour(self):
        if self.name == 'Inky':
            self.sleeptime = 5

        if self.name == 'Blinky':
            self.sleeptime = 15

        if self.name == 'Pinky':
            self.sleeptime = 20

        if self.name == 'Clyde':
            self.sleeptime = 30

    def opposite(self, direction):
        if direction == 'Right':
            return 'Left'

        elif direction == 'Left':
            return 'Right'

        elif direction == 'Up':
            return 'Down'

        else:
            return 'Up'

    def chase(self, grid, target, start):
        find = finder()
        find.grid = grid
        find.target = target

        # Find pacman go opposite way
        if self.mode == 'Run':
            self.speed = Properties.GHOST_SCARED_SPEED
            route = find.bfshelper(start)
            if len(route) != 0:
                direction = route[0]
                self.direction = self.opposite(direction)
                return

        elif self.mode == 'Caught':
            self.speed = Properties.GHOST_CAUGHT_SPEED
            find.target = self.start_pos

        else:
            self.speed = Properties.ENEMYSPEED
            if self.name == 'Blinky':
                pass

            # Tries to cut you off, goes to right, left extreme
            elif self.name == 'Inky':
                new_x = 1
                if target[1] > len(grid[0])//2:
                    new_x = len(grid[0]) - 2

                find.target = new_x, target[0]

        route = find.bfshelper(start)

        if len(route)!= 0:
            self.direction = route[0]

    def get_next(self, grid, row, col, direction):
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

        if next_row >= len(grid):
            next_row -= 1

        elif next_row < 0:
            next_row = 0

        if next_col >= len(grid[0]):
            next_col -= 1

        elif next_col < 0:
            next_col = 0

        return grid[next_row][next_col]