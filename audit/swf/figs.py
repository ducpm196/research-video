"""Hình cho khoá SWF — cây tìm kiếm nhị phân (đúng/sai bất biến), máy trạng thái đèn giao thông. Cây và kết luận lấy từ checklib (alg.*).
Màu theo bảng mặc định của skill dataviz (xanh #2a78d6, cam #eb6834); chữ màu mực; nền #fffbeb. Video là khung tĩnh nên không hover.
Chạy: .venv/Scripts/python audit/swf/figs.py → audit/swf/fig/*.svg (mỗi hình một dòng)."""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import checklib as alg  # noqa: E402

S1, S2 = "#2a78d6", "#eb6834"
INK, MUTED, BG = "#1f2937", "#6b7280", "#fffbeb"
OUT = ROOT / "audit" / "swf" / "fig"
OUT.mkdir(parents=True, exist_ok=True)


def text(x, y, t, size=22, col=INK, anchor="middle", weight="normal"):
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" fill="{col}" text-anchor="{anchor}" font-weight="{weight}">{t}</text>'


def save(name, svg):
    (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")
    print("→", name)


def bst_svg(t, bad=(), W=820, H=380, note=None):
    """Vẽ cây (khoá, trái, phải); nút trong `bad` tô cam nét đứt. Toạ độ x theo thứ tự duyệt giữa."""
    order = alg.inorder(t)
    pos = {}

    def place(n, d):
        if n is None:
            return
        place(n[1], d + 1)
        pos[n[0]] = (70 + order.index(n[0]) * (W - 140) / max(1, len(order) - 1), 55 + d * 105)
        place(n[2], d + 1)

    place(t, 0)
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']

    def edges(n):
        if n is None:
            return
        for c in (n[1], n[2]):
            if c is not None:
                (x1, y1), (x2, y2) = pos[n[0]], pos[c[0]]
                out.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{MUTED}" stroke-width="2.5"/>')
                edges(c)

    edges(t)
    for k, (x, y) in pos.items():
        if k in bad:
            out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="34" fill="#ffffff" stroke="{S2}" stroke-width="3.5" stroke-dasharray="7 5"/>')
            out.append(text(x, y + 10, str(k), 28, S2, "middle", "bold"))
        else:
            out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="34" fill="{S1}"/>')
            out.append(text(x, y + 10, str(k), 28, "#ffffff", "middle", "bold"))
    if note:
        out.append(text(W / 2, H - 14, note, 24, MUTED))
    return "".join(out) + "</svg>"


if __name__ == "__main__":
    bad_tree = (10, (5, None, (12, None, None)), (15, None, None))
    assert alg.bst_local_ok(bad_tree) and not alg.bst_ok(bad_tree)
    save("bst_bad", bst_svg(bad_tree, bad=(12,), note="duyệt giữa: 5, 12, 10, 15 — không tăng"))
