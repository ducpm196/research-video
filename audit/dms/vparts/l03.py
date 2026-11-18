import math
import itertools
from fractions import Fraction as F

import sympy

from reg import lab, quymo  # noqa


@lab("L03")
def _():
    # sympy.factorint (khác phép chia thử của lời giải): n nhỏ nhất làm giá trị hợp số
    fs = [lambda n: n * n + n + 17, lambda n: 2 * n * n + 29, lambda n: n * n - 79 * n + 1601]
    out = []
    for k, f in enumerate(fs, 1):
        n = next(n for n in itertools.count(0) if not sympy.isprime(f(n)))
        v = f(n)
        p = min(sympy.factorint(v))
        out.append(f"{k}: n={n}, {v} = {p} x {v // p}")
    return out


@quymo("L03")
def _():
    # số cặp số lẻ trong [1, n] = (số số lẻ)²; thời gian ở 1e9 cặp/giây
    odd = lambda n: (n + 1) // 2
    return [("25 / 2500 / 250000 cặp", [odd(n) ** 2 for n in (10, 100, 1000)] == [25, 2500, 250000]),
            ("10^6 → 2,5e11 cặp ≈ 4 phút", odd(10 ** 6) ** 2 == 250000000000 and 4 <= odd(10 ** 6) ** 2 / 1e9 / 60 < 4.5),
            ("10^9 → 2,5e17 cặp ≈ 8 năm", odd(10 ** 9) ** 2 == 250000000000000000 and 7.5 < odd(10 ** 9) ** 2 / 1e9 / 31557600 < 8.5),
            ("n²+n+41 sai ở n=40 (đầu bài)", [n for n in range(60) if not sympy.isprime(n * n + n + 41)][0] == 40)]
