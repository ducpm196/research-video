# IRS L08 — phản hồi ngầm, lấy mẫu âm: tính lại lũy thừa bằng căn lặp và lôgarit, kiểm phần mẫu âm bằng MÔ PHỎNG lấy mẫu thật
# (numpy, hạt giống cố định), phân số chính xác cho phần của người tích cực (khác `checks`: alg.irs_neg_probs, alg.irs_logq).
from fractions import Fraction as F
import math
import numpy as np

rec("L08a", round(math.sqrt(math.sqrt(16)) ** 3, 9) == 8 and round(math.sqrt(math.sqrt(100)) ** 3, 2) == 31.62
    and round(math.exp(0.75 * math.log(100)), 2) == 31.62 and round(math.sqrt(math.sqrt(81)) ** 3, 9) == 27 and round(math.sqrt(math.sqrt(10)) ** 3, 2) == 5.62,
    "16^0,75 = 8; 100^0,75 ≈ 31,62 (căn lặp và qua lôgarit); 81^0,75 = 27; 10^0,75 ≈ 5,62")
w = np.array([100, 10, 1.]) ** 0.75
share = w / w.sum()
rng = np.random.default_rng(0)
draws = rng.choice(3, size=2_000_000, p=share)
emp = np.bincount(draws, minlength=3) / draws.size
rec("L08b", [round(x, 3) for x in share] == [0.827, 0.147, 0.026] and np.allclose(emp, share, atol=0.002) and round(w.sum(), 2) == 38.25
    and [round(x, 3) for x in alg.irs_neg_probs([100, 10, 1])] == [0.827, 0.147, 0.026],
    "mũ 0,75: phần 0,827 / 0,147 / 0,026 (mô phỏng 2 triệu lượt lấy mẫu khớp)")
rec("L08c", [F(c, 111) for c in (100, 10, 1)] == [F(100, 111), F(10, 111), F(1, 111)] and round(100 / 111, 3) == 0.901 and round(1 / 111, 3) == 0.009
    and round(share[2] / (1 / 111), 1) == 2.9, "theo tần suất 0,901 / 0,090 / 0,009; món hiếm được chọn gấp 2,9 lần")
r2 = np.array([100, 1.]) ** 0.75
rec("L08d", round(r2[0] / r2[1], 1) == 31.6 and round(1 / r2.sum(), 3) == 0.031 and F(100, 101) == F(100, 101) and round(1 / 101, 3) == 0.01
    and round((r2[1] / r2.sum()) / (1 / 101), 1) == 3.1 and round(100 / 101 * 100, 1) == 99.0 and round(r2[0] / r2.sum() * 100, 1) == 96.9,
    "A 100 lần, B 1 lần: 31,6 : 1, phần B 0,031 so với 0,010 (gấp 3,1); A 99% → 96,9%")
rec("L08e", [1 + 40 * r for r in (0, 1, 3)] == [1, 41, 121], "độ tin cậy 1 + 40 · r: 1, 41, 121")
# hiệu chỉnh: −ln p tính bằng chuỗi ln(1/p) = 2·atanh((1/p − 1)/(1/p + 1))
lnq = lambda x: 2 * sum(((x - 1) / (x + 1)) ** (2 * k + 1) / (2 * k + 1) for k in range(400))
rec("L08f", round(lnq(50), 3) == 3.912 and round(lnq(2), 3) == 0.693 and round(1.5 + lnq(50), 3) == 5.412 and round(lnq(50) - lnq(2), 3) == 3.219
    and abs(alg.irs_logq(1.5, 0.02) - (1.5 + lnq(50))) < 1e-9, "−ln 0,02 ≈ 3,912; −ln 0,5 ≈ 0,693; 1,5 → 5,412; chênh 3,219")
rec("L08g", F(1000, 1990) == F(100, 199) and round(1000 / 1990 * 100, 1) == 50.3 and F(10, 1000) == F(1, 100),
    "người tích cực: 1000/1990 ≈ 50,3%; cố định 10 mẫu → 1%")
q = np.array([81, 1.]) ** 0.75
rec("L08h", round(q[1] / q.sum(), 4) == 0.0357 and round(1 / 82, 4) == 0.0122 and round(1 / 3, 3) == 0.333,
    "quiz: phần của D 1/28 ≈ 0,0357 so với 1/82 ≈ 0,0122; chia đều 0,333")
