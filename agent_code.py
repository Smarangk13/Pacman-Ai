from game import GamePlay

class Agent:
    def __init__(self):
        self.GameObject = GamePlay()

    def calculateOutput(self):
        pass


    def controller(self):
        self.GameObject.updateData()
        keys = self.calculateOutput()
        self.GameObject.Control(keys)