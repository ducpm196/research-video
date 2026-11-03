# RLN L07 — tính lại bằng sympy (đạo hàm ký hiệu của J(θ) và của ln π), liệt kê chính xác bằng phân số, và mô phỏng numpy
# nhiều lượt — khác `checks` (alg.rln_pg2 dùng công thức 1 − σ, −σ viết tay; chênh lệch nhỏ bằng số thực).
from fractions import Fraction as F

import numpy as np
import sympy as sp

t = sp.symbols("t")
sig = 1 / (1 + sp.exp(-t))


def grad_true(G1, G2, th=0):
    return sp.simplify(sp.diff(sig * G1 + (1 - sig) * G2, t)).subs(t, th)


dl1 = sp.simplify(sp.diff(sp.log(sig), t))       # = 1 − σ
dl2 = sp.simplify(sp.diff(sp.log(1 - sig), t))   # = −σ
rec("L07a", sp.nsimplify(dl1.subs(t, 0)) == sp.Rational(1, 2) and sp.nsimplify(dl2.subs(t, 0)) == -sp.Rational(1, 2)
    and grad_true(10, 12) == -sp.Rational(1, 2) and sp.simplify(sp.diff(sig, t) - sig * (1 - sig)) == 0,
    "sympy: d ln σ = 0,5, d ln(1 − σ) = −0,5 ở θ = 0; σ′ = σ(1 − σ); ∇J = −1/2")


def enum(G1, G2, b1=0, b2=0):
    xs = [F(G1 - b1) * F(1, 2), F(G2 - b2) * F(-1, 2)]
    m = sum(xs) / 2
    return xs, m, sum(x * x for x in xs) / 2 - m * m


rec("L07b", enum(10, 12) == ([5, -6], F(-1, 2), F(121, 4)) and enum(10, 12, 11, 11) == ([F(-1, 2)] * 2, F(-1, 2), 0)
    and enum(10, 12)[2] == alg.rln_pg2(10, 12)[3],
    "liệt kê: mẫu 5, −6; kỳ vọng −1/2; phương sai 121/4 = 30,25 → 0 khi b = 11")
rec("L07c", enum(10, 12, 10, 0)[1] == -3 and enum(110, 112)[2] == F(12321, 4) and enum(110, 112, 111, 111)[2] == 0
    and enum(4, 8) == ([2, -4], -1, 9) and grad_true(4, 8) == -1 and enum(4, 8, 6, 6) == ([-1, -1], -1, 0),
    "lỗi 2: −3; lỗi 4: 3080,25 → 0; quiz: 2, −4, kỳ vọng −1 = ∇J, phương sai 9 → 0 với b = 6")
th9 = sp.log(9)
wrong = (sig * 10 * sp.diff(sig, t) + (1 - sig) * 12 * sp.diff(1 - sig, t)).subs(t, th9)
rec("L07d", sp.nsimplify(sp.simplify(wrong)) == sp.Rational(351, 500) and sp.nsimplify(sp.simplify(grad_true(10, 12, th9))) == -sp.Rational(9, 50)
    and sp.nsimplify(sig.subs(t, th9)) == sp.Rational(9, 10),
    "lỗi 1 (π = 0,9): công thức sai +0,702 = 351/500, đúng −0,18 = −9/50 — ngược dấu")
rng = np.random.default_rng(1992)
pick = rng.random(200000) < 0.5
x = np.where(pick, 5.0, -6.0)
xb = np.where(pick, -0.5, -0.5)
rec("L07e", abs(x.mean() + 0.5) < 0.05 and abs(x.var() - 30.25) < 0.3 and xb.var() == 0,
    f"mô phỏng 200 000 lượt: trung bình {x.mean():.3f}, phương sai {x.var():.2f}; có đường cơ sở: phương sai 0")
rec("L07f", F(0) + F(1, 10) * 5 == F(1, 2) and F(1, 10) * F(-1, 2) == F(-1, 20),
    "bước học α = 0,1: θ → 0,5 (không trừ b) và −0,05 (trừ b)")
