"""Kiểm chứng bằng tính toán từng công thức / ví dụ trong CS115_Toan_cho_Khoa_hoc_May_tinh_Full.tex.

Chạy:  .venv/Scripts/python audit/verify_cs115_tex.py
Mỗi check in ra:  <ID> | PASS/FAIL | mô tả | giá trị quan sát
Exit code 0 nếu mọi check PASS, 1 nếu có FAIL.
"""
import sys
import datetime
import numpy as np
import sympy as sp

results = []


def check(cid, desc, ok, observed):
    results.append((cid, "PASS" if ok else "FAIL", desc, observed))


# ── T1. Phép chiếu trực giao (tex dòng 180-185) ──
y = sp.Matrix([6, 2, 4]); u = sp.Matrix([1, 2, 0])
dot_yu = (y.T * u)[0]; uu = (u.T * u)[0]
proj = (dot_yu / uu) * u; z = y - proj
check("T1a", "y^T u = 10", dot_yu == 10, dot_yu)
check("T1b", "u^T u = 5", uu == 5, uu)
check("T1c", "proj_u y = (2,4,0)", list(proj) == [2, 4, 0], list(proj))
check("T1d", "z = (4,-2,4) và z^T u = 0", list(z) == [4, -2, 4] and (z.T * u)[0] == 0, (list(z), (z.T * u)[0]))

# ── T2. Gram-Schmidt: công thức v_k + chuẩn hoá cho ra Q^T Q = I (dòng 193-198) ──
X = [sp.Matrix([1, 1, 0]), sp.Matrix([1, 0, 1]), sp.Matrix([0, 1, 1])]
V = []
for xk in X:
    vk = xk - sum(((xk.T * vj)[0] / (vj.T * vj)[0] * vj for vj in V), sp.zeros(3, 1))
    V.append(vk)
Q = sp.Matrix.hstack(*[v / v.norm() for v in V])
check("T2a", "các v_k đôi một vuông góc", all((V[i].T * V[j])[0] == 0 for i in range(3) for j in range(i)), [list(v) for v in V])
check("T2b", "sau chuẩn hoá Q^T Q = I", sp.simplify(Q.T * Q) == sp.eye(3), "Q^T Q = I")
check("T2c", "chưa chuẩn hoá thì V^T V != I (lỗi #1 là có thật)",
      sp.Matrix.hstack(*V).T * sp.Matrix.hstack(*V) != sp.eye(3), [ (v.T*v)[0] for v in V])
# A20: đầu vào không độc lập tuyến tính (x2 = 2 x1) → v2 = 0, bước chuẩn hoá u = v/‖v‖ chia cho 0
x1d, x2d = sp.Matrix([3, 4]), sp.Matrix([6, 8])
v2d = x2d - (x2d.T * x1d)[0] / (x1d.T * x1d)[0] * x1d
check("T2d", "đầu vào phụ thuộc tuyến tính → v_2 = 0, ‖v_2‖ = 0 (không chuẩn hoá được)", v2d == sp.zeros(2, 1) and v2d.norm() == 0, list(v2d))

# ── T3. SVD: U là vector riêng của A A^T, V của A^T A, sigma^2 = trị riêng (dòng 201-208) ──
rng = np.random.default_rng(0)
A = rng.normal(size=(4, 3))
U_, s_, Vt_ = np.linalg.svd(A)
ok_u = np.allclose(A @ A.T @ U_[:, :3], U_[:, :3] * s_**2)
ok_v = np.allclose(A.T @ A @ Vt_.T, Vt_.T * s_**2)
check("T3a", "cột U là vector riêng của A A^T (trị riêng sigma^2)", ok_u, s_.round(4).tolist())
check("T3b", "cột V là vector riêng của A^T A", ok_v, "allclose")
check("T3c", "sigma_1 >= sigma_2 >= ... >= 0", bool(np.all(np.diff(s_) <= 0) and np.all(s_ >= 0)), s_.round(4).tolist())

