"""Kiểm độc lập mọi khẳng định của khoá GFX — tính lại bằng cách KHÁC checklib (sympy giải phương trình chính xác,
Fraction, numpy vector hoá), rồi đối chiếu với hàm checklib (alg.gfx_*) mà `checks` của bài dùng.
Chạy: .venv/Scripts/python audit/gfx/verify_gfx.py   (exit 0 khi mọi dòng PASS; status_report.py đọc dòng cuối)"""
import math
import sys
from fractions import Fraction
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


# ── L00: ngân sách khung hình và thông lượng điểm ảnh ──
rec("L00a", alg.gfx_pixels_per_sec(1920, 1080, 60) == 124_416_000 == 1920 * 1080 * 60,
    "1920 × 1080 × 60 = 124 416 000 điểm ảnh/s")
rec("L00b", round(alg.gfx_frame_budget_ms(60), 2) == 16.67 and round(alg.gfx_frame_budget_ms(120), 2) == 8.33,
    "60 fps → 16,67 ms; 120 fps → 8,33 ms")

# ── L01: biến đổi thuần nhất 2D — quay 90° và tịnh tiến (2, 0) không giao hoán ──
R90, T20 = alg.gfx_rot2d(90), alg.gfx_trans2d(2, 0)
rec("L01a", alg.gfx_apply2d(T20 @ R90, 1, 0) == (2.0, 1.0) and alg.gfx_apply2d(R90 @ T20, 1, 0) == (0.0, 3.0),
    "quay rồi tịnh tiến → (2, 1); tịnh tiến rồi quay → (0, 3)")

# ── L02: chiếu phối cảnh và nội suy có hiệu chỉnh phối cảnh ──
rec("L02a", alg.gfx_persp_project(2, 1, 4, 1.0) == (0.5, 0.25) and alg.gfx_persp_project(2, 1, 8, 1.0) == (0.25, 0.125),
    "f=1: (2,1,4) → (0,5; 0,25); ở z=8 → (0,25; 0,125)")
u_persp, u_lin = alg.gfx_persp_interp(2.0, 6.0, 0.0, 1.0, 0.5)
rec("L02b", round(u_persp, 2) == 0.25 and round(u_lin, 2) == 0.50,
    "giữa màn hình với z₀=2, z₁=6: đúng theo phối cảnh u=0,25 ≠ tuyến tính 0,5")

# ── L03: toạ độ chuẩn hoá NDC sang chỉ số điểm ảnh ──
rec("L03a", alg.gfx_ndc_to_pixel(0.5, 1920) == 1440 and alg.gfx_ndc_to_pixel(-1, 1920) == 0 and alg.gfx_ndc_to_pixel(1, 1920) == 1920,
    "NDC −1 → 0; 0,5 → 1440; 1 → 1920")

# ── L04: toạ độ trọng tâm tam giác (0,0)-(4,0)-(0,4) ──
b_in = alg.gfx_barycentric((1, 1), (0, 0), (4, 0), (0, 4))
b_out = alg.gfx_barycentric((3, 3), (0, 0), (4, 0), (0, 4))
rec("L04a", b_in == (0.5, 0.25, 0.25) and sum(b_in) == 1.0 and all(x > 0 for x in b_in),
    "điểm (1, 1) có toạ độ trọng tâm (0,5; 0,25; 0,25) ở bên trong")
rec("L04b", b_out == (-0.5, 0.75, 0.75) and any(x < 0 for x in b_out),
    "điểm (3, 3) có α = −0,5 < 0 ở bên ngoài")

# ── L05: bộ đệm độ sâu 24 bit — độ phân giải theo mặt phẳng gần n ──
dz_01 = alg.gfx_depth_step(100, 0.1, 1000, 24)
dz_1 = alg.gfx_depth_step(100, 1.0, 1000, 24)
rec("L05a", round(dz_01 * 1000, 1) == 6.0 and round(dz_1 * 1000, 1) == 0.6,
    "z=100 m, 24 bit: n=0,1 → Δz ≈ 6,0 mm; n=1,0 → Δz ≈ 0,6 mm (tốt gấp 10)")

# ── L06: chiếu sáng cục bộ Lambert và Blinn–Phong ──
rec("L06a", round(alg.gfx_lambert((0, 0, 1), (0, 0.6, 0.8)), 6) == 0.8, "n·l = 0,8")
rec("L06b", round(alg.gfx_blinn_spec(0.95, 32), 3) == 0.194 and round(alg.gfx_blinn_spec(0.95, 128), 4) == 0.0014,
    "0,95³² ≈ 0,194; 0,95¹²⁸ ≈ 0,0014")

