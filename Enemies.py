import random
import time
from Shapes import Circle
from Constants import Properties
from Player import Player
from searcher import finder

class Enemy(Player):
    movement_speed = Properties.ENEMYSPEED
    speed = Properties.ENEMYSPEED
    mode = 'Chase'
    sleeping = True
    sleeptime = 0
    start_pos = [1,1]

    # Other ghosts have sub ojbectives like going to corner etc
    objective_start_time = 0
    objective_pos = [1,1]

    # Inky randomly switches modes, so keep track of who he is and when he changed
    inky_mode = 1 # 1 - r 2 - p 3 -o
    inky_last_switch = 0

    def __init__(self, type = 'Inky'):
        radius = Properties.CHARACTERRADIUS
        self.name = type
        super().__init__()
        self.behaviour()

    def behaviour(self):
        if self.name == Properties.REDGHOST:
            self.sleeptime = 5

        if self.name == Properties.BLUEGHOST:
            self.sleeptime = 10

        if self.name == Properties.PINKGHOST:
            self.sleeptime = 20

        if self.name == Properties.ORANGEGHOST:
            self.sleeptime = 25

    def opposite(self, direction):
        if direction == 'Right':
            return 'Left'

        elif direction == 'Left':
            return 'Right'

        elif direction == 'Up':
            return 'Down'

        else:
            return 'Up'

    def far_corner(self,pacman):
        find = finder()
        find.target = pacman
        c1 = [1,1]
        c2 = [25,25]
        c3 = [1,25]
        c4 = [24,1]
        corners = [c1,c2,c3,c4]
        max_d = 0
        far  = []
        for c in corners:
            d = find.get_dist(c)
            if d > max_d:
                max_d = d
                far = c
        return far

    def close_corner(self,pacman):
        find = finder()
        find.target = pacman
        c1 = [1,1]
        c2 = [25,25]
        c3 = [1,25]
        c4 = [24,1]
        corners = [c1,c2,c3,c4]
        min_d = 1000
        close = []
        for c in corners:
            d = find.get_dist(c)
            if d < min_d:
                min_d = d
                close = c
        return close

    def chase(self, grid, target, start):
        find = finder()
        find.grid = grid
        find.target = target

        # Find pacman go opposite way
        if self.mode == 'Run':
            self.speed = Properties.GHOST_SCARED_SPEED
            find.target = self.far_corner(target)

            route = find.bfshelper(start)
            if len(route) != 0:
                direction = route[0]
                self.direction = direction
                return

        elif self.mode == 'Caught':
            self.speed = Properties.GHOST_CAUGHT_SPEED
            find.target = self.start_pos

        else:
            self.speed = Properties.ENEMYSPEED
            if self.name == Properties.REDGHOST:
                pass

            # Randomly changes who he behaves like
            elif self.name == Properties.BLUEGHOST:
                elapsed = time.time() - self.inky_last_switch
                if elapsed > Properties.INKY_TIME:
                    self.inky_mode = random.randint(1,3)

                dist = find.get_dist(start)
                # Like Inky
                if self.inky_mode == 1:
                    pass

                # Like Pinky
                elif self.inky_mode == 2:
                    if dist > 12:
                        find.target = self.close_corner(target)

                # Like Clyde
                else:
                    self.clyde_chase(target, dist)

            # Tries to cut you off, goes to right, left extreme
            elif self.name == Properties.PINKGHOST:
                dist = find.get_dist(start)
                if dist > 12:
                    find.target = self.close_corner(target)

            # Run away when close
            elif self.name == Properties.ORANGEGHOST:
                dist = find.get_dist(start)
                find.target = self.clyde_chase(target,dist)

        route = find.bfshelper(start)

        if len(route)!= 0:
            self.direction = route[0]

    def clyde_chase(self, target, dist):
        current_time = time.time()
        passed_time = current_time - self.objective_start_time
        if passed_time < Properties.OBJECTIVE_TIME:
            target = self.objective_pos
        else:
            if dist < Properties.CLYDE_DIST:
                self.objective_start_time = time.time()
                target = self.far_corner(target)
                self.objective_pos = target

        return target

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