# CVI L03 — tính lại bằng numpy (ma trận K @ điểm, chia số cuối), sympy cho góc nhìn, và dạng méo của OpenCV (k2 = k3 = 0)
# — khác `checks` (alg.cvi_project / alg.cvi_distort vòng lặp thuần).
import math

import numpy as np
import sympy as sp

K = np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1.0]])
h = K @ np.array([0.5, 0.25, 2])
rec("L03a", h.tolist() == [1040, 680, 2] and (h[:2] / h[2]).tolist() == [520, 340] == list(alg.cvi_project(K.tolist(), 0.5, 0.25, 2)),
    "K·(0,5; 0,25; 2) = (1040, 680, 2) → (520, 340)")
q = K @ np.array([-0.4, 0.3, 4])
rec("L03b", (q[:2] / q[2]).tolist() == [240, 300], "tự làm 1: (240, 300)")
a = sp.atan(sp.Rational(320, 800))
rec("L03c", round(float(2 * a * 180 / sp.pi), 1) == 43.6 and round(float(a * 180 / sp.pi), 1) == 21.8 and sp.Rational(4) / sp.Rational(5, 1000) == 800,
    "góc nhìn 43,6° (nửa 21,8°); 4 mm / 0,005 mm = 800")


def ocv_dist(x, y, k1, k2=0, k3=0):  # OpenCV: x(1 + k1 r² + k2 r⁴ + k3 r⁶)
    r2 = x * x + y * y
    f = 1 + k1 * r2 + k2 * r2 ** 2 + k3 * r2 ** 3
    return x * f, y * f


xd, yd = ocv_dist(0.4, 0.3, -0.2)
rec("L03d", np.allclose([800 * xd + 320, 800 * yd + 240], [624, 468]) and math.isclose(math.dist((640, 480), (800 * xd + 320, 800 * yd + 240)), 20),
    "góc ảnh (640, 480) → (624, 468), lệch 20 điểm ảnh")
x2, y2 = ocv_dist(0.25, 0.125, -0.2)
rec("L03e", round(800 * x2 + 320, 1) == 516.9 and round(800 * y2 + 240, 1) == 338.4 and round(520 - (800 * x2 + 320), 1) == 3.1
    and round(340 - (800 * y2 + 240), 1) == 1.6, "điểm (520, 340) sau méo → (516,9; 338,4), lệch 3,1 / 1,6")
rec("L03f", round(80 - 800 * ocv_dist(0.1, 0, -0.2)[0], 2) == 0.16, "giữa ảnh (X/Z = 0,1): méo chỉ 0,16 điểm ảnh")
e = np.array([[0.6, 0.8], [0, 0.2], [0.4, 0.2]])
rec("L03g", round(float(np.sqrt((e ** 2).sum(1).mean())), 2) == 0.64, "sai số chiếu lại ≈ 0,64 điểm ảnh")
x3, y3 = ocv_dist(0.3, 0.4, -0.1)
rec("L03h", np.allclose([800 * x3 + 320, 800 * y3 + 240], [554, 552]) and math.isclose(math.dist((560, 560), (554, 552)), 10), "tự làm 2: (554, 552), lệch 10")
K2 = K / 2; K2[2, 2] = 1
s2 = K2 @ np.array([0.5, 0.25, 2])
rec("L03i", (s2[:2] / s2[2]).tolist() == [260, 170] and 840 * 0.4 - 800 * 0.4 == 16, "thu ảnh còn nửa: cột 260; tiêu cự 840: lệch 16")
# ước lượng lại k1 từ các điểm giữa ảnh bằng bình phương tối thiểu với nhiễu 0,2 điểm ảnh: độ bất định của k1 lớn → mép ảnh không đáng tin
rng = np.random.default_rng(3)


def se_k1(xmax, ymax, n=200, noise=0.2):
    xs = rng.uniform(-xmax, xmax, n); ys = rng.uniform(-ymax, ymax, n)
    g = 800 * xs * (xs ** 2 + ys ** 2)        # đạo hàm của u theo k1
    return noise / math.sqrt((g ** 2).sum())   # sai số chuẩn của k1 ước lượng bằng bình phương tối thiểu


se_c, se_f = se_k1(0.1, 0.1), se_k1(0.4, 0.3)
rec("L03j", se_c > 20 * se_f, f"bàn cờ chỉ ở giữa: sai số chuẩn của k1 = {se_c:.4f}, phủ cả ảnh = {se_f:.5f} (gấp {se_c / se_f:.0f} lần) — lỗi 4")
