"""Cây quyết định của sắp xếp chèn 3 phần tử a, b, c (bài L23 CS112) — sinh SVG từ chính thuật toán, rồi kiểm bằng máy:
mỗi lá là đúng một thứ tự, đủ 6 lá, độ cao 3. Chạy: dtree_svg.py → in SVG."""
import itertools
import sys

sys.stdout.reconfigure(encoding="utf-8")


def run(order, answers):
    """Chạy sắp xếp chèn trên các tên a, b, c; câu hỏi “x ≤ y?” trả lời theo answers (dict) → (dãy câu hỏi, kết quả)."""
    seq, asked = [], []
    for x in order:
        k = len(seq)
        while k > 0:
            q = (seq[k - 1], x)
            asked.append(q)
            if not answers[q]:          # seq[k-1] > x
                k -= 1
            else:
                break
        seq.insert(k, x)
    return asked, "".join(seq)


# cây: nút = dãy câu trả lời đã có; liệt kê theo mọi thứ tự thật của a, b, c
tree = {}
for perm in itertools.permutations([1, 2, 3]):
    val = dict(zip("abc", perm))
    ans = {(u, v): val[u] <= val[v] for u in "abc" for v in "abc" if u != v}
    asked, res = run("abc", ans)
    path = ()
    for q in asked:
        tree.setdefault(path, q)
        path += (ans[q],)
    tree[path] = res
leaves = {p: r for p, r in tree.items() if isinstance(r, str)}
assert len(leaves) == 6 and sorted(leaves.values()) == sorted("".join(p) for p in itertools.permutations("abc"))
assert max(len(p) for p in leaves) == 3
order = sorted(leaves, key=lambda p: [0 if t else 1 for t in p])   # lá theo thứ tự trái (≤ đúng) → phải
W, R, DY, TOP = 1000, 34, 92, 40
xs = {p: 70 + i * (W - 140) / 5 for i, p in enumerate(order)}
def x(p):
    if p in xs:
        return xs[p]
    kids = [q for q in tree if len(q) == len(p) + 1 and q[:len(p)] == p]
    xs[p] = sum(x(q) for q in kids) / len(kids)
    return xs[p]
H = TOP + 3 * DY + R + 6
out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
for p in tree:
    if p:
        par = p[:-1]
        out.append(f'<line x1="{x(par):.0f}" y1="{TOP + len(par) * DY + 18:.0f}" x2="{x(p):.0f}" y2="{TOP + len(p) * DY - 18:.0f}" stroke="#9ca3af" stroke-width="3"/>')
        mx, my = (x(par) + x(p)) / 2, TOP + (len(par) + 0.5) * DY
        lab, col = ("đúng", "#059669") if p[-1] else ("sai", "#dc2626")
        out.append(f'<text x="{mx + (-10 if p[-1] else 10):.0f}" y="{my + 6:.0f}" font-size="20" fill="{col}" text-anchor="{"end" if p[-1] else "start"}">{lab}</text>')
for p, v in tree.items():
    cx, cy = x(p), TOP + len(p) * DY
    if isinstance(v, str):
        out.append(f'<rect x="{cx - 34:.0f}" y="{cy - 20:.0f}" width="68" height="40" rx="8" fill="#ecfdf5" stroke="#059669" stroke-width="3"/>')
        out.append(f'<text x="{cx:.0f}" y="{cy + 8:.0f}" font-size="24" text-anchor="middle">{" ".join(v)}</text>')
    else:
        out.append(f'<rect x="{cx - 52:.0f}" y="{cy - 20:.0f}" width="104" height="40" rx="8" fill="#eff6ff" stroke="#2563eb" stroke-width="3"/>')
        out.append(f'<text x="{cx:.0f}" y="{cy + 8:.0f}" font-size="24" text-anchor="middle">{v[0]} ≤ {v[1]}?</text>')
out.append("</svg>")
print("".join(out))
print("LEAVES", {"".join("T" if t else "F" for t in p): v for p, v in leaves.items()}, file=sys.stderr)
