"""Biểu đồ thứ tự (Hasse) cho DMS L08 — sinh SVG từ dữ liệu, không vẽ tay.
Cạnh = quan hệ phủ: a chia hết b, a ≠ b, và không có c nào nằm giữa (máy tính, không gõ tay). Tầng = độ dài xích dài nhất từ dưới lên,
nên phần tử lớn hơn luôn nằm cao hơn. Chạy: .venv/Scripts/python audit/dms/hasse_svg.py → audit/dms/fig/hasse12.svg, hasse12_bad.svg"""
import sys
from pathlib import Path

R = 30
S = [1, 2, 3, 4, 6, 12]


def cover(S):
    return [(a, b) for a in S for b in S if a != b and b % a == 0
            and not any(c not in (a, b) and c % a == 0 and b % c == 0 for c in S)]


def level(S, E):
    lv = {}
    for x in sorted(S):
        lv[x] = max([lv[a] + 1 for a, b in E if b == x] or [0])
    return lv


def svg(S, extra=(), w=520, h=380):
    E = cover(S)
    lv = level(S, E)
    rows = {}
    for x in sorted(S):
        rows.setdefault(lv[x], []).append(x)
    top = max(rows)
    pos = {}
    for k, xs in rows.items():
        for i, x in enumerate(xs):
            pos[x] = ((i + 1) * w / (len(xs) + 1), h - 50 - k * (h - 100) / top)
    out = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    for (a, b), col, dash in [(e, "#6b7280", "") for e in E] + [(e, "#dc2626", ' stroke-dasharray="10 8"') for e in extra]:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        out.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{col}" stroke-width="4"{dash}/>')
    for x, (cx, cy) in pos.items():
        out.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{R}" fill="#eff6ff" stroke="#2563eb" stroke-width="4"/>'
                   f'<text x="{cx:.0f}" y="{cy + 11:.0f}" font-size="30" text-anchor="middle">{x}</text>')
    out.append("</svg>")
    return "".join(out), E


if __name__ == "__main__":
    D = Path(__file__).resolve().parent / "fig"
    D.mkdir(exist_ok=True)
    s, E = svg(S)
    assert len(E) == 7, E
    (D / "hasse12.svg").write_text(s, encoding="utf-8")
    # hình cho lỗi “vẽ cả cạnh suy ra được bằng bắc cầu”: thêm 1–4, 1–12 (nét đứt đỏ)
    s2, _ = svg(S, extra=[(1, 4), (1, 12)])
    (D / "hasse12_bad.svg").write_text(s2, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print("cạnh phủ:", E)
