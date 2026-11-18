import math
import itertools
from fractions import Fraction as F

from reg import lab, quymo  # noqa


def _mults(e):
    # số phép nhân của bình phương liên tiếp = số bit + số bit 1
    return e.bit_length() + bin(e).count("1")


@lab("L14")
def _():
    try:
        inv12 = str(pow(12, -1, 18))
    except ValueError:
        inv12 = "khong co"
    smallest = next(d for d in range(2, 562) if 561 % d == 0)
    return [f"nghich dao cua 7 theo mo-dun 40: {pow(7, -1, 40)}", f"nghich dao cua 12 theo mo-dun 18: {inv12}",
            f"6^100 mod 19: {pow(6, 100, 19)} {pow(6, 100 % 18, 19)}",
            f"so phep nhan cua luy thua nhanh voi mu 1000: {_mults(1000)}",
            f"2^560 mod 561: {pow(2, 560, 561)}, uoc nho nhat cua 561: {smallest}"]


@quymo("L14")
def _():
    return [("10, 27, 53 phép nhân", [_mults(e) for e in (100, 10 ** 6, 10 ** 12)] == [10, 27, 53]),
            ("kết quả khớp pow có sẵn: tích nhân từng lần ở cỡ nhỏ", all(pow(3, e, 1000007) == math.prod([3] * e) % 1000007 for e in (100, 3000))),
            ("10^12 phép ≈ 17 phút; 2^2048 có 617 chữ số; tối đa 4096 phép", round(10 ** 12 / 1e9 / 60) == 17 and len(str(2 ** 2048)) == 617 and 2 * 2048 == 4096 and _mults(2 ** 2048 - 1) == 4096)]
