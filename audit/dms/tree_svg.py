"""Cây nhỏ cho DMS L17 — sinh SVG từ danh sách cạnh (không vẽ tay). Ba cây có nhãn trên {1, 2, 3} (đủ 3 = 3^(3−2)) và hai hình dạng
cây 4 đỉnh (đường, sao). Chạy: .venv/Scripts/python audit/dms/tree_svg.py → audit/dms/fig/trees3.svg, shapes4.svg"""
import itertools
from pathlib import Path

R = 26


def one(pos, edges, ox):
    out = []
    for u, v in edges:
        (x1, y1), (x2, y2) = pos[u], pos[v]
        out.append(f'<line x1="{x1 + ox:.0f}" y1="{y1:.0f}" x2="{x2 + ox:.0f}" y2="{y2:.0f}" stroke="#6b7280" stroke-width="5"/>')
    for x, (cx, cy) in pos.items():
        out.append(f'<circle cx="{cx + ox:.0f}" cy="{cy:.0f}" r="{R}" fill="#eff6ff" stroke="#2563eb" stroke-width="4"/>'
                   f'<text x="{cx + ox:.0f}" y="{cy + 10:.0f}" font-size="26" text-anchor="middle">{x}</text>')
    return out


def strip(parts, w_each, h):
    out = [f'<svg width="{w_each * len(parts)}" height="{h}" viewBox="0 0 {w_each * len(parts)} {h}">']
    for k, (pos, es) in enumerate(parts):
        out += one(pos, es, k * w_each)
    return "".join(out + ["</svg>"])


if __name__ == "__main__":
    D = Path(__file__).resolve().parent / "fig"
    D.mkdir(exist_ok=True)
    tri = {1: (40, 150), 2: (110, 40), 3: (180, 150)}
    trees = [es for es in itertools.combinations([(1, 2), (1, 3), (2, 3)], 2)]
    assert len(trees) == 3
    (D / "trees3.svg").write_text(strip([(tri, es) for es in trees], 230, 190), encoding="utf-8")
    p4 = {"a": (40, 100), "b": (120, 100), "c": (200, 100), "d": (280, 100)}
    s4 = {"a": (150, 100), "b": (60, 40), "c": (240, 40), "d": (150, 180)}
    (D / "shapes4.svg").write_text(strip([(p4, [("a", "b"), ("b", "c"), ("c", "d")]), (s4, [("a", "b"), ("a", "c"), ("a", "d")])], 330, 220)
                                   .replace(">a<", "><").replace(">b<", "><").replace(">c<", "><").replace(">d<", "><"), encoding="utf-8")
    print("ok")
