# CVI L06 — tính lại bằng numpy (trượt cửa sổ bằng lát cắt + np.abs, argmin), phân số chính xác, sympy (giới hạn/xấp xỉ bậc nhất),
# chiếu thẳng bằng ma trận nội 3 × 3 — khác `checks` (alg.cvi_sad_costs vòng lặp, alg.pinhole công thức).
from fractions import Fraction as F

import numpy as np
import sympy as sp

L = np.array([10, 10, 10, 10, 20, 90, 40, 10, 10, 10, 10, 10])
R = np.concatenate([L[3:], [10, 10, 10]])
cost = [int(np.abs(L[4:7] - R[4 - d:7 - d]).sum()) for d in range(5)]
rec("L06a", cost == [120, 130, 150, 0, 130] == alg.cvi_sad_costs(L.tolist(), R.tolist(), 5, 1, 4) and int(np.argmin(cost)) == 3,
    "chi phí 120, 130, 150, 0, 130 → d = 3")
rec("L06b", F(84, 42) == 2 and F(84, 3) == 28 and F(700) * F(12, 100) == 84, "Z = 84/42 = 2 m; 84/3 = 28 m; f·B = 84")
K = np.array([[700, 0, 320], [0, 700, 240], [0, 0, 1.0]])
pl = K @ np.array([0.5, 0.3, 2]); pr = K @ np.array([0.5 - 0.12, 0.3, 2])
pl, pr = pl / pl[2], pr / pr[2]
rec("L06c", abs(pl[1] - pr[1]) < 1e-12 and round(pl[1], 6) == 345 and round(pl[0] - pr[0], 6) == 42, "hai camera: cùng hàng 345, chênh cột 42")
q8l = K @ np.array([1, 0, 8.0]); q8r = K @ np.array([0.88, 0, 8.0])
rec("L06d", round(q8l[0] / 8, 6) == 407.5 and round(q8r[0] / 8, 6) == 397 and round((q8l[0] - q8r[0]) / 8, 6) == 10.5, "ở 8 m: cột 407,5 và 397, chênh 10,5")
Z, d, fB, e = sp.symbols("Z d fB e", positive=True)
lin = sp.series(fB / (d - e) - fB / d, e, 0, 2).removeO()
rec("L06e", sp.simplify(lin - fB * e / d ** 2) == 0 and sp.simplify((fB * e / d ** 2).subs(d, fB / Z) - Z ** 2 * e / fB) == 0,
    "sympy: hiệu bậc nhất = fB·δd/d² = Z²·δd/(fB)")
rec("L06f", round(float(F(84, 41) - 2), 3) == 0.049 and round(float(2 - F(84, 43)), 3) == 0.047 and round(float(F(84, 41 * 42)), 4) == 0.0488
    and round(4 / 84, 4) == 0.0476, "ở 2 m: 0,049 / 0,047; công thức 0,0488 và 0,0476")
rec("L06g", round(float(F(84) / F(19, 2) - 8), 2) == 0.84 and round(float(8 - F(84) / F(23, 2)), 2) == 0.70 and round(64 / 84, 3) == 0.762
    and round(float(F(84) / F(19, 2) - F(84) / F(23, 2)), 2) == 1.54, "ở 8 m: +0,84 / −0,70, công thức 0,762; bề rộng 1,54")
flat = [int(np.abs(np.full(3, 50) - np.full(3, 50)).sum()) for _ in range(5)]
occl = [int(np.abs(L[4:7] - 10).sum()) for _ in range(5)]
rec("L06h", flat == [0] * 5 and occl == [120] * 5 and alg.cvi_sad_costs([50] * 12, [50] * 12, 5, 1, 4) == flat, "tường trơn: mọi d chi phí 0; bị che: mọi d 120")
rec("L06i", 84 / 0.5 == 168 and round(84 / 0.4) == 210 and 640 * 480 * 169 == 51916800, "dải tìm: 168; vật ở 0,4 m cần 210; 51 916 800 phép tính")
Lq = np.array([0, 0, 30, 60, 30, 0, 0, 0]); Rq = np.array([30, 60, 30, 0, 0, 0, 0, 0])
cq = [int(np.abs(Lq[2:5] - Rq[2 - dd:5 - dd]).sum()) for dd in range(3)]
rec("L06j", cq == [90, 90, 0] and round(16 / 84, 2) == 0.19 and float(F(84, 20)) == 4.2 and round(84 / 22, 2) == 3.82
    and round(64 / (700 * 0.2), 3) == 0.457 and round(64 / (700 * 0.46), 3) == 0.199 and round(700 * 0.46 / 0.5) == 644,
    "tự làm: chi phí 90, 90, 0 → d = 2; ở 4 m lệch 0,19; B ≥ 0,457 → chọn 0,46 (0,199), vật 0,5 m có d = 644")