# ── T4. PCA = SVD trên dữ liệu đã trừ trung bình (lỗi #5, dòng 144-146, 210-214) ──
Xd = rng.normal(size=(50, 3)) @ np.array([[3, 0, 0], [1, 1, 0], [0, 0, .2]])
Xc = Xd - Xd.mean(axis=0)
S = Xc.T @ Xc / len(Xc)
evals, evecs = np.linalg.eigh(S)
_, sv, Vt = np.linalg.svd(Xc, full_matrices=False)
ok_pca = np.allclose(np.sort(evals)[::-1], sv**2 / len(Xc)) and np.allclose(np.abs(evecs[:, ::-1]), np.abs(Vt.T))
check("T4a", "trị riêng của S = sigma^2/N, vector riêng của S = cột V (sai khác dấu)", ok_pca, (np.sort(evals)[::-1].round(4).tolist()))
_, _, Vt_raw = np.linalg.svd(Xd + 10, full_matrices=False)
check("T4b", "KHÔNG trừ trung bình thì SVD cho trục khác PCA (bước 1 là bắt buộc)",
      not np.allclose(np.abs(Vt_raw[0]), np.abs(Vt[0]), atol=1e-2), (Vt_raw[0].round(3).tolist(), Vt[0].round(3).tolist()))

# ── T5. Bài toán cực trị f = x^2 + y^2 - xy + x - y (dòng 265-278) ──
xs, ys = sp.symbols("x y")
f = xs**2 + ys**2 - xs*ys + xs - ys
grad = [sp.diff(f, xs), sp.diff(f, ys)]
crit = sp.solve(grad, [xs, ys], dict=True)
H = sp.hessian(f, (xs, ys))
check("T5a", "grad f = (2x - y + 1, 2y - x - 1)", sp.simplify(grad[0] - (2*xs - ys + 1)) == 0 and sp.simplify(grad[1] - (2*ys - xs - 1)) == 0, grad)
check("T5b", "điểm dừng duy nhất (-1/3, 1/3)", crit == [{xs: sp.Rational(-1, 3), ys: sp.Rational(1, 3)}], crit)
check("T5c", "H = [[2,-1],[-1,2]], Delta1=2, Delta2=3", H == sp.Matrix([[2, -1], [-1, 2]]) and H[0, 0] == 2 and H.det() == 3, (H.tolist(), H.det()))
check("T5d", "trị riêng H = 1, 3 > 0 (xác định dương)", sorted(H.eigenvals().keys()) == [1, 3], H.eigenvals())
check("T5e", "f(-1/3,1/3) = -1/3 (giá trị cực tiểu; tex không nêu)", f.subs(crit[0]) == sp.Rational(-1, 3), f.subs(crit[0]))

# ── T6. Sylvester cho xác định âm: Delta_k đan dấu bắt đầu bằng âm (dòng 142, 259) ──
N3 = -sp.Matrix([[2, -1, 0], [-1, 2, -1], [0, -1, 2]])
minors = [N3[:k, :k].det() for k in (1, 2, 3)]
check("T6a", "ma trận xác định âm có Delta = (-, +, -)", [sp.sign(m) for m in minors] == [-1, 1, -1] and all(e < 0 for e in N3.eigenvals()), minors)
# Phản ví dụ cho dòng 260: "không thoả tiêu chuẩn" KHÔNG suy ra yên ngựa
f2 = xs**4 + ys**4   # cực tiểu tại (0,0), Hessian = 0
H2 = sp.hessian(f2, (xs, ys)).subs({xs: 0, ys: 0})
check("T6b", "PHẢN VÍ DỤ: f=x^4+y^4 có H(0)=0 (không thoả Sylvester) nhưng (0,0) là CỰC TIỂU, không phải yên ngựa",
      H2 == sp.zeros(2, 2), "H(0,0)=0 nhưng f>=0=f(0,0)")
# Phản ví dụ cho xác định nửa dương: minor góc trên >= 0 không đủ
M = sp.Matrix([[0, 0], [0, -1]])
check("T6c", "PHẢN VÍ DỤ: Delta1=0, Delta2=0 (đều >=0) nhưng M không nửa xác định dương (trị riêng -1)",
      M[:1, :1].det() == 0 and M.det() == 0 and min(M.eigenvals()) < 0, M.eigenvals())

