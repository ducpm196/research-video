"""Hình cho khoá DBS — sơ đồ thực thể–liên kết, cây B+, đồ thị ưu tiên. Toạ độ tính bằng mã, không vẽ tay.
Màu theo bảng mặc định của skill dataviz (xanh #2a78d6, cam #eb6834 — đã kiểm validate_palette.js ở NET); chữ màu mực; nền #fffbeb.
Chạy: .venv/Scripts/python audit/dbs/figs.py → audit/dbs/fig/*.svg (mỗi hình một dòng)."""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg  # noqa: E402

S1, S2 = "#2a78d6", "#eb6834"
INK, MUTED, BG = "#1f2937", "#6b7280", "#fffbeb"
OUT = ROOT / "audit" / "dbs" / "fig"
OUT.mkdir(parents=True, exist_ok=True)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, t, size=22, col=INK, anchor="middle", weight="normal", underline=False):
    u = ' text-decoration="underline"' if underline else ""
    return (f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" fill="{col}" text-anchor="{anchor}" font-weight="{weight}"{u} '
            f'stroke="{BG}" stroke-width="6" paint-order="stroke">{esc(t)}</text>')


def entity(x, y, name, w=170, h=60):
    return (f'<rect x="{x - w / 2:.0f}" y="{y - h / 2:.0f}" width="{w}" height="{h}" rx="6" fill="#dbeafe" stroke="{S1}" stroke-width="3"/>'
            + text(x, y + 8, name, 24, weight="bold"))


def rel(x, y, name, w=150, h=80):
    pts = f"{x - w / 2:.0f},{y} {x},{y - h / 2:.0f} {x + w / 2:.0f},{y} {x},{y + h / 2:.0f}"
    return f'<polygon points="{pts}" fill="#ffedd5" stroke="{S2}" stroke-width="3"/>' + text(x, y + 7, name, 20)


def attr(x, y, name, key=False, w=120, h=44):
    """Thuộc tính (elip); thuộc tính khoá có gạch dưới vẽ bằng đường riêng (text-decoration bị viền chữ che)."""
    s = (f'<ellipse cx="{x}" cy="{y}" rx="{w / 2}" ry="{h / 2}" fill="#ffffff" stroke="{MUTED}" stroke-width="2"/>'
         + text(x, y + 7, name, 19))
    if key:
        half = len(name) * 5.2
        s += line(x - half, y + 12, x + half, y + 12, INK, 2)
    return s


def line(x1, y1, x2, y2, col=INK, w=2.5):
    return f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{col}" stroke-width="{w}"/>'


def er_full():
    W, H = 1180, 380
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    y = 200
    xs = {"Lop": 110, "thuoc": 300, "SV": 500, "dk": 720, "MH": 950}
    # đường nối trước (nằm dưới hình)
    out += [line(xs["Lop"] + 85, y, xs["thuoc"] - 75, y), line(xs["thuoc"] + 75, y, xs["SV"] - 85, y),
            line(xs["SV"] + 85, y, xs["dk"] - 75, y), line(xs["dk"] + 75, y, xs["MH"] - 85, y)]
    for ex, ey, ax, ay in ((xs["Lop"], y, 60, 80), (xs["Lop"], y, 185, 80), (xs["SV"], y, 430, 75), (xs["SV"], y, 570, 75),
                           (xs["MH"], y, 900, 80), (xs["MH"], y, 1040, 80), (xs["dk"], y, 720, 320)):
        out.append(line(ex, ey + (-30 if ay < ey else 30), ax, ay + (22 if ay < ey else -22), MUTED, 2))
    out += [entity(xs["Lop"], y, "Lop"), rel(xs["thuoc"], y, "thuộc"), entity(xs["SV"], y, "SinhVien"),
            rel(xs["dk"], y, "đăng ký"), entity(xs["MH"], y, "MonHoc")]
    out += [attr(60, 80, "ma_lop", key=True, w=110), attr(185, 80, "ten_lop", w=110), attr(430, 75, "mssv", key=True),
            attr(570, 75, "ten"), attr(900, 80, "ma_mon", key=True), attr(1040, 80, "ten_mon"), attr(720, 320, "diem")]
    for x, lab in ((xs["Lop"] + 105, "1"), (xs["SV"] - 105, "N"), (xs["SV"] + 105, "M"), (xs["MH"] - 105, "N")):
        out.append(text(x, y - 14, lab, 24, S2 if lab in "MN" else S1, weight="bold"))
    out.append(text(300, 300, "một lớp – nhiều SV", 19, MUTED))
    out.append(text(860, 300, "nhiều – nhiều", 19, MUTED))
    return "".join(out) + "</svg>"


