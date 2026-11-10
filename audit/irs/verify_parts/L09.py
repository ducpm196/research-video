# IRS L09 — khởi động lạnh, lấy mẫu theo niềm tin: tính lại bằng CÁCH KHÁC checks (công thức đóng qua hàm Beta, Fraction, mô phỏng numpy
# với bộ sinh số khác, đếm thẳng), rồi đối chiếu alg.irs_* (tích phân số trên lưới, mô phỏng random.Random).
import math
from fractions import Fraction as F
import numpy as np


def lbeta(a, b):
    return math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)


def p_new_beats(b1, a2, b2):
    """X ~ Beta(1, b1): P(X > y) = (1 − y)^b1 → kỳ vọng theo Y ~ Beta(a2, b2) = B(a2, b2 + b1) / B(a2, b2) (công thức đóng)."""
    return math.exp(lbeta(a2, b2 + b1) - lbeta(a2, b2))


rec("L09a", F(1 + 50, (1 + 50) + (1 + 950)) == F(51, 1002) and round(float(F(51, 1002)), 4) == 0.0509
    and alg.irs_beta_post(1, 1, 50, 1000) == (51, 951) and F(1, 2) == F(1, 1 + 1),
    "Beta(51, 951) trung bình 51/1002 ≈ 0,0509; Beta(1, 1) trung bình 0,5")
# độ lệch chuẩn: đếm thẳng trên lưới (Beta(1,1) = đều) và phương sai Fraction
v11 = sum(((i + 0.5) / 10 ** 6 - 0.5) ** 2 for i in range(10 ** 6)) / 10 ** 6
v = F(51 * 951, 1002 ** 2 * 1003)
rec("L09b", round(math.sqrt(v11), 3) == 0.289 == round(alg.irs_beta_sd(1, 1), 3) and round(math.sqrt(v), 4) == 0.0069 == round(alg.irs_beta_sd(51, 951), 4),
    "độ lệch chuẩn 0,289 (đều) và 0,0069")
rec("L09c", round(p_new_beats(1, 51, 951), 3) == 0.949 == round(alg.irs_beta_p_beats(1, 1, 51, 951), 3)
    and abs(p_new_beats(1, 51, 951) - (1 - 51 / 1002)) < 1e-12,
    "xác suất mới thắng = 1 − trung bình cũ ≈ 0,949 (công thức đóng = tích phân số)")
rec("L09d", [round(p_new_beats(1 + n, 51, 951), 3) for n in (19, 40, 60)] == [0.355, 0.123, 0.045]
    == [round(alg.irs_beta_p_beats(1, 1 + n, 51, 951), 3) for n in (19, 40, 60)]
    and F(1, 21) < F(51, 1002) and round(1 / 21, 4) == 0.0476,
    "sau 19/40/60 lần không bấm: 0,355 / 0,123 / 0,045; trung bình 1/21 ≈ 0,0476 < 0,0509")
# 0,92^19 bằng Fraction và bằng mô phỏng
g = np.random.default_rng(7)
sim = float((g.random((400000, 19)) >= 0.08).all(axis=1).mean())
rec("L09e", round(float(F(92, 100) ** 19), 3) == 0.205 and abs(sim - 0.2051) < 0.003 and round(0.92 * 0.92, 3) == 0.846,
    "19 lần liền không bấm khi tỉ lệ thật 0,08: 0,205 (Fraction, mô phỏng 400 nghìn chuỗi); 0,92² ≈ 0,846")


# mô phỏng độc lập (numpy Generator, không dùng alg) — xếp theo trung bình và lấy mẫu theo niềm tin
def run(rule, seed, steps=2000):
    r = np.random.default_rng(1000 + seed)
    ab = [[1, 1], [51, 951]]
    shows = [0, 0]
    for _ in range(steps):
        sc = [r.beta(a, b) for a, b in ab] if rule == "t" else [a / (a + b) for a, b in ab]
        i = int(sc[1] > sc[0])
        shows[i] += 1
        if r.random() < (0.08, 0.05)[i]:
            ab[i][0] += 1
        else:
            ab[i][1] += 1
    return shows


lock_g = sum(run("g", s)[0] < 100 for s in range(100))
lock_t = sum(run("t", s)[0] < 100 for s in range(100))
alg_g = sum(alg.irs_bandit_run([0.08, 0.05], 2000, "greedy", s, [(1, 1), (51, 951)])[0] < 100 for s in range(100))
alg_t = sum(alg.irs_bandit_run([0.08, 0.05], 2000, "thompson", s, [(1, 1), (51, 951)])[0] < 100 for s in range(100))
rec("L09f", 15 <= lock_g <= 35 and lock_t == 0 and alg_g == 25 and alg_t == 0
    and alg.irs_bandit_run([0.08, 0.05], 2000, "greedy", 0, [(1, 1), (51, 951)]) == [19, 1981],
    f"khoá chết: mô phỏng riêng {lock_g}/100 (xếp theo trung bình), {lock_t}/100 (theo niềm tin); alg 25/100 và 0/100; hạt 0: 19 lần")
