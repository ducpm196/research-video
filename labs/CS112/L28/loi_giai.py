import math
import sys

sys.setrecursionlimit(10000)


def lam_t(he_thuc):
    nho = {1: 1}

    def t(n):
        if n not in nho:
            nho[n] = he_thuc(t, n)
        return nho[n]
    return t


A = lam_t(lambda t, n: 3 * t(n // 2) + n)
B = lam_t(lambda t, n: 2 * t(n // 2) + n * n)
C = lam_t(lambda t, n: t(n // 2) + 1)
chuan = {"A": lambda n: n ** math.log2(3), "B": lambda n: n ** 2, "C": lambda n: math.log2(n)}
for ten, t in (("A", A), ("B", B), ("C", C)):
    n1, n2 = 1024, 1048576
    print(f"{ten}: T(1024) = {t(n1)}, T(1048576) = {t(n2)}, ti so: {t(n1) / chuan[ten](n1):.3f}, {t(n2) / chuan[ten](n2):.3f}")

menh = (1, 6, 10)
so = 12
n_tl, con = 0, so
for c in sorted(menh, reverse=True):
    n_tl += con // c
    con %= c
dp = [0] * (so + 1)
for a in range(1, so + 1):
    dp[a] = 1 + min(dp[a - c] for c in menh if c <= a)
print(f"Doi 12 voi 1, 6, 10: tham lam {n_tl} dong, quy hoach dong {dp[so]} dong")
