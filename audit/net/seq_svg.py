"""Sơ đồ thời gian–không gian cho khoá NET — sinh SVG từ số liệu (không vẽ tay). Mỗi bên là một trục dọc, thời gian chạy xuống;
một gói tin là một DẢI từ trục gửi sang trục nhận: cạnh trên là bit đầu, cạnh dưới là bit cuối. Độ dày dải = trễ truyền,
độ nghiêng = trễ lan truyền. Mũi tên mảnh = gói rất ngắn (ACK, SYN). Kiểm: toạ độ y suy ra từ thời gian theo một tỉ lệ duy nhất.
Chạy: .venv/Scripts/python audit/net/seq_svg.py → audit/net/fig/*.svg (một dòng mỗi tệp, dùng với audit/cs112/fill_tpl.py)."""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg  # noqa: E402

INK, BLUE, ORANGE, GREEN, RED = "#374151", "#2563eb", "#d97706", "#059669", "#dc2626"
HALO = "#fffbeb"  # màu nền khối nội dung của player


def frame(cols, W, H, top=60, mid="s"):
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           f'<defs><marker id="{mid}" markerUnits="userSpaceOnUse" markerWidth="18" markerHeight="18" refX="16" refY="9" orient="auto">'
           f'<path d="M0,0 L18,9 L0,18 z" fill="{INK}"/></marker></defs>']
    for name, x in cols:
        out.append(f'<text x="{x}" y="{top - 22}" font-size="28" font-weight="700" text-anchor="middle">{name}</text>')
        out.append(f'<line x1="{x}" y1="{top}" x2="{x}" y2="{H - 20}" stroke="#9ca3af" stroke-width="4"/>')
    return out


