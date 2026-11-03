"""Kiểm độc lập mọi khẳng định số của khoá RBM — KHÔNG dùng tools/checklib.py để tính, chỉ để đối chiếu.
Mỗi mục: tính lại bằng sympy (đúng tuyệt đối) hoặc cài đặt riêng bằng numpy, rồi so với checklib (alg) mà các `checks` trong bài dùng.
Chạy: .venv/Scripts/python audit/rbm/verify_rbm.py  → in từng dòng PASS/FAIL và tổng."""
import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402

R = []


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


d = sp.pi / 180
c, s = sp.cos, sp.sin


def Rz(t):
    return sp.Matrix([[c(t * d), -s(t * d), 0], [s(t * d), c(t * d), 0], [0, 0, 1]])


def Rx(t):
    return sp.Matrix([[1, 0, 0], [0, c(t * d), -s(t * d)], [0, s(t * d), c(t * d)]])


def Ry(t):
    return sp.Matrix([[c(t * d), 0, s(t * d)], [0, 1, 0], [-s(t * d), 0, c(t * d)]])


def R2(t):
    return sp.Matrix([[c(t * d), -s(t * d)], [s(t * d), c(t * d)]])


# ── L00 ──
rec("L00a", R2(90) * sp.Matrix([1, 0]) == sp.Matrix([0, 1]), "R(90°)(1, 0) = (0, 1)")
q = sp.simplify(R2(30) * sp.Matrix([2, 1]))
rec("L00b", q == sp.Matrix([sp.sqrt(3) - sp.Rational(1, 2), 1 + sp.sqrt(3) / 2]) and [round(float(v), 3) for v in q] == [1.232, 1.866],
    f"R(30°)(2, 1) = (√3 − 1/2, 1 + √3/2) ≈ {[round(float(v), 3) for v in q]}")
th = sp.symbols("theta", real=True)
Rt = sp.Matrix([[sp.cos(th), -sp.sin(th)], [sp.sin(th), sp.cos(th)]])
rec("L00c", sp.simplify(Rt.T * Rt) == sp.eye(2) and sp.simplify(Rt.det()) == 1 and sp.simplify(Rt.T - Rt.subs(th, -th)) == sp.zeros(2),
    "RᵀR = I, det R = 1, Rᵀ = R(−θ) (ký hiệu)")
rec("L00d", sp.Matrix([[1, 0], [0, -1]]).det() == -1, "gương det = −1")
rec("L00e", R2(90).T * sp.Matrix([0, 2]) == sp.Matrix([2, 0]) and R2(90) * sp.Matrix([3, 1]) == sp.Matrix([-1, 3]), "câu đố L00")
rec("L00x", np.allclose(alg.rot2(30), np.array(R2(30).evalf(), float)), "checklib.rot2 khớp sympy")

# ── L01 ──
rec("L01a", Rz(90) * Rx(90) * sp.Matrix([0, 1, 0]) == sp.Matrix([0, 0, 1]) and Rx(90) * Rz(90) * sp.Matrix([0, 1, 0]) == sp.Matrix([-1, 0, 0]),
    "hai thứ tự cho (0, 0, 1) và (−1, 0, 0)")
a_, b_ = sp.symbols("a b", real=True)
M = sp.simplify(Rz(a_ / d) * Ry(90) * Rx(b_ / d))
M2 = sp.simplify(M.subs({a_: a_ + 1, b_: b_ + 1}))
rec("L01b", sp.simplify(M - M2) == sp.zeros(3), "θ_y = 90°: ma trận chỉ phụ thuộc θ_x − θ_z (ký hiệu)")
rec("L01c", np.allclose(np.array((Rz(30) * Ry(90) * Rx(10)).evalf(), float), [[0, -math.sin(math.radians(20)), math.cos(math.radians(20))],
                                                                                  [0, math.cos(math.radians(20)), math.sin(math.radians(20))], [-1, 0, 0]]),
    "ma trận khoá gimbal (30°, 90°, 10°)")
