"""Quét mọi <svg> trong `show` của một khoá: chữ <text> có đường chân chữ sát/vượt đáy (y > cao − 6, dấu dưới bị cắt —
lỗi thật L08 CS112 khung 1) hoặc ra ngoài bề ngang; và độ dài dòng đầu trang (series + tiêu đề) so với khoá kia.
Chạy: svg_scan.py cs115"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

course = sys.argv[1]
n_svg = 0
for p in sorted((ROOT / "lessons" / course).glob("L??_*.yaml")):
    sp = lv.load_spec(p)
    for sc in sp["scenes"]:
        for ki, st in enumerate(sc["steps"]):
            for svg in re.findall(r"<svg\b.*?</svg>", str(st.get("show", "")), re.S):
                n_svg += 1
                m = re.search(r'viewBox="([\d.\-]+) ([\d.\-]+) ([\d.]+) ([\d.]+)"', svg)
                if not m:
                    print(f"{p.name[:3]} {sc['id']}.{ki}: svg không có viewBox"); continue
                x0, y0, w, h = map(float, m.groups())
                for t in re.finditer(r'<text\b([^>]*)>(.*?)</text>', svg, re.S):
                    a = t.group(1)
                    ty = re.search(r'\by="([\d.\-]+)"', a); tx = re.search(r'\bx="([\d.\-]+)"', a)
                    fs = re.search(r'font-size="([\d.]+)"', a)
                    if not ty or not tx:
                        continue
                    y, x, f = float(ty.group(1)), float(tx.group(1)), float(fs.group(1)) if fs else 16
                    txt = re.sub(r"<[^>]+>", "", t.group(2))
                    anchor = re.search(r'text-anchor="(\w+)"', a)
                    est = 0.55 * f * len(txt)   # bề ngang ước lượng
                    left = x - (est / 2 if anchor and anchor.group(1) == "middle" else est if anchor and anchor.group(1) == "end" else 0)
                    probs = []
                    if y > y0 + h - 0.25 * f:
                        probs.append(f"chân chữ y={y:g} sát đáy {y0 + h:g}")
                    if y - 0.8 * f < y0:
                        probs.append(f"đỉnh chữ vượt mép trên")
                    if left < x0 - 2 or left + est > x0 + w + 2:
                        probs.append(f"có thể tràn ngang (x={x:g}, ~{est:.0f}px, rộng {w:g})")
                    if probs:
                        print(f"{p.name[:3]} {sc['id']}.{ki}: “{txt[:40]}” " + "; ".join(probs))
print(f"đã quét {n_svg} svg")
for c in ("cs115", "cs112"):
    L = []
    for p in sorted((ROOT / "lessons" / c).glob("L??_*.yaml")):
        sp = lv.load_spec(p)
        L.append((len(str(sp.get("series", ""))) + len(str(sp["title"])), p.name[:3], sp["title"]))
    L.sort(reverse=True)
    print(c, "dòng đầu dài nhất:", L[:4])
