# RLN L01 — tính lại bằng giải hệ tuyến tính dạng ma trận (numpy.linalg.solve, sympy phân số) và mô phỏng Monte Carlo
# (chơi thật nhiều lượt theo chính sách, cắt ở 300 bước), khác `checks` của bài (lặp quét alg.rln_eval / số thực).
import numpy as np
import sympy as sp

g = sp.Rational(9, 10)
# trạng thái 0 = A, 1 = B; V = r_π + γ P_π V  →  (I − γ P_π) V = r_π
def solve(P, r, gam):
    M = sp.eye(2) - gam * sp.Matrix(P)
    return list(M.LUsolve(sp.Matrix(r)))

v1 = solve([[0, 1], [1, 0]], [1, 0], g)                                   # chính sách 1: A → B, B → A
v2 = solve([[sp.Rational(1, 2), sp.Rational(1, 2)], [1, 0]], [sp.Rational(1, 2), 0], g)  # chính sách 2: tung đồng xu ở A
rec("L01a", v1 == [sp.Rational(100, 19), sp.Rational(90, 19)] and [round(float(x), 3) for x in v1] == [5.263, 4.737],
    "chính sách 1: (I − γP)V = r cho V = (100/19, 90/19) ≈ (5,263; 4,737)")
rec("L01b", v2 == [sp.Rational(100, 29), sp.Rational(90, 29)] and [round(float(x), 3) for x in v2] == [3.448, 3.103],
    "chính sách 2: V = (100/29, 90/29) ≈ (3,448; 3,103)")
m = {'A': {'o': [(1, 0, 'A')], 'sang': [(1, 1, 'B')]}, 'B': {'ve': [(1, 0, 'A')]}}
e1 = alg.rln_eval(m, {'A': 'sang', 'B': 've'}, 0.9)
e2 = alg.rln_eval(m, {'A': {'o': 0.5, 'sang': 0.5}, 'B': 've'}, 0.9)
rec("L01c", abs(e1['A'] - 100 / 19) < 1e-9 and abs(e2['A'] - 100 / 29) < 1e-9 and abs(e2['B'] - 90 / 29) < 1e-9,
    "checklib (lặp) khớp nghiệm ma trận")
rng = np.random.default_rng(7)
T, N = 300, 20000
disc = 0.9 ** np.arange(T)
stay = rng.random((N, T)) < 0.5                  # chính sách 2: ở A, True = ở lại
G = np.zeros(N)
at_a = np.ones(N, dtype=bool)
for t in range(T):
    r = np.where(at_a & ~stay[:, t], 1.0, 0.0)  # sang B được 1
    G += disc[t] * r
    at_a = np.where(at_a, stay[:, t], True)     # từ A: ở lại → A, sang → B; từ B luôn về A
rec("L01d", abs(G.mean() - 100 / 29) < 0.03, f"mô phỏng 20 000 lượt theo chính sách 2: lợi nhuận trung bình {G.mean():.3f} ≈ 3,448")
rec("L01e", abs(sum(0.81 ** k for k in range(400)) - 100 / 19) < 1e-9,
    "cộng thẳng chuỗi 1, 0, 1, 0, …: Σ 0,81^k = 1/0,19")
x, y = sp.symbols("x y")
s = sp.solve([sp.Eq(x, 3 + y / 2), sp.Eq(y, x / 2)], [x, y])
s2 = solve([[0, 1], [1, 0]], [2, 0], sp.Rational(1, 2))
rec("L01f", s == {x: 4, y: 2} and s2 == [sp.Rational(8, 3), sp.Rational(4, 3)],
    "ôn nền x = 4, y = 2; quiz câu 1: V(A) = 8/3 ≈ 2,667, V(B) = 4/3 ≈ 1,333")
qa_stay, qa_go = 0 + g * v1[0], 1 + g * v1[1]
rec("L01g", qa_stay == sp.Rational(90, 19) and qa_go == sp.Rational(100, 19) and qa_stay < qa_go,
    "quiz câu 2: Q(A, ở lại) = 90/19 ≈ 4,737 < Q(A, sang B) = 100/19 → không đổi")
hist = alg.rln_eval_sweeps({'A': {'sang': [(1, 1, 'B')]}, 'B': {'ve': [(1, 0, 'A')]}}, {'A': 'sang', 'B': 've'}, 0.9, 100)
closed = [float(sum(g ** (2 * j) for j in range((k + 1) // 2))) for k in (1, 3, 10, 50, 100)]  # sau k vòng, A thấy ⌈k/2⌉ phần thưởng 1
rec("L01h", [round(c, 3) for c in closed] == [1.0, 1.81, 3.428, 5.236, 5.263]
    and all(abs(hist[k]['A'] - c) < 1e-9 for k, c in zip((1, 3, 10, 50, 100), closed)),
    "tự kiểm 2: bảng lặp 1 / 1,81 / 3,428 / 5,236 / 5,263 = tổng riêng ⌈k/2⌉ số hạng của Σ 0,81^j")
rec("L01i", 10000 ** 2 * 8 == 8 * 10 ** 8 and round(10000 ** 3 / 3 / 1e11, 1) == 3.3,
    "lỗi 4: 800 triệu byte; n³/3 ≈ 3,3·10¹¹")
