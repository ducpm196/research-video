"""Kiểm độc lập mọi khẳng định của khoá DAN — tính lại bằng cách KHÁC checklib, rồi đối chiếu với checklib (alg) mà `checks` dùng.
Định nghĩa chỉ số: đếm bằng vòng lặp thuần. Trung bình có trọng số: sympy phân số đúng. Nhân dòng: tự cài phép nối lồng nhau (không dùng SQL).
Hàm cửa sổ: tính tay bằng numpy.cumsum/diff, xếp hạng bằng định nghĩa “1 + số giá trị lớn hơn”. Nhóm theo kỳ: dựng từ nhật ký người dùng mô phỏng.
Phễu: nhật ký sự kiện có thời điểm. Trung bình trượt: numpy.convolve. Dự báo: vòng lặp. Bất thường: sắp xếp tay. Wilson: giải bất phương trình bậc hai
bằng sympy (định nghĩa gốc của khoảng điểm số) + Monte Carlo độ phủ. Cảnh báo: mô phỏng ngày. Chạy: .venv/Scripts/python audit/dan/verify_dan.py"""
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
rng = np.random.default_rng(2026)


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


# ── L00: đếm bằng vòng lặp ──
seen_login, seen_action = set(), set()
for u, e in alg.DAN_LOG:
    (seen_login if e == "dang_nhap" else seen_action).add(u)
rec("L00", (len(seen_login), len(seen_action)) == (6, 4) == (alg.dan_active(alg.DAN_LOG, "login"), alg.dan_active(alg.DAN_LOG, "action"))
    and sum(1 for u, e in alg.DAN_LOG if e == "mua") == 1, "vòng lặp: đăng nhập 6, có thao tác 4, có mua 1")

# ── L01: phân số đúng ──
rec("L01", sp.Rational(100 * 50 + 10 * 200, 110) == sp.Rational(700, 11) and round(float(sp.Rational(700, 11)), 2) == 63.64 == round(alg.weighted_mean([(100, 50), (10, 200)]), 2)
    and sp.Rational(30 * 8 + 10 * 4, 40) == 7 and sp.Rational(20 + 5, 1010) == sp.Rational(5, 202) and round(5 / 202 * 100, 2) == 2.48,
    "sympy: 700/11 ≈ 63,64; khối học sinh 7; tỉ lệ thật 25/1010 ≈ 2,48%")

# ── L02: phép nối tự cài ──
don = [(1, "A", 100), (2, "A", 50)]
dong = [(1, "a", 1), (1, "b", 2), (1, "c", 1), (2, "a", 3)]
joined = [(d, x) for d in don for x in dong if x[0] == d[0]]
per_order = {}
for x in dong:
    per_order[x[0]] = per_order.get(x[0], 0) + x[2]
rec("L02", (sum(d[2] for d, _ in joined), sum(x[2] for _, x in joined), len(joined)) == (350, 7, 4) == alg.dan_sql("SELECT SUM(d.tong), SUM(x.sl), COUNT(*) FROM don d JOIN dong x ON x.don = d.id")[0]
    and (sum(d[2] for d in don), sum(per_order.values())) == (150, 7) and 3 * 2 == 6,
    "nối tự cài: 350 / 7 / 4 dòng; gộp trước: 150 / 7")

# ── L03: numpy và định nghĩa hạng ──
t = np.array([10, 30, 20, 40])
rank = [1 + int((t > v).sum()) for v in t]
lag = [None] + list(np.diff(t))
tie = [30, 20, 30]
rec("L03", list(np.cumsum(t)) == [10, 40, 60, 100] and lag == [None, 20, -10, 20] and rank == [4, 2, 3, 1]
    and [1 + sum(1 for w in tie if w > v) for v in tie] == [1, 3, 1] and list(np.cumsum([5, 15, 10])) == [5, 20, 30]
    and [r[1] for r in alg.dan_sql("SELECT ngay, tien - LAG(tien) OVER (ORDER BY ngay) FROM dt ORDER BY ngay")] == [None, 20, -10, 20],
    "numpy: luỹ kế, chênh, hạng = 1 + số giá trị lớn hơn; đồng hạng 1, 3, 1")

# ── L04: dựng bảng nhóm từ nhật ký người dùng mô phỏng ──
users = [("T1", m) for m in range(100)] + [("T2", m) for m in range(120)]
active = {("T1", 1): set(range(30)), ("T1", 2): set(range(18)), ("T2", 1): set(range(45))}
size = {c: sum(1 for cc, _ in users if cc == c) for c in ("T1", "T2")}
ret = {k: len(v) / size[k[0]] * 100 for k, v in active.items()}
rec("L04", ret == {("T1", 1): 30.0, ("T1", 2): 18.0, ("T2", 1): 37.5} and alg.cohort_retention({"T4": [200, 60, 30]}) == {"T4": [30.0, 15.0]}
    and 30 + 120 == 150 and 18 + 45 + 150 == 213, "nhật ký mô phỏng: 30%, 18%; 37,5%; tháng 4: 30%, 15%; tổng hoạt động 100 → 150 → 213")

