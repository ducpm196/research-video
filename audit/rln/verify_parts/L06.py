# RLN L06 — tính lại bằng phân số chính xác, xác suất chính xác bằng tổ hợp (phần bù, mẫu không hoàn lại), mô phỏng numpy
# với hạt giống khác, và liệt kê đủ các khả năng nhiễu bằng itertools — khác `checks` (alg.rln_adjacent_pairs dạng kỳ vọng,
# alg.rln_max_bias, random.Random(6)).
import itertools
from fractions import Fraction as F

import numpy as np

g = F(99, 100)
rec("L06a", 1 + g * 10 == F(109, 10) and 2 + g * 6 == F(397, 50) and -1 + g * 3 == F(197, 100)
    and 1 + g * 5 == F(119, 20) and 1 + g * 6 == F(347, 50),
    "mục tiêu 10,9; quiz 7,94; quên cờ kết thúc 1,97; đích chạy 5,95 → 6,94")
rec("L06b", ((F(109, 10) - 9) ** 2 + (-1 - F(1, 2)) ** 2) / 2 == F(293, 100) and (F(109, 10) - 9) ** 2 == F(361, 100),
    "sai số lô: (3,61 + 2,25)/2 = 2,93")
rec("L06c", 1 - F(1, 10) * (1 * 2 - 4) * 2 == F(7, 5) and F(7, 5) * 2 == F(14, 5) and 2 ** 100 > 10 ** 30 and 48 * 4 == 192,
    "ôn nền: θ 1 → 1,4, đoán 2,8; 2¹⁰⁰ > 10³⁰; bảng 192 ô")
# Xác suất CÓ ÍT NHẤT một cặp liền nhau khi lấy 32 vị trí KHÁC NHAU từ N (đếm chính xác: số cách chọn k vị trí không kề nhau = C(N−k+1, k))
from math import comb


def p_any_adjacent(N, k):
    return 1 - F(comb(N - k + 1, k), comb(N, k))


p1m, p50k = p_any_adjacent(10 ** 6, 32), p_any_adjacent(50000, 32)
rec("L06d", abs(float(p1m) - alg.rln_adjacent_pairs(10 ** 6, 32)) < 2e-6 and abs(float(p50k) - 0.0198) < 0.0005,
    f"đếm chính xác (không hoàn lại): P(có cặp liền nhau) = {float(p1m):.6f} ≈ 0,001 với 1 triệu; {float(p50k):.4f} ≈ 0,02 với 50 000")
rng = np.random.default_rng(2015)
b = np.sort(rng.integers(0, 10 ** 6, size=(200000, 32)), axis=1)
cnt = (np.diff(b, axis=1) == 1).sum()
rec("L06e", abs(cnt / 200000 - 0.000992) < 0.0002, f"mô phỏng numpy 200 000 lô: {cnt / 200000:.6f} cặp liền nhau mỗi lô")
combos = list(itertools.product([-1, 1], repeat=3))
rec("L06f", F(sum(max(c) for c in combos), len(combos)) == F(3, 4) == alg.rln_max_bias(3, 1.0)
    and sum(1 for c in combos if max(c) == 1) == 7,
    "đánh giá quá cao: liệt kê 8 khả năng, max = +1 ở 7, kỳ vọng 3/4")
