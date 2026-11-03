"""Hình cho khoá ESY — dạng sóng, bậc thang ADC, đáp ứng bộ lọc, biểu đồ Gantt lập lịch. Mọi số tính từ checklib (alg.*).
Màu theo bảng mặc định của skill dataviz (xanh #2a78d6, cam #eb6834 — đã kiểm validate_palette.js ở NET); chuỗi thứ hai thêm nét
đứt; chữ màu mực; nền #fffbeb. Video là khung tĩnh nên không có lớp hover.
Chạy: .venv/Scripts/python audit/esy/figs.py → audit/esy/fig/*.svg (mỗi hình một dòng)."""
import math
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg  # noqa: E402

S1, S2 = "#2a78d6", "#eb6834"
INK, MUTED, GRID, BG = "#1f2937", "#6b7280", "#e5e7eb", "#fffbeb"
OUT = ROOT / "audit" / "esy" / "fig"
OUT.mkdir(parents=True, exist_ok=True)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, t, size=20, col=INK, anchor="middle", weight="normal"):
    return (f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" fill="{col}" text-anchor="{anchor}" font-weight="{weight}" '
            f'stroke="{BG}" stroke-width="6" paint-order="stroke">{esc(t)}</text>')


def vn(x, d=2):
    s = f"{x:.{d}f}".rstrip("0").rstrip(".") if d else f"{x:.0f}"
    return s.replace(".", ",").replace("-", "−")


def save(name, svg):
    (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")
    print("→", name)


def digital(rows, n, W=980, rowh=70, L=170, title=None, marks=()):
    """Vẽ các tín hiệu số theo từng ô thời gian: rows = [(nhãn, dãy 0/1, màu, nét đứt?)]. marks: [(chỉ số ô, chữ)]."""
    cw = (W - L - 20) / n
    H = 30 + rowh * len(rows) + 50
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    for k in range(n + 1):
        out.append(f'<line x1="{L + k * cw:.1f}" y1="20" x2="{L + k * cw:.1f}" y2="{H - 40}" stroke="{GRID}" stroke-width="1"/>')
    for r, (lab, seq, col, dash) in enumerate(rows):
        y0 = 30 + r * rowh
        hi, lo = y0 + 10, y0 + rowh - 20
        pts = []
        for k, v in enumerate(seq):
            y = hi if v else lo
            pts += [(L + k * cw, y), (L + (k + 1) * cw, y)]
        d = f' stroke-dasharray="{dash}"' if dash else ""
        out.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{col}" stroke-width="3.5"{d}/>')
        out.append(text(L - 14, (hi + lo) / 2 + 7, lab, 20, INK, "end"))
    for k, lab in marks:
        out.append(text(L + (k + 0.5) * cw, H - 14, lab, 18, MUTED))
    return "".join(out) + "</svg>"


def debounce_fig():
    raw = [0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    deb = alg.debounce(raw, 5)
    marks = [(k, f"{k}") for k in range(len(raw))]
    return digital([("chân phím", raw, S2, "10 6"), ("sau chống dội", deb, S1, None)], len(raw), marks=marks)


def pwm_fig():
    """Bộ đếm 0..TOP (vẽ thu nhỏ TOP = 9), chân ra mức cao khi bộ đếm < CMP — CMP = 3: 30%; CMP = 7: 70%."""
    W, H = 980, 330
    L = 170
    top = 9
    per = top + 1
    n = 3 * per
    cw = (W - L - 20) / n
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    # răng cưa bộ đếm
    pts = []
    for k in range(n):
        c = k % per
        x = L + k * cw
        y = 110 - c * 8
        pts.append((x, y))
        if c == top:
            pts.append((x + cw, 110 - (c + 1) * 8))
            pts.append((x + cw, 110))
    out.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{MUTED}" stroke-width="2.5"/>')
    out.append(f'<line x1="{L}" y1="{110 - 3 * 8}" x2="{W - 20}" y2="{110 - 3 * 8}" stroke="{S2}" stroke-width="2" stroke-dasharray="6 6"/>')
    out.append(text(L - 14, 70, "bộ đếm", 20, INK, "end"))
    out.append(text(W - 24, 110 - 3 * 8 - 8, "so sánh = 3", 18, MUTED, "end"))
    for r, (cmp_, col, lab) in enumerate(((3, S1, "ra, so sánh 3"), (7, S2, "ra, so sánh 7"))):
        y_hi, y_lo = 150 + r * 85, 150 + r * 85 + 50
        seq = [1 if (k % per) < cmp_ else 0 for k in range(n)]
        p = []
        for k, v in enumerate(seq):
            y = y_hi if v else y_lo
            p += [(L + k * cw, y), (L + (k + 1) * cw, y)]
        out.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in p)}" fill="none" stroke="{col}" stroke-width="3.5"/>')
        out.append(text(L - 14, y_hi + 32, lab, 20, INK, "end"))
        out.append(text(L + per * cw * 2.5, y_hi - 6, f"mức cao {cmp_}/{per} = {cmp_ * 10}%", 18, MUTED))
    return "".join(out) + "</svg>"