rec("L01d", len([t for t in __import__("itertools").product("xyz", repeat=3) if t[0] != t[1] and t[1] != t[2]]) == 12, "12 thứ tự trục")
rec("L01e", Ry(30) * sp.Matrix([0, 0, 1]) == sp.Matrix([sp.Rational(1, 2), 0, sp.sqrt(3) / 2]), "R_y(30°)(0,0,1) = (0,5; 0; 0,866)")
rec("L01x", all(np.allclose(f(t), np.array(g(t).evalf(), float)) for f, g in ((alg.rotx, Rx), (alg.roty, Ry), (alg.rotz, Rz)) for t in (17, 90, 200)),
    "checklib.rotx/roty/rotz khớp sympy")

# ── L02 ── quaternion bằng sympy.algebras.Quaternion (độc lập với alg.qmul)
from sympy.algebras.quaternion import Quaternion as Q  # noqa: E402
i_, j_, k_ = Q(0, 1, 0, 0), Q(0, 0, 1, 0), Q(0, 0, 0, 1)
rec("L02a", i_ * j_ == k_ and j_ * k_ == i_ and k_ * i_ == j_ and j_ * i_ == -k_ and i_ * i_ == Q(-1, 0, 0, 0), "bảng i, j, k")
qz = Q(sp.cos(sp.pi / 4), 0, 0, sp.sin(sp.pi / 4))
v = qz * i_ * Q(sp.cos(sp.pi / 4), 0, 0, -sp.sin(sp.pi / 4))
rec("L02b", sp.simplify(v.a) == 0 and sp.simplify(v.b) == 0 and sp.simplify(v.c) == 1 and sp.simplify(v.d) == 0, "q i q⁻¹ = j với q = (cos45°, 0, 0, sin45°)")
rec("L02c", i_ * j_ * (-i_) == -j_, "câu đố: i j (−i) = −j")
rec("L02d", all(np.allclose(alg.qmat(alg.qaxis(ax, t)), np.array(Q.from_axis_angle(ax, t * sp.pi / 180).to_rotation_matrix().evalf(), float))
                for ax in ((0, 0, 1), (1, 0, 0), (1 / math.sqrt(2), 1 / math.sqrt(2), 0)) for t in (37, 90, 250)),
    "checklib.qaxis/qmat khớp sympy Quaternion.from_axis_angle")
rec("L02e", abs(math.hypot(0.7, 0.7) - 0.99) < 0.01, "(0,7; 0; 0; 0,7) có độ dài ≈ 0,99")

# ── L03 ──
T = sp.Matrix([[0, -1, 2], [1, 0, 0], [0, 0, 1]])
D = sp.Matrix([[1, 0, 2], [0, 1, 0], [0, 0, 1]])
R90 = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
rec("L03a", T * sp.Matrix([1, 0, 1]) == sp.Matrix([2, 1, 1]) and R90 * D * sp.Matrix([1, 0, 1]) == sp.Matrix([0, 3, 1]), "(2, 1) và (0, 3)")
rec("L03b", T.inv() == sp.Matrix([[0, 1, 0], [-1, 0, 2], [0, 0, 1]]) and T.inv() * sp.Matrix([2, 1, 1]) == sp.Matrix([1, 0, 1]), "nghịch đảo")
rec("L03c", T * sp.Matrix([[1, 0, sp.Rational(1, 2)], [0, 1, 0], [0, 0, 1]]) * sp.Matrix([1, 0, 1]) == sp.Matrix([2, sp.Rational(3, 2), 1]), "chuỗi camera (2; 1,5)")
Tq = sp.Matrix([[0, -1, 1], [1, 0, 1], [0, 0, 1]])
rec("L03d", Tq * sp.Matrix([2, 0, 1]) == sp.Matrix([1, 3, 1]) and Tq.inv() * sp.Matrix([1, 1, 1]) == sp.Matrix([0, 0, 1]) and Tq * sp.Matrix([1, 0, 0]) == sp.Matrix([0, 1, 0]),
    "câu đố L03")
rec("L03x", np.allclose(alg.homog2(90, 2, 0), np.array(T, float)), "checklib.homog2 khớp")

