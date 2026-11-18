"""Hình quan hệ các lớp P, NP, NP-đầy đủ cho bài L26 CS112 (vẽ theo giả định P ≠ NP, chưa ai chứng minh).
Sinh SVG một dòng từ toạ độ khai báo ở đây, rồi kiểm bằng máy: ellipse P và ellipse NP-đầy đủ nằm TRONG ellipse NP,
hai ellipse con không giao nhau. Chạy: .venv/Scripts/python -B audit/cs112/pnp_svg.py → ghi audit/cs112/fig/L26_PNP.svg."""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

NP = (500, 175, 470, 150)      # cx, cy, rx, ry
P = (260, 185, 180, 85)
NPC = (730, 185, 170, 85)


def inside(inner, outer):
    """Ellipse con nằm trong ellipse ngoài (kiểm 360 điểm trên viền của ellipse con)."""
    import math
    for k in range(360):
        t = math.radians(k)
        x, y = inner[0] + inner[2] * math.cos(t), inner[1] + inner[3] * math.sin(t)
        if ((x - outer[0]) / outer[2]) ** 2 + ((y - outer[1]) / outer[3]) ** 2 >= 1:
            return False
    return True


def disjoint(a, b):
    import math
    for k in range(360):
        t = math.radians(k)
        x, y = a[0] + a[2] * math.cos(t), a[1] + a[3] * math.sin(t)
        if ((x - b[0]) / b[2]) ** 2 + ((y - b[1]) / b[3]) ** 2 <= 1:
            return False
    return True


def el(e, fill, stroke):
    return f'<ellipse cx="{e[0]}" cy="{e[1]}" rx="{e[2]}" ry="{e[3]}" fill="{fill}" stroke="{stroke}" stroke-width="4"/>'


def txt(x, y, s, size=26, bold=False, fill="#1f2937"):
    w = ' font-weight="700"' if bold else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="middle" fill="{fill}"{w}>{s}</text>'


def svg():
    assert inside(P, NP) and inside(NPC, NP) and disjoint(P, NPC)
    out = ['<svg style="overflow:visible" width="1000" height="360" viewBox="0 0 1000 360">',
           el(NP, "#eff6ff", "#2563eb"), el(P, "#d1fae5", "#059669"), el(NPC, "#fef3c7", "#d97706"),
           txt(500, 82, "NP: kiểm được chứng chỉ nhanh", 26, True, "#2563eb"),
           txt(260, 160, "P", 40, True, "#059669"), txt(260, 195, "giải được nhanh", 24), txt(260, 224, "sắp xếp,", 22), txt(260, 250, "đường ngắn nhất", 22),
           txt(730, 150, "NP-đầy đủ", 32, True, "#d97706"), txt(730, 187, "phủ đỉnh, tổng tập con,", 22), txt(730, 215, "người du lịch", 22), txt(730, 243, "(quyết định)", 22),
           txt(500, 345, "vẽ theo giả định P ≠ NP (chưa ai chứng minh)", 22, False, "#6b7280"),
           "</svg>"]
    return "".join(out)


if __name__ == "__main__":
    s = svg()
    out = Path(__file__).resolve().parent / "fig" / "L26_PNP.svg"
    out.write_text(s, encoding="utf-8", newline="")
    print("→", out, len(s), "ký tự; P và NP-đầy đủ nằm trong NP, rời nhau")