# ── T7. Gaussian: MLE của mu là trung bình cộng (dòng 321-329) ──
mu, sig = sp.symbols("mu sigma", positive=True)
data = [sp.Integer(v) for v in (2, 4, 9)]
logL = sum(-sp.log(sp.sqrt(2*sp.pi*sig**2)) - (x - mu)**2 / (2*sig**2) for x in data)
sol = sp.solve(sp.diff(logL, mu), mu)
check("T7a", "argmax logL theo mu = mean(2,4,9) = 5", sol == [5], sol)
check("T7b", "d2 logL/dmu2 = -N/sigma^2 < 0 (đúng là cực đại)", sp.simplify(sp.diff(logL, mu, 2) + 3/sig**2) == 0, sp.diff(logL, mu, 2))
xg = sp.symbols("x", real=True)
pdf = 1/sp.sqrt(2*sp.pi*sig**2) * sp.exp(-(xg - mu)**2/(2*sig**2))
check("T7c", "pdf Gaussian 1 chiều tích phân = 1", sp.simplify(sp.integrate(pdf, (xg, -sp.oo, sp.oo))) == 1, "∫p=1")
# Var = E[X^2] - (E[X])^2 trên một phân phối rời rạc
vals, probs = np.array([1, 2, 6]), np.array([.2, .5, .3])
E = (vals*probs).sum(); var1 = ((vals-E)**2*probs).sum(); var2 = (vals**2*probs).sum() - E**2
check("T7d", "Var(X)=E[(X-mu)^2]=E[X^2]-E[X]^2", np.isclose(var1, var2), (var1, var2))

# ── T8. Normal equation (dòng 339-342) ──
Xr = np.c_[np.ones(20), rng.normal(size=(20, 2))]; w_true = np.array([1., 2., -3.])
yr = Xr @ w_true + rng.normal(scale=.1, size=20)
w_ne = np.linalg.solve(Xr.T @ Xr, Xr.T @ yr); w_ls = np.linalg.lstsq(Xr, yr, rcond=None)[0]
check("T8a", "(X^T X)^{-1} X^T y = nghiệm bình phương tối thiểu", np.allclose(w_ne, w_ls), w_ne.round(3).tolist())
Xs = np.c_[Xr, Xr[:, 1]*2]  # cột trùng lặp -> X^T X suy biến
check("T8b", "khi cột phụ thuộc tuyến tính, X^T X suy biến (công thức nghịch đảo không dùng được)",
      np.linalg.matrix_rank(Xs.T @ Xs) < Xs.shape[1], np.linalg.matrix_rank(Xs.T @ Xs))

# ── T9. Lỗi #3: MSE + sigmoid không lồi, BCE lồi (theo w, mô hình tuyến tính) ──
w = sp.symbols("w", real=True)
sigm = 1/(1+sp.exp(-w))     # 1 mẫu x=1, y=0
mse = sigm**2; bce = -sp.log(1 - sigm)
d2_mse = sp.lambdify(w, sp.diff(mse, w, 2)); d2_bce = sp.lambdify(w, sp.diff(bce, w, 2))
grid = np.linspace(-8, 8, 801)
check("T9a", "MSE∘sigmoid có đạo hàm bậc 2 âm ở đâu đó (không lồi)", min(d2_mse(grid)) < 0, float(min(d2_mse(grid))))
check("T9b", "BCE∘sigmoid có đạo hàm bậc 2 >= 0 trên lưới (lồi theo w)", min(d2_bce(grid)) >= 0, float(min(d2_bce(grid))))

# ── T10. Softmax tổng = 1, sigmoid = softmax 2 lớp ──
s = np.array([2., 1., -1.]); p = np.exp(s)/np.exp(s).sum()
check("T10a", "softmax cộng lại = 1", np.isclose(p.sum(), 1), p.round(4).tolist())
z0 = 0.7
check("T10b", "sigmoid(z) = softmax([z,0])[0]", np.isclose(1/(1+np.exp(-z0)), np.exp(z0)/(np.exp(z0)+1)), z0)