# ── L04 ──
t1, t2, L1, L2 = sp.symbols("t1 t2 L1 L2", real=True)
X = L1 * sp.cos(t1) + L2 * sp.cos(t1 + t2)
Y = L1 * sp.sin(t1) + L2 * sp.sin(t1 + t2)
tip = [sp.nsimplify(e.subs({L1: 1, L2: 1, t1: sp.pi / 6, t2: sp.pi / 3})) for e in (X, Y)]
rec("L04a", tip == [sp.sqrt(3) / 2, sp.Rational(3, 2)], f"đầu tay {tip}")
rec("L04b", sp.simplify(X ** 2 + Y ** 2 - (L1 ** 2 + L2 ** 2 + 2 * L1 * L2 * sp.cos(t2))) == 0, "r² = L₁² + L₂² + 2L₁L₂ cos θ₂ (ký hiệu)")
rec("L04c", [sp.nsimplify(e.subs({L1: 1, L2: 1, t1: sp.pi / 2, t2: -sp.pi / 2})) for e in (X, Y)] == [1, 1], "câu đố (1, 1)")
rec("L04d", [round(float(e.subs({L1: 1, L2: 1, t1: sp.pi / 6, t2: sp.pi / 3}).subs(t1 + t2, t2)), 3) for e in
             (sp.cos(sp.pi / 6) + sp.cos(sp.pi / 3), sp.sin(sp.pi / 6) + sp.sin(sp.pi / 3))] == [1.366, 1.366], "lỗi dùng θ₂ tuyệt đối: (1,366; 1,366)")
rec("L04x", np.allclose(alg.fk2(1.3, 0.7, 40, -75)[1], [float(e.subs({L1: 1.3, L2: 0.7, t1: 40 * sp.pi / 180, t2: -75 * sp.pi / 180})) for e in (X, Y)]),
    "checklib.fk2 khớp")

# ── L05 ──


def ik_lin(xt, yt):
    """Cách giải riêng: c₂ theo định lý cos; (cos θ₁, sin θ₁) từ hệ tuyến tính 2 × 2 (quay khâu ghép) — không dùng atan2."""
    c2 = sp.nsimplify((xt ** 2 + yt ** 2 - 2) / 2)
    out = []
    for s2 in sorted({sp.sqrt(1 - c2 ** 2), -sp.sqrt(1 - c2 ** 2)}, key=lambda v: -float(v)):
        Mx = sp.Matrix([[1 + c2, -s2], [s2, 1 + c2]])
        cs = sp.simplify(Mx.inv() * sp.Matrix([xt, yt]))
        a1 = float(sp.deg(sp.atan2(cs[1], cs[0])))
        a2 = float(sp.deg(sp.atan2(s2, c2)))
        out.append((round(a1, 6), round(a2, 6)))
    return out


deg = ik_lin(sp.sqrt(3) / 2, sp.Rational(3, 2))
rec("L05a", deg == [(30.0, 60.0), (90.0, -60.0)], f"hai nghiệm (hệ tuyến tính): {deg}")
rec("L05b", math.degrees(math.atan(-1 / -1)) == 45 and math.degrees(math.atan2(-1, -1)) == -135, "arctan mất góc phần tư")
rec("L05c", (16 - 4 - 1) / 4 == 2.75 and (0.25 - 4 - 1) / 4 == -1.1875 and (9 - 4 - 1) / 4 == 1, "c = 2,75; −1,1875; 1")
dq = ik_lin(sp.Integer(1), sp.Integer(1))
rec("L05d", dq == [(0.0, 90.0), (90.0, -90.0)], f"câu đố (1, 1): {dq}")
rec("L05x", alg.ik2(1, 1, 3 ** 0.5 / 2, 1.5) == [(30.0, 60.0), (90.0, -60.0)] and alg.ik2(2, 1, 4, 0) == [], "checklib.ik2 khớp")

# ── L06 ──
J = sp.Matrix([X, Y]).jacobian([t1, t2])
rec("L06a", sp.simplify(J.det() - L1 * L2 * sp.sin(t2)) == 0, "det J = L₁L₂ sin θ₂ (ký hiệu)")
J0 = J.subs({L1: 1, L2: 1, t1: sp.pi / 6, t2: sp.pi / 3})
rec("L06b", sp.simplify(J0 - sp.Matrix([[-sp.Rational(3, 2), -1], [sp.sqrt(3) / 2, 0]])) == sp.zeros(2), "J tại (30°, 60°)")
r_ = sp.symbols("r_", positive=True)
need = [round(float(sp.Rational(1, 10) / sp.sin(sp.rad(x) / 2)), 2) for x in (90, 30, 10, 1)]
rec("L06c", need == [0.14, 0.39, 1.15, 11.46], f"tốc độ khớp 2 cần cho 0,1 m/s hướng ra: {need} (r = 2cos(θ₂/2), dr/dθ₂ = −sin(θ₂/2))")
rec("L06d", J.subs({L1: 1, L2: 1, t1: 0, t2: sp.pi / 2}) == sp.Matrix([[-1, -1], [1, 0]]), "câu đố J")
rec("L06x", np.allclose(alg.jac2(1, 1, 30, 60), np.array(J0.evalf(), float)), "checklib.jac2 khớp")

