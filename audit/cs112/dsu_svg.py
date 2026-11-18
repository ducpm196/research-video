"""Hình cây cha của hợp–tìm cho bài L25 CS112, sinh từ chính thuật toán (không vẽ tay):
  hàng 1: hai nhóm {1,2,3} (gốc 1) và {4,5} (gốc 4) -> sau union(3, 5), gắn gốc nhóm NHỎ (4) vào gốc nhóm LỚN (1)
  hàng 2: chuỗi 5->4->3->2->1 -> sau find(5) có nén đường, mọi nút trỏ thẳng về gốc 1.
Kiểm bằng máy: trạng thái "sau" tính bằng find/union cài ngay ở đây, đối chiếu với chữ trên màn hình bài.
Chạy: .venv/Scripts/python -B audit/cs112/dsu_svg.py → ghi audit/cs112/fig/L25_DSU.svg (một dòng)."""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")


class DSU:
    def __init__(self, parent):
        self.p = dict(parent)

    def size(self, r):
        return sum(1 for x in self.p if self.root(x) == r)

    def root(self, x):
        while self.p[x] != x:
            x = self.p[x]
        return x

    def find(self, x):                      # có nén đường
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]

    def union_by_size(self, a, b):          # gắn gốc nhóm nhỏ vào gốc nhóm lớn
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size(ra) < self.size(rb):
            ra, rb = rb, ra
        self.p[rb] = ra
        return True


def forest_svg(parent, x0, y0, width, dy=70, r=22, hi=None):
    """Vẽ rừng cây cha (nút -> cha) trong khung rộng `width` bắt đầu ở (x0, y0); trả về danh sách phần tử SVG."""
    hi = hi or set()
    kids = {}
    for v, p in parent.items():
        if v != p:
            kids.setdefault(p, []).append(v)
    roots = sorted(v for v, p in parent.items() if v == p)
    pos, nxt = {}, [0]

    def place(v, d):
        ks = sorted(kids.get(v, []))
        if not ks:
            pos[v] = (nxt[0], d)
            nxt[0] += 1
        else:
            for k in ks:
                place(k, d + 1)
            pos[v] = (sum(pos[k][0] for k in ks) / len(ks), d)
    for rt in roots:
        place(rt, 0)
    cols = max(1, nxt[0])
    step = width / cols
    xy = {v: (x0 + step * (c + 0.5), y0 + d * dy) for v, (c, d) in pos.items()}
    out = []
    for v, p in parent.items():
        if v != p:
            (x1, y1), (x2, y2) = xy[v], xy[p]
            out.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#6b7280" stroke-width="3"/>')
    for v in parent:
        x, y = xy[v]
        col = "#d97706" if v in hi else "#2563eb"
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#eff6ff" stroke="{col}" stroke-width="4"/>')
        out.append(f'<text x="{x:.0f}" y="{y + 8:.0f}" font-size="22" text-anchor="middle">{v}</text>')
    return out


def label(x, y, s, size=22, fill="#374151", bold=False):
    """s có thể là danh sách dòng (mỗi dòng cách 26 px) để nhãn không rộng quá cột"""
    w = ' font-weight="700"' if bold else ""
    lines = [s] if isinstance(s, str) else s
    return "".join(f'<text x="{x}" y="{y + 26 * k}" font-size="{size}" text-anchor="middle" fill="{fill}"{w}>{t}</text>' for k, t in enumerate(lines))


def build():
    before1 = {1: 1, 2: 1, 3: 1, 4: 4, 5: 4}
    d = DSU(before1)
    assert d.size(1) == 3 and d.size(4) == 2
    assert d.union_by_size(3, 5)
    after1 = dict(d.p)
    assert after1 == {1: 1, 2: 1, 3: 1, 4: 1, 5: 4}      # gốc 4 (nhóm nhỏ) gắn vào gốc 1 (nhóm lớn)
    chain = {1: 1, 2: 1, 3: 2, 4: 3, 5: 4}
    d2 = DSU(chain)
    assert d2.find(5) == 1
    star = dict(d2.p)
    assert star == {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}        # nén đường: mọi nút trỏ thẳng về gốc
    out = ['<svg style="overflow:visible" width="1000" height="590" viewBox="0 0 1000 590">']
    out += forest_svg(before1, 20, 40, 380, dy=62, hi={4})
    out.append(label(210, 222, ["trước: nhóm {1, 2, 3} (3 nút)", "và nhóm {4, 5} (2 nút)"], 21))
    out.append('<text x="470" y="75" font-size="44" text-anchor="middle" fill="#6b7280">→</text>')
    out += forest_svg(after1, 540, 40, 420, dy=62, hi={4})
    out.append(label(750, 222, ["sau union(3, 5): gốc nhóm nhỏ (4)", "gắn vào gốc nhóm lớn (1)"], 21))
    out += forest_svg(chain, 20, 285, 380, dy=48, hi={5})
    out.append(label(210, 545, ["chuỗi 5 → 4 → 3 → 2 → 1:", "tìm gốc từ 5 tốn 4 bước"], 21))
    out.append('<text x="470" y="310" font-size="44" text-anchor="middle" fill="#6b7280">→</text>')
    out += forest_svg(star, 540, 285, 420, dy=48, hi={5})
    out.append(label(750, 545, ["sau find(5) có nén đường:", "mọi nút trỏ thẳng về gốc 1"], 21))
    out.append("</svg>")
    return "".join(out)


if __name__ == "__main__":
    s = build()
    out = Path(__file__).resolve().parent / "fig" / "L25_DSU.svg"
    out.write_text(s, encoding="utf-8", newline="")
    print("→", out, len(s), "ký tự; trạng thái sau kiểm bằng find/union cài sẵn")
