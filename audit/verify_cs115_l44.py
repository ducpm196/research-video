"""Kiểm chứng bằng máy mọi con số của bài CS115 L44 (thống kê suy luận): phân phối chính xác của trung bình xúc xắc (tích chập),
độ phủ thật của khoảng tin cậy (cộng xác suất nhị thức chính xác, không mô phỏng), so sánh ghép cặp hai mô hình, phân vị t.
Chạy: .venv/Scripts/python audit/verify_cs115_l44.py   (kết quả ghi vào audit/cs115/AUDIT_L44.md)"""
import math
import sys
from fractions import Fraction as F

import mpmath as mp
import sympy as sp

sys.stdout.reconfigure(encoding="utf-8")
rows = []


def rec(cid, ok, msg):
    rows.append(ok)
    print(f"{'PASS' if ok else 'FAIL'} | {cid:4} | {msg}")


# ── xúc xắc: kỳ vọng, phương sai ──
mu = F(sum(range(1, 7)), 6)
var = sum((F(x) - mu) ** 2 for x in range(1, 7)) / 6
rec("S1", mu == F(7, 2) and var == F(35, 12) and round(math.sqrt(35 / 12), 4) == 1.7078,
    f"một xúc xắc: μ = {mu}, σ² = {var} ≈ {float(var):.4f}, σ ≈ {math.sqrt(35 / 12):.4f}")
rec("S2", round(35 / 12 / 100, 6) == 0.029167 and round(math.sqrt(35 / 12 / 100), 4) == 0.1708,
    "trung bình 100 xúc xắc: Var = σ²/100 ≈ 0,029167, độ lệch chuẩn ≈ 0,1708")


def sum_pmf(n):
    """phân phối chính xác của tổng n xúc xắc (tích chập)."""
    p = {0: F(1)}
    for _ in range(n):
        q = {}
        for s, w in p.items():
            for k in range(1, 7):
                q[s + k] = q.get(s + k, 0) + w * F(1, 6)
        p = q
    return p


p2 = sum_pmf(2)
rec("S3", p2[7] == F(6, 36) and p2[2] == F(1, 36) and sum(p2.values()) == 1, f"tổng 2 xúc xắc: P(7) = {p2[7]}, P(2) = {p2[2]}")
p10 = sum_pmf(10)
mode10 = max(p10, key=p10.get)
rec("S4", mode10 == 35 and round(float(p10[35]), 4) == 0.0727, f"tổng 10 xúc xắc: đỉnh ở 35 (trung bình 3,5), P = {float(p10[35]):.4f}")
# so với hình chuông N(35, 10·35/12) tại 35
nd = 1 / math.sqrt(2 * math.pi * 10 * 35 / 12)
rec("S4b", abs(nd - float(p10[35])) < 0.002, f"mật độ chuẩn cùng kỳ vọng, phương sai tại 35: {nd:.4f} (sai khác < 0,002)")
p100 = sum_pmf(100)
sd = math.sqrt(35 / 12 / 100)
lo, hi = 3.5 - 1.96 * sd, 3.5 + 1.96 * sd
cov = sum(w for s, w in p100.items() if lo <= s / 100 <= hi)
rec("S5", abs(float(cov) - 0.95) < 0.01, f"trung bình 100 xúc xắc rơi trong 3,5 ± 1,96·0,1708 = [{lo:.3f}; {hi:.3f}] với xác suất chính xác {float(cov):.4f}")
# 1,96
z = sp.nsolve(sp.erf(sp.Symbol("z") / sp.sqrt(2)) - sp.Rational(95, 100), 2)
rec("S6", round(float(z), 2) == 1.96 and abs(math.erf(2 / math.sqrt(2)) - 0.9545) < 0.0001,
    f"khoảng ±z chứa 95% của N(0, 1): z = {float(z):.4f}; ±2 chứa {math.erf(2 / math.sqrt(2)):.4f} (68–95–99,7 của bài 14)")