# ── L07 ──
x = sp.Rational(1)
for _ in range(10):
    x = x * sp.Rational(9, 10)
rec("L07a", round(float(x), 4) == 0.3487 and round(math.exp(-1), 4) == 0.3679, "0,9¹⁰ = 0,3487; e⁻¹ = 0,3679")
errs = [round(math.exp(-1) - (1 - h) ** round(1 / h), 4) for h in (0.1, 0.05, 0.025)]
rec("L07b", errs == [0.0192, 0.0094, 0.0046], f"sai số Euler {errs}")
rec("L07c", [0, 1, 1.5] == [0, 0 + 0.5 * 2, 1 + 0.5 * 1], "câu đố Euler x' = 2 − x")
tt = sp.symbols("t")
rec("L07d", sp.simplify(sp.diff(sp.exp(-tt), tt) + sp.exp(-tt)) == 0 and sp.simplify(sp.diff(2 * (1 - sp.exp(-tt)), tt) - (2 - 2 * (1 - sp.exp(-tt)))) == 0,
    "e⁻ᵗ và 2(1 − e⁻ᵗ) là nghiệm đúng")
rec("L07x", round(alg.euler_ode(lambda t, v: -v, 1.0, 0.1, 10)[-1], 10) == round(0.9 ** 10, 10), "checklib.euler_ode khớp")

# ── L08 ──
hh = sp.Rational(1, 10)
k1 = -1
k2 = -(1 + hh / 2 * k1)
k3 = -(1 + hh / 2 * k2)
k4 = -(1 + hh * k3)
x1 = 1 + hh / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
rec("L08a", (k2, k3, k4) == (sp.Rational(-19, 20), sp.Rational(-381, 400), sp.Rational(-36190, 40000)) and x1 == sp.Rational(9048375, 10 ** 7),
    f"bốn độ dốc và x₁ = {x1}")
z = sp.Rational(-5)
rec("L08b", 1 + z + z ** 2 / 2 + z ** 3 / 6 + z ** 4 / 24 == sp.Rational(329, 24), "hệ số RK4 với z = −5: 329/24 ≈ 13,71")
zz = sp.Rational(-5, 2)
rec("L08c", round(float(1 + zz + zz ** 2 / 2 + zz ** 3 / 6 + zz ** 4 / 24), 3) == 0.648, "hệ số RK4 với z = −2,5: 0,648")
rec("L08d", 1 + sp.Rational(1 + 3 + sp.Rational(7, 2) + sp.Rational(11, 4)) / 6 == sp.Rational(65, 24), "câu đố x' = x, h = 1: 65/24 ≈ 2,7083")


def rk4_own(f, x0, h, n):
    xv = x0
    for _ in range(n):
        a1 = f(xv)
        a2 = f(xv + h / 2 * a1)
        a3 = f(xv + h / 2 * a2)
        a4 = f(xv + h * a3)
        xv = xv + h / 6 * (a1 + 2 * a2 + 2 * a3 + a4)
    return xv


e_rk = ["%.1e" % abs(rk4_own(lambda v: -v, 1.0, h, round(1 / h)) - math.exp(-1)) for h in (0.2, 0.1, 0.05)]
rec("L08e", e_rk == ["5.8e-06", "3.3e-07", "2.0e-08"], f"sai số RK4 {e_rk}")
rec("L08x", abs(alg.rk4_ode(lambda t, v: -v, 1.0, 0.1, 10)[-1] - rk4_own(lambda v: -v, 1.0, 0.1, 10)) < 1e-15, "checklib.rk4_ode khớp")