def arrow(out, x1, y1, x2, y2, label, mid, col=INK, side="above", size=24, at=None):
    out.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{col}" stroke-width="3.5" marker-end="url(#{mid})"/>')
    lx, ly = at or ((x1 + x2) / 2, (min(y1, y2) - 12 if side == "above" else max(y1, y2) + 30))
    out.append(f'<text x="{lx:.0f}" y="{ly:.0f}" font-size="{size}" font-weight="700" fill="{col}" text-anchor="middle" '
               f'stroke="{HALO}" stroke-width="7" paint-order="stroke" stroke-linejoin="round">{label}</text>')


def band(out, x1, x2, y_send0, y_send1, y_recv0, y_recv1, col=BLUE):
    out.append(f'<polygon points="{x1},{y_send0:.0f} {x2},{y_recv0:.0f} {x2},{y_recv1:.0f} {x1},{y_send1:.0f}" fill="{col}" fill-opacity="0.25" '
               f'stroke="{col}" stroke-width="3"/>')


def brace(out, x, y0, y1, label, right=True, col=ORANGE):
    """Dấu ngoặc đo một khoảng thời gian dọc trục."""
    d = 14 if right else -14
    out.append(f'<path d="M{x},{y0:.0f} h{d} V{y1:.0f} h{-d}" fill="none" stroke="{col}" stroke-width="3"/>')
    tx = x + (d * 1.6)
    anchor = "start" if right else "end"
    out.append(f'<text x="{tx:.0f}" y="{(y0 + y1) / 2 + 9:.0f}" font-size="24" font-weight="700" fill="{col}" text-anchor="{anchor}">{label}</text>')


def delays(T, P, W=900, H=430, scale=None):
    """L01: một gói từ A sang B. T = trễ truyền, P = trễ lan truyền (cùng đơn vị). Trục thời gian vẽ theo một tỉ lệ."""
    top, xa, xb = 70, 250, 650
    s = scale or (H - top - 40) / (T + P)
    out = frame([("A (gửi)", xa), ("B (nhận)", xb)], W, H, top, "d")
    band(out, xa, xb, top, top + T * s, top + P * s, top + (P + T) * s)
    brace(out, xa - 30, top, top + T * s, "trễ truyền", right=False)
    brace(out, xb + 30, top, top + P * s, "trễ lan truyền", right=True, col=GREEN)
    brace(out, xb + 30, top + P * s, top + (P + T) * s, "trễ truyền", right=True)
    out.append(f'<text x="{(xa + xb) / 2 + 40:.0f}" y="{top + (P / 2) * s - 16:.0f}" font-size="22" fill="{BLUE}" text-anchor="start" font-weight="700" '
               f'stroke="{HALO}" stroke-width="7" paint-order="stroke">gói tin</text>')
    out.append("</svg>")
    return "".join(out)


def handshake(x=100, y=300, W=900, H=440):
    """L09: bắt tay ba bước giữa khách và máy chủ, số thứ tự ghi trên mũi tên."""
    top, xa, xb = 70, 230, 670
    out = frame([("khách", xa), ("máy chủ", xb)], W, H, top, "h")
    g = 110
    arrow(out, xa, top + 20, xb, top + 20 + 70, f"SYN, seq = {x}", "h")
    arrow(out, xb, top + 20 + g, xa, top + 20 + g + 70, f"SYN-ACK, seq = {y}, ack = {x + 1}", "h")
    arrow(out, xa, top + 20 + 2 * g, xb, top + 20 + 2 * g + 70, f"ACK, ack = {y + 1}", "h")
    out.append(f'<text x="{xa + 16}" y="{top + 20 + 2 * g + 118}" font-size="22" fill="{GREEN}" text-anchor="start" font-weight="700">khách bắt đầu gửi dữ liệu</text>')
    out.append("</svg>")
    return "".join(out)


def stop_wait(t_ratio=0.12, W=900, H=460):
    """L10: dừng–chờ. Gói (dải mỏng) đi, ACK quay về; khoảng chờ dài trên trục gửi. t_ratio = trễ truyền / RTT (để vẽ thấy được)."""
    top, xa, xb = 70, 250, 650
    rtt_px = H - top - 120
    T = rtt_px * t_ratio
    half = rtt_px / 2
    out = frame([("gửi", xa), ("nhận", xb)], W, H, top, "w")
    band(out, xa, xb, top, top + T, top + half, top + half + T)
    # nhãn đặt cạnh giữa mũi tên (480, 280): đặt dưới đầu mũi tên thì đè dòng chú thích “ACK về…” (kiểm chữ đè trong SVG, 2026-10-31)
    arrow(out, xb, top + half + T, xa, top + 2 * half + T, "ACK", "w", col=GREEN, at=(480, 280))
    brace(out, xa - 30, top, top + T, "phát gói", right=False)
    brace(out, xa - 30, top + T, top + 2 * half + T, "ngồi chờ", right=False, col=RED)
    out.append(f'<text x="{xa + 16}" y="{top + 2 * half + T + 40:.0f}" font-size="22" fill="{INK}" font-weight="700">ACK về: gói kế tiếp mới được đi</text>')
    out.append("</svg>")
    return "".join(out)


def dns_iter(W=1100, H=560):
    """L12: phân giải lặp. Máy phân giải cục bộ hỏi lần lượt máy chủ gốc, TLD, có thẩm quyền; mũi tên đánh số."""
    top = 70
    cols = [("máy bạn", 90), ("phân giải cục bộ", 330), ("gốc", 590), ("TLD .vn", 790), ("thẩm quyền", 990)]
    out = frame(cols, W, H, top, "q")
    X = dict((n, x) for n, x in cols)
    y = top + 20
    steps = [("máy bạn", "phân giải cục bộ", "1"), ("phân giải cục bộ", "gốc", "2"), ("gốc", "phân giải cục bộ", "3: hỏi .vn"),
             ("phân giải cục bộ", "TLD .vn", "4"), ("TLD .vn", "phân giải cục bộ", "5: hỏi thẩm quyền"),
             ("phân giải cục bộ", "thẩm quyền", "6"), ("thẩm quyền", "phân giải cục bộ", "7: địa chỉ IP"), ("phân giải cục bộ", "máy bạn", "8")]
    for a, b, lab in steps:
        arrow(out, X[a], y + 24, X[b], y + 40, lab, "q", size=20)
        y += 56
    out.append("</svg>")
    return "".join(out)


if __name__ == "__main__":
    fig = ROOT / "audit" / "net" / "fig"; fig.mkdir(parents=True, exist_ok=True)
    F = {
        # 1500 B ở 100 Mbps: T = 0,12 ms; 1000 km: P = 5 ms. Vẽ đúng tỉ lệ thì dải mỏng 2,3% — dùng tỉ lệ thật để thấy “mỏng”.
        "delay_real": delays(0.12, 5.0),
        # cùng gói, đường 20 km (P = 0,1 ms): hai trễ cùng cỡ
        "delay_short": delays(0.12, 0.10),
        "handshake": handshake(100, 300),
        "stopwait": stop_wait(),
        "dns": dns_iter(),
    }
    assert abs(1500 * 8 / 100e6 * 1e3 - 0.12) < 1e-12 and abs(20e3 / 2e8 * 1e3 - 0.10) < 1e-12
    for k, v in F.items():
        (fig / f"{k}.svg").write_text(v, encoding="utf-8")
    print(len(F), "hình →", fig)