# ───────── L08: cây B+ ba tầng, bậc 3 ─────────
BPT_ROOT, BPT_INNER, BPT_LEAVES = alg.BPT_ROOT, alg.BPT_INNER, alg.BPT_LEAVES
bpt_search, bpt_range = alg.bpt_search, alg.bpt_range


def node(x, y, keys, w, h=50, hl=False):
    fill, st = ("#ffedd5", S2) if hl else ("#ffffff", MUTED)
    out = [f'<rect x="{x - w / 2:.0f}" y="{y}" width="{w}" height="{h}" rx="5" fill="{fill}" stroke="{st}" stroke-width="{3 if hl else 2}"/>']
    n = len(keys)
    for t, k in enumerate(keys):
        cx = x - w / 2 + w * (t + 0.5) / n
        out.append(text(cx, y + 33, str(k), 22))
        if t:
            sx = x - w / 2 + w * t / n
            out.append(line(sx, y + 8, sx, y + h - 8, MUTED, 1.5))
    return "".join(out)


def bplus(search=None, rng=None):
    W, H = 1180, 380
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    path_i = path_j = None
    leaves_hl = set()
    if search is not None:
        path_i, path_j, _ = bpt_search(search)
        leaves_hl = {path_j}
    if rng is not None:
        leaves_hl = set(bpt_range(*rng)[0])
        path_i, path_j, _ = bpt_search(rng[0])
    rx, ry = W / 2, 30
    ix = [W * (2 * i + 1) / 6 for i in range(3)]
    iy, ly = 150, 280
    lx = [60 + i * (W - 120) / 8 for i in range(9)]
    for i in range(3):
        out.append(line(rx - 70 + 70 * i, ry + 50, ix[i], iy, S2 if path_i == i else MUTED, 3 if path_i == i else 1.5))
        for j in range(3):
            jj = 3 * i + j
            out.append(line(ix[i] - 60 + 60 * j, iy + 50, lx[jj], ly, S2 if path_j == jj and path_i == i else MUTED,
                            3 if path_j == jj and path_i == i else 1.5))
    for jj in range(8):
        out.append(f'<line x1="{lx[jj] + 52:.0f}" y1="{ly + 25}" x2="{lx[jj + 1] - 56:.0f}" y2="{ly + 25}" stroke="{S1}" '
                   f'stroke-width="2.5" marker-end="url(#lk)"/>')
    out.insert(1, f'<defs><marker id="lk" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="11" refY="6" orient="auto">'
                  f'<path d="M0,0 L12,6 L0,12 z" fill="{S1}"/></marker></defs>')
    out.append(node(rx, ry, BPT_ROOT, 150, hl=path_i is not None))
    for i in range(3):
        out.append(node(ix[i], iy, BPT_INNER[i], 140, hl=path_i == i))
    for jj in range(9):
        out.append(node(lx[jj], ly, BPT_LEAVES[jj], 104, hl=jj in leaves_hl))
    out.append(text(W - 10, ly + 85, "lá nối với nhau (mũi tên xanh) — đi ngang để quét khoảng", 18, MUTED, anchor="end"))
    out.append(text(20, ry + 33, "gốc", 20, MUTED, anchor="start"))
    out.append(text(20, iy + 33, "nút trong", 20, MUTED, anchor="start"))
    return "".join(out) + "</svg>"


