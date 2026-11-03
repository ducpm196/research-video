# SEP L01 — tính lại bằng phân số chính xác, lôgarit và mô phỏng nhiều lần (khác `checks`: lũy thừa số thực trực tiếp).
import itertools
import math
from fractions import Fraction

import numpy as np

c = len(list(itertools.product(range(365), range(80), range(2))))
rec("L01a", c == 58400 and len(list(itertools.product(range(12), range(80), range(2)))) == 1920,
    "liệt kê tổ hợp: 365 × 80 × 2 = 58 400; 12 × 80 × 2 = 1920")
u = math.exp(9999 * math.log1p(-1 / 58400))
rec("L01b", round(u, 3) == 0.843 and round(10000 * u) == 8426 and round(math.exp(-9999 / 58400), 3) == 0.843,
    f"(1 − 1/58 400)^9999 qua log1p = {u:.4f}; × 10 000 ≈ 8426; xấp xỉ e^(−0,171) = 0,843")
rng = np.random.default_rng(11)
fr = []
for _ in range(20):
    cnt = np.bincount(rng.integers(0, 58400, 10000), minlength=58400)
    fr.append((cnt == 1).sum() / 10000)
rec("L01c", abs(np.mean(fr) - 0.843) < 0.005, f"mô phỏng 20 lần rải 10 000 người vào 58 400 ô: tỉ lệ đứng một mình {np.mean(fr):.4f}")
rec("L01d", round(math.exp(9999 * math.log1p(-1 / 1920)), 4) == 0.0055 and 9999 * math.log1p(-1 / 160) < math.log(1e-20)
    and Fraction(23, 24) ** 2 == Fraction(529, 576) and round(529 / 576, 3) == 0.918,
    "tháng+năm: 0,0055; chỉ năm: < 10⁻²⁰; làm thử (23/24)² = 529/576 ≈ 0,918")
rec("L01e", 2 * 5 * 365 * 100 == 365000 > 54805 and round(216 / 248, 2) == 0.87,
    "Sweeney 2000: 365 000 tổ hợp > 54 805 cử tri; 216/248 ≈ 87%")
q = math.exp(4999 * math.log1p(-1 / 43800))
rec("L01f", 365 * 60 * 2 == 43800 and round(q, 3) == 0.892 and 4999 * math.log1p(-1 / 12) < math.log(1e-100) and round(5000 / 12) == 417,
    f"quiz: c = 43 800, duy nhất {q:.4f}; 12 nhóm, mỗi ô ≈ 417 người, duy nhất < 10⁻¹⁰⁰")