def adc_fig():
    """Bậc thang lượng tử ADC 3 bit trên 0–3,3 V (vẽ thu nhỏ để thấy bậc): mã = ⌊V · 2^bits / Vref⌋."""
    W, H = 900, 420
    L, B, T, R = 90, 60, 30, 30
    pw, ph = W - L - R, H - T - B
    X = lambda v: L + v / 3.3 * pw  # noqa: E731
    Y = lambda c: T + ph - c / 8 * ph  # noqa: E731
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    for c in range(9):
        out.append(f'<line x1="{L}" y1="{Y(c):.0f}" x2="{L + pw}" y2="{Y(c):.0f}" stroke="{GRID}" stroke-width="1.5"/>')
        if c < 8:
            out.append(text(L - 12, Y(c) + 7, str(c), 18, MUTED, "end"))
    pts = []
    for k in range(400):
        v = 3.3 * k / 400
        c = min(7, int(v * 8 / 3.3))
        pts.append((X(v), Y(c)))
    out.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{S1}" stroke-width="3.5"/>')
    out.append(f'<line x1="{X(0)}" y1="{Y(0)}" x2="{X(3.3)}" y2="{Y(8)}" stroke="{MUTED}" stroke-width="2" stroke-dasharray="6 6"/>')
    for v in (0, 1.1, 2.2, 3.3):
        out.append(text(X(v), H - 32, vn(v, 1) + " V", 18, MUTED))
    out.append(text(L + pw, H - 6, "điện áp vào", 18, MUTED, "end"))
    out.append(text(L - 60, T - 8, "mã ra", 18, MUTED, "start"))
    out.append(f'<text x="{X(0.12):.0f}" y="{Y(6.4):.0f}" font-size="19" fill="{INK}" text-anchor="start">mỗi bậc = V<tspan baseline-shift="sub" font-size="14">ref</tspan> / 2³ ≈ 0,41 V</text>')
    return "".join(out) + "</svg>"


def ema_fig():
    W, H = 900, 400
    L, B, T, R = 80, 60, 30, 40
    pw, ph = W - L - R, H - T - B
    n = 20
    X = lambda k: L + k / n * pw  # noqa: E731
    Y = lambda y: T + ph - y * ph  # noqa: E731
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    for v in (0, 0.25, 0.5, 0.75, 1.0):
        out.append(f'<line x1="{L}" y1="{Y(v):.0f}" x2="{L + pw}" y2="{Y(v):.0f}" stroke="{GRID}" stroke-width="1.5"/>')
        out.append(text(L - 12, Y(v) + 7, vn(v), 18, MUTED, "end"))
    out.append(f'<polyline points="{X(0)},{Y(0)} {X(0)},{Y(1)} {X(n)},{Y(1)}" fill="none" stroke="{MUTED}" stroke-width="2.5" stroke-dasharray="6 6"/>')
    ys, y = [0.0], 0.0
    for _ in range(n):
        y = alg.ema_step(y, 1, 0.2)
        ys.append(y)
    out.append(f'<polyline points="{" ".join(f"{X(k):.1f},{Y(v):.1f}" for k, v in enumerate(ys))}" fill="none" stroke="{S1}" stroke-width="3"/>')
    for k, v in enumerate(ys):
        out.append(f'<circle cx="{X(k):.1f}" cy="{Y(v):.1f}" r="5" fill="{S1}"/>')
    out.append(text(X(10.6), Y(0.62), f"sau 10 mẫu: {vn(ys[10], 4)}", 20, INK, "start"))
    out.append(f'<line x1="{X(10):.1f}" y1="{Y(ys[10]) + 8:.1f}" x2="{X(10.6):.1f}" y2="{Y(0.62) - 18:.1f}" stroke="{MUTED}" stroke-width="1.5"/>')
    out.append(text(X(n), Y(1) - 10, "đầu vào nhảy lên 1", 18, MUTED, "end"))
    for k in range(0, n + 1, 5):
        out.append(text(X(k), H - 32, str(k), 18, MUTED))
    out.append(text(L + pw, H - 6, "mẫu thứ k", 18, MUTED, "end"))
    return "".join(out) + "</svg>"


