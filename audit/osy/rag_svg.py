"""Đồ thị cấp phát tài nguyên cho OSY L06 — sinh SVG từ danh sách cạnh, không vẽ tay.
Tiến trình = hình tròn; tài nguyên = hình vuông, mỗi chấm bên trong = một thể hiện. Cạnh yêu cầu P → R (nét đứt),
cạnh cấp phát R → P (nét liền). Kiểm: mỗi cạnh cấp phát dùng một thể hiện, không vượt số chấm.
Chạy: .venv/Scripts/python audit/osy/rag_svg.py → audit/osy/fig/rag_*.svg"""
import math
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
R_P, S_R = 38, 84


def svg(nodes, inst, req, asg, W=760, H=330, mid="ah"):
    """nodes: {tên: (x, y)} — tên bắt đầu bằng P là tiến trình, R là tài nguyên; inst: {R: số thể hiện};
    req: [(P, R)]; asg: [(R, P)]."""
    for r in inst:
        assert sum(1 for a, _ in asg if a == r) <= inst[r], f"{r} cấp quá số thể hiện"
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           f'<defs><marker id="{mid}" markerUnits="userSpaceOnUse" markerWidth="22" markerHeight="22" refX="20" refY="11" orient="auto">'
           '<path d="M0,0 L22,11 L0,22 z" fill="#374151"/></marker></defs>']

    def edge(a, b, dashed):
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        d = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / d, (y2 - y1) / d
        ra = R_P if a[0] == "P" else S_R / 2 * 1.15
        rb = R_P if b[0] == "P" else S_R / 2 * 1.15
        sx, sy, ex, ey = x1 + ux * ra, y1 + uy * ra, x2 - ux * (rb + 4), y2 - uy * (rb + 4)
        dash = ' stroke-dasharray="12 9"' if dashed else ""
        out.append(f'<line x1="{sx:.0f}" y1="{sy:.0f}" x2="{ex:.0f}" y2="{ey:.0f}" stroke="#374151" stroke-width="4"{dash} marker-end="url(#{mid})"/>')

    for p, r in req:
        edge(p, r, True)
    for r, p in asg:
        edge(r, p, False)
    for n, (x, y) in nodes.items():
        if n[0] == "P":
            out.append(f'<circle cx="{x}" cy="{y}" r="{R_P}" fill="#eff6ff" stroke="#2563eb" stroke-width="4"/>'
                       f'<text x="{x}" y="{y + 11}" font-size="30" font-weight="700" text-anchor="middle">{n}</text>')
        else:
            out.append(f'<rect x="{x - S_R / 2:.0f}" y="{y - S_R / 2:.0f}" width="{S_R}" height="{S_R}" rx="8" fill="#fef3c7" stroke="#d97706" stroke-width="4"/>')
            k = inst[n]
            for j in range(k):
                cx = x + (j - (k - 1) / 2) * 26
                out.append(f'<circle cx="{cx:.0f}" cy="{y + 14}" r="8" fill="#92400e"/>')
            out.append(f'<text x="{x}" y="{y - 8}" font-size="26" font-weight="700" text-anchor="middle">{n}</text>')
    out.append("</svg>")
    return "".join(out)


if __name__ == "__main__":
    fig = ROOT / "audit" / "osy" / "fig"; fig.mkdir(parents=True, exist_ok=True)
    one = svg({"P1": (130, 165), "R1": (380, 60), "P2": (630, 165), "R2": (380, 270)},
              {"R1": 1, "R2": 1}, req=[("P1", "R1"), ("P2", "R2")], asg=[("R1", "P2"), ("R2", "P1")], mid="ah1")
    two = svg({"P1": (130, 165), "R1": (380, 60), "P2": (630, 165), "R2": (380, 270), "P3": (630, 40)},
              {"R1": 2, "R2": 1}, req=[("P1", "R1"), ("P2", "R2")], asg=[("R1", "P2"), ("R1", "P3"), ("R2", "P1")], H=330, mid="ah2")
    for k, v in {"rag_one": one, "rag_two": two}.items():
        (fig / f"{k}.svg").write_text(v, encoding="utf-8"); print("→", fig / f"{k}.svg")
