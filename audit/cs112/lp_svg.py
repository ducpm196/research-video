"""Hình miền chấp nhận được của bài LP (L21, L22) — toạ độ tính từ dữ liệu.
Mẫu audit/cs112/src/L21_qhtt.tpl.yaml: {{FIG}} = fig(), {{FIGL}} = fig(level=True, highlight="B"); ghi mỗi hình ra một tệp một dòng
rồi điền bằng audit/cs112/fill_tpl.py (đối chiếu 2026-11-10: hai lời gọi này cho đúng từng byte hình đang có trong bài)."""
S, X0, Y0 = 12, 70, 410
# Viền nền (màu nền khung #fff7e6) cho nhãn bị đường biên cắt qua: “z = 280” (đường bột) và “C(0, 24)” (đường đường) — LS1 2026-11-10.
HALO = ' stroke="#fff7e6" stroke-width="6" paint-order="stroke"'


def P(x, y):
    return X0 + S * x, Y0 - S * y


def fig(level=None, highlight=None):
    o = ['<svg style="overflow:visible" width="460" height="450" viewBox="0 0 460 450">']
    ax0, ay0 = P(0, 0)
    o.append(f'<line x1="{ax0}" y1="{ay0}" x2="{P(28, 0)[0]}" y2="{ay0}" stroke="#6b7280" stroke-width="3"/>')
    o.append(f'<line x1="{ax0}" y1="{ay0}" x2="{ax0}" y2="{P(0, 33)[1]}" stroke="#6b7280" stroke-width="3"/>')
    o.append(f'<text x="{P(28, 0)[0] + 6}" y="{ay0 + 8}" font-size="24" fill="#6b7280">x₁</text>')
    o.append(f'<text x="{ax0 - 14}" y="{P(0, 33)[1] - 8}" font-size="24" fill="#6b7280">x₂</text>')
    poly = " ".join(f"{a:.0f},{b:.0f}" for a, b in (P(0, 0), P(16, 0), P(8, 16), P(0, 24)))
    o.append(f'<polygon points="{poly}" fill="#dbeafe" stroke="none"/>')
    for (xa, ya), (xb, yb), col, lab, lp in [((0, 24), (24, 0), "#2563eb", "x₁ + x₂ = 24", (13, 13)),
                                             ((0, 32), (16, 0), "#059669", "2x₁ + x₂ = 32", (9.5, 23))]:
        (a, b), (c, d) = P(xa, ya), P(xb, yb)
        o.append(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke="{col}" stroke-width="4"/>')
        tx, ty = P(*lp)
        o.append(f'<text x="{tx}" y="{ty}" font-size="22" fill="{col}">{lab}</text>')
    if level:
        (a, b), (c, d) = P(0, 28), P(56 / 3, 0)
        o.append(f'<line x1="{a}" y1="{b}" x2="{c:.0f}" y2="{d}" stroke="#d97706" stroke-width="3" stroke-dasharray="10 7"/>')
        tx, ty = P(14.5, 8.5)
        o.append(f'<text x="{tx}" y="{ty}" font-size="20" fill="#d97706"{HALO}>z = 280</text>')
    for name, (x, y), dx, dy in [("O", (0, 0), -26, 26), ("A(16, 0)", (16, 0), -10, 28), ("B(8, 16)", (8, 16), 10, -6), ("C(0, 24)", (0, 24), 8, -8)]:
        a, b = P(x, y)
        col = "#e11d48" if highlight == name[0] else "#1f2937"
        o.append(f'<circle cx="{a}" cy="{b}" r="7" fill="{col}"/>')
        halo = HALO if name[0] == "C" else ""
        o.append(f'<text x="{a + dx}" y="{b + dy}" font-size="22" fill="{col}" font-weight="700"{halo}>{name}</text>')
    o.append("</svg>")
    return "".join(o)
