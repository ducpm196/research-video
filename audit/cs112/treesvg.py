"""Sinh hình cây nhị phân SVG cho bài CS112 từ cây dạng (khoá, trái, phải) — toạ độ x theo thứ tự duyệt giữa, y theo độ sâu,
nên hình luôn khớp dữ liệu (không vẽ tay). Dùng: from treesvg import svg; print(svg(tree, ...)).
Chạy trực tiếp để in các hình của bài L05 (kèm kiểm tính chất bằng máy)."""
import sys


def inorder(t):
    return [] if t is None else inorder(t[1]) + [t[0]] + inorder(t[2])


def height(t):
    return -1 if t is None else 1 + max(height(t[1]), height(t[2]))


def bf(t):
    return height(t[1]) - height(t[2])


def svg(t, w=520, h=None, r=30, dy=95, top=45, labels=None, color="#2563eb", fill="#eff6ff", note=None):
    """labels: {khoá: chữ nhỏ cạnh nút} (ví dụ hệ số cân bằng)."""
    pos, order = {}, inorder(t)
    def walk(n, d):
        if n is None:
            return
        pos[n[0]] = (d, order.index(n[0]))
        walk(n[1], d + 1); walk(n[2], d + 1)
    walk(t, 0)
    depth = max(d for d, _ in pos.values())
    h = h or top + depth * dy + r + 20
    step = (w - 2 * r - 20) / max(1, len(order) - 1) if len(order) > 1 else 0
    xy = {k: (r + 10 + i * step if len(order) > 1 else w / 2, top + d * dy) for k, (d, i) in pos.items()}
    out = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    def edges(n):
        if n is None:
            return
        for c in (n[1], n[2]):
            if c is not None:
                (x1, y1), (x2, y2) = xy[n[0]], xy[c[0]]
                out.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#6b7280" stroke-width="3"/>')
            edges(c)
    edges(t)
    for k, (x, y) in xy.items():
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{fill}" stroke="{color}" stroke-width="4"/>')
        out.append(f'<text x="{x:.0f}" y="{y + 11:.0f}" font-size="30" text-anchor="middle">{k}</text>')
        if labels and k in labels:
            # nhãn đặt NGANG bên phải nút: cạnh tới cha/con luôn đi chéo nên vùng ngang trống (lỗi thật L05 khung 34:
            # nhãn đặt chéo trên-phải đè lên cạnh nối nút với cha)
            out.append(f'<text x="{x + r + 8:.0f}" y="{y + 8:.0f}" font-size="22" fill="#d97706">{labels[k]}</text>')
    if note:
        out.append(f'<text x="10" y="{h - 8}" font-size="24" fill="#6b7280">{note}</text>')
    out.append("</svg>")
    return "".join(out)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    T1 = (8, (3, (1, None, None), (6, None, None)), (10, None, (14, None, None)))
    BAD = (8, (3, (1, None, None), (9, None, None)), None)
    CHAIN = (1, None, (2, None, (3, None, (4, None, (5, None, None)))))
    RR = (1, None, (2, None, (3, None, None)))
    OK = (2, (1, None, None), (3, None, None))
    LR = (3, (1, None, (2, None, None)), None)
    assert inorder(T1) == sorted(inorder(T1)) == [1, 3, 6, 8, 10, 14]
    assert inorder(BAD) == [1, 3, 9, 8] and inorder(BAD) != sorted(inorder(BAD))
    assert height(CHAIN) == 4 and height(T1) == 2 and height(OK) == 1
    assert bf(RR) == -2 and bf(RR[2]) == -1 and bf(LR) == 2 and bf(LR[1]) == -1 and bf(OK) == 0
    for name, t, lab in [("T1", T1, None), ("BAD", BAD, None), ("CHAIN", CHAIN, None),
                         ("RR", RR, {1: "−2", 2: "−1", 3: "0"}), ("OK", OK, {2: "0", 1: "0", 3: "0"}),
                         ("LR", LR, {3: "+2", 1: "−1", 2: "0"})]:
        print(f"--- {name}\n{svg(t, labels=lab)}")
