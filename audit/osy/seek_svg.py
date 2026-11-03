"""Đường đi của đầu đọc cho OSY L13 — sinh SVG từ thứ tự phục vụ do tools/checklib tính, không vẽ tay.
Trục ngang = số trụ 0..199; mỗi bước xuống một hàng; nhãn số trụ cạnh mỗi điểm. Kiểm: tổng |bước ngang| = quãng đường checklib.
Chạy: .venv/Scripts/python audit/osy/seek_svg.py → audit/osy/fig/seek_*.svg"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import checklib  # noqa: E402

W, X0, X1, DY = 1100, 40, 1060, 26


def svg(path, total, color="#2563eb"):
    assert sum(abs(b - a) for a, b in zip(path, path[1:])) == total
    sx = lambda c: X0 + (X1 - X0) * c / 199
    H = 50 + DY * (len(path) - 1) + 20
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           f'<line x1="{X0}" y1="30" x2="{X1}" y2="30" stroke="#9ca3af" stroke-width="3"/>']
    for c in (0, 50, 100, 150, 199):
        out.append(f'<text x="{sx(c):.0f}" y="20" font-size="20" fill="#6b7280" text-anchor="middle">{c}</text>')
    pts = " ".join(f"{sx(c):.0f},{50 + DY * i}" for i, c in enumerate(path))
    out.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="4"/>')
    for i, c in enumerate(path):
        y = 50 + DY * i
        # nhãn đặt về phía KHÔNG có nét vẽ: mọi điểm kề nằm bên trái → nhãn bên phải; mọi điểm kề bên phải → nhãn bên trái;
        # nét đi xuyên qua (một bên trái, một bên phải) → nhãn bên phải, nâng lên trên nét (lỗi thật: nhãn 14, 37, 124 bị nét cắt)
        nb = [path[j] for j in (i - 1, i + 1) if 0 <= j < len(path)]
        if all(n <= c for n in nb):
            anchor, dx, dy = "start", 12, 7
        elif all(n >= c for n in nb):
            anchor, dx, dy = "end", -12, 7
        else:
            anchor, dx, dy = "start", 10, -8
        if anchor == "start" and sx(c) > W - 90:
            anchor, dx = "end", -12
        out.append(f'<circle cx="{sx(c):.0f}" cy="{y}" r="7" fill="{color}"/>'
                   f'<text x="{sx(c) + dx:.0f}" y="{y + dy}" font-size="21" text-anchor="{anchor}">{c}</text>')
    out.append("</svg>")
    return "".join(out)


if __name__ == "__main__":
    fig = ROOT / "audit" / "osy" / "fig"; fig.mkdir(parents=True, exist_ok=True)
    Q, h = [98, 183, 37, 122, 14, 124, 65, 67], 53
    figs = {"seek_fcfs": svg([h] + Q, checklib.disk_fcfs(Q, h), "#dc2626")}
    s, path = h, [h]
    q = list(Q)
    while q:
        n = min(q, key=lambda x: abs(x - s)); path.append(n); s = n; q.remove(n)
    figs["seek_sstf"] = svg(path, checklib.disk_sstf(Q, h), "#16a34a")
    tot, order = checklib.disk_scan(Q, h)
    figs["seek_scan"] = svg([h] + [c for c in order if c <= h] + [0] + [c for c in order if c > h], tot, "#2563eb")
    for k, v in figs.items():
        (fig / f"{k}.svg").write_text(v, encoding="utf-8"); print("→", fig / f"{k}.svg")
