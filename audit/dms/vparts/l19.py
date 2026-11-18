import math
import itertools
from fractions import Fraction as F

from reg import lab, quymo  # noqa


def _min_n(m):
    # số khoá nhỏ nhất để P(trùng) ≥ 1/2 — tính bằng Fraction (chính xác) cho m nhỏ, bằng log cho m lớn
    if m <= 10 ** 6:
        p, n = F(1), 0
        while p > F(1, 2):
            p *= F(m - n, m)
            n += 1
        return n
    s, n = 0.0, 0
    while math.exp(s) > 0.5:
        s += math.log1p(-n / m)
        n += 1
    return n


@lab("L19")
def _():
    p30 = 1 - math.prod(F(365 - i, 365) for i in range(30))
    # kỳ vọng số điểm cố định = Σ_i P(vật i đúng chỗ) = 7 · 1/7 = 1 (biến chỉ báo); khác lời giải (không liệt kê)
    fixed = F(sum(F(1, 7) for _ in range(7)))
    brute = F(sum(1 for b in itertools.product(range(10), repeat=5) if len(set(b)) == 5), 10 ** 5)
    return [f"P(trung ngay sinh) voi 30 nguoi: {round(float(p30), 4)}", f"so nguoi nho nhat de P >= 0.5 voi 1000 ngay: {_min_n(1000)}",
            f"ky vong so cap va cham 200 khoa vao 10000 o: {float(F(200 * 199, 2) / 10000)}", f"so diem co dinh trung binh cua 7 vat: {float(fixed)}",
            f"P(khong trung) 5 nguoi, 10 ngay (liet ke het): {float(F(10 * 9 * 8 * 7 * 6, 10 ** 5))}"] if brute == F(30240, 10 ** 5) else ["LỖI"]


@quymo("L19")
def _():
    ratio = lambda n, m: round(n / m ** 0.5, 2)
    ns = [_min_n(365), _min_n(10 ** 6), _min_n(2 ** 32)]
    c = math.sqrt(2 * math.log(2))
    return [("23, 1178, 77164 khoá", ns == [23, 1178, 77164]), ("tỉ số n/√m = 1,2; 1,18; 1,18", [ratio(*x) for x in zip(ns, (365, 10 ** 6, 2 ** 32))] == [1.2, 1.18, 1.18]),
            ("hằng số √(2 ln 2) ≈ 1,177", abs(c - 1.17741) < 1e-4),
            ("2^64 ≈ 5 giây; 2^128 ≈ 690 năm; 2^256 ≈ 1,3e22 năm", round(c * 2 ** 32 / 1e9) == 5 and abs(c * 2 ** 64 / 1e9 / 31557600 - 688) < 3 and abs(c * 2 ** 128 / 1e9 / 31557600 / 1e22 - 1.27) < 0.02)]
