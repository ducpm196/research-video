"""Đa đồ thị cho DMS L16 — sinh SVG từ danh sách cạnh, không vẽ tay. Cạnh lặp giữa cùng hai đỉnh vẽ thành cung cong lệch đều hai phía;
nhãn bậc đặt cạnh mỗi đỉnh (tính từ danh sách cạnh). Chạy: .venv/Scripts/python audit/dms/multigraph_svg.py
→ audit/dms/fig/konigsberg.svg, envelope.svg, envelope_path.svg"""
import math
import sys
from collections import Counter
from pathlib import Path

R = 30


def degrees(edges):
    c = Counter()
    for u, v in edges:
        c[u] += 1
        c[v] += 1
    return c


def svg(pos, edges, w=560, h=380, deg_off=None, order=None):
    """order: danh sách cạnh theo thứ tự đi (đánh số 1, 2, … cạnh cạnh)."""
    deg = degrees(edges)
    out = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    seen = Counter()
    mult = Counter(frozenset(e) for e in edges)
    for i, (u, v) in enumerate(edges):
        k = frozenset((u, v))
        j = seen[k]
        seen[k] += 1
        m = mult[k]
        (x1, y1), (x2, y2) = pos[u], pos[v]
        off = (j - (m - 1) / 2) * 70
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        nx, ny = -dy / L, dx / L
        cx, cy = (x1 + x2) / 2 + nx * off * 2, (y1 + y2) / 2 + ny * off * 2
        out.append(f'<path d="M{x1:.0f},{y1:.0f} Q{cx:.0f},{cy:.0f} {x2:.0f},{y2:.0f}" fill="none" stroke="#6b7280" stroke-width="5"/>')
        if order is not None:
            # nhãn ở t = 0,35 (không ở giữa): hai đường chéo của phong bì có cùng trung điểm → nhãn sẽ đè nhau
            t = 0.35
            mx = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * cx + t * t * x2
            my = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * cy + t * t * y2
            out.append(f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="17" fill="#fff7ed" stroke="#d97706" stroke-width="3"/>'
                       f'<text x="{mx:.0f}" y="{my + 8:.0f}" font-size="22" font-weight="700" fill="#b45309" text-anchor="middle">{order.index(i) + 1}</text>')
    for x, (cx, cy) in pos.items():
        out.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{R}" fill="#eff6ff" stroke="#2563eb" stroke-width="4"/>'
                   f'<text x="{cx:.0f}" y="{cy + 11:.0f}" font-size="30" text-anchor="middle">{x}</text>')
        if deg_off:
            ox, oy = deg_off[x]
            out.append(f'<text x="{cx + ox:.0f}" y="{cy + oy:.0f}" font-size="24" font-weight="700" fill="#dc2626" text-anchor="middle">bậc {deg[x]}</text>')
    out.append("</svg>")
    return "".join(out)


def euler_path(edges, start):
    """Hierholzer trên đa đồ thị: trả về thứ tự chỉ số cạnh."""
    adj = {}
    for i, (u, v) in enumerate(edges):
        adj.setdefault(u, []).append((v, i))
        adj.setdefault(v, []).append((u, i))
    used, stack, path = set(), [(start, None)], []
    while stack:
        v, ei = stack[-1]
        while adj[v] and adj[v][-1][1] in used:
            adj[v].pop()
        if adj[v]:
            w, j = adj[v].pop()
            used.add(j)
            stack.append((w, j))
        else:
            stack.pop()
            if ei is not None:
                path.append(ei)
    return path[::-1]


KON = [("A", "C"), ("A", "C"), ("B", "C"), ("B", "C"), ("A", "D"), ("B", "D"), ("C", "D")]
KON_POS = {"A": (200, 60), "C": (200, 190), "B": (200, 320), "D": (470, 190)}
ENV = [(1, 2), (2, 3), (3, 4), (4, 1), (4, 5), (5, 3), (1, 3), (2, 4)]
ENV_POS = {1: (130, 340), 2: (390, 340), 3: (390, 170), 4: (130, 170), 5: (260, 50)}

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    D = Path(__file__).resolve().parent / "fig"
    D.mkdir(exist_ok=True)
    assert sorted(degrees(KON).values()) == [3, 3, 3, 5] and len(KON) == 7
    (D / "konigsberg.svg").write_text(svg(KON_POS, KON, deg_off={"A": (-95, 8), "B": (-95, 8), "C": (-110, 8), "D": (0, 62)}), encoding="utf-8")
    (D / "envelope.svg").write_text(svg(ENV_POS, ENV, w=520, deg_off={1: (-78, 8), 2: (78, 8), 3: (80, 8), 4: (-80, 8), 5: (90, 8)}), encoding="utf-8")
    order = euler_path(ENV, 1)
    assert sorted(order) == list(range(len(ENV)))
    (D / "envelope_path.svg").write_text(svg(ENV_POS, ENV, w=520, order=order), encoding="utf-8")
    walk = [1]
    for i in order:
        u, v = ENV[i]
        walk.append(v if walk[-1] == u else u)
    print("bậc Königsberg:", dict(degrees(KON)), "| bậc phong bì:", dict(degrees(ENV)), "| đường Euler:", walk)
