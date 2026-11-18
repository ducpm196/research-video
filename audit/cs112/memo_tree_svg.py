"""Cây lời gọi của F(5) khi GHI NHỚ (bài L18 CS112): sinh SVG từ chính lần chạy đệ quy có ghi nhớ, rồi kiểm bằng máy:
đúng 9 lời gọi (so với 15 của đệ quy thô), các nút tra bảng (xám, nét đứt) không có con.
Chạy: .venv/Scripts/python -B audit/cs112/memo_tree_svg.py → ghi audit/cs112/fig/L18_MEMO.svg (một dòng)."""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")


def call_tree(n):
    """(nhãn, đã_có_trong_bảng, [con trái, con phải]) của lời gọi F(n) có ghi nhớ."""
    memo = {}

    def f(k):
        if k in memo:
            return (k, True, [])
        kids = [] if k < 2 else [f(k - 1), f(k - 2)]
        memo[k] = True
        return (k, False, kids)
    return f(n)


def count(t):
    return 1 + sum(count(c) for c in t[2])


def svg(t, w=1000, r=22, dy=62, top=30):
    order, depth = [], {}

    def walk(nd, d):
        if len(nd[2]) == 2:
            walk(nd[2][0], d + 1)
        order.append(nd)
        depth[id(nd)] = d
        if len(nd[2]) == 2:
            walk(nd[2][1], d + 1)
    walk(t, 0)
    dmax = max(depth.values())
    h = top + dmax * dy + r + 8
    step = (w - 2 * r - 4) / (len(order) - 1)
    xy = {id(nd): (r + 2 + i * step, top + depth[id(nd)] * dy) for i, nd in enumerate(order)}
    out = [f'<svg style="overflow:visible" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']

    def edges(nd):
        for c in nd[2]:
            (x1, y1), (x2, y2) = xy[id(nd)], xy[id(c)]
            out.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#6b7280" stroke-width="3"/>')
            edges(c)
    edges(t)
    for nd in order:
        x, y = xy[id(nd)]
        if nd[1]:
            out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#e5e7eb" stroke="#6b7280" stroke-width="4" stroke-dasharray="6 4"/>')
        else:
            out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#eff6ff" stroke="#2563eb" stroke-width="4"/>')
        out.append(f'<text x="{x:.0f}" y="{y + 8:.0f}" font-size="22" text-anchor="middle">{nd[0]}</text>')
    out.append("</svg>")
    return "".join(out)


if __name__ == "__main__":
    T = call_tree(5)
    assert count(T) == 9, count(T)
    hits = [nd for nd in (T[2][0][2][0][2][0], T[2][1], T[2][0][2][1]) if nd[1]]
    assert len(hits) == 2 and all(not nd[2] for nd in hits)
    out = Path(__file__).resolve().parent / "fig" / "L18_MEMO.svg"
    out.write_text(svg(T), encoding="utf-8", newline="")
    print("→", out, "9 lời gọi, 2 nút tra bảng")
