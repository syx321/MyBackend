import numpy as np

# board基类


class Board(object):
    def __init__(self):
        self.__globalBoard = np.zeros([10, 10], dtype=int)

    def getBoard(self):
        pass

    def fire(self, player, location, itemtype):
        pass

    def history(self):
        pass

    def imports(self, history):
        pass
