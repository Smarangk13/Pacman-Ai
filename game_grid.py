import sys, pygame
import random
from Constants import Colors
from Constants import Properties
from Player import Player
from Enemies import Enemy
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

        # For externally controlled games
        self.external = False
        self.reward = 0
        self.game_over = False
        self.perfect_games = 0

        self.game_font = pygame.font.SysFont('Terminal', 45)

        self.score = 0

        self.map = GameMap()
        self.map.load_map()
        self.map.drawGrid()
        self.map.color_grid()

        # Position player
        self.pacman_drawing = pygame.image.load('pics/pacman.png')
        self.player_pos = self.map.player_start
        self.pacman.x = self.player_pos[0]
        self.pacman.y = self.player_pos[1]

        # Make Pacman spot on map an Open
        player_X = self.player_pos[0]
        player_Y = self.player_pos[1]
        player_grid_X, player_grid_Y = self.map.find_grid(player_X, player_Y)
        self.map.grid[player_grid_Y][player_grid_X] = 'O'


        # Enemies
        self.enemies = []
        self.create_enemies()
        self.num_caught = 0

        # Enemy images
        self.blinky = pygame.image.load('pics/blinky.png')
        self.inky = pygame.image.load('pics/inky.png')
        self.pinky = pygame.image.load('pics/pinky.png')
        self.clyde = pygame.image.load('pics/clyde.png')

        self.scared = pygame.image.load('pics/scared.png')
        self.caught = pygame.image.load('pics/caught.png')

        # time related
        self.start_time = pygame.time.get_ticks()
        self.round_time = self.start_time
        self.caught_mode_time = 0

    def restart(self):
        self.score = 0
        self.reward = 0

        self.map = GameMap()
        self.map.load_map()
        self.map.drawGrid()
        self.map.color_grid()

        self.pacman.lives = 3

        self.player_pos = self.map.player_start
        self.pacman.x = self.player_pos[0]
        self.pacman.y = self.player_pos[1]

        # Make Pacman spot on map an Open
        player_X = self.player_pos[0]
        player_Y = self.player_pos[1]
        player_grid_X, player_grid_Y = self.map.find_grid(player_X, player_Y)
        self.map.grid[player_grid_Y][player_grid_X] = 'O'

        self.enemies = []
        self.create_enemies()

        self.start_time = pygame.time.get_ticks()
        self.round_time = self.start_time
        self.caught_mode_time = 0

        self.game_over = False

    def create_enemies(self):
        while True:
            none_count = 0
            location_B = self.map.find_item('E')
            location_I = self.map.find_item('1')
            location_P = self.map.find_item('2')
            location_C = self.map.find_item('3')

            if location_B is not None:
                enemy = Enemy(Properties.REDGHOST)
                self.add_enemies(enemy, location_B)

            else:
                none_count+=1

            if location_I is not None:
                enemy = Enemy(Properties.BLUEGHOST)
                self.add_enemies(enemy, location_I)
            else:
                none_count+=1

            if location_P is not None:
                enemy = Enemy(Properties.PINKGHOST)
                self.add_enemies(enemy, location_P)
            else:
                none_count+=1

            if location_C is not None:
                enemy = Enemy(Properties.ORANGEGHOST)
                self.add_enemies(enemy, location_C)
            else:
                none_count+=1

            if none_count == 4:
                return

    def add_enemies(self, enemy, location):
        row = location[0]
        col = location[1]
        enemy.start_pos = row, col
        self.map.grid[row][col] = 'O'
        enemy.x, enemy.y = self.map.find_coordinates(row, col)
        self.enemies.append(enemy)

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

        if key[pygame.K_r]:
            self.restart()

    def allTokens(self):
        if self.map.find_item('T') is None:
            self.reward += 100000
            self.perfect_games += 1
            return True
        return False

    # Enemies can not warp
    def warp(self):
        # First check out of bounds
        # max_x = Properties.WINDOWWIDTH
        # max_y = Properties.WINDOWHEIGHT

        max_x = self.map.vLines[-2]
        max_y = self.map.hLines[-2]

        if self.pacman.x > max_x:
            self.pacman.x = 0

        if self.pacman.x < 0:
            self.pacman.x = max_x

        if self.pacman.y > max_y:
            self.pacman.y = 0

        if self.pacman.y < 0:
            self.pacman.y = max_y

        for enemy in self.enemies:
            if enemy.x < 1:
                enemy.x = 1
            elif enemy.x > max_x:
                enemy.x = max_x

            if enemy.y < 1:
                enemy.y = 1
            elif enemy.y > max_y:
                enemy.y = max_y

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

        elif next_row < 0:
            next_row = 0

        if next_col >= len(self.map.grid[0]):
            next_col -= 1

        elif next_col < 0:
            next_col = 0

        return self.map.grid[next_row][next_col]

    # Check collisions with walls for current path and turns
    def collisions(self, character):
        # Teleport if at edge
        self.warp()
        player_X = character.x
        player_Y = character.y

        col, row = self.map.find_grid(player_X, player_Y)
        direction = character.direction

        # If next tile is a wall stop
        next_tile = self.get_next(row, col, direction)
        gate_player = character.name == 'Player' and next_tile == 'G'
        if next_tile == 'W' or gate_player:
            character.stop_movement()
            pass
        else:
            character.start_movement()

        # For turns
        next_tile = self.get_next(row, col, character.next_turn)
        if next_tile != 'W' and not gate_player:
            character.makeTurn()

        # # If stuck in wall
        # if self.map.grid[row][col] == 'W':
        #     open_row = row
        #     open_col = col
        #     # Check neighbors and place
        #     if self.map.grid[row + 1][col] == 'O':
        #         open_row = row+1
        #
        #     elif self.map.grid[row - 1][col] == 'O':
        #         open_row = row-1
        #
        #     elif self.map.grid[row][col + 1] == 'O':
        #         open_col = col + 1
        #
        #     elif self.map.grid[row][col - 1] == 'O':
        #         open_col = col - 1
        #
        #     character.x, character.y = self.map.find_coordinates(open_row, open_col)
    # Remove tokens and update score
    def update_map(self):
        player_X = self.pacman.x
        player_Y = self.pacman.y
        col, row = self.map.find_grid(player_X, player_Y)
        try:
            current_tile = self.map.grid[row][col]
        except:
            print(row, col)
            return

        if current_tile == 'T':
            self.map.grid[row][col] = 'O'
            self.score += Properties.TOKEN_SCORE

        elif current_tile == 'P':
            self.map.grid[row][col] = 'O'
            self.score += 100
            self.caught_mode_time = pygame.time.get_ticks()
            for enemy in self.enemies:
                enemy.mode = 'Run'

    def drawEnemies(self):
        offset = 3
        for enemy in self.enemies:
            mode = enemy.mode
            if mode == 'Chase':
                if enemy.name == Properties.REDGHOST:
                    self.screen.blit(self.blinky, (enemy.x, enemy.y - offset))
                    # pygame.draw.rect(self.screen,Colors.RED,[enemy.x,enemy.y,15,15])

                elif enemy.name == Properties.BLUEGHOST:
                    self.screen.blit(self.inky, (enemy.x, enemy.y - offset))

                elif enemy.name == Properties.PINKGHOST:
                    self.screen.blit(self.pinky, (enemy.x, enemy.y - offset))

                elif enemy.name == Properties.ORANGEGHOST:
                    self.screen.blit(self.clyde, (enemy.x, enemy.y - offset))

            elif mode == 'Run':
                self.screen.blit(self.scared, (enemy.x, enemy.y - offset))

            else:
                self.screen.blit(self.caught, (enemy.x, enemy.y - offset))

    def moveEnemies(self):
        for enemy in self.enemies:
            if enemy.mode == 'Chase':
                self.chase_player(enemy)

            elif enemy.mode == 'Run':
                self.run_from_player(enemy)

            else:
                self.enemy_home(enemy)

    # Get enemeis to chase pacman but wiat until they are awake
    def chase_player(self, enemy):
        time_passed = pygame.time.get_ticks() - self.round_time

        target = self.map.find_grid(self.pacman.x, self.pacman.y)
        target = target[1], target[0]

        wait_time = enemy.sleeptime * 1000
        if time_passed < wait_time:
            enemy.stop_movement()
            enemy.sleeping = True
        else:
            enemy.start_movement()
            enemy.sleeping = False
            start = self.map.find_grid(enemy.x, enemy.y)
            start = start[1], start[0]
            # Reached pacman
            if target == start:
                self.pacman.lives -= 1
                self.reset()

            enemy.chase(self.map.grid, target, start)
            enemy.move()
            self.collisions(enemy)

    def run_from_player(self, enemy):
        passed_time = pygame.time.get_ticks() - self.caught_mode_time
        if passed_time > Properties.GHOST_SCARED_TIME * 1000:
            enemy.mode = 'Chase'
            self.num_caught = 0

        if enemy.sleeping:
            return

        target = self.map.find_grid(self.pacman.x, self.pacman.y)
        target = target[1], target[0]

        enemy.start_movement()
        start = self.map.find_grid(enemy.x, enemy.y)
        start = start[1], start[0]

        # If reached pacman
        if target == start:
            enemy.mode = 'Caught'
            self.score += 200 * self.num_caught

        enemy.chase(self.map.grid, target, start)
        enemy.move()
        self.collisions(enemy)

    def enemy_home(self, enemy):
        target =enemy.start_pos[0], enemy.start_pos[1]
        start = self.map.find_grid(enemy.x, enemy.y)
        start = start[1], start[0]
        # Reached home
        if target == start:
            enemy.mode = 'Chase'

        enemy.chase(self.map.grid, target, start)
        enemy.move()
        self.collisions(enemy)

    def drawObjects(self):
        # Draw Objects
        # Draw player
        player_X = self.pacman.x
        player_Y = self.pacman.y
        pos = [player_X, player_Y]
        pygame.draw.circle(self.screen, Colors.YELLOW, pos, Player.radius)

        # Draw map

        # self.map.drawGrid()
        self.map.color_grid()

        self.drawEnemies()

    def show_HUD(self):
        score_val = '0' * (6 - len(str(self.score))) + str(self.score)
        score_display = self.game_font.render(score_val, False, Colors.WHITE)
        score_text = self.game_font.render('SCORE', False, Colors.WHITE)
        lives_count = self.game_font.render('Lives:', False, Colors.WHITE)
        self.screen.blit(score_display, Properties.SCORE_NUMS)
        self.screen.blit(score_text, Properties.SCORE_TEXT)
        self.screen.blit(lives_count, Properties.LIVES_TEXT)

        lives_x = Properties.LIVES_START
        for i in range(self.pacman.lives):
            self.screen.blit(self.pacman_drawing, [lives_x, Properties.LIVES_LEVEL])
            lives_x += Properties.LIVES_GAP

    def reset(self):
        time = pygame.time.get_ticks()
        wait_time = time + 4000  # 4 seconds
        while True:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.pacman.stop_movement()
            self.pacman.x = self.player_pos[0]
            self.pacman.y = self.player_pos[1]

            for enemy in self.enemies:
                enemy.stop_movement()
                enemy.x, enemy.y = self.map.find_coordinates(enemy.start_pos[0], enemy.start_pos[1])

            self.drawObjects()
            self.show_HUD()

            time = pygame.time.get_ticks()
            self.round_time = time
            if self.external:
                self.reward -= 100000/(self.score + 1)
                return
            if time > wait_time:
                self.gameLoop()

            pygame.display.flip()
            self.screen.fill(Colors.BLACK)

    def gameLoop(self):
        while True:
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
                    self.target = gridPosY, gridPosX

            self.drawObjects()
            self.show_HUD()
            self.pacman.move()
            self.moveEnemies()
            self.collisions(self.pacman)
            self.update_map()

            pygame.display.flip()
            self.screen.fill(Colors.BLACK)

    def game_step(self, agent_event, draw = False):
        self.external = True
        if agent_event[0]:
            self.pacman.next_turn = 'Up'

        elif agent_event[1]:
            self.pacman.next_turn = 'Down'

        elif agent_event[2]:
            self.pacman.next_turn = 'Left'

        else:
            self.pacman.next_turn = 'Right'

        if draw:
            self.drawObjects()
            self.show_HUD()

        self.reward = self.score - (pygame.time.get_ticks()//4000)

        self.pacman.move()
        self.moveEnemies()
        self.collisions(self.pacman)
        self.update_map()

        # current_time = pygame.time.get_ticks()
        # if current_time - self.round_time > 90 * 1000:
        #     self.pacman.lives -= 1
        #     self.reset()

        if self.pacman.lives <= 0 or self.allTokens():
            self.game_over = True

        pygame.display.flip()
        self.screen.fill(Colors.BLACK)


if __name__ == '__main__':
    game = GamePlay()
    game.gameLoop()
