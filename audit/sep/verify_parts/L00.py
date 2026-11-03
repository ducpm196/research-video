# SEP L00 — tính lại bằng phân số chính xác, lôgarit và mô phỏng (khác `checks` của bài: lũy thừa số thực trực tiếp).
import math
from fractions import Fraction

import numpy as np

q = Fraction(99, 100) ** 100
rec("L00a", round(float(q), 3) == 0.366 and round(math.exp(100 * math.log1p(-0.01)), 3) == 0.366,
    "0,99¹⁰⁰ ≈ 0,366 (phân số chính xác và exp(100·ln 0,99))")
n95 = math.ceil(math.log(0.05) / math.log(0.99))
rec("L00b", n95 == 299 and Fraction(99, 100) ** 299 < Fraction(5, 100) <= Fraction(99, 100) ** 298,
    "số người thử nhỏ nhất để bỏ sót < 5%: ⌈ln 0,05 / ln 0,99⌉ = 299")
rec("L00c", [round(float(Fraction(99, 100) ** k), 3) for k in (100, 200, 300)] == [0.366, 0.134, 0.049]
    and round(float(Fraction(99, 100) ** 3), 6) == 0.970299 and Fraction(99, 100) ** 2 == Fraction(9801, 10000),
    "bảng 100/200/300 người: 0,366 / 0,134 / 0,049; 0,99³ = 0,970299; 0,99² = 0,9801")
rng = np.random.default_rng(2026)
sims = (rng.random((200000, 100)) < 0.01).any(axis=1)
rec("L00d", abs((1 - sims.mean()) - 0.366) < 0.005, f"mô phỏng 200 000 lần thử 100 người: tỉ lệ không ai gặp lỗi {1 - sims.mean():.3f} ≈ 0,366")
rec("L00e", Fraction(10 ** 6) * Fraction(1, 100) == 10000 and Fraction(2 * 10 ** 6) * Fraction(5, 1000) == 10000
    and round(float(Fraction(995, 1000) ** 200), 3) == 0.367 and Fraction(20000) * Fraction(5, 1000) == 100
    and round(float(Fraction(999, 1000) ** 100), 3) == 0.905,
    "10 000 người; quiz: 10 000 người, 0,995²⁰⁰ ≈ 0,367, phát hành 1% = 20 000 → 100 người; 0,999¹⁰⁰ ≈ 0,905")
rec("L00f", round(0.99 ** 10, 3) == 0.904 and abs(round(0.99 ** 10, 3) ** 10 - 0.366) < 0.002,
    "đường kiểm hai tầng: 0,99¹⁰ ≈ 0,904 rồi 0,904¹⁰ ≈ 0,366")
