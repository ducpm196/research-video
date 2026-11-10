# IRS L12 — tình huống ngân sách 100 ms (số minh hoạ): tính lại bằng CÁCH KHÁC checks (Fraction, dò tuyến tính số ứng viên lớn nhất,
# mô phỏng từng yêu cầu với mảnh song song, mô phỏng ba tầng độc lập để thấy “cộng phân vị 99” là cận an toàn), đối chiếu alg.irs_*.
import random
from fractions import Fraction as F

ms = F(5, 100)
rec("L12a", 10000 * ms == 500 and 10 + 1000 * ms + 20 == 80 and F(10 ** 7) * ms / 1000 == 500 and F(500, 100) == 5
    and alg.irs_latency([10, 1000 * 0.05, 20]) == 80,
    "chấm thẳng 10 000 → 500 ms; hai tầng 80 ms; cả kho 10 triệu → 500 giây, nhanh 100 lần vẫn 5 giây")


def most(budget, fixed, per):  # dò tuyến tính: số ứng viên lớn nhất còn vừa ngân sách
    n = 0
    while fixed + (n + 1) * per <= budget:
        n += 1
    return n


rec("L12b", most(100, 40, ms) == 1200 == alg.irs_max_candidates(100, 40, 0.05) and most(100, 30, ms) == 1400
    and most(100, 40, F(1, 10)) == 600 == alg.irs_max_candidates(100, 40, 0.1) and 1400 - F(10) / ms == 1200,
    "dò tuyến tính: 1200 (chừa 10 ms), 1400 (không chừa), 600 với mô hình 0,1 ms")
rec("L12c", 8 + 45 + 15 == 68 and 15 + 70 + 30 == 115 and F(70, 1000) == F(7, 100) and 15 + 600 * F(7, 100) + 30 == 87
    and 10 + 2000 * F(5, 1000) + 400 * F(1, 10) + 20 + 5 + 5 == 90,
    "trung bình 68, phân vị 99 cộng lại 115, 600 ứng viên → 87; phương án C → 90 ms")
r = random.Random(4)
slow = sum(any(r.random() < 0.01 for _ in range(10)) for _ in range(100000)) / 100000
slow100 = sum(any(r.random() < 0.01 for _ in range(100)) for _ in range(20000)) / 20000
rec("L12d", abs(slow - 0.0956) < 0.004 and abs(slow100 - 0.634) < 0.012 and round(alg.irs_tail_any(0.01, 10), 3) == 0.096
    and round(alg.irs_tail_any(0.01, 100), 3) == 0.634 and round(float(1 - F(99, 100) ** 10), 3) == 0.096,
    f"mô phỏng từng yêu cầu: 10 mảnh ≈ {slow:.4f}, 100 mảnh ≈ {slow100:.3f}")


# “cộng phân vị 99 của các tầng thường lớn hơn phân vị 99 thật của tổng”: ba tầng độc lập, mỗi tầng 2% số yêu cầu bị chậm thêm
def stage(r, base, extra):
    return base + (extra if r.random() < 0.02 else 0) + r.random()


rr = random.Random(5)
N = 100000
a = [stage(rr, 7, 8) for _ in range(N)]
b = [stage(rr, 44, 25) for _ in range(N)]
c = [stage(rr, 14, 15) for _ in range(N)]
p99 = lambda xs: sorted(xs)[int(0.99 * len(xs)) - 1]
tot = [x + y + z for x, y, z in zip(a, b, c)]
rec("L12e", p99(tot) < p99(a) + p99(b) + p99(c), f"mô phỏng ba tầng: p99 của tổng {p99(tot):.1f} < tổng p99 {p99(a) + p99(b) + p99(c):.1f} ms")
xs = sorted(list(range(1, 100)) + [250])
rec("L12f", xs[98] == 99 and F(sum(xs), 100) == F(5200, 100) and 0.80 < 0.83 < 0.88 < 0.90 < 0.93 and round(1 - 0.88, 2) == 0.12
    and 1000 + 10 * 1000 == 11000,
    "phân vị 99 của 100 lần đo = 99, trung bình 52; bảng độ phủ minh hoạ tăng dần; 12% bị bỏ; ôn 11 000 phép")
# Thêm 2026-11-09 (đợt C, bài tự đứng): phần ôn nay giảng đổi đơn vị và phân vị 99 bằng hai bộ đo; móc câu nói rõ kho 10 triệu
#   (10 000 sản phẩm chỉ là một phần nghìn); bước 4 chừa 13 ms cho xếp lại; phép 0,99 mũ 10 tách “cả 10 mảnh nhanh”.
ys = sorted([10] * 95 + [200] * 5)
rec("L12g", F(500, 1000) == F(1, 2) and ys[98] == 200 and F(sum(ys), 100) == F(195, 10) and F(99 * 100, 2) == 4950
    and F(10 ** 7, 10000) == 1000 and 100 - (15 + 600 * F(7, 100) + 30) == 13 and round(float(F(99, 100) ** 10), 3) == 0.904,
    "500 ms = 0,5 giây; 95 lần 10 ms + 5 lần 200 ms: trung bình 19,5, phân vị 99 = 200; 1+…+99 = 4950; còn 13 ms; 0,99^10 ≈ 0,904")
