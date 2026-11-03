# RLN L02 — tính lại bằng liệt kê cả 4 chính sách tất định và giải hệ ma trận (numpy), đếm vòng bằng vòng lặp số nguyên
# (so 0,9^k với 0,001 bằng Fraction), kiểm tính co trên 2000 bảng V ngẫu nhiên — khác `checks` (alg.rln_policy_iteration, math.log).
from fractions import Fraction as F
import itertools
import math

import numpy as np

G = 0.9
# A = 0, B = 1. Hành động: A: cho (0,5, ở A) / di (1, sang B); B: o (0,2, ở B) / ve (0, sang A)
ACT = {0: {"cho": (0.5, 0), "di": (1.0, 1)}, 1: {"o": (0.2, 1), "ve": (0.0, 0)}}


def value(pol):
    P, r = np.zeros((2, 2)), np.zeros(2)
    for s, a in enumerate(pol):
        rew, s2 = ACT[s][a]
        P[s, s2], r[s] = 1, rew
    return np.linalg.solve(np.eye(2) - G * P, r)


vals = {pol: value(pol) for pol in itertools.product(ACT[0], ACT[1])}
best = max(vals, key=lambda p: vals[p].sum())
rec("L02a", best == ("di", "ve") and all((vals[best] >= v - 1e-12).all() for v in vals.values())
    and np.allclose(vals[best], [100 / 19, 90 / 19]),
    "liệt kê 4 chính sách: (đi, về) tốt nhất ở MỌI ô, V = (100/19, 90/19)")
rec("L02b", np.allclose(vals[("cho", "o")], [5, 2]) and np.allclose(vals[("cho", "ve")], [5, 4.5])
    and [p for p, _ in alg.rln_policy_iteration({'A': {'cho': [(1, 0.5, 'A')], 'di': [(1, 1, 'B')]}, 'B': {'o': [(1, 0.2, 'B')], 've': [(1, 0, 'A')]}}, {'A': 'cho', 'B': 'o'}, 0.9)]
    == [{'A': 'cho', 'B': 'o'}, {'A': 'cho', 'B': 've'}, {'A': 'di', 'B': 've'}],
    "ví dụ: V(chờ, ở) = (5, 2); V(chờ, về) = (5; 4,5); lặp chính sách đi đúng 3 chính sách")
rec("L02c", abs((0.5 + G * 100 / 19) - 5.237) < 5e-4 and abs((0.2 + G * 90 / 19) - 4.463) < 5e-4
    and abs((1 + G * 4.5) - 5.05) < 1e-12 and abs((0.2 + G * 4.5) - 4.25) < 1e-12 and abs((1 + G * 2) - 2.8) < 1e-12,
    "bảng cải thiện: 2,8; 5,05; 4,25; 5,237; 4,463")
k66 = next(k for k in itertools.count() if F(9, 10) ** k <= F(1, 1000))
k688 = next(k for k in itertools.count() if F(99, 100) ** k <= F(1, 1000))
k90 = next(k for k in itertools.count() if F(95, 100) ** k <= F(1, 100))
k6905 = next(k for k in itertools.count() if 0.999 ** k <= 0.001)
rec("L02d", (k66, k688, k90, k6905) == (66, 688, 90, 6905), "đếm số nguyên nhỏ nhất: 66, 688, 90 (quiz 1), 6905 (quiz 2)")
rec("L02e", round(688 / 60, 1) == 11.5 and round(6905 / 3600, 1) == 1.9 and 688 < 15 * 60 < 6905,
    "quiz 2: 688 giây ≈ 11,5 phút vừa 15 phút; 6905 giây ≈ 1,9 giờ")
rng = np.random.default_rng(3)


def T(V):  # một vòng lặp giá trị trên trò này
    return np.array([max(r + G * V[s2] for r, s2 in ACT[s].values()) for s in (0, 1)])


ratios = []
for _ in range(2000):
    V, U = rng.normal(0, 5, 2), rng.normal(0, 5, 2)
    ratios.append(np.abs(T(V) - T(U)).max() / np.abs(V - U).max())
rec("L02f", max(ratios) <= G + 1e-12, f"tính co trên 2000 cặp bảng ngẫu nhiên: tỉ số lớn nhất {max(ratios):.4f} ≤ 0,9")
V, k, vstar = np.zeros(2), 0, np.array([100 / 19, 90 / 19])
while np.abs(V - vstar).max() >= 0.001 * 100 / 19:
    V, k = T(V), k + 1
rec("L02g", k == 65 <= 66, "đếm thật: 65 vòng để sai số < 0,001 · e0 (cận 66)")
Vs = [np.zeros(2)]
for _ in range(70):
    Vs.append(T(Vs[-1]))
rec("L02h", all(np.abs(Vs[j + 1] - Vs[j]).max() * G / (1 - G) + 1e-12 >= np.abs(Vs[j + 1] - vstar).max() for j in range(70)),
    "lỗi 4: ở mọi vòng, sai số thật ≤ γ/(1 − γ) · thay đổi giữa hai vòng")
rec("L02i", [round(x, 3) for x in (Vs[1][0], Vs[10][0], Vs[50][0], Vs[70][0])] == [1.0, 3.6, 5.239, 5.26]
    and round(math.log(1000) / 0.1) == 69 and round(math.log(1000) / 0.01) == 691,
    "tự kiểm 1: V(A) 1 / 3,6 / 5,239 …; quy tắc nhẩm 69 và 691 vòng")
