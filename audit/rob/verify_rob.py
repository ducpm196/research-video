"""Kiểm độc lập mọi khẳng định của khoá ROB — tính lại bằng cách KHÁC checklib, rồi đối chiếu với checklib (alg) mà `checks` dùng.
Xe vi sai: tích phân Euler bước rất nhỏ / công thức đóng. Cảm biến: tích phân số mật độ. Bộ lọc Bayes: phân số đúng (fractions).
Jacobian: sai phân hữu hạn. Lưới chiếm chỗ: Bayes trực tiếp trên tích xác suất. Đồ thị tư thế: sympy giải hệ đạo hàm bằng 0.
Lối hẹp: Monte Carlo. Điểm nhìn trước: giao hình học đường tròn. Camera: ma trận chiếu 3×4. Quãng dừng: mô phỏng phanh từng bước.
Chạy: .venv/Scripts/python audit/rob/verify_rob.py"""
import math
import sys
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402

R = []
rng = np.random.default_rng(2026)


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


# ── L00: ngân sách thời gian chu kỳ 50 Hz ──
rec("L00", 1000 / 50 == 20 and sum([4, 9, 2, 1]) == 16 and 1000 / 100 < 16, "chu kỳ 50 Hz = 20 ms, dùng 16 ms, dư 4 ms; ở 100 Hz (10 ms) không đủ")

# ── L01: xe vi sai — v = (vl + vr)/2, ω = (vr − vl)/b, R = v/ω; đi tròn đủ một vòng về gốc ──
vl, vr, b = 0.4, 0.6, 0.5
v, w = (vl + vr) / 2, (vr - vl) / b
x = y = th = 0.0
hh = 1e-4
for _ in range(round(2 * math.pi / w / hh)):
    x += v * hh * math.cos(th); y += v * hh * math.sin(th); th += w * hh
rec("L01", (round(v, 3), round(w, 3), round(v / w, 3)) == (0.5, 0.4, 1.25) == tuple(round(t, 3) for t in alg.diff_drive(0.4, 0.6, 0.5))
    and math.hypot(x, y) < 1e-3, "v 0,5; ω 0,4; R 1,25; đi đúng một vòng quay về gốc (Euler bước 0,0001)")

# ── L02: mã hoá vòng quay và trôi hướng ──
mm = math.pi * 100 / 1000
lat = 10 * math.tan(math.radians(1))
rec("L02", round(mm, 4) == 0.3142 == round(alg.encoder_mm_per_tick(0.1, 1000), 4) and round(3183 * mm / 1000, 3) == 1.0 and round(3342 * mm / 1000, 3) == 1.05
    and abs(lat - alg.heading_drift(10, 1)) < 1e-4 and round(alg.heading_drift(10, 1), 3) == 0.175 and round(alg.heading_drift(20, 0.5), 3) == 0.175,
    "0,3142 mm/xung; 3183 xung = 1 m; lệch 1° trên 10 m ≈ 0,175 m (sin ≈ tan)")

# ── L03: mô hình chùm tia — tích phân số kiểm mật độ, tỉ số e^4 ──
zs = np.linspace(0, 10, 2_000_001)
dens = 0.9 * np.exp(-(zs - 2) ** 2 / (2 * 0.01)) / (0.1 * math.sqrt(2 * math.pi)) + 0.1 / 10
rec("L03", abs(np.trapezoid(dens, zs) - 1) < 1e-6 and round(alg.beam_likelihood(2.1, 2, 0.1), 3) == 2.188 and round(alg.beam_likelihood(9.5, 2, 0.1), 3) == 0.01
    and abs(alg.gauss_pdf(2.1, 2, 0.1) / alg.gauss_pdf(2.3, 2, 0.1) - math.exp(4)) < 1e-9,
    "mật độ hỗn hợp tích phân bằng 1; 2,188 tại 2,1; 0,01 tại 9,5; tỉ số e mũ 4 ≈ 54,6")

