# CVI L05 — tính lại bằng phân số chính xác, mô phỏng Monte Carlo có hạt giống, numpy.polyfit, liệt kê mọi cặp bằng itertools — khác
# `checks` (alg.cvi_ransac_iters vòng while, alg.cvi_lsq_line công thức tổng, alg.cvi_ransac_line vòng lặp lồng).
import itertools
import math
from fractions import Fraction as F

import numpy as np

P = [(0, 1.0), (1, 3.2), (2, 4.9), (3, 7.1), (4, 9.0), (5, 10.8), (1, 9.0), (4, 1.0)]
x, y = np.array(P).T
a_all, b_all = np.polyfit(x, y, 1)
a_in, b_in = np.polyfit(x[:6], y[:6], 1)
rec("L05a", (round(a_all, 2), round(b_all, 2)) == (1.01, 3.22) and (round(a_in, 2), round(b_in, 2)) == (1.96, 1.1)
    and [round(v, 2) for v in alg.cvi_lsq_line(P)] == [1.01, 3.22], "bình phương tối thiểu: mọi điểm 1,01x + 3,22; 6 điểm đúng 1,96x + 1,1")
best = max(((i, j) for i, j in itertools.combinations(range(8), 2) if P[i][0] != P[j][0]),
           key=lambda ij: sum(abs(yy - ((P[ij[1]][1] - P[ij[0]][1]) / (P[ij[1]][0] - P[ij[0]][0])) * (xx - P[ij[0]][0]) - P[ij[0]][1]) <= 0.5 for xx, yy in P))
rec("L05b", alg.cvi_ransac_line(P, 0.5)[2] == [0, 1, 2, 3, 4, 5] and best[0] < 6 and best[1] < 6, "vét mọi cặp: tập đồng thuận lớn nhất là 6 điểm đúng")
res8 = [round(abs(yy - 8 * xx - 1), 2) for xx, yy in P]
res195 = [round(abs(yy - 1.95 * xx - 1.0), 2) for xx, yy in P]
rec("L05c", res195 == [0.0, 0.25, 0.0, 0.25, 0.2, 0.05, 6.05, 7.8] and sum(r <= 0.5 for r in res8) == 2
    and [sum(r <= t for r in res195) for t in (0.02, 0.5, 7)] == [2, 6, 7] and sum(r <= 0.05 for r in res195) == 3,
    "lần may 6 điểm trong, lần xui 2; ngưỡng 0,02 / 0,5 / 7 → 2 / 6 / 7 (0,05 đúng biên: 3 điểm — bài dùng 0,02 để khỏi phụ thuộc làm tròn số thực)")


def N_exact(w, s, p):  # bằng phân số: N nhỏ nhất với (1 − wˢ)ᴺ ≤ 1 − p
    q, n, fail = 1 - F(w) ** s, 0, F(1)
    while fail > 1 - F(p):
        fail *= q
        n += 1
    return n


cases = [("0.5", 4, "0.99", 72), ("0.3", 4, "0.99", 567), ("0.5", 2, "0.99", 17), ("0.5", 4, "0.9", 36), ("0.7", 2, "0.99", 7), ("0.4", 4, "0.99", 178), ("0.6", 4, "0.99", 34)]
rec("L05d", all(N_exact(w, s, p) == n == alg.cvi_ransac_iters(float(w), s, float(p)) for w, s, p, n in cases), "N bằng phân số chính xác: 72, 567, 17, 36, 7, 178, 34")
rec("L05e", round(math.log(0.1) / math.log(15 / 16), 1) == 35.7 and F(1, 2) ** 4 == F(1, 16), "ví dụ của bài báo 1981: 35,7; E(k) = 1/wⁿ = 16")
rng = np.random.default_rng(5)
succ = (rng.random((20000, 72, 4)) < 0.5).all(axis=2).any(axis=1).mean()
succ3 = (rng.random((20000, 72, 4)) < 0.3).all(axis=2).any(axis=1).mean()
rec("L05f", abs(succ - 0.99) < 0.003 and abs(succ3 - 0.443) < 0.015, f"mô phỏng 20 000 lần chạy × 72 lần bốc: thành công {succ:.4f} (w = 0,5), {succ3:.3f} (w = 0,3)")
good = sum(1 for i, j in itertools.combinations(range(8), 2) if i < 6 and j < 6)
rec("L05g", good == 15 and math.comb(8, 2) == 28 and round(good / 28, 3) == 0.536, "đếm thẳng: 15 trên 28 cặp toàn đúng")
rec("L05h", round(float((1 - F(1, 16)) ** 10), 3) == 0.524 and float((1 - F(1, 16)) ** 71) > 0.01 > float((1 - F(1, 16)) ** 72)
    and round(1 - (1 - 0.4 ** 4) ** 100, 3) == 0.925 and round(567 / 72, 1) == 7.9, "10 lần trượt cả 0,524; 71 chưa đủ, 72 đủ; 100 lần với w = 0,4: 0,925; 567/72 ≈ 7,9")
