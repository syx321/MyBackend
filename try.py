def f(n):
    a = 0
    b = 1
    for i in range(n):
        yield a
        a, b = b, a + b


if __name__ == '__main__':
    for n, i in enumerate(f(10000)):
        print( n, ':', i)