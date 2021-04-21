from Shapes import Circle
from Constants import Properties

class Player(Circle):
    playerSpeed = Properties.PLAYERSPEED
    radius = Properties.CHARACTERRADIUS
    lives = 3

    def __init__(self, x=400, y=450, r=15):
        super().__init__(x, y, r)
        self.next_turn = None

    # moveRight = True
    # moveLeft = False
    # moveUp = False
    # moveDown = False

    movement_direction = [True, False, False, False] # Old
    direction = 'Right'


    def __no_movement(self):
        self.movement_direction = [False for i in range(4)]

    def get_direction(self):
        return self.movement_direction.index(True)

    def get_direction_str(self):
        return self.direction

    def turnRight(self):
        self.__no_movement()
        self.movement_direction[0] = True
        self.direction = 'Right'

    def turnLeft(self):
        self.__no_movement()
        self.movement_direction[1] = True
        self.direction = 'Left'

    def turnUp(self):
        self.__no_movement()
        self.movement_direction[2] = True
        self.direction = 'Up'

    def turnDown(self):
        self.__no_movement()
        self.movement_direction[3] = True
        self.direction = 'Down'

    def stop_movement(self):
        self.playerSpeed = 0

    def start_movement(self):
        self.playerSpeed = Properties.PLAYERSPEED

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