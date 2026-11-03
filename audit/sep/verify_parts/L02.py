# SEP L02 — tính lại bằng phân số chính xác và mô phỏng từng người (khác `checks`: số thực theo công thức).
from fractions import Fraction as F

import numpy as np


def grp(p, tpr, fpr, n=100):
    tp, fp = n * p * tpr, n * (1 - p) * fpr
    return tp, fp, tp / (tp + fp), (tp + fp) / n


tpA, fpA, ppvA, selA = grp(F(1, 2), F(4, 5), F(1, 10))
tpB, fpB, ppvB, selB = grp(F(1, 5), F(4, 5), F(1, 10))
rec("L02a", (tpA, fpA, ppvA, selA) == (40, 5, F(8, 9), F(45, 100)) and (tpB, fpB, ppvB, selB) == (16, 8, F(2, 3), F(24, 100))
    and round(float(ppvA), 3) == 0.889 and round(float(ppvB), 3) == 0.667,
    "A: 40 đúng, 5 nhầm, PPV 8/9 ≈ 0,889, chọn 45%; B: 16, 8, PPV 2/3 ≈ 0,667, chọn 24%")


def fpr_from(p, ppv, tpr):
    return p / (1 - p) * (1 - ppv) / ppv * tpr


rec("L02b", fpr_from(F(1, 2), ppvA, F(4, 5)) == F(1, 10) and fpr_from(F(1, 5), ppvB, F(4, 5)) == F(1, 10)
    and fpr_from(F(1, 5), F(8, 9), F(4, 5)) == F(1, 40),
    "phương trình (2.6) đúng chính xác cho A, B; ép PPV_B = 8/9 → FPR_B = 1/40 = 0,025")
rng = np.random.default_rng(7)
N = 400000
good = rng.random(N) < 0.2
chosen = np.where(good, rng.random(N) < 0.8, rng.random(N) < 0.1)
rec("L02c", abs(good[chosen].mean() - 2 / 3) < 0.005 and abs(chosen.mean() - 0.24) < 0.003,
    f"mô phỏng 400 000 người nhóm B: PPV {good[chosen].mean():.3f}, chọn {chosen.mean():.3f}")
rec("L02d", F(16, 16 + 2) == F(8, 9) and F(1, 40) * 80 == 2 and F(40 + 45, 100) == F(85, 100) and F(16 + 72, 100) == F(88, 100),
    "FPR 0,025 → 2 người nhầm trên 80, 16/18 = 8/9; độ chính xác 0,85 / 0,88")
qA = grp(F(3, 10), F(9, 10), F(1, 5))
qB = grp(F(1, 10), F(9, 10), F(1, 5))
fq = fpr_from(F(1, 10), qA[2], F(9, 10))
rec("L02e", qA[:2] == (27, 14) and qB[:2] == (9, 18) and round(float(qA[2]), 3) == 0.659 and qB[2] == F(1, 3)
    and qA[3] == F(41, 100) and qB[3] == F(27, 100) and round(float(fq), 3) == 0.052,
    f"quiz: A 27/41 ≈ 0,659 chọn 41%; B 9/27 = 1/3 chọn 27%; FPR_B cần {float(fq):.4f}")
