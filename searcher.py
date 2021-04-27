class finder:
    best_path = []
    paths = []

    grid = []

    found = False
    target = 0, 0
    square = ''
    reached = {}

    def dist(self, target, pos):
        return abs(target[1] - pos[1]) + abs(target[0] - pos[0])

    def dfs(self, pos, target, steps=0, path=None):
        if path is None:
            path = []
            new_path = []
        else:
            new_path = list(path[:])

        if pos == list(target):
            self.best_path = path.copy()
            self.found = True
            return steps

        if self.found:
            return

        if steps > 10:
            return

        x = pos[0]
        y = pos[1]

        # Right
        new_path.append('Right')
        self.dfs([x + 1, y], target, steps + 1, new_path)

        # Left
        new_path_left = new_path[:]
        new_path_left[-1] = 'Left'
        self.dfs([x - 1, y], target, steps + 1, new_path_left)

        # Up
        new_path_up = new_path[:]
        new_path_up[-1] = 'Up'
        self.dfs([x, y - 1], target, steps + 1, new_path_up)

        # Down
        new_path_down = new_path[:]
        new_path_down[-1] = 'Down'
        self.dfs([x, y + 1], target, steps + 1, new_path_down)

    def at_target(self, x, y):
        if [x, y] == list(self.target):
            return True
        return False

    def at_target_pos(self, pos):
        x = pos[0]
        y = pos[1]
        return self.at_target(x, y)

    def get_dist(self, pos):
        target = self.target
        x1 = pos[0]
        y1 = pos[1]
        x2 = target[0]
        y2 = target[1]
        dist = abs(x1 - x2) + abs(y1 - y2)
        return dist

    def make_grid(self):
        row = ['O' for i in range(50)]
        cols = [row[:] for i in range(51)]
        self.grid = cols

    # Checks if current tile is not visited or a wall
    def checker(self, pos):
        x = pos[0]
        y = pos[1]
        if x < 0 or y < 0 or \
                x >= len(self.grid) or y >= len(self.grid[0]):
            return False

        if self.grid[x][y] != 'W':
            pos = str(x) + 'R' + str(y) + 'C'
            self.square = pos

            if self.at_target(x, y):
                self.found = True

            if pos not in self.reached:
                return True

        return False

    def bfshelper(self, start):
        self.found = False
        pos = list(start)
        row = pos[0]
        col = pos[1]

        if self.at_target(row, col):
            self.found = True

        pos = str(row) + 'R' + str(col) + 'C'
        self.reached = {pos: []}

        visited = 0
        depth = 15
        poses = [start]

        while visited < depth and not self.found:
            new_poses = []
            for position in poses:
                new_poses += self.bfs(position)

            poses = new_poses

            visited += 1

        if not self.found:
            shortest = 10000
            short_route = []
            for pos in self.reached:
                x = pos[:pos.find('R')]
                y = pos[pos.find('R') + 1:-1]
                location = [int(x), int(y)]
                dist = self.get_dist(location)
                if dist < shortest:
                    shortest = dist
                    short_route = self.reached[pos]
            return short_route

        else:
            tr = self.target[0]
            tc = self.target[1]
            tar = str(tr) + 'R' + str(tc) + 'C'
            return  self.reached[tar]

    # Charge to ROW COL
    def bfs(self, current):
        pos = list(current)
        row = pos[0]
        col = pos[1]

        pos = str(row) + 'R' + str(col) + 'C'

        squares_visited = []
        reach = self.reached[pos]

        # Right
        next = [row, col + 1]
        if self.checker(next):
            self.reached[self.square] = reach + ['Right']
            squares_visited.append(next)

        # Left
        next = [row, col - 1]
        if self.checker(next):
            self.reached[self.square] = reach + ['Left']
            squares_visited.append(next)

        # Up
        next = [row - 1, col]
        if self.checker(next):
            self.reached[self.square] = reach + ['Up']
            squares_visited.append(next)

        # Down
        next = [row + 1, col]
        if self.checker(next):
            self.reached[self.square] = reach + ['Down']
            squares_visited.append(next)

        return squares_visited


if __name__ == '__main__':
    d = finder()
    start =15, 18
    target = 18, 15
    # d.dfs(start,target)

    print('Best path is')
    print(d.best_path)

    d.make_grid()

    d.target = target
    route = d.bfshelper(start)
    print(route)