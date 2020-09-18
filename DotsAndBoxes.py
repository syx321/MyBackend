import numpy as np

'''
-1为点
1为先手A
2为后手B
3为A占领部分
4为B占领部分
每个坐标表示横杠的位置

 →y
↓
x
'''


class DotAndBoxes(object):
    def __init__(self):
        #         0   1   2  3   4  5  6   7   8  9  10
        board = [[-1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1],  # 0
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 1
                 [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1],  # 2
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 3
                 [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1],  # 4
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 5
                 [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1],  # 6
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 7
                 [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1],  # 8
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 9
                 [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1]]  # 10
        self.__globalBoard = board
        self.playerState = {'A': [],
                            'B': [],
                            }  # 为了快速查询占领的位置
        Used = []

    # 得到棋盘状况
    def getBoard(self):
        return self.__globalBoard

    def rollback(self, board):
        self.__globalBoard = board

    def fire(self, player, loc):
        reshape = self.__globalBoard

        if not self.isAvailable(loc): raise RuntimeError

        if player == 'A':
            self.__globalBoard[loc[0]][loc[1]] = 1
        elif player == 'B':
            self.__globalBoard[loc[0]][loc[1]] = 2

        playerResult = self.gameStatus(player, loc)

        return reshape, playerResult

    # 可下位置
    def enableMove(self):
        enableloc = []
        for x in range(len(self.__globalBoard)):
            for y in range(len(self.__globalBoard[x])):
                if self.__globalBoard[x][y] == 0 and x % 2 == 0:
                    enableloc.append([x, y])
                elif self.__globalBoard[x][y] == 0 and (y == 0 or y % 2 == 0):
                    enableloc.append([x, y])
        return enableloc

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
        elif loc[0] > 10 or loc[1] > 10:
            return True
        else:
            return False

    def gameStatus(self, player, loc):
        self.territory(player, loc)
        if len(self.enableMove()) == 0:
            if len(self.playerState['A']) > len(self.playerState['B']):
                return 'A'
            else:
                return 'B'
        else:
            return None

    # 遍历连线，如果组成回路则成闭环
    def territory(self, player, loc):
        vector = [(1, 0), (0, -1), (-1, 0), (0, 1)]

        # 找到当前放置线的节点
        if loc[0] % 2 == 0:
            point = [loc[0], loc[1] - 1]
        else:
            point = [loc[0] - 1, loc[1]]

            def check(i: int, j: int) -> bool:
                if i == point[0] and j == point[1]:
                    return True

                visited.add((i, j))
                result = False
                for di, dj in vector:
                    newi, newj = i + di, j + dj
                    if 0 <= newi < 10 and 0 <= newj < 10:
                        if (newi, newj) not in visited:
                            if check(newi, newj):
                                result = True
                                break

                visited.remove((i, j))
                return result

        visited = set()
        for x in range(10):
            for y in range(10):
                if check(x, y):
                    return True
        return False

    def setBoard(self, baord):
        self.__globalBoard = baord

    # 打印现在的棋盘
    def showBoard(self):
        for x in self.__globalBoard:
            for y in x:
                print('\t', y, end='')
            print()


if __name__ == '__main__':
    test = DotAndBoxes()
    test.showBoard()
    loc = test.enableMove()
    print(loc)
