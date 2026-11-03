"""Kiểm độc lập mọi khẳng định của khoá DSC — tính lại bằng cách KHÁC checklib, rồi đối chiếu với checklib (alg) mà `checks` dùng.
Thống kê: numpy/statistics thay cho công thức tay. Nối bảng: sqlite3. Tương quan: numpy.corrcoef + bộ tứ Anscombe thật. Cỡ mẫu A/B: sympy giải
phương trình độ mạnh. Nhìn trộm và kiểm định nhiều lần: mô phỏng riêng (hạt giống khác). Bayes: đếm trên dân số giả lập. Rò rỉ: chạy lại với
hạt giống khác (chỉ cần cùng hướng). Đa cộng tuyến: VIF bằng hồi quy x1 theo x2 (1/(1 − R²)). k-ẩn danh: đếm bằng itertools.groupby.
Chạy: .venv/Scripts/python audit/dsc/verify_dsc.py → PASS/FAIL từng dòng và tổng."""
import itertools
import math
import random
import sqlite3
import statistics
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


# ── L00, L01 ──
rec("L00a", round(float(np.corrcoef([2, 3, 9, 11], [20, 20, 100, 100])[0, 1]), 3) == 0.978 == round(alg.pearson([2, 3, 9, 11], [20, 20, 100, 100]), 3), "r = 0,978 (numpy)")
rec("L01a", round(293.15 / 283.15, 3) == 1.035 and round(303.15 / 288.15, 3) == 1.052 and statistics.mean([1, 1, 3]) != statistics.mean([3, 3, 1]), "Kelvin; trung bình mã đổi theo cách mã")

# ── L02: sqlite3 ──
con = sqlite3.connect(":memory:")
con.executescript("CREATE TABLE o(k, v); INSERT INTO o VALUES ('k',100),('k',200); CREATE TABLE a(k, d); INSERT INTO a VALUES ('k','A'),('k','B'),('k','C');"
                  "CREATE TABLE l(k, v); INSERT INTO l VALUES ('x',1),('x',2),('y',3); CREATE TABLE r(k, d); INSERT INTO r VALUES ('x','p'),('x','q'),('y','r'),('y','s'),('y','t');")
n1, s1 = con.execute("SELECT COUNT(*), SUM(v) FROM o JOIN a USING(k)").fetchone()
n2 = con.execute("SELECT COUNT(*) FROM l JOIN r USING(k)").fetchone()[0]
rec("L02a", (n1, s1, n2) == (6, 900, 7) and len(alg.join_rows([("k", 100), ("k", 200)], [("k", "A"), ("k", "B"), ("k", "C")])) == 6, "sqlite: 6 dòng, tổng 900; quiz 7 dòng")

# ── L03 ──
rec("L03a", round(statistics.variance([2, 4, 6, 8]), 3) == 6.667 and statistics.variance([2, 4, 5, 6, 5, 8]) == 4 and statistics.variance([1, 3, 5]) == 4 and statistics.variance([1, 3, 3, 5, 3]) == 2,
    "phương sai: 6,667 → 4; 4 → 2 (statistics)")
rec("L03b", statistics.mean([5, 7, 9, 11, 30, 40]) == 17 and statistics.mean([5, 7, 9, 11]) == 8, "thiếu không ngẫu nhiên: 17 → 8")

# ── L04 ──
rec("L04a", statistics.median([1, 2, 3, 4, 100]) == 3 and statistics.median([3, 5, 7, 8, 9, 40]) == 7.5, "trung vị 3; 7,5")
q = [float(x) for x in np.percentile([3, 5, 7, 8, 9, 40], [25, 75])]
rec("L04b", q == [5.5, 8.75] == list(alg.quartiles([3, 5, 7, 8, 9, 40])) and alg.iqr_outliers([1, 2, 3, 4, 100])[0] == [100], "Q1, Q3 = 5,5; 8,75 (numpy); ngoại lai 100")

# ── L05 ──
rec("L05a", round(((52 - 50) / (51 - 50) - 1) / (52 / 51 - 1)) == 51 and round(((110 - 100) / (105 - 100) - 1) / (110 / 105 - 1)) == 21, "hệ số nói dối 51; 21")

# ── L06: Anscombe thật ──
x = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
ys = [[8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68], [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74],
      [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]]
x4 = [8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8]
y4 = [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]
rs = [round(float(np.corrcoef(x, y)[0, 1]), 2) for y in ys] + [round(float(np.corrcoef(x4, y4)[0, 1]), 2)]
rec("L06a", rs == [0.82, 0.82, 0.82, 0.82], f"bộ tứ Anscombe: r = {rs}")
rec("L06b", round(float(np.corrcoef([1, 2, 3, 4, 5, 20], [2, 4, 5, 4, 5, -10])[0, 1]), 3) == -0.933 and abs(np.corrcoef([-3, -2, -1, 0, 1, 2, 3], [9, 4, 1, 0, 1, 4, 9])[0, 1]) < 1e-12,
    "ngoại lai đổi dấu −0,933; y = x² cho r = 0")

