# CAS L10 — Google Flu Trends. Đường KHÁC `checks`: khớp thẳng bằng công thức đóng (hiệp phương sai / phương sai, Fraction-free, vòng
# lặp thuần) thay np.polyfit; cùng dãy ngẫu nhiên (default_rng(0)) nhưng tự lấy tổng dồn; nhị thức bằng Fraction; MAE trễ bằng zip.
from fractions import Fraction as F
from math import comb

import numpy as np

T = [1.0, 1.2, 1.5, 2.0, 2.6, 3.3, 4.0, 4.6, 5.0, 5.2, 5.1, 4.7, 4.1, 3.4, 2.8, 2.2, 1.8, 1.5, 1.3, 1.1]
rec("L10a", T == alg.CAS_FLU, "chuỗi 20 tuần minh hoạ trùng với checklib")


def fit(x, y):                                   # bình phương tối thiểu cho y ≈ a·x + b, công thức đóng
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    a = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / sum((xi - mx) ** 2 for xi in x)
    return a, my - a * mx


def spurious(n_cand):
    Z = np.random.default_rng(0).normal(size=(n_cand, 20))
    best = None
    for z in Z:
        c, acc = [], 0.0
        for v in z:
            acc += float(v)
            c.append(acc)
        a, b = fit(c[:10], T[:10])
        tr = sum(abs(a * c[i] + b - T[i]) for i in range(10)) / 10
        if best is None or tr < best[0]:
            best = (tr, sum(abs(a * c[i] + b - T[i]) for i in range(10, 20)) / 10)
    return tuple(round(v, 2) for v in best)


got = {n: spurious(n) for n in (10, 1000, 10000)}
rec("L10b", got == {10: (0.36, 1.42), 1000: (0.16, 3.01), 10000: (0.1, 3.85)}, f"khớp quá mức (công thức đóng): {got}")
lag = sum(abs(u - v) for u, v in zip(T[10:], T[8:18])) / 10
rec("L10c", round(lag, 2) == 0.8 == round(alg.cas_lag_mae(2), 2), "dùng số đo trễ 2 tuần: MAE 0,80")
rec("L10d", round((4.2 - 2) / 2 * 100) == 110 and round((F(486) - 232) / 486 * 100) == 52 and round((F(311) - 232) / 311 * 100) == 25,
    "sai 110% (minh hoạ); kết hợp bớt 52% so với chỉ tìm kiếm, 25% so với chỉ số đo trễ")
p_ge100 = F(sum(comb(108, k) for k in range(100, 109)), 2 ** 108)
rec("L10e", p_ge100 < F(1, 10 ** 18) and round(F(100, 108) * 100, 1) == F(926, 10), "≥ 100/108 tuần cao nếu ngẫu nhiên: < 1 phần tỉ tỉ; 92,6%")
rec("L10f", round(50e6 / 1152) == 43403, "50 triệu ứng viên / 1152 điểm ≈ 43 403")
rec("L10g", F(1, 2) ** 8 == F(1, 256) and round(float(F(9 - 5, 9)) * 100) == 44, "quiz: 1/256 ≈ 0,39%; 0,9 → 0,5 bớt 44%")
