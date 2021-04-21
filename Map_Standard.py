import sys
import pygame
from Constants import Properties, Colors

'''
Map file
Grid size 
[
w w w o T T      P          B   C          E1 E2 E3 G  
Wall Open Token Power-up Bonus  Character Enemy Gate
Blue Black Yellow Orange Green White Red    Lightblue
]

'''


class BetterMaps:
    def __init__(self):
        self.Game_Props = Properties()

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode([self.Game_Props.WINDOWWIDTH, self.Game_Props.WINDOWHEIGHT])
        grid = [0, 0]
        self.squaresX = grid[0]
        self.squaresY = grid[1]

        self.vLines = []
        self.hLines = []
        self.line_width = 1

        self.grid = []

        self.player_start = [0,0]

    def make_grid(self, grid):
        grid = grid
        self.squaresX = grid[0]
        self.squaresY = grid[1]
        self.gridlines()

        gridX = ['O' for i in range(len(self.vLines) - 1)]
        grid = [gridX.copy() for i in range(len(self.hLines) - 1)]
        # print(grid)
        self.grid = grid

    def gridlines(self):
        startX = self.Game_Props.WINDOWBUFFERH
        endX = self.Game_Props.WINDOWWIDTH - self.Game_Props.WINDOWBUFFERH
        gameWidth = endX - startX
        squareGapX = gameWidth // self.squaresX
        # verticalLines = [x for x in range(startX, endX + 5, squareGapX)]  # Adding 5 to accomadate last line
        verticalLines = [startX + (x *squareGapX ) for x in range(self.squaresX + 1)]

        startY = self.Game_Props.WINDOWBUFFERTOP
        endY = self.Game_Props.WINDOWHEIGHT - self.Game_Props.WINDOWBUFFERBOTTOM
        gameHeight = endY - startY
        squareGapY = gameHeight // self.squaresY
        # horizontalLines = [y for y in range(startY, endY + 5, squareGapY)]
        horizontalLines = [startY + (y * squareGapY) for y in range(self.squaresY + 1)]

        self.vLines = verticalLines
        self.hLines = horizontalLines


    # Find which square of the grid the click corresponds to
    def find_grid(self, mx, my):
        # Easy way is to linear sear
        # Handle outside clicks
        if my > self.hLines[-1]:
            my = self.hLines[-2]

        elif my < self.hLines[0]:
            my = self.hLines[0]

        if mx > self.vLines[-1]:
            mx = self.vLines[-2]
        elif mx < self.vLines[0]:
            mx = self.vLines[0]

        # optimized start with math
        gapX = self.vLines[1] - self.vLines[0]
        startx = self.vLines[0]
        closeX = (mx - startx) // gapX

        gapY = self.hLines[1] - self.hLines[0]
        startY = self.hLines[0]

        closeY = (my - startY) // gapY

        return closeX, closeY

    def drawGrid(self):
        gray = Colors.GRAY
        vy_start = self.hLines[0]
        vy_stop = self.hLines[-1]

        for x in self.vLines:
            start = x, vy_start
            stop = x, vy_stop
            pygame.draw.line(self.screen, gray, start, stop)

        hy_start = self.vLines[0]
        hy_stop = self.vLines[-1]
        for y in self.hLines:
            start = hy_start, y
            stop = hy_stop, y
            pygame.draw.line(self.screen, gray, start, stop)

    def color_grid(self):
        boxes = []

        # Following scheme
        for i, line in enumerate(self.grid):
            for j, square in enumerate(line):
                # print(i,j)
                square = self.grid[i][j]
                # i,j is y ,x
                x0 = self.vLines[j]
                x1 = self.vLines[j + 1]
                y0 = self.hLines[i]
                y1 = self.hLines[i + 1]
                w = x1 - x0
                h = y1 - y0
                center = (x1 + x0) // 2, (y1 + y0) // 2

                box = [x0, y0, w, h]

                if square == 'O':
                    pass

                # Wall
                elif square == 'W':
                    pygame.draw.rect(self.screen, Colors.BLUE, box, border_radius=5)

                # Token
                elif square == 'T':
                    # shrink box
                    xsf = (x1 - x0) // 11
                    ysf = (y1 - y0) // 15
                    x0 = x0 + xsf * 5
                    x1 = x0 + xsf * 6
                    y0 = y0 + ysf * 7
                    y1 = y0 + ysf * 8
                    w = x1 - x0
                    h = y1 - y0
                    box = [x0, y0, w, h]
                    # radius = w//2
                    # center = ((x0 + x1) // 2, (y0 + y1) //2)

                    # pygame.draw.circle(self.screen,Colors.YELLOW,center,radius)
                    pygame.draw.rect(self.screen, Colors.YELLOW, box)

                # Powerup
                elif square == 'P':
                    radius = ((x1 - x0) // 2) - 5
                    pygame.draw.circle(self.screen,Colors.ORANGE,center,radius)

                # Character
                elif square == 'C':
                    radius = (x1 - x0) // 2
                    self.player_start = center
                    pygame.draw.circle(self.screen,Colors.YELLOW,center,radius)

                # Enemy
                elif square == 'E':
                    radius = (x1 - x0) // 2
                    pygame.draw.circle(self.screen, Colors.RED, center, radius)

    def get_starts(self):
        pass

    def autofill(self):
        # Walls
        for i in range(len(self.grid)):
            row = self.grid[i]
            for j in range(len(row)):
                if i == 0 or i == len(self.grid) - 1 or j == 0 or j == len(row) - 1:
                    self.grid[i][j] = 'W'

                if self.grid[i][j] == 'O':
                    self.grid[i][j] = 'T'

    def key_actions(self, pressed):
        mode = 'O'

        # Tokens
        if pressed[pygame.K_t]:
            mode = 'T'

        # Power ups
        if pressed[pygame.K_p]:
            mode = 'P'

        # Open Area
        if pressed[pygame.K_o]:
            mode = 'O'

        # Walls
        if pygame.key.get_pressed()[pygame.K_w]:
            mode = 'W'

        # Player-Character
        if pygame.key.get_pressed()[pygame.K_c]:
            mode = 'C'

        # Enemy
        if pygame.key.get_pressed()[pygame.K_e]:
            mode = 'E'

        # Save game
        if pygame.key.get_pressed()[pygame.K_s]:
            self.save_map()

        # Load Map
        if pygame.key.get_pressed()[pygame.K_l]:
            self.load_map()

        # Auto fill for walls and tokens
        if pygame.key.get_pressed()[pygame.K_a]:
            self.autofill()

        return mode

    def maker(self):
        mode = 'O'
        while True:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    mousePosX, mousePosY = pygame.mouse.get_pos()
                    gridPosX, gridPosY = self.find_grid(mousePosX, mousePosY)

                    print(gridPosY, gridPosX)
                    print(len(self.grid), len(self.grid[0]))
                    self.grid[gridPosY][gridPosX] = mode

                if event.type == pygame.KEYDOWN:
                    # key = pygame.key.get_pressed()
                    pressed = pygame.key.get_pressed()
                    mode = self.key_actions(pressed)

            self.drawGrid()
            self.color_grid()

            pygame.display.flip()
            self.screen.fill(Colors.BLACK)

    def save_map(self):
        file_name = 'map.txt'
        fw = open(file_name, 'w')

        gridmap = ''
        for i in self.grid:
            for j in i:
                gridmap += j + ' '
            gridmap += '\n'

        gridmap = gridmap[:-2]
        fw.write(gridmap)
        fw.close()

    def load_map(self):
        file_name = 'map.txt'
        fw = open(file_name, 'r')
        s = fw.readlines()
        grid = []
        for l in s:
            new = l.strip().replace('\n', '').split(' ')
            grid.append(new)
        self.grid = grid

        self.squaresY = len(grid)
        self.squaresX = len(grid[0])
        self.gridlines()


if __name__ == '__main__':
    # Official map = 28 X 30
    mapMaker = BetterMaps()
    mapMaker.make_grid((27, 15))
    mapMaker.maker()
