import math
def f(x, y, z):
    return g(g(x, y), z)

def f_inv(n):
    w, z = g_inv(n)
    x, y = g_inv(w)
    return (x, y, z)
def g(x, y):
    return (x + y) * (x + y + 1) / 2 + y
def g_inv(n):
    m = math.floor(math.sqrt(2 * n))
    while True:
        y = n - m * (m + 1) / 2
        if y >= 0:
            break
        m -= 1
    x = m - y
    return [int(x)+1,int(y)+1]