# ── L04: bộ lọc Bayes rời rạc bằng phân số đúng ──
D = [Fr(8, 10) if i in (1, 4, 7) else Fr(1, 10) for i in range(10)]
b0 = [Fr(1, 10)] * 10
post = [p * l for p, l in zip(b0, D)]; s = sum(post); post = [p / s for p in post]
mv = [post[(i - 3) % 10] for i in range(10)]
post2 = [p * l for p, l in zip(mv, D)]; s = sum(post2); post2 = [p / s for p in post2]
rec("L04", post[1] == Fr(8, 31) and [round(float(p), 3) for p in post2] == [round(x, 3) for x in alg.hist_filter(alg.hist_filter([0.1] * 10, [float(d) for d in D]), [float(d) for d in D], move=3)]
    and round(float(post2[4]), 3) == 0.427, "sau đo: 8/31 ≈ 0,258 ở mỗi cửa; dịch 3 ô và đo lại: 0,427 ở ô 4 và 7")

# ── L05: Jacobian bằng sai phân hữu hạn; sai số tuyến tính hoá ──
def g(s, vh=1.0):
    return np.array([s[0] + vh * math.cos(s[2]), s[1] + vh * math.sin(s[2]), s[2]])


for th0 in (0.0, math.pi / 2):
    e = 1e-6
    J = np.column_stack([(g(np.array([0, 0, th0]) + e * np.eye(3)[k]) - g(np.array([0, 0, th0]) - e * np.eye(3)[k])) / (2 * e) for k in range(3)])
    ok5 = np.allclose(J, np.array(alg.motion_jacobian(th0, 1)), atol=1e-6)
    if not ok5:
        break
P = np.array(alg.motion_jacobian(0, 1)) @ np.diag([0.01] * 3) @ np.array(alg.motion_jacobian(0, 1)).T
rec("L05", ok5 and P.round(4).tolist() == [[0.01, 0, 0], [0, 0.02, 0.01], [0, 0.01, 0.01]]
    and [round((math.radians(d) - math.sin(math.radians(d))) / math.sin(math.radians(d)) * 100, 1) for d in (10, 30, 60)] == [0.5, 4.7, 20.9],
    "Jacobian sai phân khớp ở θ = 0 và 90°; hiệp phương sai sau một bước; sai số sin θ ≈ θ: 0,5% / 4,7% / 20,9%")

# ── L06: lưới chiếm chỗ — Bayes trực tiếp trên tích xác suất ──
def bayes_occ(seq):
    po, pf = Fr(1, 2), Fr(1, 2)
    for c in seq:
        po *= Fr(7, 10) if c == "h" else Fr(4, 10)
        pf *= Fr(3, 10) if c == "h" else Fr(6, 10)
    return float(po / (po + pf))


def clamp_seq(seq, L=3.5):
    l = 0.0
    for c in seq:
        l = max(-L, min(L, l + (math.log(7 / 3) if c == "h" else math.log(4 / 6))))
    return 1 / (1 + math.exp(-l))


rec("L06", [round(bayes_occ(s), 3) for s in ("hhh", "hhhmm", "hhhhh", "hm")] == [0.927, 0.85, 0.986, 0.609]
    == [round(alg.occ_update(0.5, 0.7, *a), 3) for a in ((3,), (3, 2), (5,), (1, 1))]
    and bayes_occ("h" * 20 + "m" * 6) > 0.9999 and round(clamp_seq("h" * 20 + "m" * 6), 3) == 0.744 == round(alg.occ_sequence(0.5, 0.7, 0.4, "h" * 20 + "m" * 6, 3.5), 3)
    and round(1 / (1 + math.exp(-3.5)), 3) == 0.971,
    "Bayes trực tiếp: 0,927 / 0,85 / 0,986 / 0,609; không chặn sau 20 chiếm + 6 trống vẫn > 0,9999; chặn ±3,5 → 0,744")

# ── L07: đồ thị tư thế — sympy cho đạo hàm tổng bình phương bằng 0 ──
def pg_sym(odom, loops):
    n = len(odom)
    X = sp.symbols(f"x1:{n + 1}")
    xs = (0,) + X
    E = sum((xs[i + 1] - xs[i] - sp.nsimplify(d)) ** 2 for i, d in enumerate(odom)) + sum((xs[j] - xs[i] - sp.nsimplify(d)) ** 2 for i, j, d in loops)
    sol = sp.solve([sp.diff(E, v) for v in X], X)
    return [float(sol[v]) for v in X]


