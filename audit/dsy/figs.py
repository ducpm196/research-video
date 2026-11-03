"""Hình cho khoá DSY — sơ đồ không–thời gian (đồng hồ Lamport, vector), vòng băm nhất quán, cửa sổ thời gian. Nhãn tính từ checklib (alg.*).
Màu theo bảng mặc định của skill dataviz (xanh #2a78d6, cam #eb6834; chuỗi thứ hai nét đứt); chữ màu mực; nền #fffbeb. Khung tĩnh, không hover.
Chạy: .venv/Scripts/python audit/dsy/figs.py → audit/dsy/fig/*.svg (mỗi hình một dòng)."""
import math
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg  # noqa: E402

S1, S2 = "#2a78d6", "#eb6834"
INK, MUTED, GRID, BG = "#1f2937", "#6b7280", "#e5e7eb", "#fffbeb"
OUT = ROOT / "audit" / "dsy" / "fig"
OUT.mkdir(parents=True, exist_ok=True)
ARROW = (f'<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" '
         f'orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{S2}"/></marker></defs>')


def text(x, y, t, size=20, col=INK, anchor="middle", weight="normal"):
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" fill="{col}" text-anchor="{anchor}" font-weight="{weight}" '
            f'stroke="{BG}" stroke-width="5" paint-order="stroke">{t}</text>')