# ── L09 ──
lam = sp.symbols("lambda")
A = sp.Matrix([[0, 1], [-2, -3]])
rec("L09a", sp.factor((A - lam * sp.eye(2)).det()) == (lam + 1) * (lam + 2), "đa thức đặc trưng (λ + 1)(λ + 2)")
xs = 2 * sp.exp(-tt) * sp.Matrix([1, -1]) - sp.exp(-2 * tt) * sp.Matrix([1, -2])
rec("L09b", sp.simplify(xs.diff(tt) - A * xs) == sp.zeros(2, 1) and xs.subs(tt, 0) == sp.Matrix([1, 0]), "nghiệm dạng đóng thoả x' = Ax, x(0) = (1, 0)")
rec("L09c", [round(float(v), 4) for v in xs.subs(tt, 1)] == [0.6004, -0.4651], "x(1) = (0,6004; −0,4651)")
rec("L09d", set(sp.Matrix([[0, 1], [-5, -2]]).eigenvals()) == {-1 + 2 * sp.I, -1 - 2 * sp.I} and set(sp.Matrix([[0, 1], [2, -1]]).eigenvals()) == {1, -2}
    and set(sp.Matrix([[0, 1], [-4, 0]]).eigenvals()) == {2 * sp.I, -2 * sp.I}, "trị riêng −1 ± 2i; 1, −2; ±2i")

# ── L10 ──
Kp = sp.symbols("K", positive=True)
xss = sp.solve(-(1 + Kp) * sp.Symbol("x") + Kp, sp.Symbol("x"))[0]
rec("L10a", sp.simplify(1 - xss - 1 / (1 + Kp)) == 0 and xss.subs(Kp, 4) == sp.Rational(4, 5), "x_yên = K/(1 + K); K = 4: 0,8")
rec("L10b", set(sp.roots(lam ** 2 + 2 * lam + 4)) == {-1 + sp.sqrt(3) * sp.I, -1 - sp.sqrt(3) * sp.I} and sp.roots(lam ** 2 + 6 * lam + 9) == {-3: 2}, "−1 ± √3 i; −3 kép")
cubic = lambda K: sp.Poly((lam + 1) ** 3 + K, lam).nroots()  # noqa: E731
rec("L10c", max(sp.re(r) for r in cubic(4)) < 0 and max(sp.re(r) for r in cubic(10)) > 0 and abs(max(sp.re(r) for r in cubic(8))) < 1e-9,
    "ba tầng trễ: ổn định khi K = 4, biên K = 8, mất ổn định K = 10")
rec("L10x", abs(alg.pid_sim(4)[1] - 0.2) < 1e-6 and abs(alg.pid_sim(4, ki=4)[1]) < 1e-6, "checklib.pid_sim khớp (P còn 0,2; PI về 0)")

# ── L11 ──
hs = sp.symbols("h", positive=True)
sol = sp.solve_univariate_inequality(sp.Abs(1 - 10 * hs) < 1, hs, relational=False)
rec("L11a", sol == sp.Interval.open(0, sp.Rational(1, 5)), f"|1 − 10h| < 1 ⟺ h ∈ {sol}")
B = sp.eye(2) + sp.Rational(11, 10) * A
rec("L11b", sorted(abs(complex(v)) for v in B.eigenvals()) == sorted([0.1, 1.2]) or np.allclose(sorted(abs(complex(v)) for v in B.eigenvals()), [0.1, 1.2]),
    "I + 1,1A: trị riêng độ lớn 0,1 và 1,2")
rec("L11c", all(sp.Rational(1) - eta * 10 == sp.Rational(1) - eta * 10 for eta in (sp.Rational(3, 20), sp.Rational(1, 4))) and 1 - sp.Rational(3, 20) * 10 == sp.Rational(-1, 2),
    "GD f = 5w²: hệ số 1 − 10η, η = 0,15 → −0,5")

# ── L12 ──
w, P, Rr = sp.symbols("w P R", positive=True)
V = (1 - w) ** 2 * P + w ** 2 * Rr
wstar = sp.solve(sp.diff(V, w), w)[0]
rec("L12a", sp.simplify(wstar - P / (P + Rr)) == 0 and sp.simplify(V.subs(w, wstar) - P * Rr / (P + Rr)) == 0, "K = P/(P + R), P_mới = PR/(P + R) (ký hiệu)")
rng = np.random.default_rng(7)
mc = np.var(0.5 * rng.normal(0, 1, 400000) + 0.5 * rng.normal(0, 1, 400000))
rec("L12b", abs(mc - 0.5) < 0.005, f"Monte Carlo phương sai trung bình = {mc:.4f}")
rec("L12c", (sp.Rational(4, 8), 10 + sp.Rational(1, 2) * 2, sp.Rational(4, 8) * 4) == (sp.Rational(1, 2), 11, 2) and (sp.Rational(4, 5), 10 + sp.Rational(8, 5)) == (sp.Rational(4, 5), sp.Rational(58, 5)),
    "câu đố L12")

