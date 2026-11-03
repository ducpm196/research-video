"""Hình định lý giới hạn trung tâm cho CS115 L44: phân phối CHÍNH XÁC của trung bình n xúc xắc (tích chập, không mô phỏng),
n = 1, 2, 10, kèm đường chuông N(3,5; (35/12)/n) vẽ cùng thang. Chạy: clt_svg.py → audit/cs115/fig/clt.svg (một dòng)."""
import math
import sys
from fractions import Fraction as F
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")


def sum_pmf(n):
    p = {0: F(1)}
    for _ in range(n):
        q = {}
        for s, w in p.items():
            for k in range(1, 7):
                q[s + k] = q.get(s + k, 0) + w * F(1, 6)
        p = q
    return p


W, H, PAD, GAP = 330, 250, 30, 24
out = [f'<svg width="{3 * W + 2 * GAP}" height="{H + 46}" viewBox="0 0 {3 * W + 2 * GAP} {H + 46}">']
for i, n in enumerate((1, 2, 10)):
    ox = i * (W + GAP)
    p = sum_pmf(n)
    # mật độ theo trung bình x̄ = s/n: xác suất / bề rộng bước 1/n
    dens = {s / n: float(w) * n for s, w in p.items()}
    ymax = 0.8                       # cùng thang cho cả ba ô: đỉnh n = 10 ≈ 0,727, đường chuông ≈ 0,739 (assert bên dưới)
    X = lambda x: ox + PAD + (x - 1) / 5 * (W - 2 * PAD)
    Y = lambda y: H - 10 - y / ymax * (H - 40)
    bw = max(2.0, (W - 2 * PAD) / 5 / n * 0.8)
    out.append(f'<line x1="{ox + PAD - 6}" y1="{H - 10}" x2="{ox + W - PAD + 6}" y2="{H - 10}" stroke="#9ca3af" stroke-width="2"/>')
    for x, d in sorted(dens.items()):
        out.append(f'<rect x="{X(x) - bw / 2:.1f}" y="{Y(d):.1f}" width="{bw:.1f}" height="{H - 10 - Y(d):.1f}" fill="#93c5fd" stroke="#2563eb" stroke-width="1"/>')
    if n > 1:
        s2 = 35 / 12 / n
        pts = " ".join(f"{X(x):.1f},{Y(math.exp(-(x - 3.5) ** 2 / (2 * s2)) / math.sqrt(2 * math.pi * s2)):.1f}"
                       for x in [1 + k * 5 / 200 for k in range(201)])
        out.append(f'<polyline points="{pts}" fill="none" stroke="#d97706" stroke-width="3"/>')
    for t in (1, 3.5, 6):
        out.append(f'<text x="{X(t):.0f}" y="{H + 14}" font-size="20" text-anchor="middle" fill="#374151">{str(t).replace(".", ",")}</text>')
    out.append(f'<text x="{ox + W / 2:.0f}" y="{H + 40}" font-size="22" text-anchor="middle" font-weight="700" fill="#1e3a8a">n = {n}</text>')
    assert max(dens.values()) < ymax, (n, max(dens.values()))
out.append("</svg>")
svg = "".join(out)
dst = Path(__file__).parent / "fig" / "clt.svg"
dst.parent.mkdir(exist_ok=True)
dst.write_text(svg, encoding="utf-8")
print(dst, len(svg))
