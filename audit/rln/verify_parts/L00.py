# RLN L00 — tính lại bằng phân số chính xác (Fraction), tổng cấp số nhân dạng đóng và mô phỏng kết thúc ngẫu nhiên,
# khác `checks` của bài (alg.rln_return cộng số thực xuôi / ngược).
from fractions import Fraction as F
import math

import numpy as np


def ret(rs, g):  # cộng xuôi bằng phân số chính xác
    return sum(F(g) ** k * F(r) for k, r in enumerate(rs))


g9, g7 = F(9, 10), F(7, 10)
rec("L00a", ret([0, 0, 10], g9) == F(81, 10) and ret([0, 0, 10], g7) == F(49, 10)
    and ret([0, 0, 10], g9) > 6 > ret([0, 0, 10], g7)
    and abs(float(ret([0, 0, 10], g9)) - alg.rln_return([0, 0, 10], 0.9)) < 1e-12,
    "hook/quiz: 0, 0, 10 → 8,1 (γ = 0,9) > 6 > 4,9 (γ = 0,7)")
rec("L00b", ret([-1, -1, 10], g9) == F(31, 5) and ret([-1, 10], g9) == 8 and ret([10], g9) == 10
    and [round(x, 10) for x in alg.rln_returns_backward([-1, -1, 10], 0.9)] == [6.2, 8.0, 10.0],
    "ví dụ: G0 = 31/5 = 6,2; G1 = 8; G2 = 10 (phân số) khớp đệ quy ngược của checklib")
# Tổng 1 mãi mãi: dạng đóng (1 − γ^n)/(1 − γ) bằng phân số, và mô phỏng: kết thúc mỗi bước với xác suất 1 − γ thì kỳ vọng số bước = 1/(1 − γ)
rec("L00c", [round(float((1 - g9 ** n) / (1 - g9)), 3) for n in (10, 50, 100)] == [6.513, 9.948, 10.0]
    and 1 / (1 - g9) == 10 and F(1) / (1 - F(99, 100)) == 100,
    "tổng n số hạng 6,513 / 9,948 / 10,000; giới hạn 10; γ = 0,99 → 100")
rng = np.random.default_rng(2026)
steps = rng.geometric(0.1, size=200000)  # số phần thưởng 1 nhận được trước khi dừng (xác suất dừng 0,1 mỗi bước)
rec("L00d", abs(steps.mean() - 10) < 0.05, f"mô phỏng: dừng với xác suất 0,1 mỗi bước → trung bình {steps.mean():.3f} ≈ 10 phần thưởng")
rec("L00e", ret([0, 10], g9) == 9 and ret([0, 0, 0, 10], g9) == F(729, 100)
    and ret([2, 12], g9) == F(64, 5) and ret([2, 2, 2, 12], g9) == F(1771, 125)
    and ret([0, 10], g9) > ret([0, 0, 0, 10], g9) and ret([2, 12], g9) < ret([2, 2, 2, 12], g9),
    "lỗi 4: 9 > 7,29 nhưng cộng 2 mỗi bước: 12,8 < 14,168 → đổi lựa chọn")
rec("L00f", F(81, 100) * 10 != F(729, 1000) * 10 and F(729, 100) == F(729, 1000) * 10,
    "lỗi 2: lệch một bước cho 7,29 thay vì 8,1")
gstar = math.sqrt(0.6)
rec("L00g", round(gstar, 3) == 0.775 and abs(10 * gstar ** 2 - 6) < 1e-12
    and 10 * 0.776 ** 2 > 6 > 10 * 0.774 ** 2,
    "quiz câu 2: γ > √0,6 ≈ 0,775 (hai phía của điểm hoà)")
rec("L00h", ret([2, 3], g9) == F(47, 10) and 0.9 * 2 + 0.81 * 3 - 4.23 < 1e-12 and F(9, 10) * (2 + F(9, 10) * 3) == F(423, 100)
    and sum(F(1, 2) ** k for k in range(4)) == F(15, 8),
    "công thức: chuỗi 2, 3 → 4,7; ôn nền: thừa số chung 4,23; 1 + 0,5 + 0,25 + 0,125 = 1,875")
