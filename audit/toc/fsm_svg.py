"""Sơ đồ ôtômat và băng máy Turing cho khoá TOC — sinh SVG từ bảng chuyển, không vẽ tay.
Trạng thái = hình tròn (nhận = viền đôi); mũi tên không có gốc chỉ vào trạng thái đầu; cạnh p → q mang nhãn các ký hiệu.
Hai cạnh ngược chiều giữa cùng cặp trạng thái được uốn cong về hai phía để không đè nhau. Vòng lặp tự thân vẽ phía trên
(hoặc dưới) trạng thái. Kiểm: mọi cạnh trong bảng chuyển đều được vẽ đúng một lần (gộp nhãn theo cặp trạng thái).
Chạy: .venv/Scripts/python audit/toc/fsm_svg.py → audit/toc/fig/*.svg (mỗi tệp một dòng, dùng với audit/cs112/fill_tpl.py)."""
import math
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg  # noqa: E402

R = 40
INK, BLUE, FILL, ACC = "#374151", "#2563eb", "#eff6ff", "#dcfce7"


def label_svg(name, x, y, size=30):
    """q0 → q với chỉ số dưới 0 (giống $q_0$ của KaTeX); tên khác in thẳng."""
    if len(name) >= 2 and name[0] == "q" and name[1:].isdigit():
        return (f'<text x="{x}" y="{y + 10}" font-size="{size}" text-anchor="middle" font-style="italic" font-family="KaTeX_Math, serif">q'
                f'<tspan font-size="{int(size * 0.7)}" dy="8" font-style="normal" font-family="KaTeX_Main, serif">{name[1:]}</tspan></text>')
    return f'<text x="{x}" y="{y + 10}" font-size="{size}" font-weight="700" text-anchor="middle">{name}</text>'


