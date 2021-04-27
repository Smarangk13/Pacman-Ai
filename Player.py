from Shapes import Circle
from Constants import Properties


class Player:
    speed = Properties.PLAYERSPEED
    movement_speed = speed
    radius = Properties.CHARACTERRADIUS
    lives = 3
    x = 0
    y = 0
    name = 'Player'

    def __init__(self):
        self.next_turn = None

    direction = 'Right'

    def turnRight(self):
        self.direction = 'Right'

    def turnLeft(self):
        self.direction = 'Left'

    def turnUp(self):
        self.direction = 'Up'

    def turnDown(self):
        self.direction = 'Down'

    def stop_movement(self):
        self.speed = 0

    def start_movement(self):
        self.speed = self.movement_speed

    def move(self):
        direction = self.direction

        if direction == 'Right':
            self.x += self.speed

        elif direction == 'Left':
            self.x -= self.speed

        elif direction == 'Up':
            self.y -= self.speed

        elif direction == 'Down':
            self.y += self.speed

    def makeTurn(self):
        if self.next_turn == 'Right':
            self.turnRight()

        elif self.next_turn == 'Left':
            self.turnLeft()

        elif self.next_turn == 'Up':
            self.turnUp()

        elif self.next_turn == 'Down':
            self.turnDown()

        self.next_turn = None
