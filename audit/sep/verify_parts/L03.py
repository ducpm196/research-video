# SEP L03 — tính lại bằng phân số chính xác và dò lưới (khác `checks`: số thực, chia trực tiếp).
from fractions import Fraction as F


def score(inc, yrs):
    return F(1, 2) * inc + 2 * yrs


rec("L03a", score(20, 3) == 16 and score(28, 3) == 20 and score(20, 5) == 20 and score(24, 4) == 20 and score(27, 3) == F(39, 2),
    "chị Hoa 16 điểm; 28 triệu hoặc 5 năm hoặc (24 triệu, 4 năm) → 20; 27 triệu → 19,5")
grid_inc = min(F(k, 2) for k in range(0, 200) if score(F(k, 2), 3) >= 20)
grid_yr = min(F(k, 10) for k in range(0, 200) if score(20, F(k, 10)) >= 20)
rec("L03b", grid_inc == 28 and grid_yr == 5, "dò lưới 0,5 triệu / 0,1 năm: nhỏ nhất 28 triệu, 5 năm")
rec("L03c", score(30, 1) == 17 and (20 - 17) / F(1, 2) == 6 and F(20 - 17, 2) == F(3, 2) and score(36, 1) == 20 and score(30, F(5, 2)) == 20,
    "anh Nam 17; +6 triệu hoặc +1,5 năm; thay ngược 36 triệu / 2,5 năm → 20")


def true_model(inc, yrs):
    return score(inc, yrs) >= 20 and yrs >= 2


rec("L03d", score(36, 1) >= 20 and not true_model(36, 1) and not any(true_model(x, 1) for x in range(0, 1000)),
    "mô hình thật có luật ≥ 2 năm: 36 triệu, 1 năm bị từ chối; với 1 năm không thu nhập nào đủ")


def q(inc, yrs, asset):
    return F(2, 5) * inc + 3 * yrs + 5 * asset


rec("L03e", q(25, 2, 0) == 16 and (25 - 16) / F(2, 5) == F(45, 2) and F(9, 3) == 3 and q(25, 2, 1) == 21
    and q(35, 2, 1) == 25 and q(25, 5, 0) == 25 and round(float(F(4, 3)), 2) == 1.33 and q(25, F(10, 3), 1) == 25,
    "quiz: 16 điểm, +22,5 triệu hoặc +3 năm; có tài sản 21 → +10 triệu (35 → 25) hoặc +4/3 năm")
# Thêm 2026-11-09 (đợt C): phần “nhắc lại từ đầu” về trọng số: 21 triệu, 3 năm → 16,5; 20 triệu, 4 năm → 18.
rec("L03g", F(1, 2) * 21 + 2 * 3 == F(33, 2) and F(1, 2) * 20 + 2 * 4 == 18, "trọng số: +1 triệu → +0,5 điểm (16,5); +1 năm → +2 điểm (18)")
