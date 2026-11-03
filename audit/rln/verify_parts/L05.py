# RLN L05 — tính lại KHÔNG bằng học: lặp giá trị trên mô hình đi men vách đá (quy hoạch động), và đánh giá CHÍNH XÁC
# hai chính sách epsilon tham lam (đường sát vách / đường hàng trên) bằng giải hệ tuyến tính numpy — khác `checks`
# (alg.rln_cliff học bằng mô phỏng ngẫu nhiên). So các con số trên màn hình với cả hai đường.
from fractions import Fraction as F

import numpy as np

rec("L05a", 2 + F(1, 10) * (-1 + 5 - 2) == F(11, 5) and 2 + F(1, 10) * (-1 + 1 - 2) == F(9, 5)
    and -5 + F(1, 2) * (-1 + F(9, 10) * -4 + 5) == F(-24, 5) and -5 + F(1, 2) * (-1 + F(9, 10) * -20 + 5) == -12,
    "giáo án 2,2 / 1,8; quiz −4,8 / −12 (phân số)")
rec("L05b", [float(x) for x in (F(9, 10) + F(1, 40), F(1, 40))] == [0.925, 0.025] and F(1, 40) * -100 == F(-5, 2)
    and 11 * F(1, 40) == F(11, 40), "epsilon tham lam 4 hướng 0,925 / 0,025; mỗi bước sát vách −2,5; 11 · 0,025 = 0,275")

ACTS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
S = [(i, j) for i in range(4) for j in range(12)]
idx = {s: k for k, s in enumerate(S)}
GOAL = (3, 11)


def step(s, a):
    i, j = min(3, max(0, s[0] + ACTS[a][0])), min(11, max(0, s[1] + ACTS[a][1]))
    if i == 3 and 1 <= j <= 10:
        return (3, 0), -100.0, 1.0
    return (i, j), -1.0, 0.0


# Lặp giá trị (không chiết khấu) → giá trị tối ưu ở xuất phát và độ dài đường tối ưu
V = {s: 0.0 for s in S}
for _ in range(200):
    V = {s: 0.0 if s == GOAL else max(r + V[s2] for s2, r, _ in (step(s, a) for a in range(4))) for s in S}
rec("L05c", V[(3, 0)] == -13.0, "lặp giá trị: giá trị tối ưu ở xuất phát = −13 (đường 13 bước)")


def path_policy(row):
    """Chính sách đi lên tới hàng `row`, sang phải, rồi xuống đích."""
    pol = {}
    for (i, j) in S:
        if j == 11:
            pol[(i, j)] = 1
        elif i > row:
            pol[(i, j)] = 0
        elif i < row:
            pol[(i, j)] = 1 if j == 0 else 3
        else:
            pol[(i, j)] = 3
    return pol


def eps_eval(pol, eps=0.1):
    n = len(S)
    P, R, Fv = np.zeros((n, n)), np.zeros(n), np.zeros(n)
    for s in S:
        if s == GOAL:
            continue
        for a in range(4):
            p = (1 - eps) * (a == pol[s]) + eps / 4
            s2, r, f = step(s, a)
            if s2 != GOAL:
                P[idx[s], idx[s2]] += p
            R[idx[s]] += p * r
            Fv[idx[s]] += p * f
    A = np.eye(n) - P
    return np.linalg.solve(A, R)[idx[(3, 0)]], np.linalg.solve(A, Fv)[idx[(3, 0)]]


edge_ret, edge_falls = eps_eval(path_policy(2))
top_ret, top_falls = eps_eval(path_policy(0))
rec("L05d", 0.25 < edge_falls < 0.35 and top_falls < 0.06 and top_ret > edge_ret,
    f"đánh giá chính xác epsilon 0,1: sát vách rơi {edge_falls:.3f} lần/lượt, điểm {edge_ret:.1f}; hàng trên rơi {top_falls:.3f}, điểm {top_ret:.1f}")
# Đối chiếu với mô phỏng học (cùng số trên màn hình)
q = [alg.rln_cliff("q", 500, alpha=0.1, seed=k) for k in range(20)]
sa = [alg.rln_cliff("sarsa", 500, alpha=0.1, seed=k) for k in range(20)]
mean = lambda xs: sum(xs) / len(xs)
qret, sret = mean([mean(r[0][-100:]) for r in q]), mean([mean(r[0][-100:]) for r in sa])
qf, sf = mean([mean(r[3][-100:]) for r in q]), mean([mean(r[3][-100:]) for r in sa])
rec("L05e", round(qret) == -47 and round(sret) == -23 and round(qf, 2) == 0.30 and round(sf, 2) == 0.05
    and abs(qf - edge_falls) < 0.05 and all(r[1] == 13 for r in q),
    f"mô phỏng học: điểm −47 / −23, rơi {qf:.3f} / {sf:.3f}; học Q tham lam 13 bước ở cả 20 lần chạy; số rơi khớp đánh giá chính xác ±0,05")
