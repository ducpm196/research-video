"""Hình SVG cho bài CS112 — sinh từ dữ liệu, không vẽ tay.
svg(pos, edges): đồ thị với toạ độ đỉnh cho sẵn.  gtree(t): cây nhiều nhánh t = (nhãn, [con…]), x theo thứ tự lá, y theo độ sâu."""


def svg(pos, edges, w=900, h=330, r=30, labels=None):
    out = [f'<svg style="overflow:visible" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    for a, b in edges:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#6b7280" stroke-width="4"/>')
        if labels and (a, b) in labels:
            out.append(f'<text x="{(x1 + x2) / 2 + 8:.0f}" y="{(y1 + y2) / 2 - 8:.0f}" font-size="24" fill="#d97706">{labels[(a, b)]}</text>')
    for k, (x, y) in pos.items():
        out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#eff6ff" stroke="#2563eb" stroke-width="4"/>')
        out.append(f'<text x="{x}" y="{y + 11}" font-size="30" text-anchor="middle">{k}</text>')
    out.append("</svg>")
    return "".join(out)


def gtree(t, w=1100, dy=80, top=30, r=24, fs=24, mark=None):
    """mark: {đường đi (tuple nhãn từ gốc): màu} để tô một số nút (ví dụ lá là nghiệm)."""
    leaves, pos, edges = [], {}, []

    def collect(n, path):
        if not n[1]:
            leaves.append(path)
        for c in n[1]:
            collect(c, path + (c[0],))
    collect(t, (t[0],))
    step = (w - 2 * r - 20) / max(1, len(leaves) - 1)

    def place(n, path, d):
        if not n[1]:
            x = r + 10 + leaves.index(path) * step
        else:
            xs = [place(c, path + (c[0],), d + 1) for c in n[1]]
            x = sum(xs) / len(xs)
            for c in n[1]:
                edges.append((path, path + (c[0],)))
        pos[path] = (x, top + d * dy)
        return x
    place(t, (t[0],), 0)
    depth = max(len(p) for p in pos) - 1
    h = top + depth * dy + r + 10
    out = [f'<svg style="overflow:visible" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    for a, b in edges:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        out.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#6b7280" stroke-width="3"/>')
    for p, (x, y) in pos.items():
        col = (mark or {}).get(p, "#2563eb")
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#eff6ff" stroke="{col}" stroke-width="4"/>')
        out.append(f'<text x="{x:.0f}" y="{y + fs * 0.35:.0f}" font-size="{fs}" text-anchor="middle">{p[-1]}</text>')
    out.append("</svg>")
    return "".join(out)
