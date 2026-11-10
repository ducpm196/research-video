# SEP L11 — tính lại bằng phân số chính xác, mô phỏng, lịch thật và mô hình phạt tự viết (khác `checks` của bài).
import datetime as dt
import math
from fractions import Fraction

import numpy as np

# chặng 1: 365 000 tổ hợp, 54 805 cử tri
k1 = len({(g, z, d, y) for g in range(2) for z in range(5) for d in range(365) for y in range(100)})
p1 = math.exp(54804 * math.log1p(-1 / 365000))
rng = np.random.default_rng(11)
draw = rng.integers(0, 365000, 54805)
_, cnt = np.unique(draw, return_counts=True)
sim1 = float((cnt == 1).sum()) / 54805
rec("L11a", k1 == 365000 and round(365000 / 54805, 1) == 6.7 and round(p1, 2) == 0.86 and abs(sim1 - 0.86) < 0.01
    and Fraction(216, 248) > Fraction(86, 100) and round(216 / 248, 2) == 0.87 and round(132 / 248, 2) == 0.53,
    f"chặng 1: liệt kê 365 000 tổ hợp; (1 − 1/365 000)^54 804 ≈ 0,86; mô phỏng {sim1:.3f}; 216/248 ≈ 87%; 132/248 ≈ 53%")
# chặng 2: gộp dữ liệu
sims = []
for _ in range(20):
    a = rng.integers(0, 8000, 5000)
    _, c = np.unique(a, return_counts=True)
    sims.append((c == 1).sum())
rec("L11b", 2 * 80 == 160 and 2 * 80 * 50 == 8000 and (1 - 1 / 160) ** 4999 < 1e-12 and abs(np.mean(sims) - 2677) < 40
    and round(5000 * math.exp(-4999 / 8000)) in (2676, 2677, 2678),
    f"chặng 2: 8000 tổ hợp, 5000 người → mô phỏng {np.mean(sims):.0f} ≈ 2677 người duy nhất; bộ 160 tổ hợp ≈ 0")
# chặng 3: lịch
rec("L11c", (dt.date(2023, 7, 1) - dt.date(2023, 4, 17)).days == 75 and dt.timedelta(hours=72) == dt.timedelta(days=3)
    and dt.date(2026, 3, 2) + dt.timedelta(days=60) == dt.date(2026, 5, 1),
    "chặng 3: 17/4 → 1/7/2023 = 75 ngày; 72 giờ = 3 ngày; 2/3/2026 + 60 ngày = 1/5/2026")


# chặng 4: mô hình mức phạt tối đa theo Điều 8 (đơn vị tỉ đồng)
def max_fine(kind, base=None, person=False):
    floor = Fraction(3)
    if kind == "mua_ban":
        f = max(10 * Fraction(base), floor) if base else floor
    elif kind == "xuyen_bien_gioi":
        f = max(Fraction(5, 100) * Fraction(base), floor) if base else floor
    else:
        f = floor
    return f / 2 if person else f


rec("L11d", max_fine("mua_ban", Fraction(1, 2)) == 5 and max_fine("xuyen_bien_gioi", 200) == 10 and max_fine("khac", person=True) == Fraction(3, 2)
    and max_fine("xuyen_bien_gioi", 20) == 3 and max_fine("mua_ban", 0) == 3,
    "chặng 4: 10 × 0,5 = 5 tỉ; 5% × 200 = 10 tỉ; cá nhân 1,5 tỉ; ca biên: doanh thu 20 tỉ → 1 tỉ < 3 nên áp 3 tỉ")
t_occ = dt.datetime(2026, 1, 1)
rec("L11e", (t_occ + dt.timedelta(hours=72)).day == 4 and (t_occ + dt.timedelta(days=5) + dt.timedelta(hours=72)) == t_occ + dt.timedelta(days=8)
    and dt.datetime(2026, 11, 6, 17) + dt.timedelta(hours=72) == dt.datetime(2026, 11, 9, 17) and dt.date(2026, 11, 6).weekday() == 4
    and dt.date(2026, 11, 9).weekday() == 0,
    "72 giờ từ khi xảy ra (ngày 3) vs từ khi phát hiện ngày 5 (ngày 8); thứ Sáu 6/11/2026 17:00 + 72 giờ = thứ Hai 9/11 17:00")
# chặng 5: quy mô
users, month = 0, 0
while users < 100000:
    month += 1
    users += 4000
rest, m2 = 30000, 0
while rest < 100000:
    m2 += 1
    rest += 5000
rec("L11f", month == 25 and m2 == 14 and dt.date(2026, 1, 1).replace(year=2031) == dt.date(2031, 1, 1) and 12 // 6 == 2
    and 4000 * 24 < 100000 <= 4000 * 25,
    "chặng 5: 4000 người/tháng chạm 100 000 ở tháng 25; quiz: 30 000 + 5000/tháng → 14 tháng; 1/1/2031; 2 lần cập nhật/năm")
# Thêm 2026-11-09 (đợt C): chặng 2 nay hiện số của bộ B (4000 tổ hợp → ≈ 0,29) thay cho chữ “thấp hơn”; gộp theo mã hồ sơ chung.
rec("L11g", round(math.exp(4999 * math.log1p(-1 / 4000)), 2) == 0.29 and 80 * 50 == 4000,
    "chặng 2: bộ B {năm sinh, tổ} 4000 tổ hợp, 5000 người → (1 − 1/4000)^4999 ≈ 0,29 (qua log1p)")
