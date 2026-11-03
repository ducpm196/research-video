"""Đồ thị có trọng số cho bài CS112 L24–L25 — sinh SVG từ dữ liệu (không vẽ tay). Có hướng: mũi tên dừng ở viền vòng tròn
(marker markerUnits="userSpaceOnUse", luật E8). Nhãn trọng số đặt lệch vuông góc khỏi cạnh để không đè nét.
Dùng: from wgraph_svg import svg; svg(pos, edges, directed=True, hi={(u, v): màu}).  Chạy trực tiếp: in các hình của L24, L25."""
import math
import sys

R = 30


def svg(pos, edges, directed=True, hi=None, w=860, h=330, side=None, mid="m"):
    """edges: [(u, v, trọng số)]; side: {(u, v): +1/−1} đổi phía đặt nhãn; hi: cạnh tô màu."""
    hi, side = hi or {}, side or {}
    out = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    if directed:
        for col, name in (("#6b7280", "g"), ("#059669", "k"), ("#dc2626", "r")):
            out.append(f'<defs><marker id="{mid}{name}" markerUnits="userSpaceOnUse" markerWidth="22" markerHeight="22" refX="20" refY="11" orient="auto"><path d="M0,0 L22,11 L0,22 z" fill="{col}"/></marker></defs>')
    for u, v, wt in edges:
        (x1, y1), (x2, y2) = pos[u], pos[v]
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        sx, sy, ex, ey = x1 + ux * R, y1 + uy * R, x2 - ux * (R + 2), y2 - uy * (R + 2)
        col = hi.get((u, v), "#6b7280")
        name = {"#059669": "k", "#dc2626": "r"}.get(col, "g")
        mk = f' marker-end="url(#{mid}{name})"' if directed else ""
        sw = 6 if (u, v) in hi else 4
        out.append(f'<line x1="{sx:.0f}" y1="{sy:.0f}" x2="{ex:.0f}" y2="{ey:.0f}" stroke="{col}" stroke-width="{sw}"{mk}/>')
        s = side.get((u, v), 1)
        nx, ny = -uy * s, ux * s
        lx, ly = (x1 + x2) / 2 + nx * 22, (y1 + y2) / 2 + ny * 22 + 9
        lab = str(wt).replace("-", "−")
        out.append(f'<text x="{lx:.0f}" y="{ly:.0f}" font-size="28" font-weight="700" fill="#d97706" text-anchor="middle">{lab}</text>')
    for k, (x, y) in pos.items():
        out.append(f'<circle cx="{x}" cy="{y}" r="{R}" fill="#eff6ff" stroke="#2563eb" stroke-width="4"/>')
        out.append(f'<text x="{x}" y="{y + 11}" font-size="30" text-anchor="middle">{k}</text>')
    out.append("</svg>")
    return "".join(out)


POS24 = {"S": (60, 165), "A": (300, 55), "B": (300, 275), "C": (560, 55), "D": (800, 165)}
E24 = [("S", "A", 4), ("S", "B", 1), ("B", "A", 2), ("A", "C", 1), ("B", "C", 5), ("C", "D", 3), ("B", "D", 8)]
POSN = {"S": (60, 160), "A": (380, 50), "B": (380, 270)}
EN = [("S", "A", 2), ("S", "B", 3), ("B", "A", -2)]
POSQ = {"S": (60, 160), "A": (330, 55), "B": (330, 265), "C": (620, 160)}
EQ = [("S", "A", 1), ("S", "B", 4), ("A", "B", 2), ("A", "C", 6), ("B", "C", 3)]
POS25 = {"A": (80, 70), "B": (360, 70), "C": (220, 260), "D": (560, 160), "E": (800, 260)}
E25 = [("A", "C", 1), ("B", "C", 2), ("D", "E", 3), ("A", "B", 4), ("B", "D", 5), ("C", "D", 8), ("C", "E", 10)]

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    from pathlib import Path
    D = Path(__file__).parent / "fig"
    D.mkdir(exist_ok=True)
    tree24 = {("S", "B"): "#059669", ("B", "A"): "#059669", ("A", "C"): "#059669", ("C", "D"): "#059669"}
    figs = {
        "g24": svg(POS24, E24, mid="a", side={("B", "A"): -1}),
        "g24tree": svg(POS24, E24, hi=tree24, mid="b", side={("B", "A"): -1}),
        "g24neg": svg(POSN, EN, w=480, h=320, hi={("B", "A"): "#dc2626"}, mid="c", side={("B", "A"): -1}),
        "g24quiz": svg(POSQ, EQ, w=700, h=320, mid="d", side={("A", "B"): -1}),
        "g25": svg(POS25, E25, directed=False, w=860, h=320, side={("C", "D"): -1}),
        "g25quiz": svg({"A": (80, 60), "B": (420, 60), "C": (420, 270), "D": (80, 270)},
                       [("A", "B", 1), ("B", "C", 4), ("C", "D", 2), ("A", "D", 3), ("A", "C", 5)], directed=False, w=520, h=330,
                       side={("A", "D"): -1, ("A", "C"): -1}),
        "g25tri": svg({"A": (60, 230), "B": (260, 60), "C": (460, 230)}, [("A", "B", 3), ("B", "C", 3), ("A", "C", 5)],
                      directed=False, w=520, h=300, side={("A", "C"): -1}),
        "g25mst": svg(POS25, E25, directed=False, w=860, h=320, side={("C", "D"): -1},
                      hi={("A", "C"): "#059669", ("B", "C"): "#059669", ("D", "E"): "#059669", ("B", "D"): "#059669"}),
    }
    for k, v in figs.items():
        (D / f"{k}.svg").write_text(v, encoding="utf-8")
        print(k, len(v))


def cycle5(mark=None, w=420, h=320):
    """Chu trình 5 đỉnh 1..5 (bài L26): mark = {đỉnh: (tô nền, viền)} để chỉ tập độc lập / phủ đỉnh."""
    mark = mark or {}
    cx, cy, rr = w / 2, h / 2 + 10, 125
    pos = {k: (cx + rr * math.sin(2 * math.pi * (k - 1) / 5), cy - rr * math.cos(2 * math.pi * (k - 1) / 5)) for k in range(1, 6)}
    out = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    for k in range(1, 6):
        (x1, y1), (x2, y2) = pos[k], pos[k % 5 + 1]
        out.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#6b7280" stroke-width="4"/>')
    for k, (x, y) in pos.items():
        fill, stroke = mark.get(k, ("#eff6ff", "#2563eb"))
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{R}" fill="{fill}" stroke="{stroke}" stroke-width="5"/>')
        out.append(f'<text x="{x:.0f}" y="{y + 11:.0f}" font-size="30" text-anchor="middle">{k}</text>')
    out.append("</svg>")
    return "".join(out)


if __name__ == "__main__":
    G, O = ("#d1fae5", "#059669"), ("#ffedd5", "#d97706")
    (Path(__file__).parent / "fig" / "c5.svg").write_text(cycle5({1: G, 3: G, 2: O, 4: O, 5: O}), encoding="utf-8")
    print("c5")
