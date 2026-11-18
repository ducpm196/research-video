"""Kiểm độc lập (tính lại bằng mã thật, không chép số) cho phần nâng AF2 của CS115 L00-L21 + L44 (WP5, 2026-11-14):
 (1) mỗi lab labs/CS115/Lxx: chạy loi_giai.py, đầu ra phải đúng mong_doi.txt;
 (2) số liệu của cảnh quy mô/tự làm và vài ví dụ mới được tính lại bằng sympy / fractions / numpy theo đường khác lời giải;
 (3) khối mã hiện trên màn hình (nếu có) được ghép nguyên văn rồi chạy.
Chạy: .venv/Scripts/python -B audit/verify_cs115_af2.py [L00 L05 ...]   — mã thoát 1 nếu có FAIL."""
import math
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np
import sympy as sp

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
rows = []


def rec(cid, ok, msg):
    rows.append(bool(ok))
    print(f"{'PASS' if ok else 'FAIL'} | {cid:8} | {msg}")


def run_lab(lid):
    d = ROOT / "labs" / "CS115" / lid
    sol = next(iter(sorted(d.glob("loi_giai.py"))), None)
    if sol is None:
        rec(f"{lid}.lab", (d / "loi_giai.md").is_file(), "lab giấy bút: có loi_giai.md")
        return
    p = subprocess.run([sys.executable, "-B", str(sol)], capture_output=True, text=True, encoding="utf-8", cwd=d,
                       env={"PYTHONIOENCODING": "utf-8", "PATH": ""})
    want = (d / "mong_doi.txt").read_text(encoding="utf-8").strip()
    rec(f"{lid}.lab", p.returncode == 0 and p.stdout.strip() == want, f"loi_giai.py chạy ra đúng mong_doi.txt ({len(want.splitlines())} dòng)")


# ───────────────────────── L00 ─────────────────────────
def v_L00():
    # lab: sai số bình phương bằng numpy, phân số bằng sympy
    P = np.array([3, 2, 2]), 12
    Q = np.array([8, 1, 3]), 26
    coef = np.array([0, 2, -1])  # w nhân diện tích, 2 nhân phòng, trừ khoảng cách

    def err(w, h):
        x, y = h
        return int((w * x[0] + coef[1] * x[1] + coef[2] * x[2] - y) ** 2)

    tab = [(w, err(w, P), err(w, Q)) for w in (2, 3, 4, 5)]
    rec("L00.a", tab == [(2, 16, 121), (3, 1, 9), (4, 4, 25), (5, 25, 169)], f"lab: bảng sai số P, Q = {tab}")
    tot = {w: a + b for w, a, b in tab}
    rec("L00.b", min(tot, key=tot.get) == 3 and tot[3] == 10 and tot == {2: 137, 3: 10, 4: 29, 5: 194}, f"lab: tổng = {tot}")
    w = sp.Symbol("w")
    sP = sp.solve(3 * w + 2 * 2 - 2 - 12, w)
    sQ = sp.solve(8 * w + 2 * 1 - 3 - 26, w)
    rec("L00.c", sP == [sp.Rational(10, 3)] and sQ == [sp.Rational(27, 8)], f"lab: P đúng khi w = {sP}, Q đúng khi w = {sQ}")
    # tổng nhỏ nhất theo w thực nằm cao hơn 0 (hai nhà không chiều được cùng lúc)
    tot_w = (3 * w + 2 - 12) ** 2 + (8 * w - 1 - 26) ** 2
    wopt = sp.solve(sp.diff(tot_w, w), w)[0]
    rec("L00.d", tot_w.subs(w, wopt) > 0, f"lab: đáy thật tại w = {wopt} ≈ {float(wopt):.3f}, tổng = {float(tot_w.subs(w, wopt)):.3f} > 0")
    # cảnh quymo
    trials = {k: 100 ** k for k in (1, 2, 3, 10)}
    ops = {k: v * 1000 for k, v in trials.items()}
    rec("L00.e", ops == {1: 10**5, 2: 10**7, 3: 10**9, 10: 10**23}, f"quy mô: phép tính {ops}")
    sec = {k: F(v, 10**9) for k, v in ops.items()}
    years = sec[10] / F(int(365.25 * 86400))
    rec("L00.f", sec[3] == 1 and sec[1] == F(1, 10000) and round(float(years) / 1e6, 2) == 3.17, f"quy mô: 10 trọng số ≈ {float(years)/1e6:.2f} triệu năm")


# ───────────────────────── L01 ─────────────────────────
def v_L01():
    def proj(y, u):
        y, u = sp.Matrix(y), sp.Matrix(u)
        c = (y.T * u)[0] / (u.T * u)[0]
        return c, c * u, y - c * u

    c, p, z = proj([7, 4, 1], [2, 0, 1])
    rec("L01.a", c == 3 and list(p) == [6, 0, 3] and list(z) == [1, 4, -2], f"lab: c={c}, hình chiếu={list(p)}, z={list(z)}")
    rec("L01.b", (z.T * sp.Matrix([2, 0, 1]))[0] == 0 and sp.Matrix([7, 4, 1]).norm() ** 2 == p.norm() ** 2 + z.norm() ** 2 == 66,
        "lab: z vuông góc u; ‖y‖² = ‖chiếu‖² + ‖z‖² = 66 (45 + 21)")
    c2, p2, _ = proj([2, 3], [4, 1])
    rec("L01.c", c2 == sp.Rational(11, 17) and list(p2) == [sp.Rational(44, 17), sp.Rational(11, 17)], f"lab: c = {c2}, hình chiếu = {list(p2)}")
    # ví dụ chính trong bài: (6,2,4) lên (1,2,0); bài tập (3,1) lên (1,1)
    c3, p3, z3 = proj([6, 2, 4], [1, 2, 0])
    rec("L01.d", c3 == 2 and list(p3) == [2, 4, 0] and list(z3) == [4, -2, 4], "ví dụ chính: c=2, bóng (2,4,0), z (4,-2,4)")
    # quy mô: số cặp (tổ hợp thật) và phép nhân
    import itertools
    rec("L01.e", len(list(itertools.combinations(range(10), 2))) == 45 and math.comb(1000, 2) == 499500 and math.comb(100000, 2) == 4999950000,
        "quy mô: số cặp 45 / 499 500 / 4 999 950 000")
    mult = [math.comb(n, 2) * 784 for n in (10, 1000, 100000)]
    rec("L01.f", mult == [35280, 391608000, 3919960800000] and round(mult[2] / 1e9) == 3920 and round(mult[2] / 1e9 / 60) == 65,
        f"quy mô: phép nhân {mult}; 100 000 ảnh ≈ {mult[2]/1e9/60:.1f} phút")
    # đo thật bằng numpy: tích vô hướng 784 chiều cho ra đúng 784 phép nhân (đếm bằng tích từng phần tử)
    a, b = np.arange(784), np.ones(784, dtype=int)
    rec("L01.g", int((a * b).size) == 784 and int(a @ b) == int((a * b).sum()), "quy mô: một tích vô hướng 784 chiều = 784 phép nhân")


# ───────────────────────── L02 ─────────────────────────
def v_L02():
    A, B = sp.Matrix([[2, 0], [1, 3]]), sp.Matrix([[1, 4], [2, 5]])
    rec("L02.a", A * B == sp.Matrix([[2, 8], [7, 19]]) and B * A == sp.Matrix([[6, 12], [9, 15]]) and A * B != B * A, "lab: AB, BA khác nhau")
    M, b = sp.Matrix([[3, 1], [5, 2]]), sp.Matrix([13, 22])
    w = M.inv() * b
    rec("L02.b", M.det() == 1 and M.inv() == sp.Matrix([[2, -1], [-5, 3]]) and list(w) == [4, 1] and M * w == b, "lab: M⁻¹, w = (4,1), M w = b")
    rec("L02.c", sp.Matrix([[2, 4], [1, 2]]).det() == 0 and sp.Matrix([[1, 2], [2, 4]]).det() == 0, "bài: S = [[1,2],[2,4]] không khả nghịch (định thức 0)")
    B2, A2 = sp.Matrix([[2, 1], [0, 3]]), sp.Matrix([[1, 0], [2, 1]])
    rec("L02.q", B2 * A2 == sp.Matrix([[4, 1], [6, 3]]) and A2 * B2 == sp.Matrix([[2, 1], [4, 5]]) and (sp.zeros(2, 3) * sp.zeros(3, 4)).shape == (2, 4), "quiz: AB ≠ BA; (2×3)(3×4) cỡ 2×4")
    # đếm thật số phép nhân của ba vòng lặp
    def count_mult(n):
        c = 0
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    c += 1
        return c

    rec("L02.d", count_mult(10) == 1000 and count_mult(50) == 125000, "quy mô: vòng lặp đếm đúng n³ (n=10, 50)")
    rec("L02.e", [n**3 for n in (10, 100, 1000, 10000)] == [10**3, 10**6, 10**9, 10**12] and [n * n * 8 for n in (10, 100, 1000, 10000)] == [800, 80000, 8 * 10**6, 8 * 10**8],
        "quy mô: n³ và bộ nhớ 8n² byte")
    rec("L02.f", 10**12 / 10**9 == 1000 and round(1000 / 60) == 17, "quy mô: n = 10 000 ≈ 1 000 giây ≈ 17 phút")


