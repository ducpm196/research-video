from fractions import Fraction

x = [0, 1, 2, 3]
y = [1, 2, 4, 5]
X = [[1, t] for t in x]
XtX = [[sum(X[k][i] * X[k][j] for k in range(4)) for j in range(2)] for i in range(2)]
Xty = [sum(X[k][i] * y[k] for k in range(4)) for i in range(2)]


def chuoi(v):
    if isinstance(v[0], list):
        return "[" + ", ".join(chuoi(r) for r in v) + "]"
    return "[" + ", ".join(str(t) for t in v) + "]"


print("X^T X:", chuoi(XtX))
print("X^T y:", chuoi(Xty))
dt = XtX[0][0] * XtX[1][1] - XtX[0][1] * XtX[1][0]
print("dinh thuc:", dt)
inv = [[Fraction(XtX[1][1], dt), Fraction(-XtX[0][1], dt)], [Fraction(-XtX[1][0], dt), Fraction(XtX[0][0], dt)]]
w = [inv[0][0] * Xty[0] + inv[0][1] * Xty[1], inv[1][0] * Xty[0] + inv[1][1] * Xty[1]]
print("w:", chuoi(w))
du_doan = [w[0] + w[1] * t for t in x]
print("du doan:", chuoi(du_doan))
print("MSE:", sum((p - q) ** 2 for p, q in zip(du_doan, y)) / 4)
r = [p - q for p, q in zip(du_doan, y)]
print("X^T (Xw - y):", "[" + ", ".join(str(int(sum(X[k][i] * r[k] for k in range(4)))) for i in range(2)) + "]")
