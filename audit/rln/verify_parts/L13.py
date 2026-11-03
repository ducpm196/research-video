# RLN L13 — tính lại bằng phân số chính xác và đơn vị đổi theo chiều ngược (ngày → khung), mô phỏng hành động dính trên nhiều bước
# quyết định, cộng thẳng chuỗi chiết khấu, khác `checks` của bài (biểu thức số thực trực tiếp).
from fractions import Fraction as F

import numpy as np

day = 60 * 86400  # khung của máy mỗi ngày ở 60 Hz
rec("L13a", F(50 * 10 ** 6 * 4, day) == F(200 * 10 ** 6, day) and round(float(F(200 * 10 ** 6, day)), 1) == 38.6
    and round(float(F(50 * 10 ** 6, day)), 1) == 9.6 and 38 * day < 200 * 10 ** 6 < 39 * day,
    "hook/chặng 2/4: 50 triệu bước × 4 = 200 triệu khung ≈ 38,6 ngày (38 và 39 ngày kẹp hai bên); 50 triệu khung thô ≈ 9,6 ngày")
eps = lambda t: 1 - F(9, 10) * min(F(t, 10 ** 6), 1)
rec("L13b", eps(250_000) == F(31, 40) and eps(500_000) == F(11, 20) and eps(2_000_000) == F(1, 10)
    and F(10 ** 7 - 10 ** 6, 10 ** 7) == F(9, 10),
    "chặng 1: ε = 31/40 = 0,775; 11/20 = 0,55; 0,1 sau 1 triệu khung; 90% huấn luyện ở ε cố định")
rec("L13c", round(float(F(29, 49)) * 100, 1) == 59.2 and F(29, 49) > F(1, 2) and 43 < 49,
    "chặng 2: 29/49 ≈ 59,2% (hơn một nửa)")
rec("L13d", round(float(F(200, 7)), 1) == 28.6 and F(200 * 10 ** 6, 10) == 20 * 10 ** 6 and round(20 * 10 ** 6 / 86400) == 231
    and 223 - 153 == 70 and 53 < 57,
    "chặng 3: 200/7 ≈ 28,6 lần; 20 triệu khung/ngày ≈ 231 khung/giây; 223% − 153% = 70")
rng = np.random.default_rng(13)
# mô phỏng hành động dính: mỗi khung, với xác suất 0,25 giữ hành động trước; đếm số bước mà hành động cũ giữ suốt 4 khung
keep = rng.random((400000, 4)) < 0.25
first_new = (~keep[:, 0]).mean()
all_old = keep.all(axis=1).mean()
rec("L13e", abs(first_new - 0.75) < 0.003 and abs(all_old - 0.0039) < 0.0005 and F(1, 4) ** 4 == F(1, 256)
    and round(45 / 55 * 100) == 82,
    f"chặng 4: mô phỏng 400 000 bước — hành động mới chạy ngay {first_new:.4f} ≈ 0,75; dính cả 4 khung {all_old:.4f} ≈ 1/256")
hns = lambda a, r, h: 100 * (F(a) - F(r)) / (F(h) - F(r))
skiing = hns(-3272, "-17098.1", "-4336.9")
rec("L13f", round(float(skiing), 1) == 108.3 and round(float(skiing) - 100) == 8 and F(78 * 10 ** 9, 200 * 10 ** 6) == 390
    and F(5 * 10 ** 9, 200 * 10 ** 6) == 25 and hns(60, 10, 110) == 50,
    "chặng 5: trượt tuyết tối đa ≈ 108,3% (hơn người 8 điểm); 78 tỉ / 200 triệu = 390; 5 tỉ / 200 triệu = 25; ví dụ 50%")
g = 0.9999
s, x = 0.0, 1.0
for _ in range(200000):
    s += x
    x *= g
rec("L13g", abs(s - 10000) < 1e-3 and round(1 / (1 - g)) == 10000,
    f"chặng 5 / tự kiểm: cộng 200 000 số hạng 0,9999^k = {s:.4f} ≈ 10 000 = 1/(1 − 0,9999)")
rec("L13h", 20 * 10 ** 6 * 7 == 140 * 10 ** 6 and F(140, 5) == 28 and round(float(F(140, 3)), 1) == 46.7
    and 10 < 28 < 50 and round(F(78 * 10 ** 9, 20 * 10 ** 6)) == 3900,
    "quiz: 140 triệu khung/tuần; 5 lần × 28 triệu; 3 lần × 46,7 triệu; bài học sai 4: 3900 ngày")
