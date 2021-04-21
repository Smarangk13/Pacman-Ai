from Constants import Colors

class Rectangle:
    def __init__(self, x, y, w, h, color = Colors.BLUE):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

    def get_dims(self):
        return [self.x, self.y, self.w, self.h]

    @staticmethod
    def collision(box, obstacle):
        boxX = box.x
        boxY = box.y
        boxW = box.w
        boxH = box.h
        boxR = boxX + boxW
        boxB = boxY + boxH

        obstacleX = obstacle.x
        obstacleY = obstacle.y
        obstacleW = obstacle.w
        obstacleH = obstacle.h
        obstacleR = obstacleX + obstacleW
        obstacleB = obstacleY + obstacleH

        if boxB > obstacleY and boxY < obstacleB:
            if boxR > obstacleX and boxX < obstacleR:
                return True

        return False

class Circle:
    def __init__(self, x, y, r, color = Colors.YELLOW):
        self.x = x
        self.y = y
        self.radius = r
        self.color = color

    def toBox(self):
        l = self.x - self.radius
        t = self.y - self.radius
        diameter = 2 * self.radius

        box = Rectangle(l,t,diameter,diameter)

        return box

    def get_pos(self):
        return [self.x, self.y]