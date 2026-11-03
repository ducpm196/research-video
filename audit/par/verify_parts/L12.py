# PAR L12 — 8 thẻ mà chỉ nhanh gấp 3: mô phỏng một lượt dữ liệu theo từng lô (một tiến trình nạp ảnh nối tiếp cho mọi thẻ, các thẻ tính
# song song), đếm phút; phân số chính xác cho Amdahl (khác `checks`: alg.par_amdahl số thực).
from fractions import Fraction as F


def epoch_minutes(cards, load_serial, load_parallel, compute, batches=800):
    """Một lượt = `batches` lô. Phần nạp tuần tự (load_serial phút cả lượt) do MỘT tiến trình làm, không chồng với tính (mô hình Amdahl);
    phần nạp song song và phần tính chia đều cho các thẻ, mỗi thẻ một bộ nạp riêng."""
    t = F(0)
    for _ in range(batches // cards):
        t += F(load_serial, batches) * cards                        # nạp nối tiếp đủ lô cho cả `cards` thẻ
        t += (F(load_parallel, batches) + F(compute, batches))      # các thẻ cùng nạp phần song song rồi cùng tính lô của mình
    return t


one = epoch_minutes(1, 25, 0, 75)
eight = epoch_minutes(8, 25, 0, 75)
sixteen = epoch_minutes(16, 25, 0, 75)
fixed8 = epoch_minutes(8, 2, 23, 75)
fixed16 = epoch_minutes(16, 2, 23, 75)


def amdahl(p, n):
    return 1 / ((1 - p) + p / n)


rec("L12a", one == 100 and eight == F(1100, 32) and float(eight) == 34.375 and round(float(one / eight), 2) == 2.91
    and amdahl(F(3, 4), 8) == one / eight,
    "mô phỏng từng lô: 1 thẻ 100 phút, 8 thẻ 34,375 phút → 2,91 = Amdahl p = 3/4 (phân số chính xác)")
rec("L12b", round(float(one / sixteen), 2) == 3.37 and round(float(amdahl(F(3, 4), 16) / amdahl(F(3, 4), 8) - 1), 2) == 0.16
    and amdahl(F(3, 4), 10 ** 12) < 4 and round(float(amdahl(F(3, 4), 10 ** 12)), 6) == 4.0,
    "16 thẻ 3,37 (chỉ hơn 16%); trần tiến tới 4")
rec("L12c", float(fixed8) == 14.25 and round(float(one / fixed8), 2) == 7.02 and round(float(one / fixed16), 2) == 12.31
    and amdahl(F(98, 100), 8) == one / fixed8,
    "nạp song song (2 phút tuần tự, 23 phút chia cho các thẻ): 8 thẻ 14,25 phút → 7,02; 16 thẻ 12,31")
rec("L12d", round(float(amdahl(F(3, 4), 8)) / 8 * 100, 1) == 36.4 and round(float(amdahl(F(98, 100), 8)) / 8 * 100, 1) == 87.7
    and 25 + F(50, 8) == F(125, 4) and round(100 / 31.25, 1) == 3.2,
    "hiệu suất 36,4% và 87,7%; tối ưu nhân tính 1,5 lần: 31,25 phút, gấp 3,2")
rec("L12e", round(100 / float(amdahl(F(3, 4), 16)), 1) == 29.7 and amdahl(F(3, 4), 16) < 5 < amdahl(F(98, 100), 8)
    and round(float(amdahl(F(9, 10), 8)), 2) == 4.71 and 100 / amdahl(F(9, 10), 8) == F(85, 4) and 100 / amdahl(F(9, 10), 16) == F(125, 8)
    and float(amdahl(F(9, 10), 16)) == 6.4,
    "quiz: hạn 20 phút cần gấp 5; A 29,7 phút không đạt, B 14,25 đạt; nếu còn 10%: 8 thẻ 21,25, 16 thẻ 15,625 (6,4 lần)")
rec("L12f", round(float(amdahl(F(9, 10), 16)), 2) == 6.4 and round(1 / (0.1 + 0.9 / 16), 2) == 6.4,
    "ôn nền bài 0: 90% song song, 16 lõi → 6,4")
