# IRS L10 — thiên lệch vị trí, trọng số nghịch đảo xu hướng: tính lại bằng CÁCH KHÁC checks (Fraction; mô phỏng từng người dùng
# “nhìn rồi mới bấm” bằng random.Random; mô phỏng thí nghiệm hoán đổi), rồi đối chiếu alg.irs_ips, irs_ips_spread, irs_propensity_swap.
import random
from fractions import Fraction as F

P = {1: F(1), 2: F(6, 10), 3: F(4, 10), 4: F(3, 10), 5: F(2, 10)}   # xác suất nhìn thấy (minh hoạ)
relA, relB = F(3, 100), F(5, 100)
rec("L10a", F(30, 1000) / P[1] == relA and F(10, 1000) / P[5] == relB and F(10) / P[5] == 50 == alg.irs_ips(10, 0.2)
    and alg.irs_ips(30, 1.0) == 30 and F(30, 1000) / F(10, 1000) == 3,
    "A 0,03; B 0,01/0,2 = 0,05; 10 bấm ở vị trí 5 → 50; tỉ lệ thô 3 lần")
rec("L10b", 1000 * (relA * P[1] + relB * P[5]) == 40 and 1000 * (relB * P[1] + relA * P[2]) == 68,
    "chấm ngoại tuyến: thứ tự cũ 40, mới 68 lượt bấm / 1000")


def users(n, p_see, rel, seed):
    """Từng người: tung đồng xu ‘nhìn thấy’, nếu thấy thì tung ‘liên quan’ — đếm lượt bấm."""
    r = random.Random(seed)
    return sum(1 for _ in range(n) if r.random() < p_see and r.random() < rel)


c = users(200000, 0.2, 0.05, 1)
rec("L10c", abs(c / 200000 - 0.01) < 0.0007 and abs(c / 200000 / 0.2 - 0.05) < 0.0035,
    f"mô phỏng từng người: tỉ lệ thô ≈ {c / 200000:.4f} (sai 5 lần), chia p ≈ {c / 200000 / 0.2:.4f}")
# thí nghiệm hoán đổi: cùng một kết quả mức liên quan 0,25 đặt ở vị trí 1 hoặc 5
c1, c5 = users(100000, 1.0, 0.25, 2), users(100000, 0.2, 0.25, 3)
rec("L10d", abs((c5 / 100000) / (c1 / 100000) - 0.2) < 0.01 and alg.irs_propensity_swap(0.05, 0.25) == 0.2,
    "hoán đổi: tỉ lệ bấm vị trí 5 / vị trí 1 ≈ 0,2 = p5")
# phương sai: lặp nhật ký nhỏ 1000 lần hiện ở p = 0,02, mức liên quan 0,05
r = random.Random(9)
est, cl = [], []
for _ in range(3000):
    k = sum(1 for _ in range(1000) if r.random() < 0.001)
    est.append(k * 50 / 1000)
    cl.append(k * 10 / 1000)


def msd(xs):
    m = sum(xs) / len(xs)
    return m, (sum((x - m) ** 2 for x in xs) / len(xs)) ** 0.5


(m1, s1), (m2, s2) = msd(est), msd(cl)
e1, e2 = alg.irs_ips_spread(1000, 0.02, 0.05), alg.irs_ips_spread(1000, 0.02, 0.05, cap=10)
rec("L10e", abs(m1 - 0.05) < 0.004 and abs(s1 - 0.05) < 0.004 and abs(m2 - 0.01) < 0.001 and abs(s2 - 0.01) < 0.001
    and [round(x, 2) for x in e1] == [0.05, 0.05] and [round(x, 2) for x in e2] == [0.01, 0.01],
    f"không cắt: TB {m1:.3f}, độ lệch chuẩn {s1:.3f}; cắt 10: TB {m2:.3f}, {s2:.3f}")
rec("L10f", F(1) * 50 / 1000 == F(5, 100) and F(1) * min(50, 10) / 1000 == F(1, 100)
    and F(1, 100) / F(3, 100) == F(1, 3) and F(1, 100) / F(1, 3) == F(3, 100) and 1 * 50 == 10 * 5,
    "1 bấm may mắn ở p = 0,02 → 0,05; cắt 10 → 0,01; lỗi 2: p5 sai = 1/3 → B chỉ 0,03; 1·50 = 10·5")
rec("L10g", F(15, 1000) / F(1, 4) == F(6, 100) and F(40, 1000) == F(4, 100) and 15 * 4 == 60
    and F(1, 100) / F(5, 100) == F(1, 5) and F(10, 100) == F(1, 10) and F(4, 100) == F(1, 25)
    and alg.irs_ips(1, 0.05, cap=4) == 4,
    "quiz: C 0,06 > D 0,04; E: 0,2 / 0,1 / 0,04")
rec("L10h", F(2, 10) * F(5, 100) == F(1, 100) and F(1, 100) / F(2, 10) == F(5, 100) and 0.24 > 0.01 > -0.07,
    "ôn 0,2·0,05 = 0,01; chia ngược 0,05; ZH19 trực tuyến −0,07% / +0,01% / +0,24%")
