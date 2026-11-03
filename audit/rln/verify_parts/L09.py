# RLN L09 — tính lại bằng phân số chính xác và hàm từng khúc viết lại từ hình (không dùng min), mô phỏng lấy mẫu theo chính sách cũ,
# lưới số để kiểm “cận dưới”, khác `checks` của bài (alg.rln_ppo_clip dùng min/max số thực).
from fractions import Fraction as F

import numpy as np

e = F(1, 5)


def piece(r, A):  # đọc thẳng từ hình: A > 0 thì đi ngang sau 1 + ε; A < 0 thì đi ngang trước 1 − ε
    r, A = F(r), F(A)
    if A >= 0:
        return (r if r < 1 + e else 1 + e) * A
    return (r if r > 1 - e else 1 - e) * A


cases = {(F(3, 2), 2): F(12, 5), (F(1, 2), -2): F(-8, 5), (F(1, 2), 2): F(1), (F(3, 2), -2): F(-3)}
rec("L09a", all(piece(r, A) == v and abs(alg.rln_ppo_clip(float(r), A) - float(v)) < 1e-12 for (r, A), v in cases.items()),
    "bốn mẫu ví dụ: 2,4 / −1,6 / 1 / −3 (phân số, hàm từng khúc) khớp checklib")
q = [piece(F(11, 10), 3), piece(F(7, 5), -1), piece(F(7, 10), -1)]
rec("L09b", q == [F(33, 10), F(-7, 5), F(-4, 5)] and sum(q) / 3 == F(11, 30) and round(float(F(11, 30)), 3) == 0.367,
    "câu đố: 3,3 / −1,4 / −0,8; trung bình 11/30 ≈ 0,367")
rng = np.random.default_rng(9)
acts = rng.random(400000) < 0.5  # chính sách cũ 0,5 / 0,5; hành động 1 có A = +2, hành động 2 có A = −2
w = np.where(acts, 0.6 / 0.5, 0.4 / 0.5)
Aa = np.where(acts, 2.0, -2.0)
rec("L09c", abs((w * Aa).mean() - 0.4) < 0.01 and F(6, 10) * 2 + F(4, 10) * (-2) == F(2, 5),
    f"mô phỏng 400 000 mẫu theo chính sách cũ: trung bình ρ·A = {(w * Aa).mean():.4f} ≈ 0,4 = lợi thế trung bình dưới chính sách mới")
grid = [F(k, 20) for k in range(1, 61)]
rec("L09d", all(piece(r, A) <= r * A for r in grid for A in (-3, -2, -1, 1, 2, 3))
    and piece(3, 2) == F(12, 5) and 3 * 2 == 6,
    "cận dưới bi quan: L ≤ ρ·A trên lưới ρ = 0,05 … 3; ρ = 3, A = 2 → 2,4 thay vì 6")
rec("L09e", (piece(F(1501, 1000), 2) - piece(F(1499, 1000), 2)) == 0 and (piece(F(1001, 1000), 2) - piece(F(999, 1000), 2)) / F(2, 1000) == 2,
    "độ dốc: 0 khi ρ = 1,5 (bị cắt), 2 khi ρ = 1 (trong đoạn)")
rec("L09f", F(2048, 64) * 10 == 320 and F(2048, 64) * 30 == 960 and F(6, 10) / F(4, 10) == F(3, 2) and F(2, 10) / F(4, 10) == F(1, 2)
    and 7 * 3 == 21 and sorted([0.76, 0.82, 0.70])[-1] == 0.82,
    "320 / 960 bước gradient; ρ = 1,5 và 0,5; 21 lần chạy; biên 0,2 tốt nhất trong ba biên (Bảng 1, CITED)")
