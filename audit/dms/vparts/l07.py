import math
import itertools
from fractions import Fraction as F

from reg import lab, quymo  # noqa


@lab("L07")
def _():
    # quan hệ là TẬP CÁC CẶP; tính chất kiểm bằng tập hợp, lớp bằng phân hoạch theo "đại diện"
    A = range(1, 7)
    defs = [("R1", lambda a, b: (a - b) % 4 == 0), ("R2", lambda a, b: b % a == 0), ("R3", lambda a, b: abs(a - b) <= 1), ("R4", lambda a, b: (a + b) % 2 == 0)]
    out = []
    for name, f in defs:
        R = {(a, b) for a in A for b in A if f(a, b)}
        px = {(a, a) for a in A} <= R
        dx = {(b, a) for a, b in R} <= R
        pdx = all(a == b for a, b in R if (b, a) in R)
        bc = all((a, c) in R for a, b in R for b2, c in R if b == b2)
        line = f"{name}: PX={int(px)} DX={int(dx)} PDX={int(pdx)} BC={int(bc)}"
        if px and dx and bc:
            classes = sorted({tuple(sorted(b for b in A if (a, b) in R)) for a in A})
            line += ", tuong duong, cac lop: " + " ".join("[" + ", ".join(map(str, c)) + "]" for c in classes)
        out.append(line)
    return out


@quymo("L07")
def _():
    cnt = lambda n: sum(1 for a in range(n) for b in range(n) for c in range(n) if a % 3 == b % 3 and b % 3 == c % 3 and a % 3 != c % 3)
    return [("729 / 27000 / 1000000 bộ ba, 0 vi phạm", [cnt(n) for n in (9, 30)] == [0, 0] and [n ** 3 for n in (9, 30, 100)] == [729, 27000, 1000000]),
            ("100 số → lớp 33, 33, 34", sorted(len([x for x in range(100) if x % 3 == r]) for r in range(3)) == [33, 33, 34]),
            ("10^9 bộ ba ≈ 1 giây; 10^15 ≈ 11,6 ngày", 1000 ** 3 / 1e9 == 1 and round(1e15 / 1e9 / 86400, 1) == 11.6)]
