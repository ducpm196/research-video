# RLN L03 — tính lại bằng phân số chính xác (Fraction), mô phỏng kẻ cướp nhiều tay có hạt giống, và chạy UCB thật
# trên 2 tay — khác `checks` (alg.rln_eps_greedy / alg.rln_ucb số thực).
from fractions import Fraction as F
import math

import numpy as np

p_best = (1 - F(1, 10)) + F(1, 10) / 10
rec("L03a", p_best == F(91, 100) and F(1, 10) / 10 == F(1, 100) and p_best + 9 * F(1, 100) == 1 and 9 * F(1, 100) == F(9, 100),
    "ε = 0,1, k = 10: 91/100 cho tay tốt nhất, 1/100 mỗi tay khác, 9 tay kém = 9%")
p5 = (1 - F(1, 5)) + F(1, 5) / 5
rec("L03b", p5 == F(84, 100) and F(1, 5) / 5 == F(4, 100) and p5 + 4 * F(4, 100) == 1, "quiz 1 / tự kiểm 2: 5 tay, ε = 0,2 → 0,84 và 0,04")
rng = np.random.default_rng(11)
n = 400000
explore = rng.random(n) < 0.1
arm = np.where(explore, rng.integers(0, 10, n), 0)
rec("L03c", abs((arm == 0).mean() - 0.91) < 0.003, f"mô phỏng 400 000 lượt: tần suất chọn tay tốt nhất {(arm == 0).mean():.4f} ≈ 0,91")
xs = [1, 0, 1, 1]
rec("L03d", [sum(map(F, xs[:i])) / i for i in range(1, 5)] == [1, F(1, 2), F(2, 3), F(3, 4)]
    and [round(v, 3) for v in alg.rln_incr_means(xs)] == [1.0, 0.5, 0.667, 0.75],
    "trung bình cộng dồn 1; 0,5; 0,667; 0,75 = trung bình cộng thẳng từng đoạn")


def ucb(q, nn, t, c):
    return q + c * (math.log(t) / nn) ** 0.5


rec("L03e", [round(x, 3) for x in (ucb(1.0, 10, 12, 2), ucb(0.8, 2, 12, 2), ucb(1.0, 10, 20, 2), ucb(0.8, 10, 20, 2))] == [1.997, 3.029, 2.095, 1.895]
    and [round(x, 3) for x in (ucb(0.6, 20, 25, 1), ucb(0.5, 5, 25, 1))] == [1.001, 1.302],
    "UCB: 1,997 / 3,029 (chọn B); sau 8 lượt B: 2,095 / 1,895 (về A); quiz 2: 1,001 / 1,302 (chọn B)")
# chạy UCB thật: tay A luôn thưởng 1,0, tay B luôn 0,8 (tất định) từ N = (10, 2), t = 12 — đếm số lượt liên tiếp B được chọn
N, Q, t, picks = [10, 2], [1.0, 0.8], 12, []
for _ in range(40):
    a = max((0, 1), key=lambda i: ucb(Q[i], N[i], t, 2))
    picks.append(a)
    N[a] += 1
    t += 1
first_a = picks.index(0)
rec("L03f", picks[0] == 1 and first_a > 0 and picks.count(0) > 0,
    f"chạy thật: UCB chọn B {first_a} lượt đầu rồi quay về A (khớp ý ví dụ: khám phá có lý do rồi tự thôi)")
rec("L03g", F(9, 100) * F(1, 2) == F(45, 1000) and F(45, 1000) * 1000 == 45 and F(45, 1000) * 10000 == 450,
    "lỗi 2: mất 0,045 mỗi lượt → 45 / 450")
q_avg = F(100, 110)
q_fix = 1.0
for _ in range(10):
    q_fix += 0.1 * (0 - q_fix)
rec("L03h", round(float(q_avg), 3) == 0.909 and round(q_fix, 3) == 0.349 and abs(q_fix - 0.9 ** 10) < 1e-12,
    "lỗi 4: trung bình cộng dồn 0,909; bước cố định 1/10 lặp 10 lần → 0,349 = 0,9¹⁰")
rec("L03i", [round(math.log(x), 2) for x in (10, 100, 1000)] == [2.3, 4.61, 6.91] and round(math.log(12), 3) == 2.485
    and round(math.log(20), 3) == 2.996 and round(math.log(25), 3) == 3.219,
    "lôgarit: 2,3 / 4,61 / 6,91; ln 12, ln 20, ln 25")
