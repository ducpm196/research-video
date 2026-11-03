"""Sơ đồ khối mạch lôgic cho CSA L05 — sinh SVG từ mô tả cổng và dây, không vẽ tay.
Mỗi cổng là một khối chữ nhật ghi tên; dây đi ngang–dọc (gấp khúc) từ điểm ra của nguồn tới điểm vào của cổng; nhãn đầu vào bên trái,
nhãn đầu ra bên phải. Kiểm: mọi dây kết thúc đúng ở cạnh trái một khối hoặc ở một đầu ra.
Chạy: .venv/Scripts/python audit/csa/gates_svg.py → audit/csa/fig/half_adder.svg"""
import sys
from pathlib import Path

W, H = 640, 300
BOX_W, BOX_H = 150, 70


def svg(inputs, gates, outputs):
    """inputs: {tên: (x, y)}; gates: {id: (nhãn, x, y, [nguồn,…])}; outputs: {nhãn: gate_id}."""
    out = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    ends = []
    for gid, (label, gx, gy, srcs) in gates.items():
        for k, s in enumerate(srcs):
            sx, sy = inputs[s]
            ty = gy + BOX_H * (k + 1) / (len(srcs) + 1)
            mx = sx + 60 + 40 * k
            out.append(f'<polyline points="{sx},{sy} {mx},{sy} {mx},{ty:.0f} {gx},{ty:.0f}" fill="none" stroke="#6b7280" stroke-width="4"/>')
            out.append(f'<circle cx="{mx}" cy="{sy}" r="6" fill="#6b7280"/>')
            ends.append((gx, ty, gid))
        out.append(f'<rect x="{gx}" y="{gy}" width="{BOX_W}" height="{BOX_H}" rx="10" fill="#eff6ff" stroke="#2563eb" stroke-width="4"/>'
                   f'<text x="{gx + BOX_W / 2:.0f}" y="{gy + BOX_H / 2 + 11:.0f}" font-size="30" font-weight="700" text-anchor="middle">{label}</text>')
    for name, (x, y) in inputs.items():
        out.append(f'<text x="{x - 14}" y="{y + 10}" font-size="30" text-anchor="end">{name}</text>')
    for label, gid in outputs.items():
        _, gx, gy, _ = gates[gid]
        x1, y = gx + BOX_W, gy + BOX_H / 2
        out.append(f'<line x1="{x1}" y1="{y:.0f}" x2="{x1 + 70}" y2="{y:.0f}" stroke="#059669" stroke-width="5"/>'
                   f'<text x="{x1 + 80}" y="{y + 10:.0f}" font-size="28" fill="#059669" font-weight="700">{label}</text>')
    out.append("</svg>")
    for gx, ty, gid in ends:
        _, x, y, _ = gates[gid]
        assert gx == x and y < ty < y + BOX_H, (gid, ty)
    return "".join(out)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    D = Path(__file__).resolve().parent / "fig"
    D.mkdir(exist_ok=True)
    s = svg({"a": (60, 80), "b": (60, 220)},
            {"x": ("XOR", 300, 30, ["a", "b"]), "n": ("AND", 300, 190, ["a", "b"])},
            {"tổng s": "x", "nhớ c": "n"})
    (D / "half_adder.svg").write_text(s, encoding="utf-8")
    print("ok", len(s))