# ── khoảng tin cậy cho tỉ lệ đúng ──
n, k = 1000, 850
ph = k / n
se = math.sqrt(ph * (1 - ph) / n)
rec("C1", round(se, 4) == 0.0113 and round(1.96 * se, 4) == 0.0221 and (round(ph - 1.96 * se, 3), round(ph + 1.96 * se, 3)) == (0.828, 0.872),
    f"850/1000: p̂ = 0,85, SE = √(0,85·0,15/1000) = {se:.5f}, ±1,96·SE = ±{1.96 * se:.4f} → [{ph - 1.96 * se:.3f}; {ph + 1.96 * se:.3f}]")
# độ phủ thật của cách làm khi p = 0,85 (nhị thức chính xác)
mp.mp.dps = 50
P = mp.mpf("0.85")
covp = mp.mpf(0)
for kk in range(n + 1):
    q = kk / n
    s = math.sqrt(q * (1 - q) / n)
    if q - 1.96 * s <= 0.85 <= q + 1.96 * s:
        covp += mp.binomial(n, kk) * P ** kk * (1 - P) ** (n - kk)
rec("C2", abs(float(covp) - 0.95) < 0.01, f"độ phủ THẬT của cách làm (p thật 0,85, n = 1000, cộng chính xác mọi k): {float(covp):.4f}")
# nửa độ rộng ∝ 1/√n
rec("C3", abs(1.96 * math.sqrt(0.85 * 0.15 / 4000) * 2 - 1.96 * se) < 1e-12, "n gấp 4 → nửa độ rộng giảm một nửa")

# ── so sánh hai mô hình trên cùng 1000 mẫu ──
b, c = 30, 42                 # A đúng B sai; A sai B đúng
kA, kB = 850, 850 - b + c
d = (c - b) / n
se_pair = math.sqrt(b + c - (c - b) ** 2 / n) / n
rec("P1", kB == 862 and round(d, 3) == 0.012 and round(se_pair, 5) == 0.00848,
    f"A {kA}/1000, B {kB}/1000; bất đồng 30 và 42: hiệu {d:.3f}, SE ghép cặp = √(72 − 144/1000)/1000 = {se_pair:.5f}")
rec("P2", (round(d - 1.96 * se_pair, 4), round(d + 1.96 * se_pair, 4)) == (-0.0046, 0.0286),
    f"khoảng 95% của hiệu: [{d - 1.96 * se_pair:.4f}; {d + 1.96 * se_pair:.4f}] chứa 0 → chưa đủ bằng chứng B tốt hơn")
se_ind = math.sqrt(0.85 * 0.15 / n + 0.862 * 0.138 / n)
rec("P3", round(se_ind, 4) == 0.0157 and se_ind > se_pair, f"nếu coi hai kết quả độc lập: SE = {se_ind:.4f} — rộng gần gấp đôi, bỏ phí thông tin ghép cặp")
# kiểm công thức SE ghép cặp bằng định nghĩa: biến D_i ∈ {−1, 0, +1}
vals = [1] * c + [-1] * b + [0] * (n - b - c)
m = sum(vals) / n
v = sum((x - m) ** 2 for x in vals) / n
rec("P4", abs(math.sqrt(v / n) - se_pair) < 1e-12, "SE ghép cặp = độ lệch chuẩn của hiệu từng mẫu (−1, 0, +1) chia √n — khớp công thức")

# ── phân vị t cho mẫu nhỏ ──
def t_cdf(x, nu):
    return 1 - mp.betainc(nu / 2, mp.mpf(1) / 2, 0, nu / (nu + x * x), regularized=True) / 2
t9 = mp.findroot(lambda x: t_cdf(x, 9) - mp.mpf("0.975"), 2.2)
rec("T1", round(float(t9), 3) == 2.262, f"phân vị 97,5% của phân phối t với 9 bậc tự do (n = 10): {float(t9):.4f}")

# ── bài tự làm ──
n2, k2 = 400, 360
p2h = k2 / n2
se2 = math.sqrt(p2h * (1 - p2h) / n2)
rec("Q1", round(se2, 3) == 0.015 and (round(p2h - 1.96 * se2, 3), round(p2h + 1.96 * se2, 3)) == (0.871, 0.929),
    f"360/400: p̂ = 0,9, SE = {se2:.4f}, khoảng [{p2h - 1.96 * se2:.3f}; {p2h + 1.96 * se2:.3f}]")
print(f"\nTỔNG: {sum(rows)} PASS · {len(rows) - sum(rows)} FAIL")
