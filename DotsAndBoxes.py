import numpy as np

'''
1为先手A
2为后手B
每个坐标表示横杠的位置

 →y
↓
x
'''


class DotAndBoxes:
    def __init__(self, h, w):
        self.playerState = []
        self.__globalBoard = []

    # 得到棋盘状况
    def getBoard(self):
        return self.__globalBoard

    def rollback(self, board):
        self.__globalBoard = board

    def getPlayerLocation(self, player):
        return self.playerState[player] + self.playerState[player + '_k']

    def fire(self):
        pass

    # 可移动位置
    def enableMove(self):
        pass

    # 查看此位置是否可以下棋，调用isOutOfBound
    def isAvailable(self, loc):
        if self.isOutOfBound(loc):  # 判断是否越界
            return False
        elif self.__globalBoard[loc] != 0:  # 判断位置是否为空
            return False
        else:
            return True

    # 判断是否出界
    def isOutOfBound(self, loc):
        if loc[0] < 0 or loc[1] < 0:
            return True
        elif loc[0] > 6 or loc[1] > 6:
            return True
        else:
            return False

    # 判断胜负,需要调用enabledLocation判断是否还有可走的位置;
    def gameStatus(self):
        pass

    def setBoard(self, baord):
        self.__globalBoard = baord

    # 打印现在的棋盘
    def showBoard(self):
        print('   ', end='')
        for i in range(1, 7):
            print(i, end=' ')
        print()

        print('   ', end='')
        for i in range(6):
            print('-', end=' ')
        print()

        for i in range(6):
            if i == 0:
                print(' 1', end='|')
            elif i != 5:
                print(' ' + str(i + 1), end='|')
            else:
                print(' 6', end='|')
            # for j in range(6):
            #     print(self.__globalBoard[i, j], end=' ')
            print()


if __name__ == '__main__':
    test = DotAndBoxes(6, 6)
    test.showBoard()
