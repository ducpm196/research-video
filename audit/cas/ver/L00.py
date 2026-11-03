# CAS L00 — phương pháp hậu kiểm. Tính lại bằng đường KHÁC `checks` của bài: datetime thay phép trừ phút, Fraction + liệt kê thay số thực.
import datetime as dt
import itertools
from fractions import Fraction as F

d = dt.date(2015, 10, 21)
T = lambda hm: dt.datetime.combine(d, dt.time(*map(int, hm.split(":"))))
mins = lambda a, b: int((T(b) - T(a)).total_seconds() // 60)
rec("L00a", mins("14:54", "16:00") == 66, "bản mẫu: 14:54 → 16:00 = 66 phút, khớp “down for 66 minutes”")
rec("L00b", (mins("14:54", "15:01"), mins("14:54", "15:36"), mins("16:00", "16:30")) == (7, 42, 30), "tới công bố 7, tới giảm nhẹ 42, tới đóng 30 phút")
rec("L00c", round(F(1_210_000_000, 66) / 10 ** 6, 1) == F(183, 10) or abs(1_210_000_000 / 66 / 1e6 - 18.3) < 0.05, "1,21 tỉ / 66 ≈ 18,3 triệu mỗi phút")
types = "mitigate prevent process prevent prevent prevent prevent prevent other".split()
rec("L00d", [types.count(k) for k in ("mitigate", "prevent", "process", "other")] == [1, 6, 1, 1] and len(types) == 9, "9 việc: 1 / 6 / 1 / 1")

# ba lớp, mỗi lớp 10 ô, 1 ô là lỗ (ô 0): liệt kê thay cho 0,1 mũ 3
grid = list(itertools.product(range(10), repeat=3))
indep = F(sum(all(c == 0 for c in g) for g in grid), len(grid))
shared = F(sum(1 for a in range(10) if a == 0), 10)          # cùng giả định: cả ba lớp nhìn cùng một ô
rec("L00e", indep == F(1, 1000) and F(1000) * indep == 1, "độc lập: 1/1000 = 0,1% (1 lỗi trong 1000)")
rec("L00f", shared == F(1, 10) and shared / indep == 100, "chung giả định: 1/10 = 10%, gấp 100 lần")
rec("L00g", F(1, 10) ** 4 == F(1, 10000) and F(2, 10) ** 2 == F(4, 100), "lớp thứ tư độc lập: 0,01%; làm thử 0,2 mũ 2 = 0,04")
# câu đố: 10:05 → 10:55 và 10:05 → 10:20; người duyệt + chạy thử độc lập 10% · 10% = 1%
rec("L00h", (mins("10:05", "10:55"), mins("10:05", "10:20")) == (50, 15) and F(1, 10) * F(1, 10) == F(1, 100), "quiz: 50 phút, 15 phút; 1%")
