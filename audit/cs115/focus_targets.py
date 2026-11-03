"""Liệt kê mọi mục focus trỏ tới PHẦN CON (“u.v”) kèm thẻ và chữ của phần con đó, và báo những mục trỏ vào chữ in
đậm/nghiêng giữa câu (<b>, <i>, <span> không phải công thức) — pedagogy luật 19: trỏ cả dòng, không trỏ một chữ in đậm.
Lỗi thật L02 khung 163: “1.1” viền chữ “khác nhau” thay vì công thức. Chạy: focus_targets.py cs115 [L02 …] [--all]"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools")); sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402
from focus_dump import txt, units  # noqa: E402

course = sys.argv[1]
show_all = "--all" in sys.argv
only = {a for a in sys.argv[2:] if a.startswith("L")}
bad = n = 0
for p in sorted((ROOT / "lessons" / course).glob("L??_*.yaml")):
    lid = p.name[:3]
    if only and lid not in only:
        continue
    sp = lv.load_spec(p)
    for sc in sp["scenes"]:
        blocks = []
        for ki, st in enumerate(sc["steps"]):
            if st.get("clear"):
                blocks = []
            if st.get("show"):
                blocks.append(units(str(st["show"])))
            for j, it in enumerate(st.get("focus") or []):
                for b, u, v in lv.parse_focus(it):
                    if not v:
                        continue
                    n += 1
                    blk = blocks[-1] if b is None else blocks[b]
                    node = blk[u - 1]; kid = node["kids"][v - 1]
                    weak = kid["tag"] not in ("m", "tr", "li", "div", "p", "table", "ul", "ol")
                    if weak:
                        bad += 1
                    if weak or show_all:
                        print(f"{'[CHỮ]' if weak else '     '} {lid} {sc['id']}.{ki} câu {j + 1} → {it}: "
                              f"<{node['tag']}>/<{kid['tag']}> “{txt(kid, 50)}”")
print(f"{course}: {n} mục trỏ phần con, {bad} mục trỏ vào chữ (không phải công thức/dòng/mục)")