# ── L05: nhật ký có thời điểm ──
ev = {"u1": {"gio": 1, "mua": 2}, "u2": {"gio": 5, "mua": 3}, "u3": {"gio": 2}}
both = [u for u, e in ev.items() if {"gio", "mua"} <= set(e)]
ordered = [u for u in both if ev[u]["gio"] < ev[u]["mua"]]
steps, overall = alg.funnel([10000, 4000, 1200, 300])
rec("L05", (len(both), len(ordered)) == (2, 1) and steps == [40.0, 30.0, 25.0] and overall == 3.0 and math.isclose(0.4 * 0.3 * 0.25, 0.03)
    and alg.funnel([5000, 2000, 1000, 600]) == ([40.0, 50.0, 60.0], 12.0) and round(5000 * 0.4 * 0.6 * 0.6) == 720,
    "thứ tự: 2 người có cả hai, 1 người đúng thứ tự; phễu 40/30/25 → 3%; 720 đơn khi bước 2 lên 60%")

# ── L06: numpy.convolve ──
y = np.array([100 + (30 if d % 7 in (5, 6) else 0) + 2 * d for d in range(28)])
ma7 = np.convolve(y, np.ones(7) / 7, mode="valid")
ma5 = np.convolve(y, np.ones(5) / 5, mode="valid")
q = np.array([5, 10, 6, 8, 13, 9])
rec("L06", np.allclose(np.diff(ma7), 2) and np.allclose(ma7[:4], alg.moving_average(list(y), 7)[:4]) and not np.allclose(np.diff(ma5), 2)
    and np.allclose(np.convolve(q, np.ones(3) / 3, mode="valid"), [7, 8, 9, 10]) and y[5] - y[4] == 32 and y[12] - y[5] == 14,
    "convolve: trung bình 7 ngày tăng đều 2, 5 ngày không; chuỗi chu kỳ 3 → 7, 8, 9, 10; thứ Bảy +32 so với hôm qua, +14 so với tuần trước")

# ── L07: vòng lặp ──
test = y[21:28]
naive = [y[20]] * 7
snaive = [y[14 + i] for i in range(7)]
m1 = sum(abs(a - f) for a, f in zip(test, naive)) / 7
m2 = sum(abs(a - f) for a, f in zip(test, snaive)) / 7
rec("L07", round(m1, 2) == 20.86 and m2 == 14 == alg.mae(list(test), alg.seasonal_naive(list(y[:21]), 7, 7)) and alg.mape([0, 10, 12, 8], [2, 9, 12, 10]) is None
    and round(sum([10, 10, 0]) / 3, 2) == 6.67 and alg.mae([20, 30, 25], [22, 27, 25]) == 5 / 3,
    "vòng lặp: ngây thơ 20,86, ngây thơ theo mùa 14 = 7 · 2; sai số phần trăm không xác định khi có 0")

# ── L08: sắp xếp ──
rev = sorted([500, 200, 100, 60, 40, 30, 30, 20, 10, 10], reverse=True)
rec("L08", sum(rev[:2]) / sum(rev) == 0.7 and sum(rev[:1]) / sum(rev) == 0.5 and sum(rev[5:]) / sum(rev) == 0.1 and (rev[4] + rev[5]) / 2 == 35 and sum(rev) / 10 == 100,
    "20% đầu 70%, 10% đầu 50%, nửa dưới 10%; trung vị 35, trung bình 100")


# ── L09: trung vị tay ──
def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


v = [100, 102, 98, 101, 99, 103, 100, 500]
mu = sum(v) / 8
sd = math.sqrt(sum((x - mu) ** 2 for x in v) / 8)
md = median(v)
mad = median([abs(x - md) for x in v])
qq = [50, 52, 49, 51, 48, 50, 10]
rec("L09", round((500 - mu) / sd, 2) == 2.65 and (md, mad) == (100.5, 1.5) and round((500 - md) / (1.4826 * mad), 1) == 179.6 == round(alg.robust_z(v, 500), 1)
    and median(qq) == 50 and median([abs(x - 50) for x in qq]) == 1 and round((10 - 50) / 1.4826, 1) == -27.0,
    "tay: z 2,65 (bỏ sót), bền vững 179,6; câu hỏi: −27")


# ── L10: khoảng điểm số từ định nghĩa gốc + Monte Carlo độ phủ ──
def wilson_sym(k, n, z=1.96):
    P = sp.symbols("P")
    sols = sp.solve(sp.Eq((sp.Rational(k, n) - P) ** 2, sp.Float(z) ** 2 * P * (1 - P) / n), P)
    return sorted(float(s) for s in sols)


ok10 = all(np.allclose(wilson_sym(k, n), alg.wilson(k, n), atol=1e-9) for k, n in ((2, 2), (150, 1000), (8, 10), (70, 100), (1, 1)))
cover = 0
p_true, n = 0.15, 40
ks = rng.binomial(n, p_true, 20000)
for k in ks:
    lo, hi = alg.wilson(int(k), n)
    cover += lo <= p_true <= hi