# ── T11. Backprop f = x*y + max(x,y) tại (2,3) (dòng 366-388) ──
fb = xs*ys + sp.Max(xs, ys)
gx = sp.diff(fb, xs).subs({xs: 2, ys: 3}); gy = sp.diff(fb, ys).subs({xs: 2, ys: 3})
check("T11a", "f(2,3) = 9", fb.subs({xs: 2, ys: 3}) == 9, fb.subs({xs: 2, ys: 3}))
check("T11b", "df/dx = 3, df/dy = 3", (sp.simplify(gx), sp.simplify(gy)) == (3, 3), (gx, gy))
h = 1e-6; fn = lambda a, b: a*b + max(a, b)
num = ((fn(2+h, 3)-fn(2-h, 3))/(2*h), (fn(2, 3+h)-fn(2, 3-h))/(2*h))
check("T11c", "sai phân hữu hạn khớp (3, 3)", np.allclose(num, (3, 3)), num)

# ── T12. Momentum / GD trên f của T5 hội tụ về (-1/3, 1/3) ──
gfun = sp.lambdify([xs, ys], grad)
wv = np.array([2., 2.]); vel = np.zeros(2)
for _ in range(300):
    vel = 0.9*vel + 0.05*np.array(gfun(*wv)); wv = wv - vel
check("T12", "Momentum (beta=.9, eta=.05) hội tụ về (-1/3,1/3)", np.allclose(wv, [-1/3, 1/3], atol=1e-6), wv.round(6).tolist())

# ── T13. Jacobian kích thước E x D ──
a, b, c = sp.symbols("a b c")
J = sp.Matrix([a*b, b+c]).jacobian([a, b, c])
check("T13", "f: R^3 -> R^2 có J kích thước 2x3 (E x D)", J.shape == (2, 3), J.shape)

# ── T14. Trị riêng / vector riêng: tex dùng (dòng 205, 207, 213, 256-260) mà không định nghĩa (A21) ──
lam = sp.Symbol("lam")
A14 = sp.Matrix([[2, 1], [1, 2]]); B14 = sp.Matrix([[4, 1], [2, 3]]); R14 = sp.Matrix([[0, -1], [1, 0]])
check("T14a", "v = 0 thoả A v = lam v với MỌI lam (nên định nghĩa phải có v != 0)",
      sp.expand(A14 * sp.zeros(2, 1) - lam * sp.zeros(2, 1)) == sp.zeros(2, 1), "A·0 = lam·0")
check("T14b", "ma trận quay [[0,-1],[1,0]]: det(R - lam I) = lam^2 + 1, không có trị riêng thực",
      sp.expand((R14 - lam * sp.eye(2)).det()) == lam**2 + 1 and sp.solveset(lam**2 + 1, lam, domain=sp.S.Reals) == sp.S.EmptySet
      and all(not r.is_real for r in sp.solve(lam**2 + 1, lam)), sp.solve(lam**2 + 1, lam))
ev_a = A14.eigenvects(); ev_b = B14.eigenvects()
check("T14c", "A đối xứng: vector riêng (λ=3, λ=1) vuông góc; B = [[4,1],[2,3]] không đối xứng: không vuông góc",
      (ev_a[0][2][0].T * ev_a[1][2][0])[0] == 0 and (ev_b[0][2][0].T * ev_b[1][2][0])[0] != 0,
      ([(e[0], list(e[2][0])) for e in ev_a], [(e[0], list(e[2][0])) for e in ev_b]))
check("T14d", "trị riêng của B là 2, 5 — KHÔNG phải số trên đường chéo (4, 3); tổng = 4 + 3, tích = det B",
      sorted(B14.eigenvals()) == [2, 5] and 2 + 5 == B14.trace() and 2 * 5 == B14.det(), (B14.eigenvals(), B14.trace(), B14.det()))

# ── T15. Gradient "chỉ hướng tăng nhanh nhất" (dòng 223) — A22: điều kiện của phát biểu ──
h15 = sp.Symbol("h")
check("T15a", "đạo hàm của x^2 tại 3: thương sai phân ((3+h)^2 - 9)/h = 6 + h → 6 khi h → 0",
      sp.simplify(((3 + h15)**2 - 9) / h15 - (6 + h15)) == 0 and sp.limit(((3 + h15)**2 - 9) / h15, h15, 0) == 6, "6 + h")
