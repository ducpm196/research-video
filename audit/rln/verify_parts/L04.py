# RLN L04 — tính lại bằng phân số chính xác, mô hình hợp lý cực đại giải bằng sympy, và mô phỏng numpy độc lập
# (khác `checks`: alg.rln_batch_mc / rln_batch_td quét lặp, alg.rln_td_walk dùng random.Random).
from fractions import Fraction as F

import numpy as np
import sympy as sp

# Giáo án: 4, 6, 8 → 6; TD: 6 + 0,5·(1 + 0,9·10 − 6) = 8
rec("L04a", F(4 + 6 + 8, 3) == 6 and 6 + F(1, 2) * (1 + F(9, 10) * 10 - 6) == 8
    and [F(4), F(4) + F(1, 2) * 2, F(5) + F(1, 3) * 3] == [4, 5, 6] and F(4) + F(1, 2) * 2 + F(1, 2) * (8 - 5) == F(13, 2),
    "giáo án: trung bình 6; cộng dồn 4 → 5 → 6; α = 0,5 cho 6,5; TD cho 8")
# Ví dụ 6.4: Monte Carlo theo định nghĩa (đếm phân số), TD theo lô = giá trị đúng của mô hình ước lượng hợp lý cực đại (giải hệ)
eps = [[("A", 0), ("B", 0)]] + [[("B", 1)]] * 6 + [[("B", 0)]]
retB = [sum(r for _, r in ep[i:]) for ep in eps for i, (s, _) in enumerate(ep) if s == "B"]
retA = [sum(r for _, r in ep[i:]) for ep in eps for i, (s, _) in enumerate(ep) if s == "A"]
VA, VB = sp.symbols("VA VB")
sol = sp.solve([sp.Eq(VB, sp.Rational(6, 8) * 1 + sp.Rational(2, 8) * 0), sp.Eq(VA, 0 + 1 * VB)], [VA, VB])
mc = alg.rln_batch_mc(eps)
td = alg.rln_batch_td(eps, alpha=0.05, sweeps=3000)
rec("L04b", F(sum(retB), len(retB)) == F(3, 4) and F(sum(retA), len(retA)) == 0 and sol[VA] == sp.Rational(3, 4)
    and mc == {"A": 0.0, "B": 0.75} and abs(td["A"] - 0.75) < 1e-6 and abs(td["B"] - 0.75) < 1e-6,
    "Ví dụ 6.4: V(B) = 3/4; Monte Carlo V(A) = 0; mô hình suy từ dữ liệu (sympy) V(A) = 3/4 = TD theo lô")
# Bước ngẫu nhiên: giải hệ tuyến tính bằng ma trận (numpy.linalg.solve) thay cho quét lặp
M = np.eye(5)
b = np.zeros(5)
for k in range(5):
    if k > 0:
        M[k, k - 1] -= 0.5
    if k < 4:
        M[k, k + 1] -= 0.5
    else:
        b[k] += 0.5
v = np.linalg.solve(M, b)
rec("L04c", np.allclose(v, [k / 6 for k in range(1, 6)]), "bước ngẫu nhiên: giải hệ 5 ẩn → 1/6 … 5/6")
# Mô phỏng TD(0) độc lập bằng numpy (hạt giống khác), so cùng bậc với số trên màn hình (trung bình 100 lần chạy)


def td_np(alpha, n_ep, rng):
    V = np.full(5, 0.5)
    for _ in range(n_ep):
        s = 2
        while True:
            s2 = s + (1 if rng.random() < 0.5 else -1)
            r = 1.0 if s2 == 5 else 0.0
            nxt = V[s2] if 0 <= s2 < 5 else 0.0
            V[s] += alpha * (r + nxt - V[s])
            if not 0 <= s2 < 5:
                break
            s = s2
    return np.sqrt(np.mean((V - np.arange(1, 6) / 6) ** 2))


rng = np.random.default_rng(404)
e10 = np.mean([td_np(0.1, 10, rng) for _ in range(300)])
e100 = np.mean([td_np(0.1, 100, rng) for _ in range(300)])
e1000a = np.mean([td_np(0.1, 1000, rng) for _ in range(100)])
e1000b = np.mean([td_np(0.02, 1000, rng) for _ in range(100)])
rec("L04d", abs(td_np(0.1, 0, rng) - 0.236) < 0.001 and abs(e10 - 0.128) < 0.012 and abs(e100 - 0.055) < 0.008
    and abs(e1000a - 0.055) < 0.008 and abs(e1000b - 0.024) < 0.005 and e1000b < e1000a,
    f"mô phỏng numpy: độ lệch 0,236 → {e10:.3f} → {e100:.3f}; 1000 lượt: α 0,1 {e1000a:.3f}, α 0,02 {e1000b:.3f}")
rec("L04e", 2 + F(9, 10) * 4 - 5 == F(3, 5) and 5 + F(1, 10) * F(3, 5) == F(253, 50) and 5 + F(1, 10) * 2 == F(26, 5)
    and 1 + F(9, 10) * 0 == 1 and 6 + 1 * (8 - 6) == 8,
    "quiz: đen-ta 0,6 → 5,06; chờ hết lượt 5,2; lỗi 1: đích 1 thay vì 10; lỗi 2: α = 1 cho 8")
