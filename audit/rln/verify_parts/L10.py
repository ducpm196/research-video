# RLN L10 — tính lại bằng sympy (đạo hàm tượng trưng, giá trị chính xác), dạng ln(1 + e^−d), và mô phỏng người chọn theo mô hình
# so sánh cặp, khác `checks` của bài (alg.rln_pref_steps / rln_kl_reward dùng số thực và công thức đóng).
import math

import numpy as np
import sympy as sp

d = sp.symbols("d", real=True)
L = sp.log(1 + sp.exp(-d))  # = −ln σ(d)
dL = sp.diff(L, d)
rec("L10a", sp.simplify(dL + (1 - 1 / (1 + sp.exp(-d)))) == 0 and round(float(dL.subs(d, 1)), 3) == -0.269
    and round(float(dL.subs(d, 0)), 3) == -0.5,
    "sympy: đạo hàm của −ln σ(d) = −(1 − σ(d)); tại 1 là −0,269, tại 0 là −0,5")
# lặp lại ví dụ bằng sympy chính xác rồi mới đổi sang số
rA = rB = sp.Integer(0)
rows = []
for _ in range(3):
    dd = rA - rB
    p = 1 / (1 + sp.exp(-dd))
    rows.append((float(dd), float(p), float(-sp.log(p)), float(1 - p)))
    rA, rB = rA + (1 - p), rB - (1 - p)
rec("L10b", [tuple(round(x, 3) for x in r) for r in rows] == [(0.0, 0.5, 0.693, 0.5), (1.0, 0.731, 0.313, 0.269), (1.538, 0.823, 0.195, 0.177)]
    and all(abs(a - b) < 1e-12 for r, s in zip(rows, alg.rln_pref_steps(2)) for a, b in zip(r, s)),
    "ba bước học (sympy): d 0 → 1 → 1,538; mất mát 0,693 → 0,313 → 0,195; lực kéo 0,5 → 0,269 → 0,177 — khớp checklib")
rng = np.random.default_rng(10)
choose_A = rng.random(500000) < 1 / (1 + math.exp(-1))
rec("L10c", abs(choose_A.mean() - 0.731) < 0.003 and abs(-np.log(np.where(choose_A, 1 / (1 + math.exp(-1)), 1 - 1 / (1 + math.exp(-1)))).mean()
    - (-(0.7311 * math.log(0.7311) + 0.2689 * math.log(0.2689)))) < 0.005,
    f"mô phỏng người chọn theo σ(1): tỉ lệ chọn A {choose_A.mean():.4f} ≈ 0,731")
rec("L10d", float(sp.log(1 + sp.exp(-1)).evalf()) - 0.3132617 < 1e-6 and round(float(sp.log(1 + sp.exp(-sp.Rational(1538, 1000)))), 3) == 0.195
    and round(float(1 / (1 + sp.exp(-(sp.Integer(12) - 11)))), 3) == round(float(1 / (1 + sp.exp(-1))), 3),
    "tự kiểm: ln(1 + e^−1) ≈ 0,313; ln(1 + e^−1,538) ≈ 0,195; dời điểm (12, 11) giữ xác suất")
R = lambda r, b, p, q: r - b * sp.log(sp.Rational(p) / sp.Rational(q))
rec("L10e", round(float(R(2, sp.Rational(1, 10), "1/2", "1/20")), 2) == 1.77 and round(float(R(2, 1, "1/2", "1/20")), 3) == -0.303
    and R(sp.Rational(3, 2), 1, "1/5", "1/5") == sp.Rational(3, 2) and round(float(sp.log(10)), 3) == 2.303,
    "phạt độ lệch: A 1,77 (β 0,1) / −0,303 (β 1); B 1,5; ln 10 ≈ 2,303")
rec("L10f", round(float(1 / (1 + sp.exp(-sp.Rational(3, 2)))), 3) == 0.818 and round(float(sp.log(1 + sp.exp(-sp.Rational(3, 2)))), 3) == 0.201
    and round(2 + 0.5 * float(1 - 1 / (1 + sp.exp(-sp.Rational(3, 2)))), 3) == 2.091
    and round(float(R(3, sp.Rational(1, 2), "6/10", "6/100")), 3) == 1.849 and round(float(R(3, 1, "6/10", "6/100")), 3) == 0.697
    and math.comb(9, 2) == 36 == 9 * 8 // 2 and math.comb(4, 2) == 6,
    "câu đố: 0,818 / 0,201; r_A 2,091; A 1,849 (β 0,5) / 0,697 (β 1); 36 và 6 cặp")