th = np.linspace(0, 2 * np.pi, 3601)[:-1]; U15 = np.stack([np.cos(th), np.sin(th)], 1)
d_lin = U15 @ np.array([3.0, 4.0])  # f = 3x + 4y: thay đổi khi đi 1 đơn vị theo u (chính xác, f tuyến tính)
k_max = int(np.argmax(d_lin))
check("T15b", "f = 3x + 4y: trên 3600 hướng đơn vị, tăng nhiều nhất = 5 = ‖∇f‖ tại u = (3/5, 4/5); ít nhất −5; vuông góc 0",
      np.isclose(d_lin.max(), 5) and np.allclose(U15[k_max], [0.6, 0.8], atol=2e-3) and np.isclose(d_lin.min(), -5)
      and np.isclose(np.array([0.8, -0.6]) @ np.array([3.0, 4.0]), 0), (float(d_lin.max()), U15[k_max].round(3).tolist()))
fn = sp.lambdify((xs, ys), f); hh = 1e-6
d_num = np.array([(fn(hh * a, hh * b) - fn(0, 0)) / hh for a, b in U15])  # f của dòng 266, tại (0,0): ∇f = (1, -1)
g0 = np.array([float(g.subs({xs: 0, ys: 0})) for g in grad])
check("T15c", "f của dòng 266 tại (0,0): ∇f = (1,-1); tốc độ tăng theo u ≈ ∇f·u, lớn nhất ≈ √2 tại u ≈ ∇f/‖∇f‖",
      np.allclose(g0, [1, -1]) and np.allclose(d_num, U15 @ g0, atol=1e-5) and np.isclose(d_num.max(), np.sqrt(2), atol=1e-5)
      and np.allclose(U15[int(np.argmax(d_num))], g0 / np.linalg.norm(g0), atol=2e-3), (g0.tolist(), float(d_num.max())))
check("T15d", "tại điểm dừng (-1/3, 1/3): ∇f = 0 → mọi hướng có tốc độ 0, không có 'hướng tăng nhanh nhất'",
      all(g.subs(crit[0]) == 0 for g in grad), [g.subs(crit[0]) for g in grad])
t15 = sp.Symbol("t", positive=True); q15 = xs * ys / (xs**2 + ys**2)  # q(0,0) := 0
check("T15e", "PHẢN VÍ DỤ: q = xy/(x²+y²), q(0,0)=0 có ∂q/∂x = ∂q/∂y = 0 tại 0 nhưng q(t,t) = 1/2 với mọi t ≠ 0 "
      "(không liên tục, không khả vi) → phát biểu cần f khả vi",
      sp.limit((q15.subs({xs: t15, ys: 0}) - 0) / t15, t15, 0) == 0 and sp.limit((q15.subs({xs: 0, ys: t15}) - 0) / t15, t15, 0) == 0
      and sp.simplify(q15.subs({xs: t15, ys: t15})) == sp.Rational(1, 2), sp.simplify(q15.subs({xs: t15, ys: t15})))
p15 = xs**2 + 4 * ys**2; gp = sp.Matrix([sp.diff(p15, xs), sp.diff(p15, ys)]).subs({xs: 2, ys: 1})
check("T15f", "f = x² + 4y² tại (2,1): −∇f = (−4,−8) KHÔNG cùng hướng với (−2,−1) chỉ thẳng về đáy (0,0): hướng giảm nhanh nhất chỉ là tại chỗ",
      gp == sp.Matrix([4, 8]) and sp.Matrix([[-4, -2], [-8, -1]]).det() != 0, list(gp))

# ── T16. LDA (dòng 410) — A23: Fisher = tỉ số (giữa lớp)/(trong lớp), không chỉ “khoảng cách giữa các lớp” ──
rng16 = np.random.default_rng(0)
C16 = np.array([[9.0, 0.0], [0.0, 0.25]])  # hai lớp cùng hiệp phương sai: trải rộng theo x, hẹp theo y; tâm lệch (3, 1)
X1 = rng16.multivariate_normal([0, 0], C16, 400); X2 = rng16.multivariate_normal([3, 1], C16, 400)
m1, m2 = X1.mean(0), X2.mean(0)
Sw = np.cov(X1.T, bias=True) * 400 + np.cov(X2.T, bias=True) * 400
w_mean = (m2 - m1) / np.linalg.norm(m2 - m1)          # chỉ tối đa khoảng cách hai tâm
w_fish = np.linalg.solve(Sw, m2 - m1); w_fish /= np.linalg.norm(w_fish)


