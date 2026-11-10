# IRS L07 — phân rã ma trận: tính lại bằng phân số chính xác (Fraction), bằng numpy và đạo hàm sympy của hàm phạt, và bằng nghiệm
# đóng của điểm dừng khi có chính quy hoá (khác `checks`: vòng lặp alg.irs_mf_step / alg.irs_fit_user).
from fractions import Fraction as F
import numpy as np
import sympy as sp

rec("L07a", 480189 * 17770 == 8532958530 and round(100480507 / 8532958530 * 100, 2) == 1.18 and (480189 + 17770) * 50 == 24897950
    and round(8532958530 / 24897950) == 343, "hook: 8 532 958 530 ô, 1,18% có điểm, 24 897 950 số ≈ 1/343")
p, q, r, eta = [F(1), F(2)], [F(1, 2), F(1)], F(3), F(1, 10)
e = r - sum(a * b for a, b in zip(p, q))
pn = [a + eta * e * b for a, b in zip(p, q)]
qn = [b + eta * e * a for a, b in zip(p, q)]
pred2 = sum(a * b for a, b in zip(pn, qn))
rec("L07b", e == F(1, 2) and pn == [F(41, 40), F(41, 20)] and qn == [F(11, 20), F(11, 10)] and pred2 == F(451, 160)
    and round(float(pred2), 3) == 2.819 and round(float(r - pred2), 3) == 0.181 and round(1.025 * 0.55, 3) == 0.564,
    "một bước: e 0,5; p (1,025; 2,05); q (0,55; 1,1); đoán lại 2,819, sai số 0,181 (phân số)")
lam = F(1, 10)
pr = [a + eta * (e * b - lam * a) for a, b in zip(p, q)]
rec("L07c", pr == [F(203, 200), F(203, 100)] and [float(x) for x in pr] == [1.015, 2.03], "có lam-đa 0,1: p (1,015; 2,03)")
x1, x2 = sp.symbols("x1 x2")
L = (3 - (x1 * sp.Rational(1, 2) + x2)) ** 2
g = [sp.diff(L, v).subs({x1: 1, x2: 2}) for v in (x1, x2)]
rec("L07d", g == [sp.Rational(-1, 2), -1] and [1 - sp.Rational(1, 20) * g[0], 2 - sp.Rational(1, 20) * g[1]] == [sp.Rational(41, 40), sp.Rational(41, 20)],
    "đạo hàm sympy (−0,5; −1); trừ η/2 · đạo hàm ra đúng p mới")
pe = np.array([1, 2.]) + 1.0 * 0.5 * np.array([.5, 1.])
qe = np.array([.5, 1.]) + 1.0 * 0.5 * np.array([1, 2.])
rec("L07e", pe.tolist() == [1.25, 2.5] and qe.tolist() == [1.0, 2.0] and pe @ qe == 6.25, "η = 1: đoán 6,25")
# điểm dừng của p với q_A = (0,5; 0,5), r = 5: e·q = λp, p = c(1,1) → (5 − c)·0,5 = λc → c = 2,5 / (0,5 + λ)
c = lambda l: F(5, 2) / (F(1, 2) + l)
rec("L07f", c(F(0)) == 5 and c(F(1, 10)) == F(25, 6) and c(F(1, 2)) == F(5, 2) and 2 * c(0) == 10 and round(float(2 * c(F(1, 10))), 2) == 8.33
    and 2 * c(F(1, 2)) == 5 and abs(alg.irs_fit_user([[0.5, 0.5]], [5], 0.1, 0.1, 5000)[0] - float(c(F(1, 10)))) < 1e-9,
    "người mới: λ = 0 → (5, 5), phim B 10; λ = 0,1 → 4,167, phim B 8,33; λ = 0,5 → 2,5, phim B 5")
rec("L07g", F(37, 10) + F(1, 2) - F(3, 10) == F(39, 10) and round(0.9514 * 0.9, 4) == 0.8563 and round(1 - 0.8563 / 0.9514, 3) == 0.1,
    "độ lệch 3,7 + 0,5 − 0,3 = 3,9; 0,9514 → 0,8563 giảm 10%")
p2, q2 = [F(2), F(1)], [F(1), F(1)]
e2 = 4 - sum(a * b for a, b in zip(p2, q2))
p2n = [a + eta * e2 * b for a, b in zip(p2, q2)]
q2n = [b + eta * e2 * a for a, b in zip(p2, q2)]
p2r = [a + eta * (e2 * b - lam * a) for a, b in zip(p2, q2)]
rec("L07h", e2 == 1 and p2n == [F(21, 10), F(11, 10)] and q2n == [F(6, 5), F(11, 10)] and sum(a * b for a, b in zip(p2n, q2n)) == F(373, 100)
    and p2r == [F(52, 25), F(109, 100)], "quiz: (2,1; 1,1), (1,2; 1,1), đoán lại 3,73; có lam-đa (2,08; 1,09)")
rec("L07i", 1 * 0.5 + 2 * 1 == 2.5 and 1 - 0.1 * 2 * (1 - 3) == 1.4 and (3 - 2.5) ** 2 == 0.25, "ôn: 2,5; w 1 → 1,4; 0,25")
# ôn mở rộng (đợt C): bảng 3 × 4 có 5 ô điểm; độ dốc đo bằng nhích hữu hạn (Fraction) và đạo hàm sympy; hai bước đi xuống dốc
f = lambda v: (v - 3) ** 2
w = sp.symbols("w")
d = sp.diff((w - 3) ** 2, w)
w1 = F(1) - F(1, 10) * d.subs(w, 1)
w2 = w1 - F(1, 10) * d.subs(w, sp.Rational(7, 5))
rec("L07j", 3 * 4 == 12 and sum(c != "–" for c in "5–3––4––2––5") == 5
    and f(F(11, 10)) == F(361, 100) and (f(F(11, 10)) - 4) / F(1, 10) == F(-39, 10) and f(F(101, 100)) == F(39601, 10000)
    and (f(F(101, 100)) - 4) / F(1, 100) == F(-399, 100) and d.subs(w, 1) == -4 and w1 == F(7, 5) and f(F(7, 5)) == F(64, 25)
    and d.subs(w, sp.Rational(7, 5)) == sp.Rational(-16, 5) and w2 == sp.Rational(43, 25) and f(F(43, 25)) == F(1024, 625)
    and float(F(1024, 625)) == 1.6384 and (3 - F(7, 2)) ** 2 == F(1, 4) and (3 - 4) ** 2 == 1 and 1 ** 2 + 2 ** 2 == 5,
    "ôn: 12 ô, 5 có điểm; f(1,1) 3,61 → −3,9; f(1,01) 3,9601 → −3,99; đạo hàm −4; w 1,4 (f 2,56) → 1,72 (f 1,6384); ‖(1, 2)‖² = 5")