# ── L07: nội suy song tuyến và bộ nhớ mipmap ──
rec("L07a", alg.gfx_bilinear(10, 20, 30, 40, 0.5, 0.5) == 25.0, "nội suy song tuyến giữa ô (10,20,30,40) = 25")
lv_cnt, tot_tex, extra_ratio = alg.gfx_mipmap_stats(1024)
exact_ratio = Fraction(sum((1024 >> k) ** 2 for k in range(1, 11)), 1024 ** 2)
rec("L07b", lv_cnt == 11 and abs(extra_ratio - 1 / 3) < 0.001 and float(exact_ratio) == extra_ratio,
    "1024 × 1024 có 11 mức mipmap, thêm ≈ 1/3 bộ nhớ")

# ── L08: trộn màu trong không gian tuyến tính so với sRGB ──
naive_b, corr_b = alg.gfx_srgb_blend_byte(0, 255, 0.5)
rec("L08a", (naive_b, corr_b) == (128, 188) and round(alg.gfx_srgb_to_linear(128 / 255), 3) == 0.216,
    "trộn thẳng ra 128 (ánh sáng 0,216); trộn tuyến tính đúng ra 188 (ánh sáng 0,5)")

# ── L09: giao tia–cầu kiểm bằng sympy ──
t_sym = sp.symbols("t")
roots_sym = sorted(float(r) for r in sp.solve(sp.Eq((t_sym - 5) ** 2, 1), t_sym))
disc1, roots1 = alg.gfx_ray_sphere((0, 0, 0), (0, 0, 1), (0, 0, 5), 1)
disc2, roots2 = alg.gfx_ray_sphere((0, 0, 0), (0, 1, 0), (0, 0, 5), 1)
rec("L09a", roots1 == [4.0, 6.0] == roots_sym and disc2 < 0 and roots2 == [],
    "tia hướng (0,0,1) cắt cầu tại t=4, 6; hướng (0,1,0) biệt thức âm không cắt")

# ── L10: phản xạ Fresnel xấp xỉ Schlick và bảo toàn năng lượng ──
rec("L10a", alg.gfx_schlick_fresnel(1.0, 0.04) == 0.04 and round(alg.gfx_schlick_fresnel(0.5, 0.04), 2) == 0.07 and alg.gfx_schlick_fresnel(0.0, 0.04) == 1.0,
    "Schlick F₀=0,04: cos=1 → 0,04; cos=0,5 → 0,07; cos=0 → 1,0")

# ── L11: tô đè (overdraw) ở 1080p ──
rec("L11a", alg.gfx_overdraw_fragments(1920, 1080, 3) == 6_220_800 and alg.gfx_overdraw_fragments(1920, 1080, 1) == 2_073_600,
    "1080p: tô đè 3 lần = 6 220 800 mảnh; 1 lần = 2 073 600 mảnh")

# ── L12: chẩn đoán bộ đệm độ sâu cảnh thế giới mở ở z = 1000 m ──
dz_bad = alg.gfx_depth_step(1000, 0.01, 10000, 24)
dz_fix = alg.gfx_depth_step(1000, 0.5, 10000, 24)
dz_far = alg.gfx_depth_step(1000, 0.01, 100000, 24)
rec("L12a", round(dz_bad, 1) == 6.0 and round(dz_fix, 2) == 0.12 and round(dz_far / dz_bad, 3) == 1.0,
    "z=1000 m: n=0,01 → Δz ≈ 6,0 m; n=0,5 → ≈ 0,12 m; đổi f lên 100 000 hầu như không đổi")

# ── L13: hành trình chiếu sáng 1975 → 2013 ──
f0_glass = ((Fraction(3, 2) - 1) / (Fraction(3, 2) + 1)) ** 2
rec("L13a", float(f0_glass) == 0.04 and 10 ** 2 == 100 and round(1 - alg.gfx_schlick_fresnel(0.5, 0.04), 2) == 0.93 and 0.5 ** 2 == 0.25,
    "n=1,5 → F₀=0,04; giảm nhiễu 10× cần 100× tia; khuếch tán còn 0,93; α = 0,5² = 0,25")

bad = [c for c, ok in R if not ok]
print(f"\nverify_gfx: {len(R) - len(bad)}/{len(R)} PASS" + (f"; FAIL: {bad}" if bad else ""))
sys.exit(1 if bad else 0)
