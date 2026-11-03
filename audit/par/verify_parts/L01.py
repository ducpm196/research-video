# PAR L01 — tính lại bằng mô phỏng hai lần chạy (máy n lõi thật + một lõi làm cùng bài toán lớn), phân số chính xác và sympy
# (khác `checks`: số thực qua alg.par_gustafson / alg.par_amdahl).
from fractions import Fraction as F

import sympy as sp


def scaled_runs(serial, par_per_core, n, serial_grows=0):
    """Mô phỏng mở rộng yếu: mỗi lõi giữ `par_per_core` giây việc; `serial_grows` giây tuần tự lớn theo cỡ dữ liệu (n lần).
    Trả về (thời gian máy n lõi, thời gian một lõi làm cùng bài toán lớn) bằng cách cộng từng phần việc."""
    tasks = [par_per_core] * n
    t_n = serial + serial_grows * n + max(tasks)  # các lõi chạy cùng lúc
    t_1 = serial + serial_grows * n + sum(tasks)   # một lõi làm lần lượt
    return t_n, t_1


tn, t1 = scaled_runs(10, 90, 16)
rec("L01a", (tn, t1) == (100, 1450) and F(t1, tn) == F(29, 2) and F(29, 2) / 16 == F(29, 32) and round(29 / 32 * 100, 1) == 90.6,
    "mô phỏng: máy 16 lõi 100 s, một lõi 1450 s → 14,5 lần, hiệu suất 29/32 ≈ 90,6%")
q, n = sp.symbols("q n", positive=True)
G = (q + (1 - q) * n) / (q + (1 - q))
s1 = q / (q + (1 - q) * n)  # phần tuần tự đo trên một lõi của bài toán đã phóng to
amd = 1 / (s1 + (1 - s1) / n)
rec("L01b", sp.simplify(G - (q + (1 - q) * n)) == 0 and sp.simplify(amd - G) == 0
    and float(s1.subs({q: sp.Rational(1, 10), n: 16})) * 100 < 0.7 and round(float(s1.subs({q: sp.Rational(1, 10), n: 16})) * 100, 2) == 0.69,
    "sympy: G = q + (1 − q)n; đổi sang cách đo một lõi rồi thay vào Amdahl ra đúng G (mọi q, n); 0,1/14,5 ≈ 0,69%")
amdahl = lambda s, m: 1 / (s + (1 - s) / m)
rec("L01c", [round(1024 - 1023 * x, 1) for x in (0.008, 0.004)] == [1015.8, 1019.9]
    and [round(amdahl(x, 1024)) for x in (0.008, 0.004)] == [111, 201]
    and round(1020 / amdahl(0.004, 1024), 1) == 5.1 and round(1021 / amdahl(0.008, 1024), 1) == 9.2
    and round(0.008 / (1024 - 1023 * 0.008) * 100, 4) == 0.0008,
    "năm 1988: tăng tốc theo cỡ 1015,8 / 1019,9 (đo 1016 / 1020); Amdahl cùng tỉ lệ chỉ 111 / 201 — lệch 5,1 tới 9,2 lần; 0,0008%")
rec("L01d", round(0.1 + 0.9 * 1024, 1) == 921.7 and round((0.1 + 0.9 * 1024) / 1024 * 100) == 90 and float(1 / (F(1, 10) + F(9, 10) / 1024)) < 10,
    "1024 lõi: 921,7, hiệu suất ≈ 90%; mở rộng mạnh dưới 10")
rec("L01e", [round(float(F(100, t) * 100), 1) for t in (100, 102, 105, 111)] == [100.0, 98.0, 95.2, 90.1]
    and [round(float(F(100) / (10 + F(90, m))), 2) for m in (4, 16, 64)] == [3.08, 6.4, 8.77],
    "bảng đo: hiệu suất yếu 100 / 98,0 / 95,2 / 90,1%; mạnh 3,08 / 6,40 / 8,77")
tn3, t13 = scaled_runs(5, 90, 16, serial_grows=5)
rec("L01f", (tn3, t13) == (90 + 85, 85 + 1440) and round(t13 / tn3, 2) == 8.71, "lỗi 3: tuần tự lớn theo dữ liệu → 85 s, 1525/175 ≈ 8,71")
g64 = F(5, 100) + F(95, 100) * 64
a64 = 1 / (F(5, 100) + F(95, 100) / 64)
rec("L01g", round(float(g64), 2) == 60.85 and round(float(g64 / 64) * 100, 1) == 95.1 and round(float(F(5, 100) / g64) * 100, 3) == 0.082
    and round(float(a64), 2) == 15.42 and round(float(a64 / 64) * 100, 1) == 24.1 and round(float(g64 / a64), 2) == 3.95,
    "quiz: 60,85 (95,1%); 0,082%; 15,42 (24,1%); hai lời hứa lệch 3,95 lần")
