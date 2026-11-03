# PAR L00 — tính lại bằng phân số chính xác và mô phỏng lịch chạy từng đơn vị thời gian (khác `checks`: số thực qua alg.par_amdahl).
from fractions import Fraction as F


def run_time(serial, parallel_units, cores):
    """Mô phỏng: 'serial' đơn vị chạy trên một lõi; rồi 'parallel_units' đơn vị việc độc lập, mỗi đơn vị 1 nhịp, chia lần lượt
    cho các lõi rảnh. Trả về số nhịp tới lúc xong (chính xác khi chia hết)."""
    t = serial
    left = parallel_units
    while left > 0:
        left -= min(cores, left)
        t += 1
    return t


# Chương trình 100 giây = 10 giây tuần tự + 90 giây song song, đo bằng đơn vị 1/16 giây để 16 lõi chia hết.
U = 16
t1 = run_time(10 * U, 90 * U, 1)
t16 = run_time(10 * U, 90 * U, 16)
t4 = run_time(10 * U, 90 * U, 4)
rec("L00a", F(t1, U) == 100 and F(t16, U) == F(15625, 1000) and F(t4, U) == F(65, 2) and F(t1, t16) == F(32, 5),
    "mô phỏng nhịp: 1 lõi 100 s, 4 lõi 32,5 s, 16 lõi 15,625 s → 6,4 lần")
S = lambda p, n: 1 / ((1 - p) + p / n)
p9 = F(9, 10)
rec("L00b", S(p9, 16) == F(32, 5) and S(p9, 16) / 16 == F(2, 5) and 1 / (1 - p9) == 10
    and abs(float(S(p9, 16)) - alg.par_amdahl(0.9, 16)) < 1e-12,
    "phân số: S(16) = 32/5, E(16) = 2/5, trần 10; khớp alg.par_amdahl")
vals = [S(p9, 2 ** k) for k in range(7)]
rec("L00c", [round(float(v), 2) for v in vals] == [1.0, 1.82, 3.08, 4.71, 6.4, 7.8, 8.77] and all(a < b for a, b in zip(vals, vals[1:]))
    and all(v < 10 for v in vals) and round(float(S(p9, 32) / S(p9, 16)), 2) == 1.22,
    "đường cong gấp đôi số lõi: 1 → 8,77, tăng dần và dưới 10; 32 so với 16 lõi chỉ 1,22")
# Kiểm bằng đếm giây lõi: 16 lõi × 15,625 s = 250 giây lõi, có ích 100.
rec("L00d", 16 * F(t16, U) == 250 and F(100, 250) == F(2, 5), "đếm giây lõi 250, có ích 100 → 40%")
# Đo ngược p: giải phương trình bằng sympy (đường khác với công thức chuyển vế trên màn hình).
import sympy as sp
x = sp.symbols("x")
p_meas = sp.solve(sp.Eq(1 / ((1 - x) + x / 8), 4), x)[0]
p_back = sp.solve(sp.Eq(1 / ((1 - x) + x / 16), sp.Rational(32, 5)), x)[0]
rec("L00e", p_meas == sp.Rational(6, 7) and p_back == sp.Rational(9, 10) and round(float(p_meas), 3) == 0.857,
    "giải phương trình: S(8) = 4 → p = 6/7 ≈ 0,857; S(16) = 6,4 → p = 0,9")
A = 120 / S(F(6, 7), 32)
B = 120 / S(F(13, 14), 8)
AB = 120 / S(F(13, 14), 32)
rec("L00f", round(float(S(F(6, 7), 32)), 2) == 5.89 and round(float(A), 1) == 20.4 and round(float(S(F(13, 14), 8)), 2) == 5.33
    and B == F(45, 2) and round(float(AB), 1) == 12.1 and round(float(1 - F(6, 7)), 3) == 0.143,
    "quiz: A 20,4 s; B 22,5 s (đúng 45/2); B rồi A 12,1 s; phần tuần tự 1/7 ≈ 0,143")
# Lỗi 3: liệt kê n = 1..200 với chi phí phối hợp 0,005 mỗi lõi.
f = lambda n: 1 / (F(1, 10) + F(9, 10) / n + F(5, 1000) * n)
best = max(range(1, 201), key=f)
rec("L00g", best == 13 and round(float(f(13)), 2) == 4.27 and round(float(f(16)), 2) == 4.23 and round(float(f(64)), 2) == 2.30,
    "chi phí phối hợp: tốt nhất 13 lõi 4,27; 16 lõi 4,23; 64 lõi 2,30")
rec("L00h", F(130, 20) == F(13, 2) and F(100, 20) == 5 and round(float((1 - F(1, 6)) / (1 - F(1, 8))), 3) == 0.952,
    "nền sai 6,5 so với 5; đo ở cỡ thật 6 lần → p ≈ 0,952")
rec("L00i", 1 - F(9, 10) == F(1, 10) and (1 - F(1, 4)) == F(3, 4) and 1 - F(3, 4) == F(1, 4)
    and 1 / (F(1, 10) + F(9, 80)) == F(80, 17) and round(80 / 17, 2) == 4.71,
    "ôn nền: chuyển vế 1 − 1/4 = 0,75 và thử lại; ví dụ khoá CSA: 8 lõi = 80/17 ≈ 4,71")
