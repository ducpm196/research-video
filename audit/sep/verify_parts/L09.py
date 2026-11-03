# SEP L09 — tính lại bằng phân số chính xác và mô phỏng phân bố beta–PERT (khác `checks`: số thực trực tiếp).
from fractions import Fraction as F

import numpy as np


def pert(o, m, b):
    return F(o + 4 * m + b, 6), F(b - o, 6)


E, s = pert(2, 4, 12)
rec("L09a", E == 5 and s == F(5, 3) and round(float(s), 2) == 1.67 and round(float(E - 2 * s), 2) == 1.67
    and round(float(E + 2 * s), 2) == 8.33, "O, M, B = 2, 4, 12: E = 5; s = 10/6 ≈ 1,67; khoảng 1,67 … 8,33")
rec("L09b", F(2, 6) + F(16, 6) + F(12, 6) == 5 and F(12, 6) == 2 and 2 <= E <= 12 and E > 4,
    "đóng góp 2/6 + 16/6 + 12/6 = 5; B góp đúng 2 ngày; O ≤ E ≤ B; E > M")
# mô phỏng phân bố beta–PERT (α = 1 + 4(M − O)/(B − O), β = 1 + 4(B − M)/(B − O)) — trung bình lý thuyết đúng bằng (O + 4M + B)/6
rng = np.random.default_rng(9)
a, b_ = 1 + 4 * (4 - 2) / 10, 1 + 4 * (12 - 4) / 10
x = 2 + 10 * rng.beta(a, b_, 400000)
rec("L09c", abs(x.mean() - 5) < 0.02 and (x > 4).mean() > 0.5, f"mô phỏng beta–PERT: trung bình {x.mean():.3f} ≈ 5; hơn nửa số lần vượt M = 4 ({(x > 4).mean():.2f})")
rec("L09d", F(3 * 4) == 12 and 3 * E == 15 and round(float((3 * s * s) ** 0.5), 2) == 2.89 and round(float(3 * s), 2) == 5.0,
    "ba việc: cộng M = 12, cộng E = 15; s tổng = √3 · 1,67 ≈ 2,89 (không phải 5)")
Eq, sq = pert(3, 5, 13)
rec("L09e", Eq == 6 and round(float(sq), 2) == 1.67 and round(float(Eq + 2 * sq), 2) == 9.33 and round(float(Eq - 2 * sq), 2) == 2.67
    and 5 < Eq, "quiz: 3, 5, 13 → E = 6, s ≈ 1,67, khoảng 2,67 … 9,33; hứa 5 < 6")
rec("L09f", F(6 * 1 + 9 * 2, 3) == 8 and F(21, 6) == F(7, 2) and pert(3, 3, 3)[0] == 3 and pert(2, 5, 8)[1] == 1,
    "ôn nền: (6 + 18)/3 = 8; xúc xắc 21/6 = 3,5; làm thử O = M = B = 3 → 3; (8 − 2)/6 = 1")