ok7 = True
for od, lp in (([1, 1, 1], [(0, 3, 2.7)]), ([1, 1, 1], [(0, 3, 1.0)]), ([2, 2], [(0, 2, 3.8)])):
    ok7 &= np.allclose(pg_sym(od, lp), alg.pose_graph_1d(od, lp), atol=1e-9)
rec("L07", ok7 and [round(v, 3) for v in pg_sym([1, 1, 1], [(0, 3, 2.7)])] == [0.925, 1.85, 2.775] and [round(v, 3) for v in pg_sym([2, 2], [(0, 2, 3.8)])] == [1.933, 3.867],
    "nghiệm sympy khớp lstsq: 0,925 / 1,85 / 2,775; đóng vòng sai → 0,5 / 1 / 1,5; câu hỏi 1,933 / 3,867")

# ── L08: lối hẹp 1% — Monte Carlo ──
trials = rng.random((20_000, 300)) < 0.01
hit100, hit300 = trials[:, :100].any(1).mean(), trials.any(1).mean()
n_need = next(n for n in range(1, 2000) if 1 - 0.995 ** n >= 0.9)
rec("L08", abs(hit100 - 0.634) < 0.01 and abs(hit300 - 0.951) < 0.005 and n_need == 460 and 50 ** 7 == alg.grid_cells(50, 7) and 100 ** 6 == 10 ** 12,
    f"Monte Carlo: 100 mẫu {hit100:.3f} (≈ 0,634), 300 mẫu {hit300:.3f} (≈ 0,951); cần 460 mẫu cho 0,5% ở 90%")

# ── L09: cửa sổ động — liệt kê, an toàn bằng mô phỏng phanh ──
def brake_dist(v0, a, hstep=1e-5):
    d, vv = 0.0, v0
    while vv > 0:
        d += vv * hstep; vv -= a * hstep
    return d


cands = [(0.55, 0.5, 1.0), (0.8, 0.65, 0.6), (0.9, 0.35, 0.2)]
sc = [0.4 * a + 0.4 * c + 0.2 * s for a, c, s in cands]
sc2 = [0.2 * a + 0.2 * c + 0.6 * s for a, c, s in cands]
rec("L09", [round(x, 2) for x in sc] == [round(alg.dwa_score(*c), 2) for c in cands] == [0.62, 0.7, 0.54] and [round(x, 2) for x in sc2] == [0.81, 0.65, 0.37]
    and brake_dist(0.5, 0.5) > 0.2 > brake_dist(0.44, 0.5) and brake_dist(0.5, 0.5) < 0.5,
    "điểm 0,62 / 0,70 / 0,54; trọng số tốc độ 0,6 → 0,81 thắng; phanh từ 0,5 cần 0,25 m > 0,2 m (bị loại), < 0,5 m")

# ── L10: điểm nhìn trước — tâm (0, R) cách gốc và điểm đích đúng R ──
def circle_R(L, y):
    xg = math.sqrt(L * L - y * y)
    Rs = sp.symbols("R")
    return float(sp.solve(sp.Eq(xg ** 2 + (sp.nsimplify(y) - Rs) ** 2, Rs ** 2), Rs)[0])


rec("L10", abs(circle_R(2, 0.5) - 4) < 1e-9 and abs(circle_R(4, 0.5) - 16) < 1e-9 and abs(circle_R(1, -0.2) + 2.5) < 1e-9
    and alg.pure_pursuit(2, 0.5) == 0.25 and round(alg.pure_pursuit(1, -0.2), 3) == -0.4,
    "giao hình học: R = 4 / 16 m; điểm lệch phải 0,2 m với L = 1 → R = −2,5 (quay phải); κ khớp")

# ── L11: camera — ma trận chiếu K [I | 0], hai camera tịnh tiến B ──
K = np.array([[800, 0, 640], [0, 800, 360], [0, 0, 1.0]])


def proj(Pw, tx=0.0):
    q = K @ (np.array(Pw, float) - np.array([tx, 0, 0]))
    return tuple(np.round(q[:2] / q[2], 6))


