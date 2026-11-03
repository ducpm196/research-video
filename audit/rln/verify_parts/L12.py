# RLN L12 — tính lại bằng phân số chính xác, liệt kê mọi nhật ký 10 lượt có thể (phân phối nhị thức) và mô phỏng Monte Carlo
# nhiều nhật ký, khác `checks` (alg.rln_is_estimates số thực trên một nhật ký).
from fractions import Fraction as F
from math import comb

import numpy as np

w1, w2 = F(1, 9), F(9)
S = [(w1, 1)] * 9 + [(w2, 2)]
ordi = sum(w * g for w, g in S) / 10
wis = sum(w * g for w, g in S) / sum(w for w, _ in S)
ess = sum(w for w, _ in S) ** 2 / sum(w * w for w, _ in S)
rec("L12a", ordi == F(19, 10) and wis == F(19, 10) and ess == F(100, F(9, 81) + 81) and round(float(ess), 3) == 1.233
    and F(9, 10) * w1 * 1 + F(1, 10) * w2 * 2 == F(19, 10) == F(1, 10) * 1 + F(9, 10) * 2,
    "nhật ký 10 lượt: thường = có trọng số = 19/10; ESS = 100/81,11 ≈ 1,233; kỳ vọng 1,9 (phân số)")
rec("L12b", F(10) * w1 / 10 == F(1, 9) and F(10) * w1 * 1 / (F(10) * w1) == 1 and round(float(F(1, 9)), 3) == 0.111
    and round(0.9 ** 10, 2) == 0.35,
    "nhật ký toàn a₁: thường 1/9 ≈ 0,111; có trọng số 1; xác suất 0,9¹⁰ ≈ 0,35")
# liệt kê: số lượt chọn a₂ trong 10 lượt ~ Nhị thức(10; 0,1); ước lượng thường = (k·9·2 + (10 − k)·(1/9)·1)/10
dist = {k: F(comb(10, k)) * F(1, 10) ** k * F(9, 10) ** (10 - k) for k in range(11)}
est = {k: (k * w2 * 2 + (10 - k) * w1) / 10 for k in range(11)}
mean = sum(dist[k] * est[k] for k in dist)
var = sum(dist[k] * (est[k] - mean) ** 2 for k in dist)
rec("L12c", mean == F(19, 10) and round(float(var), 2) == 2.88 and round(float(dist[0]), 2) == 0.35,
    f"liệt kê 11 khả năng: ước lượng thường không lệch (trung bình 1,9), phương sai ≈ {float(var):.3f} — dao động rất mạnh")
rng = np.random.default_rng(12)
hits = (rng.random((20000, 1000)) < 1 / 1024).sum(axis=1)
rec("L12d", 2 ** 10 == 1024 and abs((hits > 0).mean() - 0.624) < 0.01 and abs(hits.mean() - 1000 / 1024) < 0.02
    and round(1 - (1 - 1 / 1024) ** 1000, 3) == 0.624,
    f"mô phỏng 20 000 nhật ký 1000 lượt: có ≥ 1 lượt trùng {(hits > 0).mean():.3f} ≈ 0,62; trung bình {hits.mean():.3f} ≈ 0,98 lượt")
ws = [F(4), F(4)] + [F(1, 2)] * 4
rec("L12e", sum(ws) == 10 and sum(x * x for x in ws) == 33 and round(float(sum(ws) ** 2 / sum(x * x for x in ws)), 2) == 3.03
    and round(1.5 ** 6, 1) == 11.4 and 2 ** 6 == 64 and F(8 * 5, 2) ** 2 / (8 * F(5, 2) ** 2) == 8,
    "câu đố: ESS = 100/33 ≈ 3,03; 1,5⁶ ≈ 11,4; 2⁶ = 64; tự kiểm 8 trọng số đều → 8")
rec("L12f", abs(float(ess) - alg.rln_is_estimates([(1 / 9, 1)] * 9 + [(9, 2)])[2]) < 1e-12
    and abs(alg.rln_is_estimates([(1 / 9, 1)] * 10)[2] - 10) < 1e-9,
    "đối chiếu checklib: ESS 1,233 và 10 (nhật ký toàn a₁ — “chắc chắn” mà sai)")
