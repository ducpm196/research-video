"""Biểu đồ cửa sổ tắc nghẽn TCP theo vòng RTT cho NET L11 — số liệu từ alg.cwnd_trace (không vẽ tay).
Theo skill dataviz: một trục y; nét 3px, chấm ≥ 8px; lưới mờ; màu chuỗi theo thứ tự cố định của bảng mặc định
(xanh #2a78d6, cam #eb6834 — đã chạy validate_palette.js: ALL PASS, CVD ΔE 24,7); Tahoe thêm nét đứt (mã hoá phụ);
nhãn đặt trực tiếp ở cuối đường + chú thích phía trên; chữ dùng màu mực, không dùng màu chuỗi. Video là khung tĩnh nên không có lớp hover.
Chạy: .venv/Scripts/python audit/net/cwnd_svg.py → audit/net/fig/cwnd_*.svg"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg  # noqa: E402

S1, S2 = "#2a78d6", "#eb6834"
INK, MUTED, GRID = "#1f2937", "#6b7280", "#e5e7eb"


def chart(series, rounds, ymax, th_lines=(), notes=(), W=900, H=430, legend=True):
    """series: [(tên, giá trị theo vòng, màu, nét đứt?)]; th_lines: [(y, nhãn)] đường ngưỡng; notes: [(vòng, y, chữ)]."""
    L, Rm, T, B = 80, 120, 70, 60
    pw, ph = W - L - Rm, H - T - B
    X = lambda r: L + r * pw / (rounds - 1)
    Y = lambda v: T + ph - v * ph / ymax
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    for v in range(0, ymax + 1, 4):
        out.append(f'<line x1="{L}" y1="{Y(v):.0f}" x2="{L + pw}" y2="{Y(v):.0f}" stroke="{GRID}" stroke-width="1.5"/>')
        out.append(f'<text x="{L - 12}" y="{Y(v) + 7:.0f}" font-size="20" fill="{MUTED}" text-anchor="end">{v}</text>')
    for r in range(0, rounds, 2):
        out.append(f'<text x="{X(r):.0f}" y="{T + ph + 30}" font-size="20" fill="{MUTED}" text-anchor="middle">{r}</text>')
    out.append(f'<text x="{L + pw / 2:.0f}" y="{H - 4}" font-size="20" fill="{MUTED}" text-anchor="middle">vòng gửi (mỗi vòng một RTT)</text>')
    out.append(f'<text x="18" y="{T - 14}" font-size="20" fill="{MUTED}">cửa sổ (gói)</text>')
    for y, lab in th_lines:
        out.append(f'<line x1="{L}" y1="{Y(y):.0f}" x2="{L + pw}" y2="{Y(y):.0f}" stroke="{MUTED}" stroke-width="2" stroke-dasharray="4 6"/>')
        out.append(f'<text x="{L + 10}" y="{Y(y) - 8:.0f}" font-size="20" fill="{MUTED}" stroke="#fffbeb" stroke-width="6" paint-order="stroke">{lab}</text>')
    for name, vals, col, dashed in series:
        pts = " ".join(f"{X(r):.0f},{Y(v):.0f}" for r, v in enumerate(vals))
        dash = ' stroke-dasharray="10 7"' if dashed else ""
        out.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="3"{dash} stroke-linejoin="round"/>')
        for r, v in enumerate(vals):
            out.append(f'<circle cx="{X(r):.0f}" cy="{Y(v):.0f}" r="5" fill="{col}" stroke="#fffbeb" stroke-width="2"/>')
        r, v = len(vals) - 1, vals[-1]
        if len(series) >= 2:
            out.append(f'<text x="{X(r) + 12:.0f}" y="{Y(v) + 7:.0f}" font-size="22" font-weight="700" fill="{INK}">{name}</text>')
    for r, y, txt, anchor in notes:
        dx = {"start": 14, "end": -14, "middle": 0}[anchor]
        out.append(f'<text x="{X(r) + dx:.0f}" y="{Y(y) - 16:.0f}" font-size="20" fill="{INK}" text-anchor="{anchor}" font-weight="700" '
                   f'stroke="#fffbeb" stroke-width="6" paint-order="stroke">{txt}</text>')
    if legend and len(series) >= 2:
        x = L
        for name, _, col, dashed in series:
            dash = ' stroke-dasharray="10 7"' if dashed else ""
            out.append(f'<line x1="{x}" y1="22" x2="{x + 40}" y2="22" stroke="{col}" stroke-width="3"{dash}/>')
            out.append(f'<text x="{x + 50}" y="29" font-size="20" fill="{INK}">{name}</text>')
            x += 200
    out.append("</svg>")
    return "".join(out)


if __name__ == "__main__":
    fig = ROOT / "audit" / "net" / "fig"; fig.mkdir(parents=True, exist_ok=True)
    reno = alg.cwnd_trace(14, 16, loss_at=(8,))
    tahoe = alg.cwnd_trace(14, 16, loss_at=(8,), variant="tahoe")
    assert reno[:9] == [1, 2, 4, 8, 16, 17, 18, 19, 20] and reno[9] == 10 and tahoe[9] == 1
    F = {
        "cwnd_ss": chart([("cửa sổ", reno[:8], S1, False)], 8, 24, th_lines=[(16, "ngưỡng 16")], legend=False,
                         notes=[(3, 8, "nhân đôi", "end"), (5, 17, "+1 mỗi vòng", "end")], W=900, H=400),
        "cwnd_loss": chart([("Reno", reno, S1, False), ("Tahoe", tahoe, S2, True)], 14, 24,
                           th_lines=[(16, "ngưỡng 16"), (10, "ngưỡng mới 10")], notes=[(8, 20, "mất gói", "middle")]),
    }
    for k, v in F.items():
        (fig / f"{k}.svg").write_text(v, encoding="utf-8")
    print(len(F), "hình →", fig)
