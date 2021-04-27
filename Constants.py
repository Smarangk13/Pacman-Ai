class Colors:
    BLACK = (0, 0, 0)
    RED = (250, 0, 0)
    BLUE = (0, 0, 200)
    BROWN = (66, 22, 14)
    ORANGE = (220,150,0)
    PINK = (255,0,255)
    GRAY = (120, 120, 120)
    YELLOW = (255,255,0)
    LIGHTBLUE = (120, 120, 210)
    DARKBLUE = (40, 40, 170)
    WHITE = (255,255,255)


class Properties:
    # Game Window
    WINDOWWIDTH = 600
    WINDOWHEIGHT = 800

    WINDOWBUFFERH = 40
    WINDOWBUFFERTOP = 70
    WINDOWBUFFERBOTTOM = 20

    SCORE_TEXT = [0,0]
    SCORE_NUMS = [250,0]
    LIVES_LEVEL = WINDOWHEIGHT - WINDOWBUFFERBOTTOM - 10
    LIVES_TEXT = [10, LIVES_LEVEL]
    LIVES_START = 120
    LIVES_GAP = 30
    # Keymap
    LEFTARROW = 80
    UPARROW = 82
    RIGHTARROW = 79
    DOWNARROW = 81

    # Characters
    CHARACTERRADIUS = 12
    PLAYERSPEED = 10
    ENEMYSPEED = 4
    GHOST_SCARED_SPEED = 2
    GHOST_SCARED_TIME = 12
    GHOST_CAUGHT_SPEED = 10

    # Game Map related
    WALLGAP = CHARACTERRADIUS * 3
    ORBGAP = int(WALLGAP/2)
    ORBSPACING = CHARACTERRADIUS
    ORBSIZE = int(CHARACTERRADIUS/5)
    POWERUPSIZE = int(CHARACTERRADIUS/2)

    TOKEN_SCORE = 135

    # Derived Properties
    def map_resize(self, X_Space,Y_Space):
        diameter = Y_Space - 1
        if X_Space < Y_Space:
            diameter = X_Space - 1
        # Characters
        self.CHARACTERRADIUS = diameter

        # Game Map related
        self.WALLGAP = self.CHARACTERRADIUS * 3
        self.ORBSIZE = int(self.CHARACTERRADIUS / 5)
        self.POWERUPSIZE = int(self.CHARACTERRADIUS / 2)