def fsm(pos, edges, start, accept, W, H, mid, loops_below=(), bend=None, hl=None, rad=None):
    """pos: {trạng thái: (x, y)}; edges: {(p, q): "nhãn"}; bend: {(p, q): độ cong px} (dương = lệch trái theo chiều đi);
    hl: tập trạng thái tô đậm (đang ở); rad: {trạng thái: bán kính} cho tên dài."""
    bend = dict(bend or {}); hl = set(hl or ()); rad = dict(rad or {})
    for (p, q) in edges:
        if p != q and (q, p) in edges:
            bend.setdefault((p, q), 46)
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           f'<defs><marker id="{mid}" markerUnits="userSpaceOnUse" markerWidth="20" markerHeight="20" refX="18" refY="10" orient="auto">'
           f'<path d="M0,0 L20,10 L0,20 z" fill="{INK}"/></marker></defs>']
    lab = []
    for (p, q), text in edges.items():
        (x1, y1), (x2, y2) = pos[p], pos[q]
        rp, rq = rad.get(p, R), rad.get(q, R)
        if p == q:
            s = 1 if p in loops_below else -1
            a1, a2 = math.radians(-120 if s < 0 else 120), math.radians(-60 if s < 0 else 60)
            sx, sy = x1 + rp * math.cos(a1), y1 + rp * math.sin(a1) * 1
            ex, ey = x1 + rp * math.cos(a2), y1 + rp * math.sin(a2)
            sy, ey = (y1 - rp * math.sin(math.radians(60)), y1 - rp * math.sin(math.radians(60))) if s < 0 else \
                     (y1 + rp * math.sin(math.radians(60)), y1 + rp * math.sin(math.radians(60)))
            sx, ex = x1 - rp * 0.5, x1 + rp * 0.5
            cy = y1 + s * (rp + 78)
            out.append(f'<path d="M{sx:.0f},{sy:.0f} C{sx - 34:.0f},{cy:.0f} {ex + 34:.0f},{cy:.0f} {ex:.0f},{ey:.0f}" fill="none" '
                       f'stroke="{INK}" stroke-width="3.5" marker-end="url(#{mid})"/>')
            ly = y1 + s * (rp + 66) + (26 if s > 0 else -8)
            lab.append((x1, ly, text))
            continue
        d = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / d, (y2 - y1) / d
        nx, ny = uy, -ux  # pháp tuyến bên trái theo chiều đi (toạ độ màn hình, y hướng xuống)
        b = bend.get((p, q), 0)
        mx, my = (x1 + x2) / 2 + nx * b * 2, (y1 + y2) / 2 + ny * b * 2   # điểm điều khiển Bezier bậc hai
        # điểm đầu/cuối nằm trên đường tròn, theo hướng tới điểm điều khiển
        def on_circle(cx, cy, r, tx, ty, extra=0):
            dd = math.hypot(tx - cx, ty - cy)
            return cx + (tx - cx) / dd * (r + extra), cy + (ty - cy) / dd * (r + extra)
        sx, sy = on_circle(x1, y1, rp, mx, my)
        ex, ey = on_circle(x2, y2, rq, mx, my, 3)
        out.append(f'<path d="M{sx:.0f},{sy:.0f} Q{mx:.0f},{my:.0f} {ex:.0f},{ey:.0f}" fill="none" stroke="{INK}" stroke-width="3.5" '
                   f'marker-end="url(#{mid})"/>')
        # nhãn ở giữa đường cong (t = 0,5), lùi thêm theo pháp tuyến
        lx, ly = 0.25 * sx + 0.5 * mx + 0.25 * ex, 0.25 * sy + 0.5 * my + 0.25 * ey
        off = 24 if b >= 0 else -24
        if b == 0:
            off = 24
        lab.append((lx + nx * off, ly + ny * off + 9, text))
    sx0, sy0 = pos[start]
    rs = rad.get(start, R)
    out.append(f'<line x1="{sx0 - rs - 62}" y1="{sy0}" x2="{sx0 - rs - 4}" y2="{sy0}" stroke="{INK}" stroke-width="3.5" marker-end="url(#{mid})"/>')
    for n, (x, y) in pos.items():
        r = rad.get(n, R)
        fill = ACC if n in accept else FILL
        sw = 6 if n in hl else 3.5
        col = "#dc2626" if n in hl else BLUE
        out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{col}" stroke-width="{sw}"/>')
        if n in accept:
            out.append(f'<circle cx="{x}" cy="{y}" r="{r - 8}" fill="none" stroke="{col}" stroke-width="3"/>')
        out.append(label_svg(n, x, y, 30 if r <= R else 26))
    for x, y, t in lab:
        out.append(f'<text x="{x:.0f}" y="{y:.0f}" font-size="28" font-weight="700" fill="#b45309" text-anchor="middle">{t}</text>')
    out.append("</svg>")
    return "".join(out)


def tape(cells, head, state, W=760, H=170, cw=76, blank="_"):
    """Băng máy Turing: các ô, ô dưới đầu đọc tô đỏ, tam giác chỉ đầu đọc kèm tên trạng thái phía trên."""
    n = len(cells); x0 = (W - n * cw) / 2
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    for i, c in enumerate(cells):
        x = x0 + i * cw
        st = ' stroke="#dc2626" stroke-width="5"' if i == head else f' stroke="{INK}" stroke-width="3"'
        fill = "#fee2e2" if i == head else "#ffffff"
        out.append(f'<rect x="{x:.0f}" y="70" width="{cw}" height="{cw}" fill="{fill}"{st}/>')
        t = "" if c == blank else c
        out.append(f'<text x="{x + cw / 2:.0f}" y="{70 + cw / 2 + 12:.0f}" font-size="36" font-weight="700" text-anchor="middle">{t}</text>')
    hx = x0 + head * cw + cw / 2
    out.append(f'<path d="M{hx - 16:.0f},34 L{hx + 16:.0f},34 L{hx:.0f},62 z" fill="#dc2626"/>')
    out.append(label_svg(state, hx, 14, 26).replace(f'y="{14 + 10}"', 'y="26"'))
    out.append(f'<text x="{x0 - 20:.0f}" y="{70 + cw / 2 + 12:.0f}" font-size="34" fill="#9ca3af" text-anchor="end">…</text>')
    out.append(f'<text x="{x0 + n * cw + 20:.0f}" y="{70 + cw / 2 + 12:.0f}" font-size="34" fill="#9ca3af">…</text>')
    out.append("</svg>")
    return "".join(out)