def fisher(w):
    return float((w @ (m2 - m1))**2 / (w @ Sw @ w))


def overlap(w):  # tỉ lệ điểm bị phân sai khi cắt ở giữa hai tâm sau khi chiếu
    t = w @ (m1 + m2) / 2
    return float(((X1 @ w) > t).mean() + ((X2 @ w) < t).mean()) / 2


check("T16", "LDA: hướng Fisher S_w⁻¹(m₂−m₁) cho tỉ số Fisher lớn hơn và phân sai ít hơn hướng chỉ nối hai tâm "
      "→ ‘tối đa khoảng cách giữa các lớp’ thiếu vế ‘so với độ phân tán trong lớp’",
      fisher(w_fish) > 2 * fisher(w_mean) and overlap(w_fish) < overlap(w_mean),
      (round(fisher(w_fish), 4), round(fisher(w_mean), 4), round(overlap(w_fish), 3), round(overlap(w_mean), 3)))

# ── T17. K-Means (dòng 408) — A24: inertia là tổng BÌNH PHƯƠNG khoảng cách ──
pts17 = np.array([0.0, 1.0, 10.0])
grid17 = np.linspace(-1, 11, 120001)
c_sq = grid17[np.argmin(((pts17[None] - grid17[:, None])**2).sum(1))]
c_abs = grid17[np.argmin(np.abs(pts17[None] - grid17[:, None]).sum(1))]
check("T17", "tâm tối ưu của bước ‘tính lại tâm’ = trung bình chỉ khi đo tổng BÌNH PHƯƠNG khoảng cách; "
      "tổng khoảng cách (không bình phương) cho trung vị: {0,1,10} → 11/3 vs 1",
      np.isclose(c_sq, 11 / 3, atol=1e-3) and np.isclose(c_abs, 1, atol=1e-3), (round(float(c_sq), 4), round(float(c_abs), 4)))

# ── T18. Ridge (L2) — A9/A25: XᵀX suy biến nhưng XᵀX + λI khả nghịch với mọi λ > 0 ──
X18 = sp.Matrix([[1, 2, 2], [1, 3, 3], [1, 5, 5]])   # cột 3 trùng cột 2 (như T8b)
lam = sp.Symbol("lam", positive=True)
G18 = X18.T * X18
check("T18", "Ridge: cột trùng → det(XᵀX) = 0, nhưng det(XᵀX + λI) > 0 với λ > 0 (XᵀX nửa xác định dương ⇒ trị riêng + λ > 0)",
      G18.det() == 0 and all(ev >= 0 for ev in G18.eigenvals()) and sp.factor((G18 + lam * sp.eye(3)).det()).subs(lam, sp.Rational(1, 100)) > 0
      and sp.Poly((G18 + lam * sp.eye(3)).det(), lam).all_coeffs()[-1] == 0 and all(c >= 0 for c in sp.Poly((G18 + lam * sp.eye(3)).det(), lam).all_coeffs()),
      sp.factor((G18 + lam * sp.eye(3)).det()))

# ── T19. SVM (dòng 406) — lề giữa wᵀx + b = 1 và wᵀx + b = −1 là 2/‖w‖ ──
w19 = sp.Matrix([3, 4]); b19 = -2
p_plus = (1 - b19) * w19 / (w19.T * w19)[0]; p_minus = (-1 - b19) * w19 / (w19.T * w19)[0]   # điểm gần gốc nhất trên mỗi đường
check("T19", "SVM: w = (3,4), b = −2: khoảng cách hai đường wᵀx+b = ±1 bằng 2/‖w‖ = 2/5",
      (w19.T * p_plus)[0] + b19 == 1 and (w19.T * p_minus)[0] + b19 == -1 and (p_plus - p_minus).norm() == sp.Rational(2, 5),
      (p_plus - p_minus).norm())

