import math
import itertools
from fractions import Fraction as F

from reg import lab, quymo  # noqa


@lab("L02")
def _():
    # đếm bằng tập hợp và tích Descartes (không dùng all/any)
    D = list(range(20))
    out = []
    bad = [x for x in D if x * x <= x]
    out.append("1: dung" if not bad else f"1: sai, phan vi du x={min(bad)}")
    good = [x for x in D if x * x - 2 * x - 3 == 0]
    out.append(f"2: dung, vi du x={min(good)}" if good else "2: sai")
    pairs = {(x, y) for x in D for y in D if x + y == 19}
    out.append("3: dung" if all(any((x, y) in pairs for y in D) for x in D) else "3: sai")   # ∀x∃y
    out.append("4: dung" if len({y for y in D if all((x, y) in pairs for x in D)}) else "4: sai")   # ∃y∀x
    gt = {(x, y) for x in D for y in D if y > x}
    nox = [x for x in D if not [y for y in D if (x, y) in gt]]
    out.append("5: dung" if not nox else f"5: sai, phan vi du x={min(nox)}")
    return out


@quymo("L02")
def _():
    def dem(n):
        c = 0
        for x in range(n):
            y = 0
            while True:
                c += 1
                if y > x or y == n - 1:
                    break
                y += 1
        return c
    return [("64 phép (n=10)", dem(10) == 64), ("5149 phép (n=100)", dem(100) == 5149), ("501499 phép (n=1000)", dem(1000) == 501499),
            ("gấp ~100 lần khi miền gấp 10", 90 < dem(1000) / dem(100) < 110),
            ("câu sai trên miền hữu hạn: số lớn nhất không có số lớn hơn", all(not any(y > n - 1 for y in range(n)) for n in (10, 100)))]