def leaves(t):
    """Đọc lá từ trái sang phải (bỏ ε) — phải ra đúng chuỗi được suy dẫn."""
    lab, kids = t
    return ("" if lab == "ε" else lab) if not kids else "".join(leaves(k) for k in kids)


def evaluate(t):
    """Giá trị của cây biểu thức E → E+E | E*E | E-E | số (nút trong có 3 con: trái, phép toán, phải; hoặc 1 con là số)."""
    lab, kids = t
    if not kids:
        return int(lab)
    if len(kids) == 1:
        return evaluate(kids[0])
    a, op, b = evaluate(kids[0]), kids[1][0], evaluate(kids[2])
    return {"+": a + b, "-": a - b, "×": a * b}[op]


def tree(t, W=560, dy=92, top=40):
    """Cây suy dẫn: lá xếp đều theo thứ tự trái → phải, nút trong nằm giữa các con. Biến (chữ hoa) tô xanh đậm,
    ký hiệu kết thúc đen, ε xám. Chiều cao tính theo độ sâu."""
    pos, order = {}, []

    def depth(n):
        return 1 + max((depth(k) for k in n[1]), default=0)

    def walk(n, d, path):
        lab, kids = n
        if not kids:
            order.append(path); pos[path] = [None, top + d * dy, lab]
            return
        for i, k in enumerate(kids):
            walk(k, d + 1, path + (i,))
        pos[path] = [None, top + d * dy, lab]

    walk(t, 0, ())
    step = (W - 80) / max(1, len(order) - 1) if len(order) > 1 else 0
    for i, p in enumerate(order):
        pos[p][0] = 40 + i * step

    def fix(path, n):
        if n[1]:
            xs = [fix(path + (i,), k) for i, k in enumerate(n[1])]
            pos[path][0] = sum(xs) / len(xs)
        return pos[path][0]

    fix((), t)
    H = top + (depth(t) - 1) * dy + 40
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    for path, (x, y, lab) in pos.items():
        if path:
            px, py, _ = pos[path[:-1]]
            out.append(f'<line x1="{px:.0f}" y1="{py + 16:.0f}" x2="{x:.0f}" y2="{y - 22:.0f}" stroke="#9ca3af" stroke-width="3"/>')
    for path, (x, y, lab) in pos.items():
        if lab == "ε":
            out.append(f'<text x="{x:.0f}" y="{y + 10:.0f}" font-size="32" font-style="italic" fill="#6b7280" text-anchor="middle" '
                       f'font-family="KaTeX_Math, serif">&#949;</text>')
        elif lab.isupper():
            out.append(f'<text x="{x:.0f}" y="{y + 10:.0f}" font-size="32" font-weight="700" fill="#1d4ed8" text-anchor="middle" '
                       f'font-family="KaTeX_Math, serif" font-style="italic">{lab}</text>')
        else:
            out.append(f'<text x="{x:.0f}" y="{y + 10:.0f}" font-size="32" font-weight="700" text-anchor="middle">{lab}</text>')
    out.append("</svg>")
    return "".join(out)


def check_edges(delta, edges):
    """Mọi chuyển của bảng có mặt trong sơ đồ: nhãn của cạnh (p, q) gồm đúng các ký hiệu đưa p tới q."""
    want = {}
    for (p, a), q in delta.items():
        for r in (q if isinstance(q, (set, frozenset)) else [q]):
            want.setdefault((p, r), set()).add(a)
    got = {k: set(v.replace(" ", "").split(",")) for k, v in edges.items()}
    assert want == got, (want, got)


