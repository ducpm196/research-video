# CVI L02 — tính lại bằng numpy theo biểu đồ tần suất (cách của hướng dẫn OpenCV: cực tiểu phương sai TRONG lớp) và phân số chính xác —
# khác `checks` (alg.cvi_otsu cực đại phương sai GIỮA lớp trên danh sách điểm ảnh).
from fractions import Fraction as F

import numpy as np


def otsu_within(px, levels=256):
    h = np.bincount(px, minlength=levels).astype(float)
    p = h / h.sum()
    v = np.arange(levels)
    best = None
    for t in range(levels - 1):
        q1, q2 = p[:t + 1].sum(), p[t + 1:].sum()
        if q1 < 1e-12 or q2 < 1e-12:
            continue
        m1, m2 = (v[:t + 1] * p[:t + 1]).sum() / q1, (v[t + 1:] * p[t + 1:]).sum() / q2
        s1 = (((v[:t + 1] - m1) ** 2) * p[:t + 1]).sum() / q1
        s2 = (((v[t + 1:] - m2) ** 2) * p[t + 1:]).sum() / q2
        fn = q1 * s1 + q2 * s2
        if best is None or fn < best[0] - 1e-12:
            best = (fn, t)
    return best[1], best[0]


px = [10, 10, 12, 50, 52, 55]
t, w = otsu_within(px)
# phân số chính xác cho t = 12
m0, m1 = F(32, 3), F(157, 3)
sb = F(1, 4) * (m0 - m1) ** 2
tot = sum((F(x) - F(189, 6)) ** 2 for x in px) / 6
rec("L02a", 10 <= t < 50 and alg.cvi_otsu(px)[0] == 12 and round(w, 3) == 2.556,
    "ngưỡng cực tiểu trong lớp nằm ở khe 12…49 (biểu đồ: mọi mức giữa cho cùng tách) = ngưỡng 12 của alg.cvi_otsu; σ_W² = 2,556")
rec("L02b", round(float(sb), 3) == 434.028 and round(float(tot), 3) == 436.583 and abs(float(tot - sb) - 2.556) < 0.001,
    "phân số: σ_B² = 434,028; cả ảnh 436,583; hiệu = 2,556")
vals = {}
for tt in (10, 12, 50, 52):
    a = [F(x) for x in px if x <= tt]; b = [F(x) for x in px if x > tt]
    vals[tt] = F(len(a), 6) * F(len(b), 6) * (sum(a) / len(a) - sum(b) / len(b)) ** 2
rec("L02c", [round(float(vals[k]), 1) for k in (10, 12, 50, 52)] == [231.1, 434.0, 242.0, 110.5] and max(vals, key=vals.get) == 12,
    "bảng bốn ngưỡng 231,1 / 434,0 / 242,0 / 110,5")
rec("L02d", round(float(sum((F(x) - F(32, 3)) ** 2 for x in [10, 10, 12]) / 3), 3) == 0.889 and round(32 / 3, 3) == 10.667,
    "ôn nền: trung bình 10,667, phương sai 0,889")
# cân bằng biểu đồ bằng numpy cumsum
def eq(px, L):
    c = np.cumsum(np.bincount(px, minlength=L))
    return [int(np.floor((L - 1) * x / len(px) + 0.5)) for x in c]


rec("L02e", eq([0, 0, 1, 1, 1, 1, 2, 7], 8) == alg.cvi_equalize([0, 0, 1, 1, 1, 1, 2, 7], 8) == [2, 5, 6, 6, 6, 6, 6, 7]
    and eq([2, 2, 2, 2, 5, 6, 7, 7], 8)[2] == 4 and eq([0, 1, 1, 1, 1, 1, 2, 3], 4) == [0, 2, 3, 3],
    "cân bằng (làm tròn nửa lên, không có ca .5): A 0→2, 1→5, 2→6; B mức 2 → 4; tự làm 0, 2, 3, 3")
rec("L02f", otsu_within([200, 200, 200, 120, 110, 110, 110, 30])[0] in range(120, 200) and otsu_within([110, 110, 110, 30])[0] in range(30, 110)
    and otsu_within([200, 200, 200, 120])[0] in range(120, 200), "bóng: ngưỡng toàn cục đặt giấy 110 vào lớp tối; ngưỡng riêng nửa bóng tách 30 | 110")
u = np.arange(100, 106)
sbu = max(alg.cvi_otsu(list(u))[1], key=lambda r: r[5])[5]
rec("L02g", round(sbu / u.var(), 3) == 0.771 and round(float(sb / tot), 3) == 0.994, "tỉ số tách: nền một đỉnh 0,771, ảnh hai đỉnh 0,994")
q = [20, 22, 24, 80, 84]
rec("L02h", 24 <= otsu_within(q)[0] < 80 and round(0.6 * 0.4 * 60 ** 2, 6) == 864, "tự làm: ngưỡng 24, 864")
