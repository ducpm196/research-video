"""Đồ thị đơn cho DMS L18 — sinh SVG từ danh sách cạnh và toạ độ (không vẽ tay); tô màu đỉnh theo kết quả thuật toán tham lam tính
trong script. Chạy: .venv/Scripts/python audit/dms/plain_svg.py → audit/dms/fig/k4.svg, k5.svg, greedy_good.svg, greedy_bad.svg"""
import itertools
import math
from pathlib import Path

R = 28
PAL = ["#bfdbfe", "#fde68a", "#fecaca"]          # màu 1, 2, 3 (xanh, vàng, đỏ nhạt)


def svg(pos, edges, w, h, fill=None, faces=None):
    out = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    for u, v in edges:
        (x1, y1), (x2, y2) = pos[u], pos[v]
        out.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#6b7280" stroke-width="4"/>')
    for label, (fx, fy) in (faces or {}).items():
        out.append(f'<text x="{fx:.0f}" y="{fy:.0f}" font-size="24" font-weight="700" fill="#059669" text-anchor="middle">{label}</text>')
    for x, (cx, cy) in pos.items():
        f = PAL[fill[x]] if fill else "#eff6ff"
        out.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{R}" fill="{f}" stroke="#2563eb" stroke-width="4"/>'
                   f'<text x="{cx:.0f}" y="{cy + 10:.0f}" font-size="26" text-anchor="middle">{x}</text>')
    return "".join(out + ["</svg>"])


def greedy(edges, order):
    c = {}
    for v in order:
        used = {c[u] for a, b in edges for u in ((b,) if a == v else (a,) if b == v else ()) if u in c}
        k = 0
        while k in used:
            k += 1
        c[v] = k
    return c


if __name__ == "__main__":
    D = Path(__file__).resolve().parent / "fig"
    D.mkdir(exist_ok=True)
    k4 = {1: (190, 40), 2: (40, 300), 3: (340, 300), 4: (190, 200)}
    (D / "k4.svg").write_text(svg(k4, list(itertools.combinations([1, 2, 3, 4], 2)), 380, 340,
                                  faces={"M1": (135, 205), "M2": (245, 205), "M3": (190, 285), "M4 (ngoài)": (300, 110)}), encoding="utf-8")
    k5 = {i + 1: (190 + 140 * math.sin(2 * math.pi * i / 5), 175 - 140 * math.cos(2 * math.pi * i / 5)) for i in range(5)}
    (D / "k5.svg").write_text(svg(k5, list(itertools.combinations(range(1, 6), 2)), 380, 340), encoding="utf-8")
    P = [(1, 2), (2, 3), (3, 4)]
    pp = {1: (50, 60), 2: (160, 60), 3: (270, 60), 4: (380, 60)}
    g1, g2 = greedy(P, [1, 2, 3, 4]), greedy(P, [1, 4, 2, 3])
    assert max(g1.values()) == 1 and max(g2.values()) == 2
    (D / "greedy_good.svg").write_text(svg(pp, P, 430, 120, fill=g1), encoding="utf-8")
    (D / "greedy_bad.svg").write_text(svg(pp, P, 430, 120, fill=g2), encoding="utf-8")
    print("tham lam 1,2,3,4:", g1, "| 1,4,2,3:", g2)