mc = np.random.default_rng(11)
y = mc.beta(51, 951, 300000)
rec("L09g", abs(float((mc.beta(1, 1, 300000) > y).mean()) - 0.949) < 0.004 and abs(float((mc.beta(1, 20, 300000) > y).mean()) - 0.355) < 0.004
    and abs(float(y.mean()) - 0.0509) < 0.0002,
    "rút thật 300 nghìn cặp: ≈ 0,949; ≈ 0,355; trung bình ≈ 0,0509")
rec("L09h", F(1, 1 + 101) < F(51, 1002) < F(1 + 5, 1 + 5 + 1 + 95) and round(1 / 102, 4) == 0.0098
    and round(6 / 102, 4) == 0.0588 and round(0.1 / 10000, 5) == 0.00001 and 90 + 5 + 5 == 100,
    "lượt bấm về trễ: Beta(1, 101) ≈ 0,0098 < 0,0509 < Beta(6, 96) ≈ 0,0588; khám phá đều 0,00001; chia 90/5/5")
q = np.random.default_rng(5)
rec("L09i", F(3, 12) == F(1, 4) and alg.irs_beta_post(1, 1, 2, 10) == (3, 9)
    and abs(float((q.beta(3, 9, 400000) > q.beta(51, 951, 400000)).mean()) - 0.983) < 0.003 and round(math.sqrt(27 / (144 * 13)), 3) == 0.120,
    "quiz: Beta(3, 9), trung bình 0,25, thắng ≈ 0,983, độ lệch chuẩn ≈ 0,120")
rec("L09j", round(1 - 0.1 + 0.1 / 10, 2) == 0.91, "ôn: tay tốt nhất 0,91 với xác suất khám phá 0,1, 10 tay")
# đợt C: (1) hook — chạy lại tay lượt xếp theo trung bình với random.Random(0) (cùng thứ tự rút như alg), ghi lượt nào hiện tai nghe mới
import random
rr, ab, seen, clk = random.Random(0), [[1, 1], [51, 951]], [], 0
for t in range(1, 2001):
    i = 0 if F(ab[0][0], sum(ab[0])) >= F(ab[1][0], sum(ab[1])) else 1
    hit = rr.random() < (0.08, 0.05)[i]
    ab[i][0 if hit else 1] += 1
    if i == 0:
        seen.append(t)
        clk += hit
rec("L09k", len(seen) == 19 and clk == 0 and seen[:18] == list(range(1, 19)) and seen[18] == 77,
    "hook: tai nghe mới hiện 19 lần (lượt 1–18 và lượt 77), 0 lượt bấm, sau đó không hiện tới lượt 2000")
# (2) ôn: kẻ cướp nhiều tay 3/10, 0/2, 0,5² = 0,25; (3) độ lệch chuẩn Beta bằng phương sai Fraction ab/((a+b)²(a+b+1))
var = lambda a, b: F(a * b, (a + b) ** 2 * (a + b + 1))
rec("L09l", F(3, 10) == F(3, 10) and F(1, 2) ** 2 == F(1, 4) and var(1, 1) == F(1, 12) and round(math.sqrt(var(1, 1)), 3) == 0.289
    and round(math.sqrt(var(6, 6)), 3) == 0.139 and round(math.sqrt(var(51, 51)), 3) == 0.049 and round(math.sqrt(var(6, 6) / var(51, 51)), 1) == 2.8
    and F(9, 10) + F(1, 10) * F(1, 10) == F(91, 100),
    "ôn: 0,25 bỏ rơi tay tốt; Beta(1,1) √(1/12) ≈ 0,289; Beta(6,6) 0,139 vs Beta(51,51) 0,049 (gấp 2,8); 0,9 + 0,1/10 = 0,91")
# (4) tự kiểm: số hiện trên màn hình là của đúng các bộ rút trong checks
rec("L09m", round(float((np.random.default_rng(0).beta(1, 1, 200000) > np.random.default_rng(1).beta(51, 951, 200000)).mean()), 3) == 0.950
    and round(float((np.random.default_rng(2).beta(1, 20, 200000) > np.random.default_rng(3).beta(51, 951, 200000)).mean()), 3) == 0.357
    and abs(0.357 - p_new_beats(20, 51, 951)) < 3 * math.sqrt(0.355 * 0.645 / 200000),
    "tự kiểm: rút 200 nghìn cặp ≈ 0,950 và ≈ 0,357 (lệch 0,355 dưới 3 sai số chuẩn)")