def gantt(tasks, horizon, policy, labels=("A", "B", "C")):
    """Biểu đồ Gantt từ alg.schedule_sim: mỗi tác vụ một hàng, ô tô màu khi tác vụ chạy; mũi tên đỏ ở chỗ trễ hạn."""
    tl, misses = alg.schedule_sim(tasks, horizon, policy)
    W = 980
    L = 110
    cw = (W - L - 20) / horizon
    rowh = 56
    H = 30 + rowh * len(tasks) + 84
    cols = [S1, S2, "#7c3aed"]
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    for k in range(horizon + 1):
        out.append(f'<line x1="{L + k * cw:.1f}" y1="24" x2="{L + k * cw:.1f}" y2="{H - 66}" stroke="{GRID}" stroke-width="1"/>')
        if k % 2 == 0:
            out.append(text(L + k * cw, H - 44, str(k), 17, MUTED))
    for i, (c, p) in enumerate(tasks):
        y = 30 + i * rowh
        out.append(text(L - 14, y + 32, f"{labels[i]} ({c}, {p})", 19, INK, "end"))
        for k in range(0, horizon + 1, p):
            out.append(f'<line x1="{L + k * cw:.1f}" y1="{y - 2}" x2="{L + k * cw:.1f}" y2="{y + 44}" stroke="{INK}" stroke-width="2"/>')
        for k, who in enumerate(tl):
            if who == i:
                out.append(f'<rect x="{L + k * cw + 1:.1f}" y="{y + 6}" width="{cw - 2:.1f}" height="34" rx="3" fill="{cols[i]}"/>')
    for i, t in misses:
        y = 30 + i * rowh
        out.append(f'<text x="{L + t * cw - 8:.1f}" y="{y + 30}" font-size="19" fill="#dc2626" text-anchor="end" font-weight="bold">trễ hạn</text>')
    out.append(text(W - 20, H - 4, "vạch đen: thời điểm thả việc mới = hạn của việc trước", 17, MUTED, "end"))
    return "".join(out) + "</svg>"


def current_fig():
    """Dòng điện theo thời gian chu kỳ thức–ngủ (vẽ phóng to tỉ lệ thức để nhìn thấy)."""
    W, H = 900, 300
    L, T = 100, 30
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    per, on = 200, 12
    pts = []
    for k in range(3):
        x0 = L + k * per
        pts += [(x0, 60), (x0 + on, 60), (x0 + on, 230), (x0 + per, 230)]
    out.append(f'<polyline points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="none" stroke="{S1}" stroke-width="3.5"/>')
    out.append(text(L - 12, 66, "10 mA", 18, MUTED, "end"))
    out.append(text(L - 12, 236, "10 µA", 18, MUTED, "end"))
    out.append(text(L + 3 * per, 30, "thức 1% thời gian, ngủ 99% (tỉ lệ vẽ phóng to)", 19, INK, "end"))
    out.append(text(L + 3 * per, 280, "thời gian", 18, MUTED, "end"))
    return "".join(out) + "</svg>"


if __name__ == "__main__":
    save("debounce", debounce_fig())
    save("pwm", pwm_fig())
    save("adc", adc_fig())
    save("ema", ema_fig())
    save("rm_ok", gantt([(1, 4), (1, 5), (2, 10)], 20, "RM"))
    save("rm_rta", gantt([(1, 4), (2, 6), (3, 12)], 12, "RM"))
    save("rm_miss", gantt([(2, 4), (3, 6)], 12, "RM"))
    save("edf_ok", gantt([(2, 4), (3, 6)], 12, "EDF"))
    save("sleep", current_fig())
