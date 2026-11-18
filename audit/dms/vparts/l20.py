import math
import itertools
from fractions import Fraction as F

from reg import lab, quymo  # noqa


@lab("L20")
def _():
    # số bit n nhỏ nhất có 2^(n/2) ≥ 2^100 ⇔ n ≥ 200 (so sánh bằng Fraction mũ: n/2 ≥ 100)
    n = next(n for n in itertools.count(1) if F(n, 2) >= 100)
    pairs = F(10 ** 6 * (10 ** 6 - 1), 2)
    sec_year = 365 * 24 * 3600
    return ["2^80 = " + str(1 << 80), f"2^64 lan thu o 1e9 lan moi giay: {round((1 << 64) / F(10 ** 9) / sec_year)} nam", f"nhanh hon vet can (2^80 / 2^61): {1 << 19} lan",
            f"1000000 tep, ma 32 bit: ky vong cap trung gia {round(float(pairs / 2 ** 32), 1)}", "1000000 tep, ma 64 bit: ky vong cap trung gia " + "%.1e" % float(pairs / 2 ** 64),
            f"ma bang bit can de vet can ngay sinh >= 2^100: {n}"]
