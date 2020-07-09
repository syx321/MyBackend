num = 5


def Calsulate(n):
    if n > 0:
        return n + Calsulate(n - 1)
    else:
        return 0


print(Calsulate(num))
