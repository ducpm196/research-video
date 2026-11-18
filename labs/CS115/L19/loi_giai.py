from fractions import Fraction

X = [[1, 1], [2, 2], [3, 3]]
y = [2, 4, 6]
A = [[sum(r[i] * r[j] for r in X) for j in range(2)] for i in range(2)]
b = [sum(r[i] * t for r, t in zip(X, y)) for i in range(2)]
print("dinh thuc X^T X:", A[0][0] * A[1][1] - A[0][1] * A[1][0])


def giai(lam):
    lam = Fraction(lam)
    M = [[A[0][0] + lam, A[0][1]], [A[1][0], A[1][1] + lam]]
    dt = M[0][0] * M[1][1] - M[0][1] * M[1][0]
    w = [(M[1][1] * b[0] - M[0][1] * b[1]) / dt, (-M[1][0] * b[0] + M[0][0] * b[1]) / dt]
    return dt, w


dt, w = giai(1)
print("dinh thuc X^T X + 1*I:", dt)
print("w (lambda=1):", "[" + ", ".join(str(t) for t in w) + "]")
dt, w = giai(Fraction(1, 10))
print("w (lambda=1/10):", "[" + ", ".join(str(t) for t in w) + "]")


def l1(a, lam=2):
    a = Fraction(a)
    if abs(a) <= Fraction(lam, 2):
        return Fraction(0)
    return a - Fraction(lam, 2) if a > 0 else a + Fraction(lam, 2)


print(f"L1 lambda=2: a=3 -> {l1(3)}, a=1/2 -> {l1(Fraction(1, 2))}, a=-2 -> {l1(-2)}")
n, k = 12, 4
print(f"kiem dinh cheo {k} phan, {n} mau: moi luot huan luyen {n - n // k}, kiem dinh {n // k}")