def save(name, svg):
    (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")
    print("→", name)


def spacetime(procs, events, labels, W=980, rowh=120, cols=None):
    """Mỗi tiến trình một đường ngang; sự kiện thứ j đặt ở cột cols[j] (mặc định j). Mũi tên cam nét đứt từ gửi tới nhận. labels[j] in trên chấm."""
    cols = cols or list(range(len(events)))
    ncol = max(cols) + 1
    L = 90
    X = lambda c: L + 50 + c * (W - L - 100) / max(1, ncol - 1)  # noqa: E731
    Y = {p: 50 + i * rowh for i, p in enumerate(procs)}
    H = 50 + rowh * (len(procs) - 1) + 50
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">', ARROW]
    for p in procs:
        out.append(f'<line x1="{L}" y1="{Y[p]}" x2="{W - 20}" y2="{Y[p]}" stroke="{INK}" stroke-width="2.5"/>')
        out.append(text(L - 14, Y[p] + 7, p, 22, INK, "end", "bold"))
    send_at = {}
    for j, (p, kind, msg) in enumerate(events):
        if kind == "send":
            send_at[msg] = (X(cols[j]), Y[p])
    for j, (p, kind, msg) in enumerate(events):
        if kind == "recv":
            x1, y1 = send_at[msg]
            x2, y2 = X(cols[j]), Y[p]
            dy = 14 if y2 > y1 else -14
            out.append(f'<line x1="{x1:.0f}" y1="{y1 + dy:.0f}" x2="{x2:.0f}" y2="{y2 - dy:.0f}" stroke="{S2}" stroke-width="2.5" '
                       f'stroke-dasharray="8 6" marker-end="url(#ar)"/>')
    for j, (p, kind, msg) in enumerate(events):
        x, y = X(cols[j]), Y[p]
        out.append(f'<circle cx="{x:.0f}" cy="{y}" r="11" fill="{S1}"/>')
        out.append(text(x, y - 22, labels[j], 20, INK, "middle", "bold"))
    return "".join(out) + "</svg>"


LAMPORT_EV = [("P1", "local", None), ("P1", "send", "m1"), ("P2", "local", None), ("P2", "recv", "m1"), ("P2", "send", "m2"),
              ("P3", "recv", "m2"), ("P3", "local", None)]
VECTOR_EV = [("P1", "send", "m2"), ("P3", "send", "m"), ("P2", "local", None), ("P2", "recv", "m2"), ("P1", "recv", "m")]


def ring_fig(nodes=4, keys=(24, 36, 12, 7)):
    """Vòng băm minh hoạ: nút và khoá đặt theo vị trí băm (rút về 0..1), khoá thuộc nút đầu tiên theo chiều kim đồng hồ."""
    W, H, cx, cy, r = 900, 540, 320, 270, 200
    pos = lambda v: (cx + r * math.sin(2 * math.pi * v), cy - r * math.cos(2 * math.pi * v))  # noqa: E731
    npos = sorted((alg._h(f"nút{n}") % 1000 / 1000, f"N{n}") for n in range(nodes))
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{MUTED}" stroke-width="3"/>')
    for v, name in npos:
        x, y = pos(v)
        out.append(f'<rect x="{x - 26:.0f}" y="{y - 18:.0f}" width="52" height="36" rx="8" fill="{S1}"/>')
        out.append(text(x, y + 7, name, 20, "#ffffff", "middle", "bold").replace(f'stroke="{BG}"', 'stroke="none"'))
    for k in keys:
        v = alg._h(f"khoá{k}") % 1000 / 1000
        own = next((n for nv, n in npos if nv >= v), npos[0][1])
        x, y = pos(v)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="{S2}"/>')
        lx, ly = cx + (r + 46) * math.sin(2 * math.pi * v), cy - (r + 46) * math.cos(2 * math.pi * v)
        out.append(text(lx, ly + 6, f"k{k} → {own}", 18, INK))
    out.append(text(600, 230, "khoá thuộc nút đầu tiên", 20, MUTED, "start"))
    out.append(text(600, 260, "đi theo chiều kim đồng hồ", 20, MUTED, "start"))
    return "".join(out) + "</svg>"


def window_fig(times=(1, 2, 3, 7, 8, 12), size=5, horizon=15):
    """Trục thời gian, sự kiện là chấm, cửa sổ nhảy là các khối nền xen màu, số đếm mỗi cửa sổ phía trên."""
    W, H, L, R = 900, 200, 50, 30
    X = lambda t: L + t * (W - L - R) / horizon  # noqa: E731
    cnt = alg.tumbling(list(times), size)
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    for k in range(horizon // size):
        out.append(f'<rect x="{X(k * size):.0f}" y="40" width="{X(size) - X(0):.0f}" height="90" fill="{"#dbeafe" if k % 2 == 0 else "#fde4d4"}"/>')
        out.append(text((X(k * size) + X((k + 1) * size)) / 2, 30, f"[{k * size}, {(k + 1) * size}): {cnt.get(k, 0)} sự kiện", 19, INK, "middle", "bold"))
    out.append(f'<line x1="{L}" y1="130" x2="{W - R}" y2="130" stroke="{INK}" stroke-width="2"/>')
    for t in range(0, horizon + 1):
        out.append(f'<line x1="{X(t):.0f}" y1="130" x2="{X(t):.0f}" y2="137" stroke="{INK}" stroke-width="1.5"/>')
        if t % 5 == 0 or t in times:
            out.append(text(X(t), 160, str(t), 17, MUTED))
    for t in times:
        out.append(f'<circle cx="{X(t):.0f}" cy="95" r="10" fill="{S1}"/>')
    out.append(text(W - R, 190, "giây (thời gian sự kiện)", 17, MUTED, "end"))
    return "".join(out) + "</svg>"


if __name__ == "__main__":
    lam = alg.lamport_run(LAMPORT_EV)
    save("lamport", spacetime(["P1", "P2", "P3"], LAMPORT_EV, [str(c) for c in lam], cols=[0, 1, 0, 2, 3, 4, 5]))
    vec = alg.vector_run(VECTOR_EV, ["P1", "P2", "P3"])
    save("vector", spacetime(["P1", "P2", "P3"], VECTOR_EV, ["(" + ",".join(map(str, v)) + ")" for v in vec], cols=[0, 0, 0, 2, 2]))
    save("ring", ring_fig())
    save("windows", window_fig())