p1 = 1 / 20
rec("L10", ok10 and abs(cover / 20000 - 0.95) < 0.02 and round(p1 - 1.96 * math.sqrt(p1 * (1 - p1) / 20), 3) == -0.046 and [round(x, 3) for x in alg.wilson(0, 5)] == [0.0, 0.434],
    f"sympy giải (p̂ − P)² = z²P(1 − P)/n khớp; Monte Carlo n = 40, p = 0,15: độ phủ {cover / 20000:.3f} ≈ 0,95; xấp xỉ chuẩn cho 1/20 ra −0,046")

# ── L11: mô phỏng ngày ──
days = rng.random((20000, 20)) < 0.05
days100 = rng.random((20000, 100)) < 0.01
rec("L11", abs(days.any(1).mean() - (1 - 0.95 ** 20)) < 0.01 and abs(days.sum(1).mean() - 1) < 0.03 and abs(days100.any(1).mean() - 0.634) < 0.01
    and round(11000 * 0.027 * 200) == 59400 and (105 - 95) / (100 - 95) == 2 and 8000 * 0.035 * 250 == 70000,
    "mô phỏng: 20 cảnh báo 5% → 64% số ngày có báo nhầm, trung bình 1/ngày; 100 chỉ số 1% → 63%; cây chỉ số −1%")

# ── L12: hành trình thử nghiệm có đối chứng (KO07, KO12, KO13, DE13, FA19 — audit/dan/sources_L12.md) ──
def _n07(r, sd, delta):  # công thức cỡ mẫu KO07 §3.2: n = (4 r σ / Δ)², tin cậy 95%, độ mạnh 90%
    return (4 * r * sd / delta) ** 2
_Phi = lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2)))
_rng12 = np.random.default_rng(12)
_d1 = float(np.mean(np.abs(_rng12.standard_normal(200000)) > 1.96 / math.sqrt(21)))  # ngày 1 so với ngưỡng ngày 21, hiệu ứng 0
_aa = np.random.default_rng(7).random((4000, 2, 2000)) < 0.1  # 4000 thử nghiệm hai nhóm giống hệt, 2000 người mỗi nhóm, tỉ lệ 10%
_pa, _pb = _aa[:, 0].mean(1), _aa[:, 1].mean(1)
_z = (_pa - _pb) / np.sqrt(0.1 * 0.9 * 2 / 2000)
_fp1 = 1 - np.prod([0.975] * 5)
_mc5 = float(np.mean((np.random.default_rng(3).standard_normal((40000, 5)) > 1.96).any(1)))  # 5 phiên bản, một phía 2,5%
rec("L12", round(_n07(2, 30, 3.75 * 0.05)) == 1638400 and round(_n07(2, math.sqrt(0.05 * 0.95), 0.05 * 0.05)) == 486400
    and round(_n07(2, math.sqrt(0.05 * 0.95), 0.05 * 0.2)) == 30400 and round(1 / (4 * 0.01 * 0.99), 2) == 25.25
    and round(2 * (1 - _Phi(1.96 / math.sqrt(21))), 2) == 0.67 and round(2 * (1 - _Phi(1.96 * math.sqrt(2 / 21))), 2) == 0.55 and abs(_d1 - 0.669) < 0.005
    and abs(float(np.mean(np.abs(_z) > 1.96)) - 0.05) < 0.01
    and round(_fp1, 3) == 0.119 and abs(_mc5 - _fp1) < 0.006 and round(1 - 0.975 ** 30, 3) == 0.532
    and 5 ** 15 == 30517578125 and 4 ** 4 == 256 and 200 * 199 // 2 == 19900
    and round(10000 * 0.06 / 365, 2) == 1.64
    and round((0.5 - 499 / 999) / math.sqrt(0.25 / 1e6), 1) == 1.0 and round((0.5 - 499 / 999) / math.sqrt(0.25 / 1e7), 2) == 3.17
    and round(30400 / 20000, 2) == 1.52,
    f"cỡ mẫu KO07: 1 638 400 / 486 400 / 30 400; 99/1 lâu 25,25 lần; ngày 1 ngoài ngưỡng ngày 21: 0,669 (mô phỏng {_d1:.3f}; KO12 “67%”), ngày 2 0,545 (“55%”); "
    f"A/A 4000 lần báo khác biệt {float(np.mean(np.abs(_z) > 1.96)):.3f} ≈ 5% (KO07); 5 phiên bản {_fp1:.3f} (mô phỏng {_mc5:.3f}; KO13 “12%”); 30 vòng 0,532; "
    "5¹⁵, 4⁴ = 256, 19 900 cặp; 1,64 ca lệch tỉ lệ mỗi ngày (FA19); 499/999: 1,0 và 3,17 sai số chuẩn; quiz 1,52 tuần")

bad = [c for c, ok in R if not ok]
print(f"\nverify_dan: {len(R) - len(bad)}/{len(R)} PASS" + (f"; FAIL: {bad}" if bad else ""))
sys.exit(1 if bad else 0)