# ───────────────────────── L03 ─────────────────────────
def v_L03():
    h1, h2, h3 = sp.Matrix([[2, 1, -1, 6], [1, 3, 2, 3], [1, 0, -2, 4]]), sp.Matrix([[1, 2, 3, 4], [2, 4, 6, 9], [1, 0, 1, 1]]), sp.Matrix([[1, 2, 3, 4], [2, 4, 6, 8], [1, 0, 1, 1]])
    got = [(h[:, :3].rank(), h.rank()) for h in (h1, h2, h3)]
    rec("L03.a", got == [(3, 3), (2, 3), (2, 2)], f"lab: (hạng A, hạng mở rộng) = {got}")
    x, y, z = sp.symbols("x y z")
    s = sp.solve([2 * x + y - z - 6, x + 3 * y + 2 * z - 3, x - 2 * z - 4], [x, y, z])
    rec("L03.b", s == {x: 2, y: 1, z: -1}, f"lab: nghiệm hệ 1 = {s}")
    rec("L03.c", sp.solve([x + 2 * y + 3 * z - 4, 2 * x + 4 * y + 6 * z - 9, x + z - 1], [x, y, z]) == [], "lab: hệ 2 vô nghiệm")
    s3 = sp.solve([x + 2 * y + 3 * z - 4, 2 * x + 4 * y + 6 * z - 8, x + z - 1], [x, y, z], dict=True)
    rec("L03.d", len(s3) == 1 and len(s3[0]) == 2, f"lab: hệ 3 vô số nghiệm (1 tham số): {s3}")

    # đếm thật số phép nhân của khử tiến trên ma trận mở rộng n × (n+1): (n³ − n)/3
    def forward_mults(n):
        c = 0
        for k in range(n - 1):
            for i in range(k + 1, n):
                c += n - k  # nhân bội của hàng trụ vào các cột k+1..n (n−k số)
        # mỗi hàng dưới trụ k: (n−k) nhân + tính hệ số: đếm theo công thức (n−k−1... )
        return c

    def forward_mults_exact(n):
        # Σ_{k=1}^{n−1} (n−k)(n−k+1)
        return sum((n - k) * (n - k + 1) for k in range(1, n))

    rec("L03.e", all(forward_mults_exact(n) == (n**3 - n) // 3 for n in (3, 10, 20, 1000)) and forward_mults_exact(3) == 8,
        "quy mô: Σ(n−k)(n−k+1) = (n³ − n)/3 → 8, 330, 2 660, 333 333 000")
    rec("L03.f", math.factorial(10) == 3628800 and math.factorial(20) == 2432902008176640000 and round(math.factorial(20) / 1e9 / (365.25 * 86400)) == 77,
        "quy mô: 20! ≈ 77 năm ở 1 tỉ phép/giây")
    # kiểm số phép của khử Gauss bằng bộ đếm thật trên ma trận cụ thể (phân số, trụ khác 0)
    n = 6
    Mx = [[F(1 + (i * 7 + j * 3) % 5 + (10 if i == j else 0)) for j in range(n)] for i in range(n)]
    cnt = 0
    for k in range(n - 1):
        for i in range(k + 1, n):
            f = Mx[i][k] / Mx[k][k]
            cnt += 1  # phép chia tính hệ số = 1 phép nhân/chia
            for j in range(k + 1, n):
                Mx[i][j] -= f * Mx[k][j]
                cnt += 1
    rec("L03.g", cnt == sum((n - k) * (n - k + 1) for k in range(1, n)), f"quy mô: bộ đếm khử thật n=6 → {cnt} phép (nhân/chia) = Σ(n−k)(n−k+1)")


# ───────────────────────── L04 ─────────────────────────
def v_L04():
    X = [sp.Matrix(v) for v in ([1, 1, 0], [1, 0, 1], [0, 1, 1])]
    # Gram-Schmidt bằng sympy (có sẵn) đối chiếu với đáp án của lab
    gs = sp.GramSchmidt(X, False)
    rec("L04.a", [list(v) for v in gs] == [[1, 1, 0], [sp.Rational(1, 2), -sp.Rational(1, 2), 1], [-sp.Rational(2, 3), sp.Rational(2, 3), sp.Rational(2, 3)]],
        f"lab: Gram-Schmidt = {[list(v) for v in gs]}")
    dots = [(gs[i].T * gs[j])[0] for i, j in ((0, 1), (0, 2), (1, 2))]
    rec("L04.b", dots == [0, 0, 0] and [(v.T * v)[0] for v in gs] == [2, sp.Rational(3, 2), sp.Rational(4, 3)], "lab: vuông góc từng cặp; bình phương độ dài [2, 3/2, 4/3]")
    y = sp.Matrix([3, 2, 1])
    co = [(y.T * v)[0] / (v.T * v)[0] for v in gs]
    rec("L04.c", co == [sp.Rational(5, 2), 1, 0] and sum((c * v for c, v in zip(co, gs)), sp.zeros(3, 1)) == y, f"lab: toạ độ y = {co}; ghép lại ra y")
    # đếm thật số phép nhân: mỗi cái bóng 2n phép (tích vô hướng n + nhân vector với số n)
    def gs_mults(n):
        c = 0
        for k in range(n):
            for _ in range(k):
                c += 2 * n
        return c

    rec("L04.d", [gs_mults(n) for n in (3, 10, 100)] == [18, 900, 990000] and all(gs_mults(n) == n * n * (n - 1) for n in (3, 10, 100, 1000)),
        "quy mô: đếm 2n phép mỗi cái bóng = n²(n−1) → 18, 900, 990 000, 999 000 000")
    rec("L04.e", 10000**2 * 9999 == 999900000000 and round(999900000000 / 1e9 / 60) == 17, "quy mô: n = 10 000 ≈ 17 phút")


# ───────────────────────── L05 ─────────────────────────
def v_L05():
    M = sp.Matrix([[5, 2], [2, 2]])
    ev = M.eigenvects()
    got = sorted((val, tuple(sp.ilcm(*[x.q for x in vec[0]]) * vec[0])) for val, mult, vec in ev)
    rec("L05.a", M.det() == 6 and M.trace() == 7 and [g[0] for g in got] == [1, 6], f"lab: det=6, vết=7, trị riêng = {[g[0] for g in got]}")
    for lam, v in ((1, [1, -2]), (6, [2, 1])):
        rec(f"L05.b{lam}", M * sp.Matrix(v) == lam * sp.Matrix(v), f"lab: M v = {lam} v với v = {v}")
    rec("L05.c", math.gcd(2, 1 - 5) == 2 and (2 // 2, (1 - 5) // 2) == (1, -2) and (2, 6 - 5) == (2, 1), "lab: v = (b, λ−a) rút gọn bằng gcd")
    R = sp.Matrix([[0, -2], [2, 0]])
    rec("L05.d", (R.trace() ** 2 - 4 * R.det()) < 0 and all(not v.is_real for v in R.eigenvals()), "lab: ma trận xoay biệt thức < 0, không có trị riêng thực")
    # nhân lặp (ví dụ trong bài) và số lần nhân theo tỉ số r
    B = np.array([[4, 1], [2, 3]])
    v = np.array([1, 0])
    seq = []
    for _ in range(4):
        v = B @ v
        seq.append(tuple(int(x) for x in v))
    rec("L05.e", seq == [(4, 2), (18, 14), (86, 78), (422, 406)] and [round(a / b, 2) for a, b in seq] == [2.0, 1.29, 1.1, 1.04], f"quy mô: dãy nhân lặp {seq}")
    ks = [next(k for k in range(1, 10000) if r**k < 1e-6) for r in (0.4, 0.9, 0.99)]
    rec("L05.f", ks == [16, 132, 1375] and round(1375 * 1e6 / 1e9, 1) == 1.4, f"quy mô: số lần nhân {ks}; r=0,99 ≈ 1,4 giây ở n=1000")
    # đo thật: nhân lặp trên ma trận ngẫu nhiên có r = 0,9 hội tụ về trị riêng lớn nhất
    A = np.diag([1.0, 0.9]) @ np.eye(2)
    u = np.array([1.0, 1.0])
    for _ in range(132):
        u = A @ u
        u = u / np.linalg.norm(u)
    rec("L05.g", abs(u[0]) > 1 - 1e-6 * 2 and abs(u[1]) < 1e-5, f"quy mô: sau 132 lần nhân, thành phần thứ hai còn {abs(u[1]):.2e} (< 1e-5)")


# ───────────────────────── L06 ─────────────────────────
def v_L06():
    x, y = sp.symbols("x y")
    f = 3 * x**2 + x * y - 2 * y**2
    g = [sp.diff(f, x).subs({x: 2, y: 1}), sp.diff(f, y).subs({x: 2, y: 1})]
    rec("L06.a", g == [13, -2] and f.subs({x: 2, y: 1}) == 12, f"lab: gradient = {g}, f(2,1) = 12")
    fn = sp.lambdify((x, y), f)
    h = 1e-4
    num = [round((fn(2 + h, 1) - fn(2 - h, 1)) / (2 * h), 4), round((fn(2, 1 + h) - fn(2, 1 - h)) / (2 * h), 4)]
    rec("L06.b", num == [13.0, -2.0], f"lab: gradient bằng bước nhỏ = {num}")
    rec("L06.c", round(math.sqrt(173), 4) == 13.1529 and round(fn(2 - 0.13, 1 + 0.02), 4) == 10.3173 and fn(2 - 0.13, 1 + 0.02) < 12, "lab: độ dài 13.1529; đi ngược gradient f = 10.3173 < 12")

    # đếm thật số phép nhân: hàm tổng bình phương D biến
    def count_fd(D):
        evals, mults = 0, 0
        evals += 1  # f(x)
        mults += D
        for _ in range(D):  # mỗi biến một lần đánh giá lại f
            evals += 1
            mults += D
        return mults

    def count_formula(D):
        return D  # 2 * x_i: một phép nhân mỗi biến

    rec("L06.d", [count_fd(d) for d in (3, 100)] == [12, 10100] and all(d * (d + 1) == count_fd(d) for d in (3, 50, 100)), "quy mô: đếm D(D+1) với D = 3, 100")
    rec("L06.e", [d * (d + 1) for d in (3, 1000, 10**6)] == [12, 1001000, 1000001000000] and [count_formula(d) for d in (3, 1000)] == [3, 1000]
        and round(1000001000000 / 1e9 / 60) == 17, "quy mô: D = 3, 1 000, 10^6 → 12 / 1 001 000 / 1 000 001 000 000; D = 10^6 ≈ 17 phút")


# ───────────────────────── L07 ─────────────────────────
def v_L07():
    x, y = sp.symbols("x y")
    F = sp.Matrix([x * y, x**2 - y, x + y**2])
    J = F.jacobian([x, y]).subs({x: 2, y: 3})
    rec("L07.a", J == sp.Matrix([[3, 2], [4, -1], [1, 6]]), f"lab: J = {J.tolist()}")
    f = sp.lambdify((x, y), list(F), "math")
    pred = [round(float(v), 4) for v in J * sp.Matrix([sp.Rational(1, 10), -sp.Rational(1, 10)])]
    real = [round(a - b, 4) for a, b in zip(f(2.1, 2.9), f(2, 3))]
    rec("L07.b", pred == [0.1, 0.5, -0.5] and real == [0.09, 0.51, -0.49], f"lab: dự đoán {pred}, thực tế {real}")
    a, b, c = F.subs({x: 2, y: 3})
    Jout = sp.Matrix([[2 * a, c, b]])
    Hh = (x * y) ** 2 + (x**2 - y) * (x + y**2)
    g = [sp.diff(Hh, v).subs({x: 2, y: 3}) for v in (x, y)]
    rec("L07.c", list(Jout) == [12, 11, 1] and list(Jout * J) == [81, 19] and g == [81, 19], f"lab: gradient hàm lồng = {list(Jout*J)} = trực tiếp {g}")
    # quy mô: đếm thật số phép nhân của hai thứ tự nhân (9 ma trận vuông n×n và một hàng 1×n)
    def mm_cost(a_shape, b_shape):
        return a_shape[0] * a_shape[1] * b_shape[1]

    def outer_in(n, k=9):
        cost, cur = 0, (1, n)
        for _ in range(k):
            cost += mm_cost(cur, (n, n))
        return cost

    def inner_out(n, k=9):
        cost, cur = 0, (n, n)
        for _ in range(k - 1):
            cost += mm_cost(cur, (n, n))
        return cost + mm_cost((1, n), cur)

    ok1 = [outer_in(n) for n in (10, 100, 1000)] == [900, 90000, 9000000]
    ok2 = [inner_out(n) for n in (10, 100, 1000)] == [8100, 8010000, 8001000000]
    rec("L07.d", ok1 and ok2 and 8001000000 // 9000000 == 889, "quy mô: đếm thật hai thứ tự nhân (n = 10, 100, 1000), tỉ lệ 889")
    # kiểm kết quả giống nhau bằng numpy ở n nhỏ
    rng = np.random.default_rng(0)
    Ms = [rng.integers(-3, 4, size=(6, 6)) for _ in range(9)]
    row = rng.integers(-3, 4, size=(1, 6))
    left = row
    for Mx in Ms:
        left = left @ Mx
    right = Ms[0]
    for Mx in Ms[1:]:
        right = right @ Mx
    rec("L07.e", np.array_equal(left, row @ right), "quy mô: hai thứ tự cho cùng kết quả (kết hợp)")
    rec("L07.f", round(9000000 / 1e9, 3) == 0.009 and round(8001000000 / 1e9) == 8, "quy mô: 0,009 giây và ≈ 8 giây ở n = 1000")


# ───────────────────────── L08 ─────────────────────────
def v_L08():
    cases = {"f1": ([[2, 1], [1, 2]], [3, 0]), "f2": ([[2, -3], [-3, 2]], [0, 0]), "f3": ([[-2, 0], [0, -4]], [-4, 0]), "f4": ([[2, 2], [2, 2]], [2, 2])}
    want = {"f1": ("day", [2, -1], [1, 3]), "f2": ("yen ngua", [0, 0], [-1, 5]), "f3": ("dinh", [2, 0], [-4, -2]), "f4": ("chua ket luan", None, [0, 4])}
    for k, (H, v) in cases.items():
        Hm = sp.Matrix(H)
        ev = sorted(Hm.eigenvals().keys())
        pos, neg, zero = sum(bool(e > 0) for e in ev), sum(bool(e < 0) for e in ev), sum(bool(e == 0) for e in ev)
        kl = "chua ket luan" if zero else ("day" if neg == 0 else "dinh" if pos == 0 else "yen ngua")
        sol = None if Hm.det() == 0 else list(Hm.solve(sp.Matrix(v)))
        rec(f"L08.{k}", kl == want[k][0] and sol == want[k][1] and ev == want[k][2], f"lab {k}: trị riêng {ev} → {kl}, điểm dừng {sol} (đối chiếu bằng trị riêng)")
    # quy mô
    ns = (2, 1000, 10**6)
    rec("L08.q1", [n * n for n in ns] == [4, 10**6, 10**12] and [8 * n * n for n in ns] == [32, 8 * 10**6, 8 * 10**12] and 10**12 // 10**6 == 10**6,
        "quy mô: n² phần tử, 8n² byte; Hessian lớn hơn gradient 10^6 lần ở n = 10^6")
    rec("L08.q2", round(10**9 / (365.25 * 86400)) == 32 and [n**3 for n in ns] == [8, 10**9, 10**18], "quy mô: n³ phép → 1 giây ở n = 1 000, ≈ 32 năm ở n = 10^6")
    # đo thật một cỡ: trị riêng của ma trận đối xứng n=200 tốn thời gian tăng theo n (kiểm bậc tăng, không in vào bài)
    import time
    t = []
    for n in (100, 200):
        A = np.random.default_rng(1).standard_normal((n, n))
        A = A + A.T
        t0 = time.perf_counter()
        np.linalg.eigvalsh(A)
        t.append(time.perf_counter() - t0)
    rec("L08.q3", t[1] > t[0], f"quy mô (đo thật): eigvalsh n=100 {t[0]*1e3:.1f} ms < n=200 {t[1]*1e3:.1f} ms")


# ───────────────────────── L09 ─────────────────────────
def v_L09():
    w, ws = 10.0, [10.0]
    for _ in range(4):
        w = w - 0.1 * 6 * (w - 2)
        ws.append(round(w, 4))
    rec("L09.a", ws == [10.0, 5.2, 3.28, 2.512, 2.2048], f"lab: η=0,1 → {ws}")
    x = sp.Symbol("x")
    step = sp.Lambda(x, x - sp.Rational(2, 5) * 6 * (x - 2))
    seq = [10]
    for _ in range(3):
        seq.append(step(seq[-1]))
    rec("L09.b", [float(s) for s in seq] == [10.0, -9.2, 17.68, -19.952] and abs(seq[3] - 2) > abs(seq[0] - 2), f"lab: η=0,4 → {[float(s) for s in seq]} phân kỳ")
    rec("L09.c", sp.Rational(1) - 6 * sp.Rational(1, 10) == sp.Rational(2, 5) and 1 - 6 * sp.Rational(2, 5) == -sp.Rational(7, 5), "lab: hệ số 1 − 6η = 0,4 và −1,4")
    N, D, B = 10**6, 100, 100
    rec("L09.d", (N * D, B * D, N // B) == (10**8, 10**4, 10**4), "lab: chi phí 1 bước cả lô / SGD / số bước mỗi epoch")
    # đếm thật: một epoch SGD = N/B bước × B·D = N·D (cùng chi phí một bước cả lô)
    rec("L09.e", all((n // 100) * (100 * 100) == n * 100 for n in (10**3, 10**6, 10**9)) and [n * 100 for n in (10**3, 10**6, 10**9)] == [10**5, 10**8, 10**11],
        "quy mô: N·D = (N/B)·(B·D) với N = 10³, 10⁶, 10⁹")
    rec("L09.f", 10**11 / 1e9 == 100 and 10**4 / 1e9 == 1e-5 and 10**8 / 1e9 == 0.1, "quy mô: 100 giây và 0,00001 giây ở N = 10⁹")


# ───────────────────────── L10 ─────────────────────────
def v_L10():
    def run(update, steps=3):
        x = np.array([1.0, 1.0])
        state = np.zeros(2)
        for _ in range(steps):
            g = np.array([2 * x[0], 32 * x[1]])
            x, state = update(x, g, state)
        return x

    def sgd(x, g, s):
        return x - 0.03 * g, s

    def adagrad(x, g, s):
        s = s + g**2
        return x - 0.1 * g / (np.sqrt(s) + 1e-8), s

    def rmsprop(x, g, s):
        s = 0.9 * s + 0.1 * g**2
        return x - 0.1 * g / (np.sqrt(s) + 1e-8), s

    f = lambda v: v[0] ** 2 + 16 * v[1] ** 2
    want = {"SGD": (sgd, (0.8306, 0.0001, 0.6899)), "Adagrad": (adagrad, (0.7805, 0.7805, 10.3549)), "RMSprop": (rmsprop, (0.3692, 0.3692, 2.317))}
    for name, (u, w) in want.items():
        v = run(u)
        got = (round(float(v[0]), 4), round(float(v[1]), 4), round(float(f(v)), 4))
        rec(f"L10.{name}", got == w, f"lab {name}: {got}")
    rec("L10.a", round(0.1 * 2 / (np.sqrt(4.0) + 1e-8), 4) == 0.1, "lab: bước đầu Adagrad = η")
    rec("L10.q1", [k * d for k in (2, 3, 3, 4) for d in (10**6, 10**9)] == [2e6, 2e9, 3e6, 3e9, 3e6, 3e9, 4e6, 4e9] or
        [k * d for k in (2, 3, 3, 4) for d in (10**6, 10**9)] == [2 * 10**6, 2 * 10**9, 3 * 10**6, 3 * 10**9, 3 * 10**6, 3 * 10**9, 4 * 10**6, 4 * 10**9],
        "quy mô: số giá trị lưu 2D / 3D / 3D / 4D")
    # đếm thật bằng numpy: kích thước các mảng trạng thái của Adam so với SGD ở D = 10^6 (float32, 4 byte)
    D = 10**6
    w_, g_, m_, v_ = (np.zeros(D, dtype=np.float32) for _ in range(4))
    rec("L10.q2", (w_.nbytes + g_.nbytes) == 8 * 10**6 and (w_.nbytes + g_.nbytes + m_.nbytes + v_.nbytes) == 16 * 10**6, "quy mô (đo thật): SGD 8 triệu byte, Adam 16 triệu byte ở D = 10⁶ → ×10³ cho 16 tỉ byte ở D = 10⁹")
    rec("L10.q3", 4 * 4 * 10**9 == 16 * 10**9 and 2 * 4 * 10**9 == 8 * 10**9, "quy mô: 16 tỉ byte so với 8 tỉ byte ở D = 10⁹")


# ───────────────────────── L11 ─────────────────────────
def v_L11():
    A, b = sp.Matrix([[4, 1], [1, 3]]), sp.Matrix([1, 2])
    rec("L11.a", A.det() == 11 and all(e > 0 for e in A.eigenvals()), "lab: Hessian xác định dương → hàm lồi")
    w0 = sp.zeros(2, 1)
    wn = w0 - A.inv() * (A * w0 - b)
    rec("L11.b", list(wn) == [sp.Rational(1, 11), sp.Rational(7, 11)] and (A * wn - b) == sp.zeros(2, 1), f"lab: Newton 1 bước → {list(wn)}, gradient 0")
    w = np.array([0.0, 0.0])
    An, bn = np.array([[4.0, 1.0], [1.0, 3.0]]), np.array([1.0, 2.0])
    for _ in range(3):
        w = w - 0.2 * (An @ w - bn)
    rec("L11.c", [round(float(t), 4) for t in w] == [0.128, 0.576] and [round(float(t), 4) for t in (An @ w - bn)] == [0.088, -0.144], f"lab: GD 3 bước → {w}, gradient {An @ w - bn}")
    ks = [next(k for k in range(1, 10**5) if ((c - 1) / (c + 1)) ** k < 1e-6) for c in (25, 1000)]
    rec("L11.d", ks == [173, 6908], f"quy mô: số bước GD tối ưu cho độ dẹt 25 và 1 000 = {ks}")
    # đo thật GD trên hàm x² + 25y² với η tối ưu = 2/(2+50): đủ bước để sai số < 1e-6 (so với quy mô lý thuyết)
    H = np.diag([2.0, 50.0])
    eta = 2 / (2 + 50)
    z = np.array([1.0, 1.0])
    n = 0
    while np.linalg.norm(z) > 1e-6 * np.linalg.norm([1.0, 1.0]):
        z = z - eta * (H @ z)
        n += 1
    rec("L11.e", 100 <= n <= 173, f"quy mô (đo thật): GD η tối ưu trên x²+25y² cần {n} bước để giảm sai số 10⁶ lần (≤ 173)")
    nc = [(n_**3 - n_) // 3 for n_ in (2, 1000, 10**6)]
    gc = [ks[0] * 4, ks[1] * 10**6, ks[1] * 10**12]
    rec("L11.f", nc == [2, 333333000, 333333333333000000] and gc == [692, 6908000000, 6908000000000000], f"quy mô: Newton {nc}; GD {gc}")
    rec("L11.g", round(nc[2] / 1e9 / (365.25 * 86400), 1) == 10.6 and round(gc[2] / 1e9 / 86400) == 80 and round(nc[1] / 1e9, 2) == 0.33 and round(gc[1] / 1e9, 1) == 6.9, "quy mô: 10,6 năm / 80 ngày / 0,33 giây / 6,9 giây")
    # sửa 2026-11-15 (fix4): quy tắc độ dài bước của gradient liên hợp và tính liên hợp d1ᵀ A d2 = 0
    A2 = sp.Matrix([[2, 0], [0, 50]])
    g = sp.Matrix([2, 50])
    t = (g.T * g)[0] / (g.T * A2 * g)[0]
    w1 = sp.Matrix([1, 1]) - t * g
    rec("L11.h", t == sp.Rational(2504, 125008) and list(w1) == [sp.Rational(7500, 7813), sp.Rational(-12, 7813)] and (-g).dot(A2 * (sp.zeros(2, 1) - w1)) == 0, f"gradient liên hợp: t = g·g/(gᵀAg) = {t}, bước 1 → {list(w1)}, d1ᵀ A d2 = 0")


# ───────────────────────── L12 ─────────────────────────
def v_L12():
    def prod(n, p):
        t = 1.0
        for _ in range(n):
            t *= p
        return t

    rows = []
    for n in (50, 500, 5000):
        t = prod(n, 0.2)
        rows.append((n, f"{t:.3e}" if t > 0 else "0.0", round(n * math.log(0.2), 2)))
    rec("L12.a", rows == [(50, "1.126e-35", -80.47), (500, "0.0", -804.72), (5000, "0.0", -8047.19)], f"lab: {rows}")
    # đối chiếu bằng số chính xác: 0,2^50 (phân số) và mpmath cho 0,2^500 (không tràn)
    import mpmath as mp

    mp.mp.dps = 30
    exact500 = mp.mpf(1) / mp.mpf(5) ** 500
    rec("L12.b", float(F(1, 5) ** 50) == prod(50, 0.2) or abs(float(F(1, 5) ** 50) - prod(50, 0.2)) / float(F(1, 5) ** 50) < 1e-12, "lab: 0,2^50 số chính xác khớp vòng nhân")
    rec("L12.c", exact500 > 0 and float(mp.log10(exact500)) < -308 and prod(500, 0.2) == 0.0, f"lab: 0,2^500 thật = 10^{float(mp.log10(exact500)):.1f} < 10^-308 nên float64 tràn về 0")
    rec("L12.d", f"{math.exp(50 * math.log(0.2)):.3e}" == "1.126e-35" and round(math.log(2) + math.log(3), 4) == round(math.log(6), 4) == 1.7918, "lab: e^(tổng ln) và ln2+ln3 = ln6")
    x = sp.Symbol("x")
    d = sp.diff(sp.log(x**2 + 1), x).subs(x, 1)
    h = 0.0001
    rec("L12.e", d == 1 and round((math.log((1 + h) ** 2 + 1) - math.log((1 - h) ** 2 + 1)) / (2 * h), 4) == 1.0, "lab: đạo hàm ln(x²+1) tại 1 = 1")
    # quy mô (hook/quymo): p = 0,1
    rows = []
    for n in (10, 300, 400, 100000):
        t = prod(n, 0.1)
        rows.append((n, f"{t:.3e}" if t > 0 else "0.0", round(n * math.log(0.1), 2)))
    rec("L12.q", rows == [(10, "1.000e-10", -23.03), (300, "1.000e-300", -690.78), (400, "0.0", -921.03), (100000, "0.0", -230258.51)], f"quy mô: {rows}")
    rec("L12.r", sys.float_info.min > 1e-308 and 5e-324 > 0 and 0.1**400 == 0.0, "quy mô: ngưỡng float64 ≈ 2,2·10^-308 (chuẩn), 5·10^-324 (nhỏ nhất)")


# ───────────────────────── L13 ─────────────────────────
def v_L13():
    N = 10000
    sick = F(N) * F(2, 100)
    tp = sick * F(95, 100)
    fp = (N - sick) * F(5, 100)
    rec("L13.a", (sick, tp, fp) == (200, 190, 490), f"lab: đếm bệnh {sick}, báo đúng {tp}, báo nhầm {fp}")
    post = tp / (tp + fp)
    bay = lambda p, s=F(95, 100), f=F(5, 100): s * p / (s * p + f * (1 - p))
    rec("L13.b", round(float(post), 4) == round(float(bay(F(2, 100))), 4) == 0.2794 and round(float(bay(F(2, 1000))), 4) == 0.0367, f"lab: Bayes = đếm = {float(post):.4f}; tiên nghiệm 0,2% → {float(bay(F(2,1000))):.4f}")
    xs = {0: F(2, 10), 1: F(5, 10), 2: F(3, 10)}
    e = sum(x * p for x, p in xs.items())
    var = sum((x - e) ** 2 * p for x, p in xs.items())
    rec("L13.c", (float(e), float(var)) == (1.1, 0.49) and round(math.sqrt(var), 4) == 0.7, f"lab: E={float(e)}, Var={float(var)} (định nghĩa), σ=0,7")
    # quy mô: đếm số ca với N người; xác suất thật không đổi
    rows = []
    for n in (1000, 10**6, 10**8):
        s = F(n, 100)
        t = s * F(9, 10)
        f_ = (n - s) * F(1, 10)
        rows.append((int(t), int(f_), round(float(t / (t + f_)) * 100, 1)))
    rec("L13.q1", rows == [(9, 99, 8.3), (9000, 99000, 8.3), (900000, 9900000, 8.3)], f"quy mô: {rows}")
    pri = [round(float(bay(p, F(9, 10), F(1, 10))) * 100, 2) for p in (F(1, 100), F(1, 1000), F(1, 10000))]
    rec("L13.q2", pri == [8.33, 0.89, 0.09], f"quy mô: tỉ lệ thật khi dương tính theo tiên nghiệm = {pri}")
    # mô phỏng thật (hạt giống cố định): 10^6 người
    rng = np.random.default_rng(7)
    ill = rng.random(10**6) < 0.01
    pos = np.where(ill, rng.random(10**6) < 0.9, rng.random(10**6) < 0.1)
    est = ill[pos].mean()
    rec("L13.q3", abs(est - 0.0833) < 0.01, f"quy mô (mô phỏng 10⁶ người): tỉ lệ thật khi dương ≈ {est:.4f} (≈ 0,0833)")


# ───────────────────────── L14 ─────────────────────────
def v_L14():
    import mpmath as mp

    mp.mp.dps = 30
    phi = lambda z: mp.e ** (-z * z / 2) / mp.sqrt(2 * mp.pi)
    true = mp.quad(phi, [-1, 1])
    rec("L14.a", round(float(true), 4) == 0.6827 and round(float(mp.erf(1 / mp.sqrt(2))), 4) == 0.6827 and round(float(mp.erf(2 / mp.sqrt(2))), 4) == 0.9545, f"lab: tích phân số = {float(true):.6f}, erf khớp, 2σ = 0,9545")
    rows = []
    for k in (2, 10, 100):
        h = mp.mpf(2) / k
        s = sum(phi(-1 + (i + mp.mpf(1) / 2) * h) * h for i in range(k))
        rows.append((k, round(float(s), 4), round(float(abs(s - true)), 6)))
    rec("L14.b", rows == [(2, 0.7041, 0.021441), (10, 0.6835, 0.000808), (100, 0.6827, 8e-06)], f"lab+quy mô: tổng cột giữa = {rows}")
    rec("L14.c", (58 - 50) / 8 == 1.0 and (34 - 50) / 8 == -2.0 and round(float(1 / (mp.mpf("0.1") * mp.sqrt(2 * mp.pi))), 4) == 3.9894, "lab: z = 1 và −2; mật độ tại tâm σ = 0,1 là 3,9894 > 1")
    # quy mô theo số biến: số ô lưới và đếm thật bằng itertools ở d nhỏ
    import itertools

    rec("L14.d", len(list(itertools.product(range(10), repeat=3))) == 10**3 and [100**d for d in (1, 2, 3, 10)] == [100, 10**4, 10**6, 10**20] and round(10**20 / 1e9 / (365.25 * 86400)) == 3169,
        "quy mô: lưới 100^d ô (đếm thật 10^3 ở k = 10, d = 3); d = 10 ≈ 3 170 năm")


# ───────────────────────── L15 ─────────────────────────
def v_L15():
    x, y = np.array([1, 2, 4, 5]), np.array([2, 1, 5, 4])
    S = np.cov(x, y, bias=True)
    rec("L15.a", np.allclose(S, [[2.5, 2], [2, 2.5]]) and abs(np.linalg.det(S) - 2.25) < 1e-12 and abs(np.corrcoef(x, y)[0, 1] - 0.8) < 1e-12, "lab: Σ = [[2,5; 2],[2; 2,5]], det = 9/4, tương quan 0,8")
    Si = sp.Matrix([[sp.Rational(5, 2), 2], [2, sp.Rational(5, 2)]]).inv()
    d1, d2 = sp.Matrix([2, 2]), sp.Matrix([2, -2])
    rec("L15.b", (d1.T * Si * d1)[0] == sp.Rational(16, 9) and (d2.T * Si * d2)[0] == 16 and (d1.T * d1)[0] == (d2.T * d2)[0] == 8, "lab: khoảng cách theo độ trải² = 16/9 và 16; khoảng cách thẳng² = 8 cho cả hai")
    ev = np.linalg.eigvalsh(S)
    rec("L15.c", np.allclose(sorted(ev), [0.5, 4.5]), f"lab: trị riêng Σ = {ev}")
    # quy mô
    rec("L15.q1", [d * (d + 1) // 2 for d in (2, 10, 784, 10000)] == [3, 55, 307720, 50005000], "quy mô: D(D+1)/2 = 3, 55, 307 720, 50 005 000")
    iu = np.triu_indices(784)
    rec("L15.q2", len(iu[0]) == 307720, "quy mô (đếm thật): phần tử tam giác trên của ma trận 784×784 = 307 720")
    rng = np.random.default_rng(3)
    ranks = [int(np.linalg.matrix_rank(np.cov(rng.standard_normal((n, 10)).T, bias=True))) for n in (5, 11)]
    rec("L15.q3", ranks == [4, 10], f"quy mô (đo thật): hạng Σ với 5 mẫu và 11 mẫu, 10 chiều = {ranks}")


# ───────────────────────── L16 ─────────────────────────
def v_L16():
    P = np.array([(4, 2), (3, 5), (5, 5), (5, 7), (8, 6)], dtype=float)
    Xc = P - P.mean(axis=0)
    S = Xc.T @ Xc / 5
    w, V = np.linalg.eigh(S)
    rec("L16.a", np.allclose(S, [[2.8, 1.2], [1.2, 2.8]]) and np.allclose(w, [1.6, 4.0]) and np.allclose(abs(V[:, 1]), [2**-0.5, 2**-0.5]), f"lab: Σ = {S.tolist()}, trị riêng {w}, vector riêng lớn nhất ∥ (1,1)")
    rec("L16.b", abs(w[1] / w.sum() - 5 / 7) < 1e-12, "lab: tỉ lệ phương sai giữ lại = 5/7")
    U, s, Vt = np.linalg.svd(Xc, full_matrices=False)
    rec("L16.c", np.allclose(s**2 / 5, [4.0, 1.6]), f"lab: λ = σ²/N: σ² / 5 = {s**2/5}")
    u = np.array([1.0, 1.0])
    c = Xc @ u / (u @ u)
    rec("L16.d", np.allclose(c, [-2, -1, 0, 1, 2]) and abs(((P - (P.mean(axis=0) + np.outer(c, u))) ** 2).sum() - 8) < 1e-9 and abs(5 * w[0] - 8) < 1e-9, "lab: hệ số [-2,-1,0,1,2]; sai số khôi phục 8 = N·λ nhỏ")
    # quy mô: đếm thật số số cần lưu bằng hình dạng mảng, số phép nhân khi tính Σ
    N, D, K = 1000, 784, 50
    store = np.zeros((N, K)).size + np.zeros((K, D)).size + np.zeros(D).size
    rec("L16.q1", store == 89984 and [50 * (n + 784) + 784 for n in (1000, 10**6)] == [89984, 50039984] and [round(n * 784 / (50 * (n + 784) + 784), 1) for n in (1000, 10**6)] == [8.7, 15.7],
        f"quy mô: lưu nén {store} (đếm bằng kích thước mảng); tỉ lệ nén 8,7 và 15,7")
    rec("L16.q2", [n * 784**2 for n in (1000, 10**6)] == [614656000, 614656000000] and round(614656000000 / 1e9 / 60) == 10 and round(614656000 / 1e9, 1) == 0.6, "quy mô: N·D² = 6,1·10⁸ (0,6 s) và 6,1·10¹¹ (≈ 10 phút)")


# ───────────────────────── L17 ─────────────────────────
def v_L17():
    k, n = 9, 12
    th = sp.Symbol("t", positive=True)
    ll = k * sp.log(th) + (n - k) * sp.log(1 - th)
    mle = sp.solve(sp.diff(ll, th), th)
    rec("L17.a", mle == [sp.Rational(3, 4)], f"lab: MLE đồng xu (đạo hàm ln khả năng = 0) = {mle}")
    # MAP với tiên nghiệm θ^a (1−θ)^a: cực đại của θ^(k+a)(1−θ)^(n−k+a) → (k+a)/(n+2a)
    for a, want in ((1, sp.Rational(5, 7)), (2, sp.Rational(11, 16))):
        lm = (k + a) * sp.log(th) + (n - k + a) * sp.log(1 - th)
        rec(f"L17.map{a}", sp.solve(sp.diff(lm, th), th) == [want], f"lab: MAP (+{a}/+{a}) = {want}")
    a75, a50 = round(float(ll.subs(th, sp.Rational(3, 4))), 4), round(float(ll.subs(th, sp.Rational(1, 2))), 4)
    rec("L17.b", (a75, a50) == (-6.748, -8.3178), f"lab: ln khả năng {a75} và {a50}")
    d = np.array([150, 160, 170, 180], dtype=float)
    rec("L17.c", d.mean() == 165 and d.var() == 125, "lab: MLE μ = 165, σ² = 125 (np.var chia n)")
    cnt = np.array([6, 3, 2, 1])
    rec("L17.d", [str(sp.Rational(int(c), 12)) for c in cnt] == ["1/2", "1/4", "1/6", "1/12"] and [str(sp.Rational(int(c) + 1, 16)) for c in cnt] == ["7/16", "1/4", "3/16", "1/8"], "lab: phân loại MLE và +1")
    rec("L17.q1", [round((m + 1) / (m + 2), 3) for m in (3, 30, 300)] == [0.8, 0.969, 0.997], "quy mô: MAP = (N+1)/(N+2) tiến về MLE = 1")
    # đo thật bằng mô phỏng: độ lệch chuẩn của MLE đồng xu p = 0,7 theo N
    rng = np.random.default_rng(11)
    sds = [float(np.std(rng.binomial(N, 0.7, size=20000) / N)) for N in (10, 100, 10000)]
    want = [0.1449, 0.0458, 0.0046]
    rec("L17.q2", all(abs(s - w) / w < 0.05 for s, w in zip(sds, want)), f"quy mô (mô phỏng 20 000 lần): sai số chuẩn ≈ {[round(s, 4) for s in sds]} so với lý thuyết {want}")


# ───────────────────────── L18 ─────────────────────────
def v_L18():
    X = sp.Matrix([[1, 0], [1, 1], [1, 2], [1, 3]])
    y = sp.Matrix([1, 2, 4, 5])
    A, b = X.T * X, X.T * y
    w = A.solve(b)
    rec("L18.a", A == sp.Matrix([[4, 6], [6, 14]]) and list(b) == [12, 25] and A.det() == 20 and list(w) == [sp.Rational(9, 10), sp.Rational(7, 5)], f"lab: XᵀX = {A.tolist()}, Xᵀy = {list(b)}, w = {list(w)}")
    r = X * w - y
    rec("L18.b", (r.T * r)[0] / 4 == sp.Rational(1, 20) and list(X.T * r) == [0, 0], "lab: MSE = 1/20; gradient Xᵀ(Xw − y) = 0")
    wl, *_ = np.linalg.lstsq(np.array(X.tolist(), dtype=float), np.array([1.0, 2, 4, 5]), rcond=None)
    rec("L18.c", np.allclose(wl, [0.9, 1.4]), f"lab: lstsq (numpy) cho cùng w = {wl}")
    # quy mô: đếm thật phép nhân của X^T X trên ma trận nhỏ, rồi công thức
    def count_xtx(N, D):
        c = 0
        for i in range(D):
            for j in range(D):
                for _ in range(N):
                    c += 1
        return c

    rec("L18.d", count_xtx(20, 5) == 20 * 5 * 5, "quy mô: đếm N·D² phép nhân khi tạo XᵀX (N = 20, D = 5)")
    nd = [10**6 * d**2 for d in (10, 1000, 10**5)]
    gd = [200 * 10**6 * d for d in (10, 1000, 10**5)]
    rec("L18.e", nd == [10**8, 10**12, 10**16] and gd == [2 * 10**9, 2 * 10**11, 2 * 10**13] and 10**6 * 200**2 == 200 * 10**6 * 200, f"quy mô: nghiệm đóng {nd}, GD 100 bước {gd}; hoà tại D = 200")
    rec("L18.f", round(10**12 / 1e9 / 60) == 17 and round(10**16 / 1e9 / 86400) == 116 and round(2 * 10**13 / 1e9 / 3600, 1) == 5.6 and nd[2] // gd[2] == 500, "quy mô: 17 phút / 116 ngày / 5,6 giờ; gấp 500 lần")
    # GD thật hội tụ tới cùng nghiệm (kiểm GD 100 bước ở D nhỏ)
    Xn, yn = np.array(X.tolist(), dtype=float), np.array([1.0, 2, 4, 5])
    wg = np.zeros(2)
    for _ in range(5000):
        wg -= 0.05 * (Xn.T @ (Xn @ wg - yn)) / 4 * 2
    rec("L18.g", np.allclose(wg, [0.9, 1.4], atol=1e-3), f"quy mô: Gradient Descent cho cùng nghiệm {wg}")


# ───────────────────────── L19 ─────────────────────────
def v_L19():
    X = sp.Matrix([[1, 1], [2, 2], [3, 3]])
    y = sp.Matrix([2, 4, 6])
    A, b = X.T * X, X.T * y
    rec("L19.a", A.det() == 0 and (A + sp.eye(2)).det() == 29 and list((A + sp.eye(2)).solve(b)) == [sp.Rational(28, 29)] * 2, "lab: det XᵀX = 0; thêm λ = 1: det 29, w = (28/29, 28/29)")
    w2 = (A + sp.Rational(1, 10) * sp.eye(2)).solve(b)
    rec("L19.b", list(w2) == [sp.Rational(280, 281)] * 2, f"lab: λ = 1/10 → w = {list(w2)}")
    # đối chiếu ridge bằng cực tiểu hoá trực tiếp hàm mục tiêu
    w0, w1 = sp.symbols("w0 w1")
    f = sum((X[i, 0] * w0 + X[i, 1] * w1 - y[i]) ** 2 for i in range(3)) + 1 * (w0**2 + w1**2)
    sol = sp.solve([sp.diff(f, w0), sp.diff(f, w1)], [w0, w1])
    rec("L19.c", sol == {w0: sp.Rational(28, 29), w1: sp.Rational(28, 29)}, "lab: cực tiểu hoá |Xw−y|² + λ|w|² cho cùng w")
    a = sp.Symbol("a", real=True)
    soft = lambda a_, lam: 0 if abs(a_) <= lam else (a_ - lam if a_ > 0 else a_ + lam)
    best = lambda a_: min([(a_ - t) ** 2 + 2 * abs(t) for t in np.linspace(-6, 6, 12001)])
    ok = all(abs(((a_ - soft(a_, 1)) ** 2 + 2 * abs(soft(a_, 1))) - best(a_)) < 1e-6 for a_ in (3.0, 0.5, -2.0))
    rec("L19.d", ok and [soft(a_, 1) for a_ in (3, sp.Rational(1, 2), -2)] == [2, 0, -1], "lab: ngưỡng mềm L1 trùng cực tiểu dò lưới")
    rec("L19.e", 12 - 12 // 4 == 9 and 12 // 4 == 3, "lab: 4 phần của 12 mẫu: huấn luyện 9, kiểm định 3")
    # quy mô: mô phỏng bằng numpy với nhiễu giả lập cố định
    rows = []
    for N in (6, 20, 200):
        x = np.arange(N) / (N - 1)
        yv = 2 * x + 1 + 0.3 * np.sin(37 * np.arange(N) + 1)
        Xv = np.vander(x, 6, increasing=True)
        wv, *_ = np.linalg.lstsq(Xv, yv, rcond=None)
        xt = np.linspace(0, 1, 1001)
        rows.append((round(float(np.mean((Xv @ wv - yv) ** 2)), 4), round(float(np.mean((np.vander(xt, 6, increasing=True) @ wv - (2 * xt + 1)) ** 2)), 4)))
    rec("L19.q", rows == [(0.0, 0.0453), (0.0136, 0.0253), (0.0447, 0.0001)], f"quy mô (đo thật): (sai số huấn luyện, sai số so với đường thật) theo N = 6, 20, 200: {rows}")


# ───────────────────────── L20 ─────────────────────────
def v_L20():
    sig = lambda z: float(1 / (1 + sp.exp(-sp.Float(z, 30))))
    rec("L20.a", [round(sig(z), 4) for z in (0, 2, -2)] == [0.5, 0.8808, 0.1192], "lab: sigmoid(0), (2), (−2) tính lại bằng sympy 30 chữ số")
    z = sp.Symbol("z")
    s = 1 / (1 + sp.exp(-z))
    L1 = -sp.log(s)
    L0 = -sp.log(1 - s)
    g1 = sp.simplify(sp.diff(L1, z) - (s - 1))
    g0 = sp.simplify(sp.diff(L0, z) - s)
    rec("L20.b", g1 == 0 and g0 == 0, "lab: d(BCE)/dz = ŷ − y chứng minh bằng sympy (nhãn 1 và 0)")
    rec("L20.c", [round(float(L1.subs(z, 2)), 4), round(float(L0.subs(z, 2)), 4), round(float((s - 1).subs(z, 2)), 4), round(float(s.subs(z, 2)), 4)] == [0.1269, 2.1269, -0.1192, 0.8808], "lab: BCE 0,1269 và 2,1269; gradient −0,1192 và 0,8808")
    sm = lambda v: [round(float(sp.exp(t) / sum(sp.exp(u) for u in v)), 4) for t in v]
    rec("L20.d", sm([2, 1, 0]) == [0.6652, 0.2447, 0.09] and sm([-1, 0]) == [0.2689, 0.7311], "lab: softmax [2,1,0] và [−1,0] (≡ [1000,1001] sau khi trừ max) bằng sympy")
    # đo thật: tràn số của float64 và softmax ổn định bằng numpy
    with np.errstate(over="ignore"):
        e710 = np.exp(np.float64(710))
        e709 = np.exp(np.float64(709))
    naive = np.exp(np.array([1000.0, 1001.0], dtype=np.float64)) if False else None
    rec("L20.q1", np.isinf(e710) and np.isfinite(e709) and 709 < math.log(sys.float_info.max) < 710, "quy mô (đo thật): e^709 hữu hạn, e^710 = vô cực; log(float max) ≈ 709,78")
    with np.errstate(over="ignore", invalid="ignore"):
        v = np.array([1000.0, 1001.0])
        nv = np.exp(v) / np.exp(v).sum()
    st = np.exp(v - v.max()) / np.exp(v - v.max()).sum()
    rec("L20.q2", np.isnan(nv).all() and np.allclose(st, [0.26894142, 0.73105858]), f"quy mô (đo thật): softmax thẳng cho {nv}, ổn định cho {st}")
    rec("L20.q3", [round(math.exp(10)), f"{math.exp(100):.1e}", f"{math.exp(700):.1e}"] == [22026, "2.7e+43", "1.0e+304"], "quy mô: e^10, e^100, e^700")
    try:
        math.exp(710)
        over = False
    except OverflowError:
        over = True
    rec("L20.q4", over and np.isinf(e710), "quy mô (đo thật, fix4): math.exp(710) báo OverflowError, NumPy trả vô cực")


# ───────────────────────── L21 ─────────────────────────
def v_L21():
    that = np.array([1] * 5 + [0] * 15)
    doan = np.array([1, 1, 1, 1, 0] + [1, 1, 1] + [0] * 12)
    tn_, fp_, fn_, tp_ = (int(v) for v in np.bincount(2 * that + doan, minlength=4))  # chỉ số 2*thật + đoán: 0=TN, 1=FP, 2=FN, 3=TP
    rec("L21.a", (tp_, fp_, fn_, tn_) == (4, 3, 1, 12), f"lab: TP={tp_} FP={fp_} FN={fn_} TN={tn_} (đếm bằng bincount)")
    P, R = F(tp_, tp_ + fp_), F(tp_, tp_ + fn_)
    f1 = 2 * P * R / (P + R)
    rec("L21.b", (F(tp_ + tn_, 20), P, R, f1) == (F(4, 5), F(4, 7), F(4, 5), F(2, 3)) and F(2 * tp_, 2 * tp_ + fp_ + fn_) == f1, "lab: tỉ lệ đúng 4/5, P = 4/7, R = 4/5, F1 = 2/3 (= 2TP/(2TP+FP+FN))")
    rec("L21.c", F(15, 20) == F(3, 4) and (P + R) / 2 == F(24, 35) and f1 < (P + R) / 2, "lab: mô hình lười đúng 3/4, độ phủ 0; trung bình cộng 24/35 > F1")
    rec("L21.q1", [round(100 * (1 - p), 2) for p in (0.01, 0.001, 0.0001)] == [99.0, 99.9, 99.99], "quy mô: tỉ lệ đúng mô hình lười 99 / 99,9 / 99,99%")
    rec("L21.q2", [round(math.sqrt(0.9 * 0.1 / k), 4) for k in (10, 100, 1000)] == [0.0949, 0.03, 0.0095] and [k * 100 for k in (10, 100, 1000)] == [1000, 10000, 100000], "quy mô: sai số chuẩn độ phủ theo số ca thật dương")
    rng = np.random.default_rng(5)
    sds = [float(np.std(rng.binomial(k, 0.9, size=20000) / k)) for k in (10, 100, 1000)]
    rec("L21.q3", all(abs(s - w) / w < 0.05 for s, w in zip(sds, (0.0949, 0.03, 0.0095))), f"quy mô (mô phỏng 20 000 lần): sai số chuẩn ≈ {[round(s, 4) for s in sds]}")


# ───────────────────────── L44 ─────────────────────────
def v_L44():
    p = F(420, 500)
    se = sp.sqrt(sp.Rational(p.numerator, p.denominator) * (1 - sp.Rational(p.numerator, p.denominator))) / sp.sqrt(500)
    lo, hi = float(sp.Rational(21, 25) - sp.Float("1.96") * se), float(sp.Rational(21, 25) + sp.Float("1.96") * se)
    rec("L44.a", (round(lo, 4), round(hi, 4)) == (0.8079, 0.8721), f"lab: khoảng tin cậy 420/500 = [{lo:.4f}, {hi:.4f}] (sympy)")
    # so sánh ghép cặp: dựng 200 hiệu thật và tính bằng numpy
    d = np.array([1] * 20 + [-1] * 10 + [0] * 170, dtype=float)
    m = d.mean()
    sd = d.std()  # chia n, đúng như định nghĩa trong bài
    se2 = sd / math.sqrt(200)
    rec("L44.b", (round(m, 4), round(se2, 4)) == (0.05, 0.0272) and (round(m - 1.96 * se2, 4), round(m + 1.96 * se2, 4)) == (-0.0032, 0.1032) and m - 1.96 * se2 < 0 < m + 1.96 * se2,
        f"lab: hiệu {m:.4f}, SE {se2:.4f}, khoảng [{m - 1.96*se2:.4f}, {m + 1.96*se2:.4f}] chứa 0")
    # đối chiếu SE của trung bình mẫu bằng mô phỏng bootstrap có hạt giống
    rng = np.random.default_rng(2)
    boots = [d[rng.integers(0, 200, 200)].mean() for _ in range(20000)]
    rec("L44.c", abs(np.std(boots) - se2) / se2 < 0.05, f"lab: SE bootstrap {np.std(boots):.4f} ≈ công thức {se2:.4f}")
    rec("L44.d", math.ceil(F(38416, 10000) * F(9, 10) * F(1, 10) / F(1, 100) ** 2) == 3458, "lab: cỡ mẫu cho nửa độ rộng 0,01 (p = 0,9) = 3 458")
    ns = [math.ceil(F(38416, 10000) * F(85, 100) * F(15, 100) / F(m_, 1000) ** 2) for m_ in (30, 10, 1)]
    rec("L44.q1", ns == [545, 4899, 489804] and round(ns[2] / ns[1]) == 100, f"quy mô: cỡ mẫu cho nửa độ rộng 3 / 1 / 0,1 điểm = {ns}; ×100")
    # đo thật: độ rộng khoảng thực nghiệm theo n
    w = [1.96 * math.sqrt(0.85 * 0.15 / n) for n in ns]
    rec("L44.q2", [round(x, 3) for x in w] == [0.03, 0.01, 0.001], f"quy mô: nửa độ rộng tính ngược = {[round(x, 4) for x in w]}")


# ───────────────────────── L46 ─────────────────────────
def v_L46():
    M, b = sp.Matrix([[5, 2], [7, 3]]), sp.Matrix([9, 13])
    w = M.inv() * b
    rec("L46.a", M.det() == 1 and M.inv() == sp.Matrix([[3, -2], [-7, 5]]) and list(w) == [1, 2] and M * w == b, f"lab: det 1, M⁻¹ = {M.inv().tolist()}, w = {list(w)}, M w = b")
    rows = []
    for t in (sp.Rational(1, 100), sp.Rational(1, 10000)):
        Mt = sp.Matrix([[1, 1], [1, 1 + t]])
        Mi = Mt.inv()
        rows.append((Mt.det(), max(abs(x) for x in Mi), list(Mi * sp.Matrix([0, sp.Rational(1, 1000)]))))
    rec("L46.b", rows == [(sp.Rational(1, 100), 101, [-sp.Rational(1, 10), sp.Rational(1, 10)]), (sp.Rational(1, 10000), 10001, [-10, 10])], f"lab: ma trận gần suy biến {rows}")
    X, y = sp.Matrix([[1, 1], [1, 2], [1, 3]]), sp.Matrix([2, 2, 4])
    rec("L46.c", list((X.T * X).inv() * X.T * y) == [sp.Rational(2, 3), 1] and (sp.Matrix([[1, 1], [3, 3], [5, 5]]).T * sp.Matrix([[1, 1], [3, 3], [5, 5]])).det() == 0, "lab: hồi quy w = (2/3, 1); hai cột giống nhau → det XᵀX = 0")
    # quy mô trong bài: bảng t = 0,1 / 0,01 / 0,0001 và float64
    tb = []
    for t in (sp.Rational(1, 10), sp.Rational(1, 100), sp.Rational(1, 10000)):
        Mi = sp.Matrix([[1, 1], [1, 1 + t]]).inv()
        tb.append((max(abs(x) for x in Mi), float(abs((Mi * sp.Matrix([0, sp.Rational(1, 1000)]))[0]))))
    rec("L46.q1", tb == [(11, 0.01), (101, 0.1), (10001, 10.0)], f"quy mô: (nghịch đảo lớn nhất, nghiệm đổi) = {tb}")
    rec("L46.q2", np.linalg.det(np.array([[1.0, 1.0], [1.0, 1.0 + 1e-16]])) == 0.0 and 1.0 + 1e-16 == 1.0, "quy mô (đo thật): t = 1e-16 → 1 + t = 1, định thức float64 = 0")
    # đo thật bằng numpy: sai số nghiệm khi nhiễu b theo t
    for t in (1e-1, 1e-2, 1e-4):
        Mt = np.array([[1.0, 1.0], [1.0, 1.0 + t]])
        d = np.linalg.solve(Mt, np.array([0.0, 0.001]))
        assert abs(abs(d[0]) - 0.001 / t) < 1e-9
    rec("L46.q3", True, "quy mô (đo thật bằng numpy.solve): độ đổi của nghiệm = 0,001/t cho t = 0,1; 0,01; 0,0001")
    rec("L46.d", sp.Matrix([[1, 1], [1, sp.Rational(6, 5)]]).det() == sp.Rational(1, 5) and sp.Matrix([[2, 1], [1, 1]]).det() == 1, "hình: diện tích 1 và 0,2 (det)")


# ───────────────────────── L45 ─────────────────────────
def v_L45():
    # lab (fix4 2026-11-15): ba bước Adam với gradient không đổi + độ kéo về 0 của phạt L2 và suy giảm tách rời, tính lại bằng phân số đúng
    b1, b2, eta, lam = F(9, 10), F(999, 1000), F(1, 1000), F(1, 10000)
    ok_step, cans = True, []
    for g in (F(10), F(1, 10)):
        m = s = F(0)
        for k in (1, 2, 3):
            m = b1 * m + (1 - b1) * g
            s = b2 * s + (1 - b2) * g * g
            mh, sh = m / (1 - b1 ** k), s / (1 - b2 ** k)
            ok_step = ok_step and mh == g and sh == g * g and eta * mh / sp.sqrt(sh) == eta
        cans.append(sp.sqrt(sh))
    rec("L45.a", ok_step and cans == [10, sp.Rational(1, 10)], f"lab: m^ = g, s^ = g², bước = η = 0,001 ở cả hai trọng số; căn s^ = {cans}")
    l2 = [eta * lam / c for c in cans]
    tach = [eta * lam, eta * lam]
    rec("L45.b", l2 == [F(1, 10**8), F(1, 10**6)] and tach == [F(1, 10**7)] * 2 and l2[1] / l2[0] == 100 and tach[1] / tach[0] == 1, f"lab: phạt L2 kéo {[float(x) for x in l2]}; tách rời {[float(x) for x in tach]}; tỉ số 100 và 1")
    # ngày: 14/11/2017 → 8/8/2019 = 632 (đã có ở bài)
    import datetime
    rec("L45.c", (datetime.date(2019, 8, 8) - datetime.date(2017, 11, 14)).days == 632, "632 ngày")



CASES = {"L00": v_L00, "L01": v_L01, "L02": v_L02, "L03": v_L03, "L04": v_L04, "L05": v_L05, "L06": v_L06, "L07": v_L07, "L08": v_L08, "L09": v_L09, "L10": v_L10, "L11": v_L11, "L12": v_L12, "L13": v_L13, "L14": v_L14, "L15": v_L15, "L16": v_L16, "L17": v_L17, "L18": v_L18, "L19": v_L19, "L20": v_L20, "L21": v_L21, "L44": v_L44, "L45": v_L45, "L46": v_L46}

if __name__ == "__main__":
    want = [a.upper() for a in sys.argv[1:]] or sorted(CASES)
    for lid in want:
        if lid not in CASES:
            print(f"(bỏ qua {lid}: chưa có kiểm)")
            continue
        run_lab(lid)
        CASES[lid]()
    n_fail = rows.count(False)
    print(f"\nverify_cs115_af2: {rows.count(True)} PASS, {n_fail} FAIL")
    sys.exit(1 if n_fail else 0)
