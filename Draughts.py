import numpy as np

'''
board中
1为先手白字A
2为后手黑字B
3为先手白王琪A_k
4为后手黑王琪B_k
'''

vector1 = [(1, -1), (2, -2)]  # 左下
vector2 = [(1, 1), (2, 2)]  # 右下
vector3 = [(-1, 1), (-2, 2)]  # 右上
vector4 = [(-1, -1), (-2, -2)]  # 左上
vectorall = [vector1, vector2, vector3, vector4]


# blackBlock = []
# # 初始黑格位置
# for i in range(10):
#     for j in range(10):
#         if i % 2 == 0 and j % 2 != 0:
#             blackBlock.append([i, j])
#         elif i % 2 != 0 and j % 2 == 0:
#             blackBlock.append([i, j])


class Draughts(object):
    def __init__(self, h, w):
        board = np.zeros((10, 10), dtype=int)
        # 初始化白子A位置,白子的王用3表示
        # board[0, 1] = board[0, 3] = board[0, 5] = board[0, 7] = board[0, 9] = 1
        # board[1, 0] = board[1, 2] = board[1, 4] = board[1, 6] = board[1, 8] = 1
        # board[2, 1] = board[2, 3] = board[2, 5] = board[2, 7] = board[2, 9] = 1
        # board[3, 0] = board[3, 2] = board[3, 4] = board[3, 6] = board[3, 8] = 1
        # # 初始化黑字B位置，黑字的王用4表示
        # board[6, 1] = board[6, 3] = board[6, 5] = board[6, 7] = board[6, 9] = 2
        # board[7, 0] = board[7, 2] = board[7, 4] = board[7, 6] = board[7, 8] = 2
        # board[8, 1] = board[8, 3] = board[8, 5] = board[8, 7] = board[8, 9] = 2
        # board[9, 0] = board[9, 2] = board[9, 4] = board[9, 6] = board[9, 8] = 2
        board[4, 5] = 1
        board[5, 4] = 2

        self.__globalBoard = board
        self.width = int(w)
        self.heigh = int(h)
        # self.playerState = {'A': [(0, 1), (0, 3), (0, 5), (0, 7), (0, 9),
        #                           (1, 0), (1, 2), (1, 4), (1, 6), (1, 8),
        #                           (2, 1), (2, 3), (2, 5), (2, 7), (2, 9),
        #                           (3, 0), (3, 2), (3, 4), (3, 6), (3, 8)],
        #                     'A_k': [],  # 存储A中王的位置
        #                     'B': [(6, 1), (6, 3), (6, 5), (6, 7), (6, 9),
        #                           (7, 0), (7, 2), (7, 4), (7, 6), (7, 8),
        #                           (8, 1), (8, 3), (8, 5), (8, 7), (8, 9),
        #                           (9, 0), (9, 2), (9, 4), (9, 6), (9, 8)],
        #                     'B_k': []  # 存储B中王的位置
        #                     }  # 为了快速查询得到棋子位置
        self.playerState = {'A': [(4, 5)],
                            'A_k': [],
                            'B': [(5, 4)],
                            'B_k': []
                            }

    # 得到棋盘状况
    def getBoard(self):
        return self.__globalBoard

    def rollback(self, board):
        self.__globalBoard = board

    def getPlayerLocation(self, player):
        return self.playerState[player] + self.playerState[player + '_k']

    # 下棋
    def fire(self, player, location):
        pass

    # 查看是否可以吃子,player需要区分普通和王琪,只返回能吃的子，并不判断吃完后可以到哪
    def move(self, loc, player):
        index = []

        p = []
        if player == 'A' or 'A_k':
            p.extend(['A', 'B'])
        elif player == 'B' or 'B_k':
            p.extend(['B', 'A'])

        if player == p[0]:
            for vector in vectorall:
                if (loc[0] + vector[0][0], loc[1] + vector[0][1]) in self.playerState[p[1]] + self.playerState[
                    p[1] + '_k'] \
                        and self.__globalBoard[loc[0] + vector[1][0], loc[1] + vector[1][1]] == 0:
                    index.append((loc[0] + vector[0][0], loc[1] + vector[0][1]))
            return index

        else:
            vectorK1 = []  # 左上
            vectorK2 = []  # 右上
            vectorK3 = []  # 左下
            vectorK4 = []  # 右下
            vector = [vectorK1, vectorK2, vectorK3, vectorK4]
            minus = loc[0] - loc[1]
            add = loc[0] + loc[1]

            # 初始四个方向上可走的位置
            for i in range(10):
                for j in range(10):
                    if (i - j) == minus and i <= loc[0] and j <= loc[1]:
                        vectorK1.append((i, j))
                    elif (i + j) == add and i <= loc[0] and j >= loc[1]:
                        vectorK2.append((i, j))
                    elif (i + j) == add and i >= loc[0] and j <= loc[1]:
                        vectorK3.append((i, j))
                    elif (i - j) == minus and i >= loc[0] and j >= loc[1]:
                        vectorK4.append((i, j))

            vectorK1.reverse()  # 为了使点由中心向外排列
            vectorK2.reverse()

            if player == p[0] + '_k':
                for v_a in vector:  # 四个方向
                    for v_b in v_a:  # 各方向的点
                        if (v_b[0], v_b[1]) in self.playerState[p[1]] + self.playerState[p[1] + '_k']:  # 是敌方子
                            for i in range(v_a.index(v_b), len(v_a)):  # 历遍此子后的位置
                                if self.isAvailable((v_a[i][0], v_a[i][1])) \
                                        and self.isAvailable((v_a[v_a.index(v_b) + 1][0], v_a[v_a.index(v_b) + 1][1])):
                                    if (v_b[0], v_b[1]) not in index: index.append((v_b[0], v_b[1]))

                return index

    # 此棋所有可下位置,调用isAvailable
    def enabledLocation(self, loc, player):
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
        elif loc[0] > 9 or loc[1] > 9:
            return True
        else:
            return False

    # 判断时候在“王棋位”,由fire调用
    def isKingPosition(self, loc, player):

        if player == 'A' and loc[0] == 9:
            return True
        elif player == 'B' and loc[0] == 0:
            return True
        else:
            return False

    # 判断胜负,需要调用enabledLocation判断是否还有可走的位置;
    def gameStatus(self):
        global index_A
        global index_B
        A = self.playerState['A'] + self.playerState['A_k']
        B = self.playerState['B'] + self.playerState['B_k']
        index_A = False
        index_B = False
        for loc in A:
            if self.isAvailable(loc):
                index_A = True
                break
        for loc in B:
            if self.isAvailable(loc):
                index_B = True
                break
        if len(A) == 0:
            return 'B'
        elif len(B) == 0:
            return 'A'
        elif index_A == False:
            return 'B'
        elif index_B == False:
            return 'A'

    def setBoard(self, baord):
        self.__globalBoard = baord

    # 打印现在的棋盘
    def showBoard(self):
        print('   ', end='')
        for i in range(1, 11):
            print(i, end=' ')
        print()

        print('   ', end='')
        for i in range(10):
            print('-', end=' ')
        print()

        for i in range(10):
            if i == 0:
                print(' 1', end='|')
            elif i != 9:
                print(' ' + str(i + 1), end='|')
            else:
                print('10', end='|')
            for j in range(10):
                print(self.__globalBoard[i, j], end=' ')
            print()


test = Draughts(10, 10)
print(test.move((4, 5), 'A_k'))