if __name__ == "__main__":
    fig = ROOT / "audit" / "toc" / "fig"; fig.mkdir(parents=True, exist_ok=True)
    F = {}
    # L01: DFA số dư khi chia 3
    D3 = {(f"q{r}", b): f"q{(2 * r + int(b)) % 3}" for r in range(3) for b in "01"}
    E3 = {("q0", "q0"): "0", ("q0", "q1"): "1", ("q1", "q0"): "1", ("q1", "q2"): "0", ("q2", "q1"): "0", ("q2", "q2"): "1"}
    check_edges(D3, E3)
    P3 = {"q0": (150, 175), "q1": (390, 175), "q2": (630, 175)}
    F["dfa3"] = fsm(P3, E3, "q0", {"q0"}, 760, 330, "a3", loops_below=())
    # L06: cây suy dẫn 0011 theo S → 0S1 | ε
    E = ("ε", [])
    T0011 = ("S", [("0", []), ("S", [("0", []), ("S", [E]), ("1", [])]), ("1", [])])
    assert leaves(T0011) == "0011"
    F["tree0011"] = tree(T0011)
    # L07: hai cây của 1 + 2 * 3 theo E → E+E | E*E | số
    def num(n):
        return ("E", [(str(n), [])])
    TA = ("E", [("E", [num(1), ("+", []), num(2)]), ("×", []), num(3)])     # (1 + 2) × 3
    TB = ("E", [num(1), ("+", []), ("E", [num(2), ("×", []), num(3)])])     # 1 + (2 × 3)
    assert leaves(TA) == leaves(TB) == "1+2×3" and evaluate(TA) == 9 and evaluate(TB) == 7
    F["tree_mul_top"] = tree(TA, W=520)
    F["tree_add_top"] = tree(TB, W=520)
    # L02: NFA kết thúc bằng 01
    N = {("A", "0"): {"A", "B"}, ("A", "1"): {"A"}, ("B", "1"): {"C"}}
    EN = {("A", "A"): "0, 1", ("A", "B"): "0", ("B", "C"): "1"}
    check_edges(N, EN)
    F["nfa01"] = fsm({"A": (150, 175), "B": (390, 175), "C": (630, 175)}, EN, "A", {"C"}, 760, 300, "an")
    # L02: DFA từ dựng tập con
    order, tr = alg.subset_construct(N, "A", "01")
    nm = {frozenset("A"): "A", frozenset("AB"): "AB", frozenset("AC"): "AC"}
    assert set(order) == set(nm)
    DS = {(nm[S], a): nm[T] for (S, a), T in tr.items()}
    ES = {("A", "A"): "1", ("A", "AB"): "0", ("AB", "AB"): "0", ("AB", "AC"): "1", ("AC", "AB"): "0", ("AC", "A"): "1"}
    check_edges(DS, ES)
    F["dfa01"] = fsm({"A": (150, 150), "AB": (390, 150), "AC": (630, 150)}, ES, "A", {"AC"}, 760, 380, "ad",
                     loops_below=(), bend={("AC", "A"): 150, ("AB", "AC"): 30, ("AC", "AB"): 30}, rad={"AB": 44, "AC": 44})
    # L09: băng máy Turing cộng một
    INC = {("C", "1"): ("C", "0", "L"), ("C", "0"): ("H", "1", "S"), ("C", "_"): ("H", "1", "S")}
    _, _, _, trace = alg.tm_run(INC, "_1011", 4, "C")
    name = {"C": "q0", "H": "q1"}      # q0 = đang cộng (còn nhớ 1), q1 = dừng
    for i, (st, h, snap) in enumerate(trace):
        F[f"tm_inc_{i}"] = tape(list(snap), h, name[st])
    out, steps, st, _ = alg.tm_run(INC, "_1011", 4, "C")
    st_l, h_l, snap_l = trace[-1]
    nq, b, mv = INC[(st_l, snap_l[h_l])]
    end = list(snap_l); end[h_l] = b
    F["tm_inc_end"] = tape(end, h_l + {"L": -1, "R": 1, "S": 0}[mv], name[nq])
    assert out == "1100" and steps == 3 and "".join(end) == "_1100" and nq == "H"
    for k, v in F.items():
        (fig / f"{k}.svg").write_text(v, encoding="utf-8")
    print(len(F), "hình →", fig)