# ── L13 ──
F = sp.Matrix([[1, 1], [0, 1]])
H = sp.Matrix([[1, 0]])
Pp = F * sp.eye(2) * F.T
S = (H * Pp * H.T)[0] + 1
K = Pp * H.T / S
xn = F * sp.Matrix([0, 1]) + K * (sp.Rational(3, 2) - (H * F * sp.Matrix([0, 1]))[0])
Pn = (sp.eye(2) - K * H) * Pp
rec("L13a", Pp == sp.Matrix([[2, 1], [1, 1]]) and K == sp.Matrix([sp.Rational(2, 3), sp.Rational(1, 3)]) and xn == sp.Matrix([sp.Rational(4, 3), sp.Rational(7, 6)])
    and Pn == sp.Matrix([[sp.Rational(2, 3), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(2, 3)]]), "một bước Kalman vận tốc không đổi (phân số đúng)")
rec("L13b", set(Pn.eigenvals()) == {1, sp.Rational(1, 3)}, "trị riêng P mới: 1 và 1/3")
rec("L13x", np.allclose(alg.kalman_cv((0, 1), np.eye(2), 1.5, 1, np.zeros((2, 2)), 1)[3], np.array(xn, float).ravel()), "checklib.kalman_cv khớp")

# ── L14 ──
nn = sp.symbols("n", integer=True)
rec("L14a", sp.simplify(sp.cos(2 * sp.pi * 7 * nn / 10) - sp.cos(2 * sp.pi * 3 * nn / 10)) == 0 or
    all(sp.simplify(sp.cos(2 * sp.pi * 7 * k / 10) - sp.cos(2 * sp.pi * 3 * k / 10)) == 0 for k in range(20)), "mẫu 7 Hz = mẫu 3 Hz (lấy 10 lần/giây)")
rec("L14b", all(sp.sin(2 * sp.pi * 7 * k / 14) == 0 for k in range(28)), "sin 7 Hz lấy 14 lần/giây: toàn 0")
Xk = [abs(complex(sum(sp.N(sp.cos(2 * sp.pi * 2 * k / 10) + sp.Rational(1, 2) * sp.cos(2 * sp.pi * 4 * k / 10)) * sp.exp(-2 * sp.pi * sp.I * m * k / 10)
                       for k in range(10)))) for m in range(10)]
rec("L14c", [round(v, 3) for v in Xk] == [0, 0, 5, 0, 2.5, 0, 2.5, 0, 5, 0], f"|X_k| (dạng mũ phức) = {[round(v, 2) for v in Xk]}")
rec("L14d", [alg.alias_freq(f, fs) for f, fs in ((7, 10), (13, 10), (7, 15), (9, 10), (12, 10), (50, 90))] == [3, 3, 7, 1, 2, 40], "tần số biểu kiến")
rec("L14x", np.allclose(alg.dft_mag([math.cos(2 * math.pi * 2 * k / 10) + 0.5 * math.cos(2 * math.pi * 4 * k / 10) for k in range(10)]), Xk), "checklib.dft_mag khớp")

# ── L15 ── BFS riêng (không dùng alg) để kiểm độ dài và tính chấp nhận được
from collections import deque  # noqa: E402


def bfs(g, s0):
    dist, dq = {s0: 0}, deque([s0])
    while dq:
        p0 = dq.popleft()
        for dr, dc in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            q0 = (p0[0] + dr, p0[1] + dc)
            if 0 <= q0[0] < len(g) and 0 <= q0[1] < len(g[0]) and g[q0[0]][q0[1]] == "." and q0 not in dist:
                dist[q0] = dist[p0] + 1
                dq.append(q0)
    return dist


