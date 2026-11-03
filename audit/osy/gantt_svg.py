"""Biểu đồ thời gian (Gantt) cho OSY L02, L03 — sinh SVG từ lịch chạy do mô phỏng tính, không vẽ tay.
Mỗi đoạn chạy là một khối ghi tên tiến trình; trục dưới ghi mốc thời gian tại mọi ranh giới đoạn.
Kiểm: các đoạn nối liền nhau, tổng độ dài = tổng thời gian chạy, mỗi tiến trình chạy đúng thời lượng của nó.
Chạy: .venv/Scripts/python audit/osy/gantt_svg.py → audit/osy/fig/*.svg"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COL = ["#dbeafe", "#dcfce7", "#fef3c7", "#fce7f3", "#ede9fe"]
EDGE = ["#2563eb", "#16a34a", "#d97706", "#db2777", "#7c3aed"]


def fcfs_runs(bursts, order):
    t, runs = 0, []
    for i in order:
        runs.append((i, t, t + bursts[i])); t += bursts[i]
    return runs


def rr_runs(bursts, q):
    rem, t, runs, queue = list(bursts), 0, [], list(range(len(bursts)))
    while queue:
        i = queue.pop(0); run = min(q, rem[i])
        runs.append((i, t, t + run)); t += run; rem[i] -= run
        if rem[i]:
            queue.append(i)
    return runs


def svg(runs, bursts, width=1200, unit=None):
    total = runs[-1][2]
    assert all(a[2] == b[1] for a, b in zip(runs, runs[1:])) and runs[0][1] == 0, "đoạn không liền"
    assert total == sum(bursts)
    for i, b in enumerate(bursts):
        assert sum(e - s for j, s, e in runs if j == i) == b, f"P{i + 1} chạy sai thời lượng"
    unit = unit or (width - 40) / total
    W, H, y0, h = int(total * unit) + 40, 130, 10, 64
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    ticks = {0}
    for i, s, e in runs:
        x, w = 20 + s * unit, (e - s) * unit
        out.append(f'<rect x="{x:.1f}" y="{y0}" width="{w:.1f}" height="{h}" fill="{COL[i]}" stroke="{EDGE[i]}" stroke-width="3"/>')
        if w >= 44:
            out.append(f'<text x="{x + w / 2:.1f}" y="{y0 + h / 2 + 10:.1f}" font-size="28" font-weight="700" text-anchor="middle">P{i + 1}</text>')
        ticks.add(e)
    for tk in sorted(ticks):
        out.append(f'<text x="{20 + tk * unit:.1f}" y="{y0 + h + 40}" font-size="26" text-anchor="middle">{tk}</text>')
    out.append("</svg>")
    return "".join(out)


if __name__ == "__main__":
    fig = ROOT / "audit" / "osy" / "fig"; fig.mkdir(parents=True, exist_ok=True)
    B = [24, 3, 3]
    figs = {
        "fcfs": svg(fcfs_runs(B, [0, 1, 2]), B, 1100),
        "sjf": svg(fcfs_runs(B, [1, 2, 0]), B, 1100),
        "rr4": svg(rr_runs(B, 4), B, 1100),
        "rr2_quiz": svg(rr_runs([5, 3, 8], 2), [5, 3, 8], 1100),
    }
    for k, v in figs.items():
        (fig / f"{k}.svg").write_text(v, encoding="utf-8"); print("→", fig / f"{k}.svg")
    print(rr_runs(B, 4))