# ── L07 ──
rec("L07a", [round(100 * a / b) for a, b in ((81, 87), (234, 270), (192, 263), (55, 80), (273, 350), (289, 350))] == [93, 87, 73, 69, 78, 83], "sỏi thận: 93/87, 73/69, 78/83")
rec("L07b", (80 / 100 < 18 / 20) and (10 / 50 < 30 / 100) and (90 / 150 > 48 / 120), "tuyển sinh: nữ cao hơn từng khoa, thấp hơn khi gộp")

# ── L08: cỡ mẫu bằng sympy, nhìn trộm mô phỏng riêng ──
n = sp.symbols("n", positive=True)
p1, p2 = sp.Rational(1, 10), sp.Rational(11, 100)
pb = (p1 + p2) / 2
za, zb = 1.959963984540054, 0.8416212335729143
nn = sp.nsolve(za * sp.sqrt(2 * pb * (1 - pb)) + zb * sp.sqrt(p1 * (1 - p1) + p2 * (1 - p2)) - abs(p1 - p2) * sp.sqrt(n), n, 15000)
rec("L08a", math.ceil(float(nn)) == 14751 == alg.ab_sample_size(0.10, 0.11) and alg.ab_sample_size(0.10, 0.12) == 3841, f"cỡ mẫu (sympy nsolve) {math.ceil(float(nn))}; 3841")
rng = np.random.default_rng(99)
peek = final = 0
T = 3000
for _ in range(T):
    a = rng.random((10, 100)) < 0.1
    b = rng.random((10, 100)) < 0.1
    ca, cb = a.sum(axis=1).cumsum(), b.sum(axis=1).cumsum()
    m = np.arange(1, 11) * 100
    p = (ca + cb) / (2 * m)
    se = np.sqrt(2 * p * (1 - p) / m)
    sig = np.abs(ca - cb) / m > 1.959963984540054 * se
    peek += bool(sig.any())
    final += bool(sig[-1])
rec("L08b", 0.15 < peek / T < 0.23 and 0.035 < final / T < 0.065 and alg.peeking_fpr(1000, 10, 2000) == (0.189, 0.0495), f"nhìn trộm (numpy, hạt giống khác): {peek / T:.3f} vs {final / T:.3f}")

# ── L09 ──
rr = random.Random(5)
hits = sum(any(rr.random() < 0.05 for _ in range(20)) for _ in range(20000)) / 20000
rec("L09a", abs(hits - (1 - 0.95 ** 20)) < 0.01 and round(1 - 0.95 ** 20, 3) == 0.642, f"mô phỏng 20 kiểm định: {hits:.3f} ≈ 0,642")
rec("L09b", round(1 - 0.9975 ** 20, 4) == 0.0488 and round(45 / 125, 2) == 0.36 and round(1 - 0.95 ** 10, 3) == 0.401, "Bonferroni 4,9%; 36% giả; quiz 40%")

# ── L10 ──
leak2 = alg.leak_demo(seed=7, reps=30)
rec("L10a", alg.leak_demo() == (0.889, 0.494) and leak2[0] > 0.8 and abs(leak2[1] - 0.5) < 0.05, f"rò rỉ: hạt giống khác {leak2}")
rec("L10b", statistics.mean([1, 2, 3]) == 2 and statistics.mean([1, 2, 3, 10]) == 4 and statistics.mean([4, 6, 8]) == 6 and statistics.mean([4, 6, 8, 2]) == 5, "chuẩn hoá: 2 vs 4; quiz 6 vs 5")

# ── L11: đếm trên dân số giả lập ──
pop = 10000
sick, healthy = int(pop * 0.01), pop - int(pop * 0.01)
tp, fp = round(sick * 0.99), round(healthy * 0.05)
rec("L11a", (tp, fp) == (99, 495) and round(tp / (tp + fp), 3) == round(alg.ppv(0.99, 0.95, 0.01), 3) == 0.167, "99 / 594 = 0,167")
rec("L11b", round(alg.ppv(0.99, 0.95, 0.10), 4) == 0.6875 and round(alg.ppv(0.99, 0.95, 0.5), 3) == 0.952 and (595, 1099, 505, 199) == (100 + 495, 1000 + 99, 10 + 495, 100 + 99), "68,75%; 95,2%; chi phí")

# ── L12: VIF bằng hồi quy x1 theo x2 ──
rng = np.random.default_rng(3)
x1 = rng.standard_normal(200000)
x2 = 0.9 * x1 + math.sqrt(1 - 0.81) * rng.standard_normal(200000)
r2 = float(np.corrcoef(x1, x2)[0, 1]) ** 2
rec("L12a", abs(1 / (1 - r2) - 5.26) < 0.1 and round(alg.vif_two(0.9), 2) == 5.26 and round(alg.vif_two(0.8), 2) == 2.78, f"VIF mô phỏng {1 / (1 - r2):.2f} ≈ 5,26")
r, h1, h2 = alg.collinear_demo(seed=2)
rec("L12b", abs(h1[0] - h2[0]) > 0.5 and abs((h1[0] + h1[1]) - (h2[0] + h2[1])) < 0.3, f"hệ số dao động mạnh, tổng ổn định: {h1}, {h2}")

