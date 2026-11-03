# RLN L08 — tính lại bằng phân số chính xác, sympy (σ(0,075)), và mô phỏng numpy một bài toán nhỏ: nhà phê bình học bằng sai phân
# thời gian tới hội tụ, so lợi thế trung bình với Q − V tính bằng định nghĩa — khác `checks` (số thực viết tay, random.Random(8)).
from fractions import Fraction as F

import numpy as np
import sympy as sp

g = F(9, 10)
rec("L08a", 1 + g * 5 - 4 == F(3, 2) and 1 + g * 2 - 4 == F(-6, 5) and (1 + g * 5) - 4 == F(3, 2),
    "lợi thế 1,5; nhà phê bình sai (V(s′) = 2) → −1,2; định nghĩa Q − V = 1,5")
th = F(1, 10) * F(3, 2) * F(1, 2)
rec("L08b", th == F(3, 40) and round(float(1 / (1 + sp.exp(-sp.Rational(3, 40)))), 3) == 0.519
    and 4 + F(1, 10) * F(3, 2) == F(83, 20) and 1 + g * 5 - F(83, 20) == F(27, 20),
    "một bước: θ = 0,075, π(a1) ≈ 0,519; V(s) = 4,15; đen-ta lần sau 1,35")
rec("L08c", F(1, 2) * (1 + g * 5) + F(1, 2) * (1 + g * 3) - 4 == F(3, 5) and (1 + g * 4) - 4 == F(3, 5)
    and 1 + g * 14 - 14 == F(-2, 5) and -(1 - g) * 10 == -1,
    "s′ ngẫu nhiên: kỳ vọng đen-ta 0,6 = Q − V; lệch đều +10 → −0,4 (lệch −(1 − γ)·10 = −1)")
rec("L08d", 2 + g * 5 - 6 == F(1, 2) and 6 + F(1, 5) * F(1, 2) == F(61, 10) and F(1, 10) * F(1, 2) * F(1, 2) == F(1, 40)
    and 2 + 0 - 6 == -4 and 1 + 0 - 4 == -3,
    "quiz: đen-ta 0,5, V 6,1, θ 0,025; kết thúc → −4; lỗi 2: −3")
# Mô phỏng: ô s (thưởng 1) sang ô 5 hoặc 3 (kết thúc với lợi nhuận đúng bằng giá trị đó, γ = 0,9); nhà phê bình học V tới hội tụ
rng = np.random.default_rng(88)
V = {"s": 0.0}
deltas = []
for k in range(60000):
    v2 = 5.0 if rng.random() < 0.5 else 3.0
    d = 1 + 0.9 * v2 - V["s"]
    V["s"] += 0.01 * d
    if k > 20000:
        deltas.append(1 + 0.9 * v2 - 4.0)   # lợi thế ước lượng khi V(s) = 4 cố định như bài
rec("L08e", abs(V["s"] - 4.6) < 0.1 and abs(np.mean(deltas) - 0.6) < 0.02,
    f"mô phỏng: nhà phê bình hội tụ về V(s) = {V['s']:.2f} ≈ 4,6 = Q; trung bình đen-ta (V = 4) {np.mean(deltas):.3f} ≈ 0,6")
