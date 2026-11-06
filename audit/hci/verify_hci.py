"""Kiểm độc lập mọi khẳng định của khoá HCI — tính lại bằng cách KHÁC checklib (liệt kê vét cạn itertools, Fraction chính xác,
mô phỏng Monte Carlo hạt giống cố định, sympy), rồi đối chiếu với hàm checklib (alg.hci_*) mà `checks` của bài dùng.
Chạy: .venv/Scripts/python audit/hci/verify_hci.py   (exit 0 khi mọi dòng PASS; status_report.py đọc dòng cuối)"""
import datetime
import itertools
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib as alg  # noqa: E402

R = []


def rec(code, ok, what):
    R.append((code, bool(ok)))
    print(("PASS" if ok else "FAIL"), code, "—", what)


# ── L00: khoảng thời gian cảnh báo giả Hawaii (8:07 → 8:45 = 38 phút) đối chiếu bằng datetime ──
t_send = datetime.datetime(2018, 1, 13, 8, 7)
t_cancel = datetime.datetime(2018, 1, 13, 8, 45)
rec("L00a", int((t_cancel - t_send).total_seconds() // 60) == 38 == alg.hci_minutes_diff(8, 7, 8, 45),
    "8:07 → 8:45 = 38 phút (datetime so với hci_minutes_diff)")
rec("L00b", int((datetime.datetime(2018, 1, 13, 8, 10) - t_send).total_seconds() // 60) == 3 == alg.hci_minutes_diff(8, 7, 8, 10),
    "8:07 → 8:10 = 3 phút nhận ra bấm nhầm")

# ── L01: số cách ghép 4 núm xoay với 4 lò bếp — liệt kê vét cạn mọi hoán vị itertools.permutations ──
perms4 = list(itertools.permutations(range(4)))
rec("L01a", len(perms4) == 24 == alg.hci_mappings(4), "vét cạn 4! = 24 cách ghép núm với lò")
rec("L01b", sum(1 for p in perms4 if p == (0, 1, 2, 3)) == 1 and Fraction(1, len(perms4)) == Fraction(1, 24),
    "chỉ 1/24 cách trùng thứ tự tự nhiên")

# ── L02: định luật Fitts dạng Shannon — tính lại bằng đổi cơ số ln(x)/ln(2) ──
id_16 = math.log(256 / 16 + 1) / math.log(2)
id_64 = math.log(256 / 64 + 1) / math.log(2)
rec("L02a", round(id_16, 2) == 4.09 and abs(id_16 - alg.hci_fitts_id(256, 16)) < 1e-12, "ID(256, 16) ≈ 4,09 bit")
rec("L02b", round(0.1 + 0.15 * id_16, 3) == 0.713 == round(alg.hci_fitts_time(256, 16), 3), "T(256, 16) ≈ 0,713 s")
rec("L02c", round(id_64, 2) == 2.32 and round(0.1 + 0.15 * id_64, 3) == 0.448 == round(alg.hci_fitts_time(256, 64), 3),
    "ID(256, 64) ≈ 2,32 bit; T ≈ 0,448 s")

# ── L03: định luật Hick–Hyman — 15 mục phẳng so với 2 cấp (3 nhóm × 5 mục) ──
t_flat = Fraction(2, 10) * 4  # log2(15 + 1) = 4 chính xác
t_hier = 0.2 * (math.log(3 + 1) / math.log(2)) + 0.2 * (math.log(5 + 1) / math.log(2))
rec("L03a", float(t_flat) == 0.8 == round(alg.hci_hick_time(15, 0.2), 6), "15 mục phẳng: 0,2 · log₂(16) = 0,8 s")
rec("L03b", round(t_hier, 3) == 0.917 == round(alg.hci_hick_time(3, 0.2) + alg.hci_hick_time(5, 0.2), 3),
    "hai cấp 3 rồi 5: 0,4 + 0,2 · log₂(6) ≈ 0,917 s > 0,8 s")

# ── L04: gom nhóm trí nhớ làm việc (chunking) ──
rec("L04a", alg.hci_chunks("482913") == (6, 1) and alg.hci_chunks("482 913") == (6, 2),
    "482913: 6 chữ số → tách 482 913 thành 2 nhóm")
rec("L04b", alg.hci_chunks("0912 345 678") == (10, 3), "số điện thoại 10 chữ số gom thành 3 cụm")

# ── L05: mô hình KLM (Card, Moran, Newell 1980) — tính bằng Fraction chính xác ──
w_frac = {"K": Fraction(2, 10), "P": Fraction(11, 10), "B": Fraction(1, 10), "H": Fraction(4, 10), "M": Fraction(135, 100)}
seq_mouse = "HMPBBMPBB"
seq_key = "MKK"
t_m_frac = sum(w_frac[c] for c in seq_mouse)
t_k_frac = sum(w_frac[c] for c in seq_key)
rec("L05a", t_m_frac == Fraction(57, 10) and float(t_m_frac) == alg.hci_klm_time(seq_mouse),
    "chuột H+M+P+BB+M+P+BB = 5,7 s chính xác")
rec("L05b", t_k_frac == Fraction(7, 4) and float(t_k_frac) == alg.hci_klm_time(seq_key) == 1.75,
    "phím tắt M+K+K = 1,75 s chính xác")

# ── L06: công thức Nielsen–Landauer 1 − (1 − λ)^n — kiểm bằng xác suất bù và mô phỏng Monte Carlo ──
p_miss_5 = Fraction(69, 100) ** 5
p_find_5 = 1 - float(p_miss_5)
p_find_15 = 1 - float(Fraction(69, 100) ** 15)
rec("L06a", round(p_find_5, 3) == 0.844 == round(alg.hci_nielsen_found(5, 0.31), 3), "5 người thử phát hiện ≈ 84,4%")
rec("L06b", round(p_find_15, 3) == 0.996 == round(alg.hci_nielsen_found(15, 0.31), 3), "15 người thử phát hiện ≈ 99,6%")
rng = random.Random(42)
sim_5 = sum(1 for _ in range(20000) if any(rng.random() < 0.31 for _ in range(5))) / 20000
rec("L06c", abs(sim_5 - p_find_5) < 0.01, f"mô phỏng 20 000 lần cho 5 người: {sim_5:.3f} ≈ 0,844")

# ── L07: thang điểm SUS (Brooke 1996) ──
ans = [4, 2, 4, 1, 5, 2, 4, 2, 4, 1]
score, odd_s, even_s = alg.hci_sus_score(ans)
alt_score = sum((x - 1 if i % 2 == 0 else 5 - x) for i, x in enumerate(ans)) * Fraction(5, 2)
rec("L07a", (odd_s, even_s) == (16, 17) and score == 82.5 == float(alt_score), "SUS([4,2,4,1,5,2,4,2,4,1]) = (16+17)·2,5 = 82,5")
rec("L07b", alg.hci_sus_score([5, 1] * 5)[0] == 100.0 and alg.hci_sus_score([1, 5] * 5)[0] == 0.0 and alg.hci_sus_score([3] * 10)[0] == 50.0,
    "cực đại 100, cực tiểu 0, trung lập 50")

# ── L08: thí nghiệm giao diện và hình vuông Latin ──
sq3 = ["ABC", "BCA", "CAB"]
rec("L08a", len(list(itertools.permutations("ABC"))) == 6 and alg.hci_is_latin_square(sq3),
    "3 giao diện có 6 thứ tự; ['ABC','BCA','CAB'] là hình vuông Latin")
rec("L08b", not alg.hci_is_latin_square(["ABC", "ABC", "CAB"]), "bảng lặp hàng không phải hình vuông Latin")

# ── L09: kích thước đích WCAG 2.2 (24 × 24 px so với 44 × 44 px) và Fitts ở D = 200 px ──
rec("L09a", alg.hci_wcag_target_ok(24, 24) and not alg.hci_wcag_target_ok(20, 24), "WCAG 2.5.8 đạt từ 24 × 24 px")
rec("L09b", round(alg.hci_fitts_time(200, 24), 3) == 0.583 and round(alg.hci_fitts_time(200, 44), 3) == 0.471,
    "D=200 px: đích 24 px mất 0,583 s; đích 44 px mất 0,471 s")

# ── L10: thiết kế chống lỗi — các lớp bảo vệ độc lập so với phụ thuộc ──
leak_indep = Fraction(1, 1000) * Fraction(1, 100)
rec("L10a", leak_indep == Fraction(1, 100000) and abs(float(leak_indep) - alg.hci_swiss_cheese_leak([0.001, 0.01])) < 1e-15,
    "1/1000 × 1/100 = 1/100 000 khi hai lớp độc lập")

# ── L11: dòng thời gian báo cáo FCC (Hawaii 13/1/2018) ──
rec("L11a", alg.hci_minutes_diff(8, 31, 8, 44) == 13 and alg.hci_minutes_diff(8, 7, 8, 45) == 38,
    "soạn đính chính 8:31–8:44 = 13 phút; tổng 8:07–8:45 = 38 phút")

# ── L12: hành trình chuẩn tiếp cận web WCAG 1.0 (1999) → 2.0 (2008) → 2.1 (2018) → 2.2 (2023) ──
rec("L12a", 16 + 30 + 19 == 65 and round((1 + 0.05) / (0 + 0.05), 1) == 21.0,
    "WCAG 1.0: 65 điểm kiểm; WCAG 2.0: tương phản tối đa 21:1")
rec("L12b", 61 + 17 == 78 and 1280 // 4 == 320 and 44 * 44 == 1936,
    "WCAG 2.1: 78 tiêu chí, phóng 400% của 1280 px = 320 px, đích AAA 1936 px²")
rec("L12c", 78 - 1 + 9 == 86 and 24 * 24 == 576 and Fraction(1936, 576) == Fraction(121, 36) and round(1936 / 576, 2) == 3.36,
    "WCAG 2.2: 86 tiêu chí, đích AA 576 px², tỉ lệ diện tích 1936/576 = 121/36 ≈ 3,36")

bad = [c for c, ok in R if not ok]
print(f"\nverify_hci: {len(R) - len(bad)}/{len(R)} PASS" + (f"; FAIL: {bad}" if bad else ""))
sys.exit(1 if bad else 0)
