import math
import itertools
from fractions import Fraction as F

from reg import lab, quymo  # noqa


@lab("L00")
def _():
    # bảng chân trị (p ∧ ¬q) ∨ r bằng phép bit trên số nguyên 3 bit (p = bit 2, q = bit 1, r = bit 0), từ 111 xuống 000
    rows = ["p q r kq"]
    dem = 0
    for m in range(7, -1, -1):
        p, q, r = (m >> 2) & 1, (m >> 1) & 1, m & 1
        kq = (p & (1 - q)) | r
        rows.append(f"{p} {q} {r} {kq}")
        dem += kq
    rows.append(f"so dong dung: {dem}")
    return rows


@quymo("L00")
def _():
    # số dòng = số dãy bit độ dài n: len(range(2**n)); 60 mệnh đề tính bằng dịch bit (không dùng **)
    return [("10 mệnh đề: 1024 dòng", len(range(1 << 10)) == 1024), ("20 mệnh đề: 1048576 dòng", len(range(1 << 20)) == 1048576),
            ("30 mệnh đề: 1073741824 dòng, khoảng 1 giây", 1 << 30 == 1073741824 and (1 << 30) // 10 ** 9 == 1),
            ("60 mệnh đề: 1152921504606846976 dòng, 1152921504 giây", 1 << 60 == 1152921504606846976 and (1 << 60) // 10 ** 9 == 1152921504),
            ("36,5 năm", abs((1 << 60) / 1e9 / (86400 * 365.25) - 36.5) < 0.05)]