G = ["....", ".##.", "...."]
dg = bfs(G, (1, 3))
rec("L15a", dg[(1, 0)] == 5 and all(abs(r - 1) + abs(cc - 3) <= dg[(r, cc)] for r, cc in dg), "đường ngắn nhất 5; Manhattan không vượt thật")
rec("L15b", len(alg.astar_grid(G, (1, 0), (1, 3))[2]) == 6 and len(alg.astar_grid(G, (1, 0), (1, 3), lambda p0, q0: 0)[2]) == 10, "A* mở 6 ô, Dijkstra 10 ô")
G5 = [".....", ".#.#.", ".#...", "....#", "..#.."]
rec("L15c", bfs(G5, (0, 0))[(4, 4)] == 8 and alg.astar_grid(G5, (0, 0), (4, 4), lambda p0, q0: 3 * (abs(p0[0] - q0[0]) + abs(p0[1] - q0[1])))[0] == 10,
    "lưới 5 × 5: thổi phồng ×3 cho 10, đúng là 8")
rec("L15x", alg.astar_grid(G, (1, 0), (1, 3))[0] == dg[(1, 0)], "checklib.astar_grid khớp BFS")

# ── L16 ──
xv, yv = [0, 1, 2, 3], [sp.Integer(1), sp.Integer(3), sp.Rational(51, 10), sp.Rational(69, 10)]
xb, yb = sp.Rational(sum(xv), 4), sum(yv) / 4
a16 = sum((x0 - xb) * (y0 - yb) for x0, y0 in zip(xv, yv)) / sum((x0 - xb) ** 2 for x0 in xv)
b16 = yb - a16 * xb
rec("L16a", (a16, b16) == (sp.Rational(99, 50), sp.Rational(103, 100)), f"a = {a16}, b = {b16}")
res = [y0 - (a16 * x0 + b16) for x0, y0 in zip(xv, yv)]
s16 = sp.sqrt(sum(r0 ** 2 for r0 in res) / 2)
rec("L16b", sum(r0 ** 2 for r0 in res) == sp.Rational(18, 1000) and round(float(s16), 4) == 0.0949 and round(float(s16 / sp.sqrt(5)), 4) == 0.0424, "s, sai số chuẩn của a")
from sympy.stats import StudentT, cdf  # noqa: E402
rec("L16c", abs(float(cdf(StudentT("T", 2))(sp.Rational(4303, 1000))) - 0.975) < 1e-4, "t₀,₉₇₅ với 2 bậc tự do ≈ 4,303 (sympy.stats)")
rec("L16d", [round(float(s16 * sp.sqrt(sp.Rational(1, 4) + (x0 - xb) ** 2 / 5)), 3) for x0 in (sp.Rational(3, 2), 10)] == [0.047, 0.364], "độ không chắc 0,047 và 0,364")
xq, yq = [0, 1, 2], [0, sp.Rational(21, 10), sp.Rational(39, 10)]
aq = sum((x0 - 1) * (y0 - 2) for x0, y0 in zip(xq, yq)) / 2
rec("L16e", (aq, 2 - aq) == (sp.Rational(39, 20), sp.Rational(1, 20)) and round(float((3 - (2 - aq)) / aq), 3) == 1.513, "câu đố L16")
rec("L16x", tuple(round(v, 10) for v in alg.lsq_line([0, 1, 2, 3], [1, 3, 5.1, 6.9])[:2]) == (1.98, 1.03), "checklib.lsq_line khớp")

# ── L17 ── hành trình Kalman 1960 → 1985 (nguồn: audit/rbm/sources_L17.md); số minh hoạ ghi ở bài
Rt = sp.Rational
K1, K4 = [(1 + Rt(1, 2) * g) / (1 + Rt(1, 2) * g + 1) for g in (1, 4)]
rec("L17a", (K1, K4) == (Rt(3, 5), Rt(3, 4)), f"đo sau 1 giờ / 4 giờ (Q = 0,5 mỗi giờ): K = {K1}, {K4}")
Pn = sp.Integer(1)
for _ in range(99):
    Pn = Pn / (Pn + 1)
rec("L17b", Pn == Rt(1, 100) and round(float(Pn / (Pn + 1)), 4) == 0.0099, "Q = 0: sau 99 phép đo P = 1/100, K kế tiếp ≈ 0,0099")
Msym = sp.symbols("M", positive=True)
Mst = [r for r in sp.solve(sp.Eq(Msym - Rt(1, 10), Msym / (Msym + 1)), Msym)][0]
Pq = 1.0
for _ in range(300):
    Pq = (Pq + 0.1) / (Pq + 0.1 + 1)