# ── T20. Jacobian, Hessian, quy tắc chuỗi (dòng 132–134, 224–246) — A3, A13 ──
x20, y20, t20 = sp.symbols("x y t", real=True)
g20 = sp.Matrix([x20**2 * y20, 5 * x20 + sp.sin(y20)])           # R² → R²
J20 = g20.jacobian([x20, y20])
check("T20a", "Jacobian của g = (x²y, 5x + sin y) là [[2xy, x²], [5, cos y]]; hàng = đầu ra, cột = đầu vào (E×D)",
      J20 == sp.Matrix([[2 * x20 * y20, x20**2], [5, sp.cos(y20)]]), J20)
A20 = sp.Matrix([[1, 2, 0], [3, -1, 4]]); v20 = sp.Matrix(sp.symbols("v1:4", real=True))
check("T20b", "hàm tuyến tính v ↦ A v (A cỡ 2×3) có Jacobian chính là A (cỡ 2×3)", (A20 * v20).jacobian(list(v20)) == A20, A20.shape)
f20 = x20**3 + 2 * x20 * y20**2
H20 = sp.hessian(f20, (x20, y20)); grad20 = sp.Matrix([f20]).jacobian([x20, y20]).T
check("T20c", "Hessian = Jacobian của gradient; f = x³ + 2xy²: H = [[6x, 4y], [4y, 4x]], đối xứng; tại (1, 2): [[6, 8], [8, 4]]",
      H20 == grad20.jacobian([x20, y20]) and H20 == H20.T and H20.subs({x20: 1, y20: 2}) == sp.Matrix([[6, 8], [8, 4]]),
      H20.subs({x20: 1, y20: 2}))
# A3: phản ví dụ — đạo hàm cấp 2 hỗn hợp KHÔNG bằng nhau khi không liên tục
q20 = x20 * y20 * (x20**2 - y20**2) / (x20**2 + y20**2)          # q(0,0) := 0
qx = sp.simplify(sp.diff(q20, x20)); qy = sp.simplify(sp.diff(q20, y20))
qx_on_y = sp.simplify(sp.limit(qx, x20, 0))      # ∂q/∂x tại (0, y), y ≠ 0  = −y
qy_on_x = sp.simplify(sp.limit(qy, y20, 0))      # ∂q/∂y tại (x, 0), x ≠ 0  =  x
# ∂q/∂x(0,0) = ∂q/∂y(0,0) = 0 vì q(h,0) = q(0,h) = 0 → f_xy(0,0) = d/dy[−y] = −1, f_yx(0,0) = d/dx[x] = 1
check("T20d", "A3 PHẢN VÍ DỤ: q = xy(x²−y²)/(x²+y²): ∂/∂y(∂q/∂x) tại 0 = −1 nhưng ∂/∂x(∂q/∂y) tại 0 = 1 → Hessian chỉ đối xứng khi đạo hàm cấp 2 liên tục",
      qx_on_y == -y20 and qy_on_x == x20 and q20.subs(y20, 0) == 0 and q20.subs(x20, 0) == 0
      and sp.diff(qx_on_y, y20) == -1 and sp.diff(qy_on_x, x20) == 1, (qx_on_y, qy_on_x))
# Quy tắc chuỗi: một biến, và dạng ma trận (Jacobian của hàm hợp = tích Jacobian, theo đúng thứ tự)
check("T20e", "quy tắc chuỗi một biến: d/dx (3x + 1)² = 2(3x + 1)·3; tại x = 1: 24",
      sp.diff((3 * x20 + 1)**2, x20) == 6 * (3 * x20 + 1) and sp.diff((3 * x20 + 1)**2, x20).subs(x20, 1) == 24, 24)
