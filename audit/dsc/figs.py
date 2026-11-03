"""Hình cho khoá DSC — biểu đồ cột trục cắt và trục từ 0 (bài 5), phân tán có ngoại lai (bài 6). Số liệu lấy từ checklib (alg.*).
Theo skill dataviz: một chuỗi một màu (xanh #2a78d6), không trục kép, lưới nhạt, chữ màu mực, nền #fffbeb; nhãn số đặt trực tiếp trên cột.
Chạy: .venv/Scripts/python audit/dsc/figs.py → audit/dsc/fig/*.svg (mỗi hình một dòng)."""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg  # noqa: E402

S1, S2 = "#2a78d6", "#eb6834"
INK, MUTED, GRID, BG = "#1f2937", "#6b7280", "#e5e7eb", "#fffbeb"
OUT = ROOT / "audit" / "dsc" / "fig"
OUT.mkdir(parents=True, exist_ok=True)


def text(x, y, t, size=20, col=INK, anchor="middle", weight="normal"):
    return f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" fill="{col}" text-anchor="{anchor}" font-weight="{weight}">{t}</text>'


def save(name, svg):
    (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")
    print("→", name)


def bars(x0, vals, labels, lo, hi, title, W=420, H=320, nt=4):
    """Một biểu đồ cột tại vị trí x0: trục y từ lo tới hi, vạch lưới và nhãn trục, nhãn số trên đầu cột."""
    L, T, B = 60, 50, 50
    ph = H - T - B
    Y = lambda v: T + ph - (v - lo) / (hi - lo) * ph  # noqa: E731
    out = [text(x0 + W / 2, 26, title, 20, INK, "middle", "bold")]
    for k in range(nt + 1):
        v = lo + (hi - lo) * k / nt
        out.append(f'<line x1="{x0 + L}" y1="{Y(v):.0f}" x2="{x0 + W - 20}" y2="{Y(v):.0f}" stroke="{GRID}" stroke-width="1.5"/>')
        out.append(text(x0 + L - 8, Y(v) + 6, f"{v:g}".replace(".", ","), 16, MUTED, "end"))
    bw = 90
    for i, (v, lab) in enumerate(zip(vals, labels)):
        cx = x0 + L + 70 + i * 150
        out.append(f'<rect x="{cx - bw / 2:.0f}" y="{Y(v):.0f}" width="{bw}" height="{Y(lo) - Y(v):.0f}" rx="4" fill="{S1}"/>')
        out.append(text(cx, Y(v) - 8, str(v), 18, INK, "middle", "bold"))
        out.append(text(cx, H - 18, lab, 18, MUTED))
    out.append(f'<line x1="{x0 + L}" y1="{Y(lo):.0f}" x2="{x0 + W - 20}" y2="{Y(lo):.0f}" stroke="{INK}" stroke-width="2"/>')
    return "".join(out)


def trunc_vs_zero():
    vals = [51, 52]
    return (f'<svg width="900" height="320" viewBox="0 0 900 320">'
            + bars(0, vals, ["A", "B"], 50, 52.5, "trục bắt đầu từ 50", nt=5)
            + bars(470, vals, ["A", "B"], 0, 60, "trục bắt đầu từ 0") + "</svg>")


def scatter_outlier():
    xs, ys = [1, 2, 3, 4, 5], [2, 4, 5, 4, 5]
    W, H, L, T, B, R = 900, 340, 70, 30, 50, 30
    X = lambda x: L + (x + 1) / 22 * (W - L - R)  # noqa: E731
    Y = lambda y: T + (H - T - B) - (y + 12) / 20 * (H - T - B)  # noqa: E731
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    for yv in (-10, -5, 0, 5):
        out.append(f'<line x1="{L}" y1="{Y(yv):.0f}" x2="{W - R}" y2="{Y(yv):.0f}" stroke="{GRID}" stroke-width="1.5"/>')
        out.append(text(L - 10, Y(yv) + 6, str(yv).replace("-", "−"), 16, MUTED, "end"))
    for xv in (0, 5, 10, 15, 20):
        out.append(text(X(xv), H - 18, str(xv), 16, MUTED))
    for x, y in zip(xs, ys):
        out.append(f'<circle cx="{X(x):.0f}" cy="{Y(y):.0f}" r="9" fill="{S1}"/>')
    out.append(f'<circle cx="{X(20):.0f}" cy="{Y(-10):.0f}" r="10" fill="#ffffff" stroke="{S2}" stroke-width="3.5"/>')
    out.append(text(X(20) - 18, Y(-10) - 4, "(20, −10)", 18, S2, "end", "bold"))
    r1 = alg.pearson(xs, ys)
    r2 = alg.pearson(xs + [20], ys + [-10])
    out.append(text(X(6.5), Y(6.5), f"5 điểm: r = {r1:.3f}".replace(".", ","), 19, S1, "start", "bold"))
    out.append(text(X(9), Y(-6), f"thêm 1 điểm: r = {r2:.3f}".replace(".", ",").replace("-", "−"), 19, S2, "start", "bold"))
    return "".join(out) + "</svg>"


if __name__ == "__main__":
    save("trunc_vs_zero", trunc_vs_zero())
    save("scatter_outlier", scatter_outlier())