rec("L17c", abs(float(Mst / (Mst + 1)) - Pq) < 1e-12 and round(Pq, 2) == 0.27 and round(float(Mst), 3) == 0.370 and round(1.1 / 2.1, 3) == 0.524,
    f"Q = 0,1: P + Q dừng ở {float(Mst):.4f}, K dừng ở {Pq:.4f} (nghiệm đúng của M² − 0,1M − 0,1 = 0)")
Kq, Pq_, Rq = sp.symbols("K P R", positive=True)
jos = (1 - Kq) ** 2 * Pq_ + Kq ** 2 * Rq
rec("L17d", sp.simplify(jos.subs(Kq, Pq_ / (Pq_ + Rq)) - (1 - Pq_ / (Pq_ + Rq)) * Pq_) == 0 and jos.subs({Kq: Rt(3, 10), Pq_: 1, Rq: 4}) == Rt(17, 20)
    and (1 - Rt(3, 10)) * 1 == Rt(7, 10), "dạng Joseph = dạng ngắn khi K tối ưu; K = 0,3: Joseph 0,85, dạng ngắn 0,7")
rng = np.random.default_rng(17)
xs_, zs_ = rng.normal(0, 1, 400000), rng.normal(0, 2, 400000)
rec("L17e", abs(np.var(0.7 * xs_ + 0.3 * zs_) - 0.85) < 0.01, f"Monte Carlo: phương sai thật khi K = 0,3 ≈ {np.var(0.7 * xs_ + 0.3 * zs_):.3f}")


def mults(a, b, c_):
    return a * b * c_


rec("L17f", mults(6, 1, 6) + mults(6, 6, 6) == 252 and mults(1, 6, 6) + mults(6, 1, 6) == 72 and sum(range(1, 101)) == 5050 and 6 + 36 == 42 and 6 * 7 // 2 == 21,
    "(KH)P 252 phép nhân, K(HP) 72; gom lô 5050 lần; lưu 42 số; nửa trên 21 ô")
hx = lambda x0, x: x0 ** 2 + 2 * x0 * (x - x0)  # noqa: E731
rec("L17g", hx(1, 3) == 5 and round(hx(2.8, 3), 10) == 8.96, "tuyến tính hoá x² quanh 1 → 5 (sai 4); quanh 2,8 → 8,96 (sai 0,04)")
rec("L17h", 3 * sp.sqrt(3 + 1) == 6 and 3 * sp.sqrt(12 + 4) == 12 and 3 * sp.sqrt(0 + 4) == 6, "ngưỡng 3 lần độ lệch chuẩn: 6; câu đố 12 và 6")
rec("L17i", 2 ** 24 == 16777216 and Rt(10 ** 6, 2 ** 24) > Rt(1, 100) and round(10 ** 6 / 2 ** 24, 4) == 0.0596 and Rt(1, 10) / Rt(1000, 2 ** 24) > 1600
    and Rt(400) / Rt(4, 10000) == 10 ** 6 and Rt(400) / Rt(4, 10 ** 6) == 10 ** 8, "từ 24 bit: phương sai 0,01 dưới một nấc 0,0596; độ lệch chuẩn 0,1 = hơn 1600 nấc; câu đố 10⁶ và 10⁸")
s17 = sp.sqrt(Rt(4, 5))
rec("L17j", sp.simplify(s17 ** 2 - (1 - Rt(1, 5)) * 1) == 0 and round(float(s17), 3) == 0.894, "căn bậc hai: s mới = √0,8 ≈ 0,894, bình phương = 0,8 của bài 12")
U17, D17 = sp.Matrix([[1, 1], [0, 1]]), sp.eye(2)
rec("L17k", U17 * D17 * U17.T == sp.Matrix([[2, 1], [1, 1]]), "U D Uᵀ = ma trận dự đoán của bài 13")
rec("L17x", alg.kalman1d_update(0, 3, 1, 1)[0] == 0.75 and alg.kalman1d_update(0, 1, 1, 4)[2] == 0.8, "checklib.kalman1d_update khớp")

n_ok = sum(ok for _, ok in R)
print(f"\n{n_ok}/{len(R)} PASS")
sys.exit(0 if n_ok == len(R) else 1)
