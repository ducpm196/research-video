# CVI L10 — tính lại bằng đếm ảnh nguyên (số nguyên, không tỉ lệ), mô phỏng có hạt giống, và nhị thức chính xác (scipy không dùng:
# phương sai nhị thức tính bằng liệt kê) — khác `checks` (alg.cvi_mix_acc số thực, công thức căn).
from fractions import Fraction as F
from math import comb, sqrt

import numpy as np

rec("L10a", F(900 * 95 + 100 * 50, 1000 * 100) == F(905, 1000) and F(500 * 95 + 500 * 50, 1000 * 100) == F(725, 1000)
    and alg.cvi_mix_acc([(900, 0.95), (100, 0.5)]) == 0.905, "đếm nguyên: 905/1000 và 725/1000")
r = np.random.default_rng(11)
n = 200000
night = r.random(n) < 0.5
ok = np.where(night, r.random(n) < 0.5, r.random(n) < 0.95)
rec("L10b", abs(ok.mean() - 0.725) < 0.004, f"mô phỏng 200 000 ảnh trên đường: {ok.mean():.4f} ≈ 0,725")


def sd_of_mean(a, n):  # độ lệch chuẩn chính xác của tỉ lệ đúng trên n ảnh, liệt kê phân phối nhị thức
    ps = [comb(n, k) * a ** k * (1 - a) ** (n - k) for k in range(n + 1)]
    m = sum(k / n * p for k, p in enumerate(ps))
    return sqrt(sum((k / n - m) ** 2 * p for k, p in enumerate(ps)))


rec("L10c", abs(sd_of_mean(0.5, 100) - 0.05) < 1e-9 and round(sd_of_mean(0.5, 10), 3) == 0.158 and round(sd_of_mean(0.95, 900), 4) == 0.0073,
    "liệt kê nhị thức: 0,05 (100 ảnh), 0,158 (10 ảnh), 0,0073 (900 ảnh ngày)")
need = next(k for k in range(1, 10000) if 2 * sqrt(0.25 / k) <= 0.02 + 1e-12)
need_rain = next(k for k in range(1, 10000) if 2 * sqrt(0.21 / k) <= 0.05 + 1e-12)
rec("L10d", need == 2500 and need_rain == 336, "cỡ mẫu nhỏ nhất (dò từng n): 2500 ảnh đêm; 336 ảnh mưa")
rec("L10e", F(4108 - 2083, 2083) > F(97, 100) - F(1, 200) and round((41.08 - 20.83) / 20.83 * 100) == 97, "Beery 2018: 20,83% → 41,08%, tăng ≈ 97% (nguồn ghi “97% cis-to-trans increase”)")
rec("L10f", F(3 * 95 + 7 * 50, 1000) == F(635, 1000) and F(8 * 92 + 2 * 70, 1000) == F(876, 1000) and F(6 * 92 + 4 * 70, 1000) == F(832, 1000),
    "mùa đông 63,5%; tự làm 87,6% và 83,2%")
rec("L10g", 2 * 0.05 == 0.1 and round(0.5 - 2 * sd_of_mean(0.5, 10), 2) == 0.18 and round(0.5 + 2 * sd_of_mean(0.5, 10), 2) == 0.82, "khoảng 40–60% và 18–82%")
