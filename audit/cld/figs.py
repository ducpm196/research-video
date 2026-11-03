"""Hình cho khoá CLD — đường cong độ trễ M/M/1 (bài 10), xếp Pod vào nút (bài 6), tải các máy khi cân bằng (bài 9). Số liệu lấy từ checklib (alg.*).
Theo skill dataviz: một chuỗi một màu (xanh #2a78d6; chuỗi thứ hai cam #eb6834 nét đứt), không trục kép, lưới nhạt, chữ màu mực, nền #fffbeb.
Chạy: .venv/Scripts/python audit/cld/figs.py → audit/cld/fig/*.svg (mỗi hình một dòng)."""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg  # noqa: E402

S1, S2 = "#2a78d6", "#eb6834"
INK, MUTED, GRID, BG = "#1f2937", "#6b7280", "#e5e7eb", "#fffbeb"
OUT = ROOT / "audit" / "cld" / "fig"
OUT.mkdir(parents=True, exist_ok=True)


def text(x, y, t, size=20, col=INK, anchor="middle", weight="normal"):
    return f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" fill="{col}" text-anchor="{anchor}" font-weight="{weight}">{t}</text>'


def save(name, svg):
    (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")
    print("→", name)


def latency_curve():
    """W = 1/(μ − λ) với μ = 100 yêu cầu/s, λ từ 0 tới 97; đánh dấu λ = 50, 80, 95."""
    W, H, L, T, B, R = 900, 380, 80, 50, 60, 40
    xmax, ymax = 100, 300
    X = lambda x: L + x / xmax * (W - L - R)  # noqa: E731
    Y = lambda y: T + (H - T - B) - min(y, ymax) / ymax * (H - T - B)  # noqa: E731
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    for yv in (0, 100, 200, 300):
        out.append(f'<line x1="{L}" y1="{Y(yv):.0f}" x2="{W - R}" y2="{Y(yv):.0f}" stroke="{GRID}" stroke-width="1.5"/>')
        out.append(text(L - 10, Y(yv) + 6, str(yv), 16, MUTED, "end"))
    for xv in (0, 20, 40, 60, 80, 100):
        out.append(text(X(xv), H - 30, str(xv), 16, MUTED))
    out.append(text((L + W - R) / 2, H - 6, "tải đến (yêu cầu/giây), công suất 100 yêu cầu/giây", 17, MUTED))
    out.append(text(L - 60, T - 26, "độ trễ (ms)", 16, MUTED, "start"))
    pts = []
    lam = 0.0
    while lam <= 97.01:
        w = alg.mm1(lam, 100)[0] * 1000
        pts.append(f"{X(lam):.1f},{Y(w):.1f}")
        lam += 0.5
    out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{S1}" stroke-width="3"/>')
    out.append(f'<line x1="{X(100):.0f}" y1="{T}" x2="{X(100):.0f}" y2="{Y(0):.0f}" stroke="{S2}" stroke-width="2.5" stroke-dasharray="8 6"/>')
    out.append(text(X(100) - 8, T + 18, "công suất", 16, S2, "end", "bold"))
    for lam, dx, anchor in ((50, 0, "middle"), (80, -14, "end"), (95, -14, "end")):
        w = alg.mm1(lam, 100)[0] * 1000
        out.append(f'<circle cx="{X(lam):.0f}" cy="{Y(w):.0f}" r="8" fill="{S1}" stroke="{BG}" stroke-width="2"/>')
        out.append(text(X(lam) + dx, Y(w) - 16, f"{lam}/s → {w:.0f} ms", 18, INK, anchor, "bold"))
    out.append(f'<line x1="{L}" y1="{Y(0):.0f}" x2="{W - R}" y2="{Y(0):.0f}" stroke="{INK}" stroke-width="2"/>')
    return "".join(out) + "</svg>"


def binpack():
    """Nút 4 CPU, Pod yêu cầu 1,5 CPU: 2 Pod vừa, 1 CPU thừa không đủ cho Pod thứ ba."""
    W, H = 900, 290
    k, rest = alg.pods_fit(4, 1.5)
    x0, y0, unit, h = 90, 70, 170, 90
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    out.append(text(x0, 40, "nút: 4 CPU", 20, INK, "start", "bold"))
    out.append(f'<rect x="{x0}" y="{y0}" width="{4 * unit}" height="{h}" rx="6" fill="none" stroke="{INK}" stroke-width="2.5"/>')
    for i in range(k):
        x = x0 + i * 1.5 * unit
        out.append(f'<rect x="{x + 3:.0f}" y="{y0 + 3}" width="{1.5 * unit - 6:.0f}" height="{h - 6}" rx="4" fill="{S1}"/>')
        out.append(text(x + 0.75 * unit, y0 + h / 2 + 8, f"Pod {i + 1}: 1,5", 20, "#ffffff", "middle", "bold"))
    xr = x0 + k * 1.5 * unit
    out.append(f'<rect x="{xr + 3:.0f}" y="{y0 + 3}" width="{rest * unit - 6:.0f}" height="{h - 6}" rx="4" fill="none" stroke="{S2}" stroke-width="2.5" stroke-dasharray="8 6"/>')
    out.append(text(xr + rest * unit / 2, y0 + h / 2 + 8, f"thừa {rest:g}".replace(".", ","), 20, S2, "middle", "bold"))
    for c in range(5):
        out.append(text(x0 + c * unit, y0 + h + 30, str(c), 16, MUTED))
    out.append(text(x0 + 2 * unit, y0 + h + 72, "Pod 3 cần 1,5 CPU → không vừa phần thừa 1 CPU", 18, MUTED, "middle"))
    return "".join(out) + "</svg>"


def lb_loads():
    """Tải lớn nhất trong 100 máy, 20 000 yêu cầu (trung bình 200): chọn 1 máy ngẫu nhiên và chọn ít tải hơn trong 2."""
    W, H, L, T, B = 900, 340, 70, 50, 60
    m1, m2 = alg.lb_max_load(1), alg.lb_max_load(2)
    lo, hi = 0, 260
    Yv = lambda v: T + (H - T - B) - (v - lo) / (hi - lo) * (H - T - B)  # noqa: E731
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    for v in (0, 50, 100, 150, 200, 250):
        out.append(f'<line x1="{L}" y1="{Yv(v):.0f}" x2="{W - 30}" y2="{Yv(v):.0f}" stroke="{GRID}" stroke-width="1.5"/>')
        out.append(text(L - 10, Yv(v) + 6, str(v), 16, MUTED, "end"))
    out.append(f'<line x1="{L}" y1="{Yv(200):.0f}" x2="{W - 30}" y2="{Yv(200):.0f}" stroke="{S2}" stroke-width="2.5" stroke-dasharray="8 6"/>')
    out.append(text(W - 34, Yv(200) - 8, "trung bình 200", 16, S2, "end", "bold"))
    for i, (v, lab) in enumerate(((m1, "chọn 1 máy ngẫu nhiên"), (m2, "ít tải hơn trong 2 máy"))):
        cx = L + 200 + i * 360
        out.append(f'<rect x="{cx - 60}" y="{Yv(v):.0f}" width="120" height="{Yv(lo) - Yv(v):.0f}" rx="4" fill="{S1}"/>')
        out.append(text(cx, Yv(v) - 10, f"máy tải nhất: {v}", 19, INK, "middle", "bold"))
        out.append(text(cx, H - 22, lab, 18, MUTED))
    out.append(text(L - 50, T - 26, "yêu cầu", 16, MUTED, "start"))
    out.append(f'<line x1="{L}" y1="{Yv(lo):.0f}" x2="{W - 30}" y2="{Yv(lo):.0f}" stroke="{INK}" stroke-width="2"/>')
    return "".join(out) + "</svg>"


if __name__ == "__main__":
    save("latency_curve", latency_curve())
    save("binpack", binpack())
    save("lb_loads", lb_loads())
