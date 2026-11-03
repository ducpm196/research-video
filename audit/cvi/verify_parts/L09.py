# CVI L09 — tính lại bằng mặt nạ numpy (phép & | trên mảng bool), phân số chính xác và sympy cho công thức đổi —
# khác `checks` (alg.cvi_mask_counts vòng lặp, alg.cvi_iou_dice số thực).
from fractions import Fraction as F

import numpy as np
import sympy as sp

G = np.zeros((10, 10), bool); G[1:6] = True
P = np.zeros((10, 10), bool); P[2:7] = True
tp, fp, fn, tn = (G & P).sum(), (P & ~G).sum(), (G & ~P).sum(), (~G & ~P).sum()
rec("L09a", (tp, fp, fn, tn) == (40, 10, 10, 40) == alg.cvi_mask_counts(P.astype(int).tolist(), G.astype(int).tolist()), "lưới 10 × 10: 40, 10, 10, 40")
rec("L09b", F(int(tp), int((G | P).sum())) == F(2, 3) and F(2 * int(tp), int(G.sum() + P.sum())) == F(4, 5) and (tp + tn) / 100 == 0.8,
    "IoU = 2/3, Dice = 2·|G∩P|/(|G| + |P|) = 4/5, độ chính xác điểm ảnh 0,8")
iou_bg = F(int((~G & ~P).sum()), int((~G | ~P).sum()))
rec("L09c", iou_bg == F(2, 3) and round(float((F(2, 3) + iou_bg) / 2), 3) == 0.667, "IoU của nền 2/3; mIoU 0,667")
q = sp.symbols("q", nonnegative=True)
I, U = sp.symbols("I U", positive=True)
rec("L09d", sp.simplify(2 * I / (I + U) - 2 * (I / U) / (1 + I / U)) == 0 and sp.simplify(2 * q / (1 + q) - q - q * (1 - q) / (1 + q)) == 0,
    "Dice = 2IoU/(1 + IoU); Dice − IoU = IoU(1 − IoU)/(1 + IoU) ≥ 0")
rec("L09e", [round(2 * x / (1 + x), 3) for x in (0, 0.5, 2 / 3, 0.9, 1)] == [0, 0.667, 0.8, 0.947, 1], "bảng đổi 0 / 0,667 / 0,8 / 0,947 / 1")
Gs = np.zeros((20, 20), bool); Gs[:2, :2] = True
Ps = np.zeros((20, 20), bool)
rec("L09f", Gs.sum() == 4 and (Ps == Gs).mean() == 0.99 and (Ps & Gs).sum() == 0 and F(int((~Ps & ~Gs).sum()), int((~Ps | ~Gs).sum())) == F(396, 400)
    and round((396 / 400 + 0) / 2, 3) == 0.495, "vết nứt 4/400: độ chính xác điểm ảnh 0,99, IoU vật 0, mIoU 0,495")
rec("L09g", round(2 * 0.7 / 1.7, 3) == 0.824 and F(2 * 90, 2 * 90 + 10) == F(18, 19) and F(2, 5) == F(2 * 1, 2 + 0 + 3)
    and round(float((F(18, 19) + F(2, 5)) / 2), 3) == 0.674 and F(2 * 91, 2 * 91 + 13) == F(182, 195) and round(182 / 195, 3) == 0.933,
    "lỗi 2: 0,824; lỗi 4: theo ảnh 0,674, gộp 0,933")
rec("L09h", F(30, 60) == F(1, 2) and F(60, 90) == F(2, 3) and round(0.9 / 1.1, 3) == 0.818 and sp.solve(sp.Eq(2 * q / (1 + q), sp.Rational(9, 10)), q) == [sp.Rational(9, 11)],
    "tự làm: 0,5 và 0,667; Dice 0,9 → IoU 9/11 ≈ 0,818 (giải bằng sympy)")
rec("L09i", F(25, 175) == F(1, 7) and (F(1, 2) + F(3, 4)) / 2 == F(5, 8) and F(4, 6) == F(2, 3), "ôn nền: 1/7; 0,625 so với 0,667")