u20 = sp.Matrix([x20 + y20, x20 * y20])                           # trong: R² → R²
a20, b20 = sp.symbols("a b", real=True)
h20 = sp.Matrix([a20**2 + b20])                                    # ngoài: R² → R
comp = h20.subs({a20: u20[0], b20: u20[1]})
Jc = comp.jacobian([x20, y20]); Jh = h20.jacobian([a20, b20]).subs({a20: u20[0], b20: u20[1]}); Ju = u20.jacobian([x20, y20])
pt = {x20: 1, y20: 2}
check("T20f", "A13: Jacobian của h(u(x, y)) = J_h · J_u (nhân ma trận, ngoài trước trong sau); tại (1, 2): [8, 7]; "
      "nhân từng phần tử hoặc đảo thứ tự thì sai",
      sp.simplify(Jc - Jh * Ju) == sp.zeros(1, 2) and Jc.subs(pt) == sp.Matrix([[8, 7]])
      and Jh.subs(pt).multiply_elementwise(sp.Matrix([[Ju.subs(pt)[0, 0], Ju.subs(pt)[1, 1]]])) != Jc.subs(pt),
      Jc.subs(pt))

# ── T21. Bài 7 — tiêu chuẩn định thức con 2×2 khớp dấu trị riêng; Sarrus; độ cong theo hướng (dòng 140–142, 250–279) ──
rng21 = np.random.default_rng(7)
bad21 = []
for _ in range(3000):
    a21, b21, c21 = (int(v) for v in rng21.integers(-5, 6, 3))
    M21 = np.array([[a21, b21], [b21, c21]], float); ev = np.linalg.eigvalsh(M21)
    d1, d2 = a21, a21 * c21 - b21 * b21
    by_minor = "min" if d1 > 0 and d2 > 0 else "max" if d1 < 0 and d2 > 0 else "saddle" if d2 < 0 else "?" if d2 == 0 else "other"
    by_eig = "min" if ev.min() > 1e-12 else "max" if ev.max() < -1e-12 else "saddle" if ev.min() < -1e-12 < 1e-12 < ev.max() else "?"
    if by_minor != by_eig:
        bad21.append((a21, b21, c21, by_minor, by_eig))
check("T21a", "3000 ma trận đối xứng 2×2 nguyên ngẫu nhiên: bảng định thức con (Δ₁, Δ₂) cho cùng kết luận với dấu trị riêng "
      "(kể cả Δ₂ < 0 ⇒ yên ngựa, Δ₂ = 0 ⇒ có trị riêng 0)", not bad21, bad21[:3])
M3 = rng21.integers(-5, 6, (200, 3, 3))
sarrus = lambda m: (m[0,0]*m[1,1]*m[2,2] + m[0,1]*m[1,2]*m[2,0] + m[0,2]*m[1,0]*m[2,1]
                    - m[0,2]*m[1,1]*m[2,0] - m[0,0]*m[1,2]*m[2,1] - m[0,1]*m[1,0]*m[2,2])
check("T21b", "quy tắc Sarrus = định thức 3×3 trên 200 ma trận nguyên ngẫu nhiên",
      all(int(sarrus(m)) == int(sp.Matrix(m.tolist()).det()) for m in M3), "200/200")
u21 = sp.Matrix(sp.symbols("u1 u2", real=True)); t21 = sp.Symbol("t", real=True)
g21 = f.subs({xs: sp.Rational(-1, 3) + t21 * u21[0], ys: sp.Rational(1, 3) + t21 * u21[1]})
check("T21c", "độ cong theo hướng u tại điểm dừng của f dòng 266: k''(0) = uᵀ H u; và f(x*+h) − f* = ½hᵀHh (đúng tuyệt đối, A4)",
      sp.simplify(sp.diff(g21, t21, 2).subs(t21, 0) - (u21.T * H * u21)[0]) == 0
      and sp.expand(f.subs({xs: sp.Rational(-1, 3) + u21[0], ys: sp.Rational(1, 3) + u21[1]}) + sp.Rational(1, 3)
                    - sp.Rational(1, 2) * (u21.T * H * u21)[0]) == 0, (u21.T * H * u21)[0])

sys.stdout.reconfigure(encoding="utf-8")  # Windows: stdout bị pipe mặc định cp1252, không in được “đ”
fails = [r for r in results if r[1] != "PASS"]
for r in results:
    print(" | ".join(str(x) for x in r))
print(f"TOTAL={len(results)} PASS={len(results)-len(fails)} FAIL={len(fails)}")
print("checked_at=" + datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
sys.exit(1 if fails else 0)
