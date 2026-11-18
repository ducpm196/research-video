import math


def f(x, y):
    return x**2 + 16 * y**2


def grad(x, y):
    return 2 * x, 32 * y


def chay(ten, buoc):
    x, y = 1.0, 1.0
    G = [0.0, 0.0]
    for _ in range(3):
        g = grad(x, y)
        x, y, G = buoc((x, y), g, G)
    print(f"{ten}: x={round(x, 4)} y={round(y, 4)} f={round(f(x, y), 4)}")


def sgd(w, g, G):
    return w[0] - 0.03 * g[0], w[1] - 0.03 * g[1], G


def adagrad(w, g, G):
    G = [G[0] + g[0] ** 2, G[1] + g[1] ** 2]
    return (w[0] - 0.1 * g[0] / (math.sqrt(G[0]) + 1e-8), w[1] - 0.1 * g[1] / (math.sqrt(G[1]) + 1e-8), G)


def rmsprop(w, g, s):
    s = [0.9 * s[0] + 0.1 * g[0] ** 2, 0.9 * s[1] + 0.1 * g[1] ** 2]
    return (w[0] - 0.1 * g[0] / (math.sqrt(s[0]) + 1e-8), w[1] - 0.1 * g[1] / (math.sqrt(s[1]) + 1e-8), s)


chay("SGD", sgd)
chay("Adagrad", adagrad)
chay("RMSprop", rmsprop)
g0 = grad(1.0, 1.0)
print("buoc dau Adagrad moi toa do:", round(0.1 * g0[0] / (math.sqrt(g0[0] ** 2) + 1e-8), 4))
