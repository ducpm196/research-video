"""Xoá mục `asr_reviewed` của câu KHÔNG còn trong bài (lint E30) — dùng sau khi viết lại / đào sâu một bài.
Chỉ xoá dòng `- {sentence: "…", reason: …}` mà câu không còn là phụ đề nào của bài; in từng dòng đã xoá để đọc lại.
Chạy: .venv/Scripts/python audit/review/prune_stale_asr.py lessons/<khoá>/<bài>.yaml [...]"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

for f in sys.argv[1:]:
    p = Path(f)
    spec = lv.load_spec(p)
    caps = {s.strip() for _, _, _, st in lv.iter_steps(spec) for s in lv.sentences(st.get("say") or "")}
    stale = {str(x.get("sentence", "")).strip() for x in spec.get("asr_reviewed") or []} - caps
    if not stale:
        print(f"{p.name}: 0 mục cũ")
        continue
    out, n = [], 0
    for line in p.read_text(encoding="utf-8").split("\n"):
        m = re.match(r'\s*- \{sentence: "(.*?)", reason:', line)
        if m and m.group(1).strip() in stale:
            print(f"{p.name}: xoá “{m.group(1)[:70]}”")
            n += 1
            continue
        out.append(line)
    assert n == len(stale), f"{p.name}: tìm thấy {n}/{len(stale)} dòng — sửa tay"
    p.write_text("\n".join(out), encoding="utf-8")
