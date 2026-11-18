import math
import itertools
from fractions import Fraction as F

import sympy

from reg import lab, quymo  # noqa


@lab("L15")
def _():
    p, q, e = 7, 13, 5
    n, L = p * q, math.lcm(p - 1, q - 1) * math.gcd(p - 1, q - 1)   # (p-1)(q-1) = lcm·gcd
    d = pow(e, -1, L)
    c = (10 ** e) % n
    ok = sum(1 for x in range(n) if (x ** e % n) ** d % n == x)
    f = sympy.factorint(n)
    return [f"n = {n}, L = {L}", f"khoa bi mat d = {d}", f"ma hoa 10: {c}", f"giai ma {c}: {pow(c, d, n)}",
            f"ma hoa roi giai ma moi ban tin 0..90: {ok} / 91 dung", f"phan tich n: {n} = {min(f)} x {n // min(f)}"]


@quymo("L15")
def _():
    smallest = lambda n: min(sympy.factorint(n))
    return [("ước nhỏ nhất 3, 1009, 1000003", [smallest(p * q) for p, q in ((3, 11), (1009, 1013), (1000003, 1000033))] == [3, 1009, 1000003]),
            ("số lần chia thử = ước nhỏ nhất − 1 + 1 (33→2, 1022117→1008, 1000036000099→1000002)", [smallest(p * q) - 1 for p, q in ((3, 11), (1009, 1013), (1000003, 1000033))] == [2, 1008, 1000002]),
            ("2^1023 có 308 chữ số; ≈ 2,8e291 năm", len(str(2 ** 1023)) == 308 and 2.8e291 < 2 ** 1023 / 1e9 / 31557600 < 2.9e291)]
