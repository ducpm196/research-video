"""Hình cho khoá PLC — cây cú pháp, đồ thị tham chiếu trên đống, trạng thái ngăn xếp. Mọi cây và kết quả lấy từ checklib (alg.*).
Màu theo bảng mặc định của skill dataviz (xanh #2a78d6, cam #eb6834); chữ màu mực; nền #fffbeb. Video là khung tĩnh nên không hover.
Chạy: .venv/Scripts/python audit/plc/figs.py → audit/plc/fig/*.svg (mỗi hình một dòng)."""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg  # noqa: E402

S1, S2 = "#2a78d6", "#eb6834"
INK, MUTED, GRID, BG = "#1f2937", "#6b7280", "#e5e7eb", "#fffbeb"
OUT = ROOT / "audit" / "plc" / "fig"
OUT.mkdir(parents=True, exist_ok=True)
SYM = {"+": "+", "-": "-", "*": "*", "/": "/"}  # cùng ký tự với mã nguồn trên màn hình


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, t, size=22, col=INK, anchor="middle", weight="normal"):
    return (f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" fill="{col}" text-anchor="{anchor}" font-weight="{weight}">{esc(t)}</text>')


def save(name, svg):
    (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")
    print("→", name)


def tree_svg(t, W=520, H=320, title=None, show_val=True):
    """Vẽ cây cú pháp: nút phép là hình tròn xanh (nhãn phép, dưới là giá trị nếu show_val), lá là ô chữ nhật."""
    leaves = []

    def collect(n):
        if isinstance(n, tuple):
            collect(n[1])
            collect(n[2])
        else:
            leaves.append(n)

    collect(t)

    def depth(n):
        return 1 + max(depth(n[1]), depth(n[2])) if isinstance(n, tuple) else 1

    D = depth(t)
    top = 40 if title is None else 76
    dy = (H - top - 40) / max(1, D - 1)
    dx = (W - 80) / max(1, len(leaves) - 1) if len(leaves) > 1 else 0
    pos, k = {}, [0]

    def place(n, d):
        if isinstance(n, tuple):
            a = place(n[1], d + 1)
            b = place(n[2], d + 1)
            x = (a[0] + b[0]) / 2
        else:
            x = 40 + k[0] * dx
            k[0] += 1
        p = (x, top + d * dy)
        pos[id(n)] = p
        return p

    place(t, 0)
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    if title:
        out.append(text(W / 2, 30, title, 22, INK, "middle", "bold"))

    def draw(n):
        x, y = pos[id(n)]
        if isinstance(n, tuple):
            for c in n[1:]:
                cx, cy = pos[id(c)]
                out.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{cx:.0f}" y2="{cy:.0f}" stroke="{MUTED}" stroke-width="2.5"/>')
                draw(c)
            out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="24" fill="{S1}"/>')
            out.append(text(x, y + 9, SYM[n[0]], 26, "#ffffff", "middle", "bold"))
            if show_val:
                out.append(text(x + 34, y + 8, f"= {alg.ast_eval(n)}", 19, S2, "start", "bold"))
        else:
            out.append(f'<rect x="{x - 24:.0f}" y="{y - 20:.0f}" width="48" height="40" rx="6" fill="{BG}" stroke="{INK}" stroke-width="2"/>')
            out.append(text(x, y + 8, str(n), 22, INK))

    draw(t)
    return "".join(out) + "</svg>"


def two_trees(t1, t2, cap1, cap2):
    """Hai cây cạnh nhau trong một hình, mỗi cây một tiêu đề."""
    a = tree_svg(t1, 460, 330, cap1)
    b = tree_svg(t2, 460, 330, cap2)
    inner = lambda s: s[s.index(">") + 1:-6]  # noqa: E731
    return (f'<svg width="960" height="330" viewBox="0 0 960 330"><g>{inner(a)}</g>'
            f'<g transform="translate(500,0)">{inner(b)}</g></svg>')


def heap_fig():
    """Đồ thị tham chiếu: gốc → A → B → C; D ↔ E là vòng không ai trỏ tới. Màu theo alg.mark_sweep."""
    heap = {"A": ["B"], "B": ["C"], "C": [], "D": ["E"], "E": ["D"]}
    live, dead = alg.mark_sweep(heap, ["A"])
    P = {"A": (230, 150), "B": (420, 150), "C": (610, 150), "D": (420, 290), "E": (610, 290)}
    out = ['<svg width="960" height="340" viewBox="0 30 960 340"><defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" '
           f'markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker></defs>']
    out.append(f'<rect x="20" y="125" width="110" height="50" rx="8" fill="{BG}" stroke="{INK}" stroke-width="2"/>')
    out.append(text(75, 158, "gốc", 22))
    out.append(f'<line x1="130" y1="150" x2="200" y2="150" stroke="{INK}" stroke-width="2.5" marker-end="url(#ar)"/>')

    def edge(a, b, bend=0):
        (x1, y1), (x2, y2) = P[a], P[b]
        if bend:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + bend
            out.append(f'<path d="M{x1 + 30},{y1 + bend / 6} Q{mx},{my} {x2 - 30},{y2 + bend / 6}" fill="none" stroke="{INK}" '
                       f'stroke-width="2.5" marker-end="url(#ar)"/>')
        else:
            out.append(f'<line x1="{x1 + 30}" y1="{y1}" x2="{x2 - 32}" y2="{y2}" stroke="{INK}" stroke-width="2.5" marker-end="url(#ar)"/>')

    edge("A", "B")
    edge("B", "C")
    (dx, dy), (ex, ey) = P["D"], P["E"]
    out.append(f'<path d="M{dx + 24},{dy - 18} Q{(dx + ex) / 2},{dy - 70} {ex - 26},{ey - 20}" fill="none" stroke="{INK}" stroke-width="2.5" marker-end="url(#ar)"/>')
    out.append(f'<path d="M{ex - 24},{ey + 18} Q{(dx + ex) / 2},{dy + 70} {dx + 26},{dy + 20}" fill="none" stroke="{INK}" stroke-width="2.5" marker-end="url(#ar)"/>')
    for k, (x, y) in P.items():
        fill, dash = (S1, "") if k in live else ("#ffffff", ' stroke-dasharray="7 5"')
        out.append(f'<circle cx="{x}" cy="{y}" r="30" fill="{fill}" stroke="{S1 if k in live else S2}" stroke-width="3"{dash}/>')
        out.append(text(x, y + 9, k, 26, "#ffffff" if k in live else S2, "middle", "bold"))
    out.append(text(700, 155, "sống (đi tới được từ gốc)", 19, S1, "start", "bold"))
    out.append(text(700, 295, "rác (D, E trỏ vòng nhau)", 19, S2, "start", "bold"))
    return "".join(out) + "</svg>"


if __name__ == "__main__":
    save("tree_123", tree_svg(alg.parse_expr("1+2*3"), 520, 320))
    save("tree_left_right", two_trees(alg.parse_expr("8-3-2"), alg.parse_expr("8-3-2", "right"),
                                      "kết hợp trái: (8-3)-2", "kết hợp phải: 8-(3-2)"))
    save("tree_fold", tree_svg(alg.parse_expr("2*3+x"), 520, 300, show_val=False))
    save("heap", heap_fig())
