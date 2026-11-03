"""Nhất quán siêu dữ liệu mọi bài: tiêu đề “Bài N” khớp id; `course` khớp thư mục; `series`, `voice`, `rate` giống nhau trong một
khoá; tên bài khớp tên trong lộ trình; mọi bài trong lộ trình có đặc tả và ngược lại.
Chạy: .venv/Scripts/python audit/review/check_meta.py"""
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.stdout.reconfigure(encoding="utf-8")
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"^Bài \d+( \([^)]*\))? — ", "", str(s))).strip()
bad = 0
for cp in sorted((ROOT / "curriculum").glob("*.yaml")):
    cur = yaml.safe_load(cp.read_text(encoding="utf-8")) or {}
    C = str(cur.get("course") or "")
    if not C:
        continue
    d = ROOT / "lessons" / C.lower()
    specs = {f.name.split("_")[0]: f for f in d.glob("L*_*.yaml")}
    meta = {}
    for l in cur.get("lessons", []):
        lid = str(l["id"])
        sp = l.get("spec")
        if not sp and l.get("spec_planned"):
            continue                      # bài mới ở mức giáo án — chưa có đặc tả là đúng quy ước
        if not sp or not (ROOT / sp).exists():
            print(C, lid, "lộ trình trỏ tới đặc tả không có:", sp); bad += 1; continue
        y = yaml.safe_load((ROOT / sp).read_text(encoding="utf-8"))
        meta[lid] = y
        n = int(lid[1:])
        if not re.match(rf"Bài {n}( \([^)]*\))? — ", str(y.get("title", ""))):
            print(C, lid, "tiêu đề không bắt đầu bằng “Bài", n, "—”:", y.get("title")); bad += 1
        if str(y.get("course") or "CS115") != C or str(y.get("id")) != lid:
            print(C, lid, "course/id trong đặc tả:", y.get("course"), y.get("id")); bad += 1
        if norm(y.get("title")) != norm(l.get("title")):
            print(C, lid, "tên khác lộ trình:\n   đặc tả:", norm(y.get("title")), "\n   lộ trình:", norm(l.get("title"))); bad += 1
    for lid in set(specs) - set(meta):
        print(C, lid, "có đặc tả nhưng không có trong lộ trình:", specs[lid].name); bad += 1
    for key in ("series", "voice", "rate"):
        cnt = Counter(str(y.get(key)) for y in meta.values())
        if len(cnt) > 1:
            common = cnt.most_common(1)[0][0]
            for lid, y in meta.items():
                if str(y.get(key)) != common:
                    print(C, lid, f"`{key}` = {y.get(key)!r}, các bài khác = {common!r}"); bad += 1
print(f"\ncheck_meta: {bad} vấn đề")