# ── L13: groupby ──
rows = sorted([("100**", "2*"), ("100**", "2*"), ("101**", "3*"), ("101**", "3*")])
rec("L13a", min(len(list(g)) for _, g in itertools.groupby(rows)) == 2 and alg.k_anonymity([("A", 1)] * 2 + [("B", 2)] * 3, [0, 1]) == 2, "2-ẩn danh; quiz k = 2")

# ── L14 ──
se = math.sqrt(0.1 * 0.9 / 15000 + 0.112 * 0.888 / 15000)
rec("L14a", (round((0.012 - 1.96 * se) * 100, 1), round((0.012 + 1.96 * se) * 100, 1)) == (0.5, 1.9), "khoảng [0,5; 1,9] điểm phần trăm")
rec("L14b", float(np.random.default_rng(42).normal(size=5).mean()) == float(np.random.default_rng(42).normal(size=5).mean()), "cùng hạt giống, cùng kết quả")

# ── L15: hành trình Netflix Prize (số CITED trong audit/dsc/sources_L15.md; tính lại bằng Fraction / mô phỏng, không dùng checks của bài) ──
from fractions import Fraction as _F
_imp = lambda old, new: (_F(old) - _F(new)) / _F(old) * 100  # phần trăm cải thiện, số hữu tỉ chính xác
rec("L15a", round(float(_imp("0.9514", "0.8712")), 2) == 8.43 and round(float(_imp("0.9525", "0.8567")), 2) == 10.06
    and _F("0.9525") * _F("0.9") == _F("0.85725") and round(float(_imp("0.88", "0.8567")), 1) == 2.6,
    "8,43% (giải 2007, tập công khai), 10,06% (tập kín 2009), 0,9525 × 0,9 = 0,85725 → mốc 0,8572; phần thêm sau 0,88 ≈ 2,6%")
_e = np.array([1.0, -1.0, 2.0, 0.0])
rec("L15b", round(float(np.sqrt(np.mean(_e ** 2))), 2) == 1.22 and round(float(np.sqrt(statistics.fmean([1, 1, 4, 0]))), 2) == 1.22
    and round(3.7 - 0.3 + 0.5, 1) == 3.9, "sai số căn quân phương của (1, −1, 2, 0) ≈ 1,22; dự đoán nền 3,7 − 0,3 + 0,5 = 3,9")
_bits = 0
while 2 ** _bits < 480189:
    _bits += 1
rec("L15c", _bits == 19 and round(100480507 / 480189) == 209 and round(100480507 / (480189 * 17770) * 100, 2) == 1.18,
    "19 câu có–không để chỉ ra 1 trong 480 189 người; ≈ 209 lượt mỗi người; 1,18% số ô có điểm")
# mức lạc quan 2p/N: mô phỏng hồi quy bình phương tối thiểu với p cột nhiễu thuần trên N dòng → MSE trong mẫu thấp hơn thật ≈ 2p/N
_rng = np.random.default_rng(15)
_N, _p, _gap = 4000, 40, []
for _ in range(30):
    _X = _rng.normal(size=(_N, _p)); _y = _rng.normal(size=_N); _Xt = _rng.normal(size=(_N, _p)); _yt = _rng.normal(size=_N)
    _b = np.linalg.lstsq(_X, _y, rcond=None)[0]
    _gap.append(np.mean((_yt - _Xt @ _b) ** 2) - np.mean((_y - _X @ _b) ** 2))
rec("L15d", abs(np.mean(_gap) - 2 * _p / _N) < 0.006 and round(2 * 800 / (2817131 / 2), 5) == 0.00114
    and round(math.sqrt(0.8558 ** 2 + 0.00114) - 0.8558, 5) == 0.00067 and round(0.856714 - 0.856704, 6) == 0.00001,
    f"mô phỏng: chênh MSE ngoài/trong mẫu {np.mean(_gap):.4f} ≈ 2p/N = {2 * _p / _N}; 2 × 800 / 1 408 566 ≈ 0,00114 → 0,00067 trên thước RMSE, gấp 67 lần 0,00001")
_score = {k: 2 * pop + 1 * r for k, (pop, r) in {"A": (0.9, 3.0), "B": (0.2, 4.5)}.items()}
rec("L15e", max(_score, key=_score.get) == "B" and max({k: v + 7 for k, v in _score.items()}.items(), key=lambda t: t[1])[0] == "B"
    and round(math.sqrt(0.89 ** 2 + 2 * 50 / 2000) - 0.89, 3) == 0.028 and round(float(_imp("0.95", "0.90")), 2) == 5.26 and round(float(_imp("0.95", "0.89")), 2) == 6.32,
    "xếp hạng 2 × phổ biến + dự đoán: B (4,9) trước A (4,8), cộng hằng số không đổi thứ tự; quiz 5,26% / 6,32%, lạc quan của Y ≈ 0,028")

n_ok = sum(o for _, o in R)
print(f"\n{n_ok}/{len(R)} PASS")
sys.exit(0 if n_ok == len(R) else 1)
