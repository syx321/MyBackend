from numpy import np


def test():
    board = np.zeros((6, 6), dtype=int)


def showBoard():
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
        print()