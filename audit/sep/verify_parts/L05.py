# SEP L05 — tính lại bằng phân số chính xác, lôgarit và mô phỏng nhiều năm × nhiều máy (khác `checks`: số thực trực tiếp).
import math
from fractions import Fraction as F

import numpy as np

rec("L05a", F(1, 1000) * 10 ** 6 == 1000 and F(1, 10) * 1000 == 100 and F(1000, 100) == 10 and F(1, 10) / F(1, 1000) == 100,
    "kỳ vọng A 1000, B 100: A gấp 10 dù hiếm hơn 100 lần")
at_least = 1 - F(999, 1000) ** 1000
rec("L05b", round(float(at_least), 3) == 0.632 and abs(-math.expm1(1000 * math.log1p(-0.001)) - 0.632) < 0.001
    and round(1 - math.exp(-1), 3) == 0.632 and F(1000) * F(1, 1000) == 1,
    "1000 máy × 0,001: ít nhất một lần 0,632 (phân số chính xác, log1p, 1 − 1/e); trung bình 1 lần/năm")
rng = np.random.default_rng(5)
yrs = (rng.random((20000, 1000)) < 0.001).any(axis=1).mean()
rec("L05c", abs(yrs - 0.632) < 0.01, f"mô phỏng 20 000 năm × 1000 máy: tỉ lệ năm có sự cố {yrs:.3f}")
rec("L05d", round(float(1 - F(999, 1000) ** 10), 4) == 0.01 and round(float(1 - F(99, 100) ** 100), 3) == 0.634
    and F(1, 10000) * 100000 == 10 and round(float(1 - F(9999, 10000) ** 1000), 3) == 0.095,
    "1 máy 10 năm ≈ 0,01; ôn nền 0,634; lỗi C: kỳ vọng 10 khách, 1000 máy ≈ 0,095")
r3 = 1 - F(9998, 10000) ** 1000
rec("L05e", F(2, 100) * 50000 == 1000 and F(1, 2) * 1000 == 500 and F(2, 10000) * 2 * 10 ** 6 == 400 and round(float(r3), 3) == 0.181
    and 1000 * F(2, 10000) == F(1, 5) and F(1, 5) * 2 * 10 ** 6 == 400000 and F(400000, 1000) == 400,
    "quiz: 1000 / 500 / 400; R3 trên 1000 máy: 0,181, 0,2 lần, kỳ vọng 400 000 = 400 × R1")
