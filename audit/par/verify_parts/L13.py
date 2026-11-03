# PAR L13 — tính lại con số của hành trình bằng đường khác `checks`: phân số chính xác, chia đôi từng lượt, mô phỏng rút gọn lượt vẽ
# trên dữ liệu thật, mô phỏng vòng bằng numpy với dữ liệu ngẫu nhiên, đếm bằng vòng lặp.
from fractions import Fraction as F

import numpy as np


def halving_passes(vals):
    """Rút gọn theo lượt vẽ năm 2005: mỗi lượt điểm ra i = nửa đầu[i] + nửa sau[i]. Trả về (các ảnh trung gian, số phép cộng)."""
    imgs, adds = [list(vals)], 0
    while len(vals) > 1:
        h = len(vals) // 2
        vals = [vals[i] + vals[h + i] for i in range(h)]
        adds += h
        imgs.append(vals)
    return imgs, adds


imgs, adds = halving_passes([3, 1, 4, 1, 5, 9, 2, 6])
rec("L13a", imgs[1:] == [[8, 10, 6, 7], [14, 17], [31]] and adds == 7 and len(imgs) - 1 == 3,
    "hình chặng 1: 8 → [8, 10, 6, 7] → [14, 17] → [31], 3 lượt, 7 phép cộng (bản nháp từng ghi sai 7/15/32, checks đã bắt)")
n, passes = 2 ** 20, 0
while n > 1:
    n, passes = n // 2, passes + 1
big, big_adds = halving_passes(list(range(2 ** 12)))
rec("L13b", passes == 20 and big_adds == 2 ** 12 - 1 and big[-1] == [sum(range(2 ** 12))] and F(63, 1) / F(148, 10) > 4.25
    and round(63 / 14.8, 2) == 4.26,
    "chia đôi 2^20 tới 1: 20 lượt; rút gọn 4096 số làm thật đúng tổng với 4095 phép cộng; 63/14,8 ≈ 4,26")
rec("L13c", sum(32 for _ in range(24)) == 768 and 768 * 16 == 12288 and sum(8 for _ in range(14)) == 112 and F(768, 8) == 96,
    "chặng 2: 24 nhóm × 32 = 768; 16 cụm = 12 288; 14 × 8 = 112; 96 luồng mỗi lõi")
warp = ["A"] * 16 + ["B"] * 16
passes2 = len(set(warp))
rec("L13d", passes2 == 2 and F(32, passes2 * 32) == F(1, 2) and alg.par_warp_passes(warp) == (2, F(1, 2)), "rẽ hai nhánh: 2 lượt, 50%")
imgs_total = 90 * 1_200_000
rec("L13e", imgs_total == 108_000_000 and [round(F(imgs_total, d * 86400)) for d in (6, 5)] == [208, 250],
    "chặng 3: 108 triệu ảnh; 208–250 ảnh mỗi giây")
ideal = F(29 * 8, 256)
rec("L13f", 256 * 32 == 8192 and 8 * 32 == 256 and round(float(ideal), 3) == 0.906 and round(float(ideal * 60), 1) == 54.4
    and round(float(ideal / F(9, 10)), 3) == 1.007 and round(float(ideal / F(9, 10) * 60), 1) == 60.4
    and F(1, 10) * F(8192, 256) == F(16, 5) and round(float(F(9, 10) / ideal), 3) == 0.993,
    "chặng 4: 32 ảnh mỗi thẻ; 0,906 h = 54,4 phút; chia 90% → 1,007 h; tốc độ học 3,2; 1 giờ làm được 0,993 việc")
rng = np.random.default_rng(13)
vecs = [list(rng.integers(0, 100, 128 * 2)) for _ in range(128)]
res, sent, steps = alg.par_ring_allreduce(vecs)
tot = np.sum(np.array(vecs), axis=0).tolist()
rec("L13g", all(r == tot for r in res) and steps == 254 and all(s == 2 * 127 * 2 for s in sent) and round(2 * 127 / 128, 2) == 1.98
    and F(sent[0], 256) == F(254, 128),
    "chặng 5: mô phỏng vòng 128 máy (numpy làm tổng đối chứng): đúng tổng, 254 bước, mỗi máy gửi 254/128 ≈ 1,98 D")
rec("L13h", F(88, 100) * 128 == F(2816, 25) and round(float(F(88, 100) * 128), 1) == 112.6 and F(1, 2) * 128 == 64
    and F(88, 100) / F(1, 2) == F(44, 25) and 100 * 254 == 25_400,
    "128 thẻ: 64 so với ≈ 112,6 thẻ hiệu dụng, tỉ 1,76; 100 khối nhỏ: 25 400 bước so với 254")
t64 = F(29 * 8, 64) / F(9, 10)
t64b = F(29 * 8, 64) / F(1, 2)
rec("L13i", round(float(t64), 2) == 4.03 and round(float(64 * t64), 1) == 257.8 and 8 * 29 == 232 and t64b == F(29, 4)
    and 64 * t64b == 464 and 64 * 32 == 2048 and F(1, 10) * F(2048, 256) == F(4, 5) and round(float(64 * t64 / 232), 2) == 1.11,
    "quiz: 4,03 giờ, 257,8 giờ thẻ (+11%); 50% → 7,25 giờ, 464 giờ thẻ; lô 2048, tốc độ học 0,8")
