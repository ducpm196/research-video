import math
import itertools
from fractions import Fraction as F

from reg import lab, quymo  # noqa


@lab("L05")
def _():
    A, B = {2, 3, 5, 7, 11, 13}, {1, 3, 5, 7, 9, 11}
    U = sorted(A | B)
    fmt = lambda xs: " ".join(map(str, xs))
    out = ["hop: " + fmt(U),
           "giao: " + fmt([x for x in U if x in A and x in B]),
           "A bo B: " + fmt([x for x in U if x in A and x not in B]),
           "B bo A: " + fmt([x for x in U if x in B and x not in A])]
    subs = sum(1 for r in range(len(A) + 1) for _ in itertools.combinations(sorted(A), r))   # liệt kê thật mọi tập con
    out.append(f"so tap con cua A: {subs}")
    N = 1000
    brute = len({x for x in range(4, N + 1, 4)} | {x for x in range(6, N + 1, 6)})   # hợp hai tập bội
    out.append(f"chia het cho 4 hoac 6, tu 1 den 1000: dem={brute} congthuc={len(range(4, N + 1, 4)) + len(range(6, N + 1, 6)) - len(range(12, N + 1, 12))}")
    return out


@quymo("L05")
def _():
    f = lambda n: len(set(range(2, n + 1, 2)) | set(range(3, n + 1, 3)))
    g = lambda n: n // 2 + n // 3 - n // 6
    return [("67 (n=100)", f(100) == g(100) == 67), ("666667 (n=10^6)", f(10 ** 6) == g(10 ** 6) == 666667),
            ("666666666667 (n=10^12)", g(10 ** 12) == 666666666667), ("17 phút / 11,6 ngày", round(10 ** 12 / 1e9 / 60) == 17 and round(10 ** 15 / 1e9 / 86400, 1) == 11.6)]