dL, dR = proj((0.5, 0, 4)), proj((0.5, 0, 4), 0.12)
rec("L11", proj((0.5, 0, 4)) == proj((1, 0, 8)) == alg.pinhole(0.5, 0, 4, 800, 640, 360) and proj((-1, 0, 5)) == (480, 360)
    and abs((dL[0] - dR[0]) - 24) < 1e-9 and alg.stereo_depth(800, 0.12, 24) == 4.0 and [round(alg.stereo_depth(800, 0.12, d), 2) for d in (23, 25, 11, 13)] == [4.17, 3.84, 8.73, 7.38]
    and round(5 * math.tan(math.radians(1)), 2) == 0.09,
    "ma trận chiếu: hai điểm khác độ sâu cùng (740, 360); độ chênh hai camera tại 4 m đúng 24 điểm ảnh; 1° ở 5 m ≈ 9 cm")

# ── L12: quãng dừng — mô phỏng: chạy đều trong t, rồi phanh ──
def stop_sim(v0, a, t):
    return v0 * t + brake_dist(v0, a)


rec("L12", abs(stop_sim(1.5, 1, 0.2) - 1.425) < 1e-3 and abs(stop_sim(3, 1, 0.2) - 5.1) < 1e-3 and abs(stop_sim(1.5, 0.5, 0.2) - 2.55) < 1e-3
    and abs(stop_sim(alg.max_safe_speed(2, 1, 0.2), 1, 0.2) - 2) < 1e-3 and abs(stop_sim(2, 0.8, 0.25) - 3) < 1e-3
    and round(alg.max_safe_speed(3, 0.8, 0.25), 3) == 2.0 and round(alg.stop_distance(3, 1, 0.2) / alg.stop_distance(1.5, 1, 0.2), 2) == 3.58,
    "mô phỏng phanh: 1,425 / 5,1 / 2,55 m; tốc độ 1,81 m/s dừng đúng 2 m; 2 m/s, 0,8 m/s², 0,25 s dừng đúng 3 m")

# ── L13: hành trình xe tự lái — mô phỏng phanh từng bước (không dùng công thức đóng), hình học bằng toạ độ, đếm thẳng ──
_mph = 1609.344 / 3600                       # 1 dặm/giờ ra m/s, đổi từ định nghĩa 1 dặm = 1609,344 m
_s25, _s35 = stop_sim(25 * _mph, 4, 0.2), stop_sim(35 * _mph, 4, 0.2)
_lo = 0.0; _hi = 30.0                         # tìm nhị phân tốc độ lớn nhất dừng kịp trong 22 m (đường khác alg.max_safe_speed)
for _ in range(40):
    _mid = (_lo + _hi) / 2
    _lo, _hi = (_mid, _hi) if 0.2 * _mid + _mid * _mid / 8 <= 22 else (_lo, _mid)
_pt = (30 * math.cos(math.radians(0.5)), 30 * math.sin(math.radians(0.5)))   # điểm laser ở 30 m khi nghiêng 0,5°: toạ độ thật
_sim = [1] * 29 + [0] * 18                    # 1 = sự kiện chỉ có trong mô phỏng (người kèm đã ngăn)
rec("L13", abs(_s25 - 17.8) < 0.06 and _s25 < 22 < abs(_s35) and abs(_s35 - 33.7) < 0.06 and _s35 < 70
    and abs(_lo / _mph - alg.max_safe_speed(22, 4, 0.2) / _mph) < 1e-6 and round(_lo / _mph, 1) == 27.9
    and round(_pt[1], 3) == 0.262 > 0.15 and len(_sim) == 47 and round(sum(_sim) / len(_sim), 2) == 0.62
    and round(sum([24, 16, 8, 0]) / sum([31.159, 18.26, 6.448, 0.834]), 2) == 0.85
    and abs(stop_sim(3, 0.8, 0.25) - alg.stop_distance(3, 0.8, 0.25)) < 1e-3 and abs(stop_sim(2, 0.8, 0.25) - 3) < 1e-3,
    "phanh từng bước: 17,8 m (25 dặm/giờ) < 22 m < 33,7 m (35) < 70 m; nhị phân: 27,9 dặm/giờ; 0,5° ở 30 m → 0,262 m; 29/47 ≈ 62%; "
    "48 vụ / 56,7 triệu dặm ≈ 0,85; câu đố 3 m/s → 6,375 m, 2 m/s → 3 m")

bad = [c for c, ok in R if not ok]
print(f"\nverify_rob: {len(R) - len(bad)}/{len(R)} PASS" + (f"; FAIL: {bad}" if bad else ""))
sys.exit(1 if bad else 0)
