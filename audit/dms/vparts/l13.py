import math
import itertools
from fractions import Fraction as F

from reg import lab, quymo  # noqa


def _steps(a, b):
    n = 0
    while b:
        a, b, n = b, a % b, n + 1
    return a, n


@lab("L13")
def _():
    # gcd bằng tập ước chung; Bézout kiểm bằng tìm kiếm trong lưới nhỏ; số dư bằng Fraction/floor; ngày bằng cộng từng ngày
    div = lambda n: {d for d in range(1, n + 1) if n % d == 0}
    g = max(div(462) & div(1071))
    bez = any(462 * x + 1071 * y == 21 for x in range(-20, 21) for y in range(-20, 21))
    neg = -17 - 5 * math.floor(F(-17, 5))
    prod = 123456789 * 987654321
    day = 1
    for _ in range(1000):
        day = (day + 1) % 7
    names = ['Hai', 'Ba', 'Tu', 'Nam', 'Sau', 'Bay', 'CN']
    xs = [x for x in range(30) if (7 * x - 3) % 30 == 0]
    return [f"gcd(462, 1071) = {g}", f"he so Bezout (x, y) thoa 462x + 1071y = 21: {'dung' if bez else 'sai'}", f"-17 mod 5 = {neg}",
            f"(123456789 * 987654321) mod 1000: {prod % 1000} {(prod % 10 ** 3)}",
            f"1000 ngay nua tu thu Ba la thu {names[day]}", f"so buoc Euclid cua (832040, 514229): {_steps(832040, 514229)[1]}", f"7x = 3 (mod 30): x = {xs[0]}"]


@quymo("L13")
def _():
    pairs = [(252, 198), (10 ** 6 + 3, 10 ** 6), (2880067194370816120, 1779979416004714189)]
    res = [_steps(a, b) for a, b in pairs]
    return [("gcd và số bước: (18,4), (1,3), (1,88)", res == [(18, 4), (1, 3), (1, 88)]),
            ("ước chung kiểm bằng math.gcd", all(math.gcd(a, b) == r[0] for (a, b), r in zip(pairs, res))),
            ("thử ước ≈ 56 năm ở cặp lớn", round(pairs[2][1] / 1e9 / 31557600) == 56)]
