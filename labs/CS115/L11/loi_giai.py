from fractions import Fraction

A = [[4, 1], [1, 3]]
b = [1, 2]


def gradient(w):
    return [A[0][0] * w[0] + A[0][1] * w[1] - b[0], A[1][0] * w[0] + A[1][1] * w[1] - b[1]]


a, c = A[0][0], A[1][1]
dt = a * c - A[0][1] * A[1][0]
print("ham loi:", a > 0 and dt > 0)
w = [Fraction(0), Fraction(0)]
g = gradient(w)
p = [Fraction(c * g[0] - A[0][1] * g[1], dt), Fraction(-A[1][0] * g[0] + a * g[1], dt)]
wn = [w[0] - p[0], w[1] - p[1]]
print(f"Newton 1 buoc: w = [{wn[0]}, {wn[1]}]")
print("gradient sau Newton:", [int(t) for t in gradient(wn)])
w = [0.0, 0.0]
for _ in range(3):
    g = gradient(w)
    w = [w[0] - 0.2 * g[0], w[1] - 0.2 * g[1]]
print("GD eta=0.2 sau 3 buoc:", [round(t, 4) for t in w])
print("gradient sau GD:", [round(t, 4) for t in gradient(w)])
