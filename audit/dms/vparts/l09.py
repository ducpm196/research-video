import math
import itertools
from fractions import Fraction as F

from reg import lab, quymo  # noqa


@lab("L09")
def _():
    # công thức: math.perm / math.factorial / lũy thừa; vét cạn: đếm bằng đệ quy xây chuỗi (không itertools)
    def _count(alphabet, k, distinct, used=()):
        if k == 0:
            return 1
        return sum(_count(alphabet, k - 1, distinct, used + (a,)) for a in alphabet if not (distinct and a in used))
    D = list(range(10))
    out = [f"ma PIN 4 chu so (duoc lap): {10 ** 4} {_count(D, 4, False)}",
           f"ma PIN 4 chu so khac nhau: {math.perm(10, 4)} {_count(D, 4, True)}",
           f"xep 5 nguoi thanh hang: {math.factorial(5)} {_count(list('ABCDE'), 5, True)}",
           f"chuoi 3 ky tu tu abcd, duoc lap: {4 ** 3} {_count(list('abcd'), 3, False)}",
           f"chuoi 3 ky tu tu abcd, khong lap: {math.perm(4, 3)} {_count(list('abcd'), 3, True)}"]
    even = sum(1 for a in range(1, 6) for b in range(1, 6) for c in range(1, 6) if len({a, b, c}) == 3 and c % 2 == 0)
    out.append(f"so chan 3 chu so khac nhau tu 1..5: {2 * math.perm(4, 2)} {even}")
    return out


@quymo("L09")
def _():
    sec = lambda n: n / 1e9
    return [("PIN 10^4, 10^6", len(range(10 ** 4)) == 10000 and len(range(10 ** 6)) == 1000000),
            ("62^8 ≈ 2,5 ngày; 62^12 hơn 37 triệu ngày", 62 ** 8 // 10 ** 9 // 86400 == 2 and abs(sec(62 ** 8) / 86400 - 2.5) < 0.05 and 37.3e6 < sec(62 ** 12) / 86400 < 37.4e6),
            ("62^12 ≈ 102 000 năm", 100000 < sec(62 ** 12) / 31557600 < 105000)]