# ───────── L12: đồ thị ưu tiên hai giao dịch ─────────
def prec(schedule, title, labels=None):
    """Vẽ đồ thị ưu tiên của lịch (cạnh lấy từ alg.precedence_graph); cạnh nào nằm trên chu trình tô cam."""
    edges, cyc = alg.precedence_graph(schedule)
    W, H = 560, 250
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           f'<defs><marker id="pa" markerUnits="userSpaceOnUse" markerWidth="16" markerHeight="16" refX="14" refY="8" orient="auto">'
           f'<path d="M0,0 L16,8 L0,16 z" fill="{INK}"/></marker>'
           f'<marker id="pc" markerUnits="userSpaceOnUse" markerWidth="16" markerHeight="16" refX="14" refY="8" orient="auto">'
           f'<path d="M0,0 L16,8 L0,16 z" fill="{S2}"/></marker></defs>']
    pos = {"T1": (140, 120), "T2": (420, 120)}
    both = ("T1", "T2") in edges and ("T2", "T1") in edges
    for a, b in sorted(edges):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        bend = (-55 if a == "T1" else 55) if both else 0
        col, mk = (S2, "pc") if cyc else (INK, "pa")
        sx, ex = (x1 + 46, x2 - 50) if x1 < x2 else (x1 - 46, x2 + 50)
        out.append(f'<path d="M{sx},{y1} Q{(x1 + x2) / 2:.0f},{y1 + bend * 1.6:.0f} {ex},{y2}" fill="none" stroke="{col}" stroke-width="3.5" marker-end="url(#{mk})"/>')
        if labels and (a, b) in labels:
            out.append(text((x1 + x2) / 2, y1 + bend * 0.8 + (-10 if bend <= 0 else 26), labels[(a, b)], 20))
    for n, (x, y) in pos.items():
        out.append(f'<circle cx="{x}" cy="{y}" r="44" fill="#dbeafe" stroke="{S1}" stroke-width="3"/>' + text(x, y + 9, n, 28, weight="bold"))
    out.append(text(W / 2, H - 14, title, 20, MUTED))
    return "".join(out) + "</svg>"


# ───────── L16: đồ thị bạn bè ─────────
FRIENDS = [("An", "Bình"), ("An", "Chi"), ("Bình", "Dũng"), ("Chi", "Dũng"), ("Chi", "Em"), ("Dũng", "Giang")]


def friends():
    """An (đậm), bạn trực tiếp (xanh), bạn của bạn (cam) — tính từ danh sách cạnh, không gán tay."""
    adj = {}
    for x, y in FRIENDS:
        adj.setdefault(x, set()).add(y)
        adj.setdefault(y, set()).add(x)
    direct = adj["An"]
    fof = {z for y in direct for z in adj[y]} - direct - {"An"}
    pos = {"An": (110, 190), "Bình": (330, 90), "Chi": (330, 290), "Dũng": (560, 150), "Em": (560, 320), "Giang": (790, 150)}
    W, H = 900, 400
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    for x, y in FRIENDS:
        (x1, y1), (x2, y2) = pos[x], pos[y]
        out.append(line(x1, y1, x2, y2, MUTED, 3))
    for n, (x, y) in pos.items():
        fill, st = ("#1f2937", INK) if n == "An" else (("#dbeafe", S1) if n in direct else (("#ffedd5", S2) if n in fof else ("#ffffff", MUTED)))
        out.append(f'<circle cx="{x}" cy="{y}" r="46" fill="{fill}" stroke="{st}" stroke-width="3.5"/>')
        out.append(text(x, y + 8, n, 22, "#ffffff" if n == "An" else INK, weight="bold") if n != "An" else
                   f'<text x="{x}" y="{y + 8}" font-size="22" fill="#ffffff" text-anchor="middle" font-weight="bold">An</text>')
    out.append(text(20, 385, "xanh: bạn trực tiếp của An;  cam: bạn của bạn (chưa là bạn)", 19, MUTED, anchor="start"))
    return "".join(out) + "</svg>"


def save(name, svg):
    (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")
    print("→", name)


if __name__ == "__main__":
    save("er", er_full())
    save("bplus", bplus())
    save("bplus45", bplus(search=45))
    save("bplus_rng", bplus(rng=(35, 65)))
    save("prec_cycle", prec([("T1", "R", "A"), ("T2", "W", "A"), ("T2", "R", "B"), ("T1", "W", "B")], "có chu trình: không tuần tự hoá được", {("T1", "T2"): "vì A: R1 trước W2", ("T2", "T1"): "vì B: R2 trước W1"}))
    save("friends", friends())
    save("prec_ok", prec([("T1", "R", "A"), ("T1", "W", "A"), ("T2", "R", "A"), ("T2", "W", "A"), ("T1", "R", "B"), ("T1", "W", "B"), ("T2", "R", "B"), ("T2", "W", "B")], "không chu trình: tương đương T1 rồi T2", {("T1", "T2"): "vì A và B"}))
