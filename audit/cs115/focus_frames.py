"""Chọn khung để xem bằng mắt các focus mới chèn (audit/cs115/focus_plan/Lxx.yaml): ưu tiên câu trỏ phần con (“2.3”) hay
nhiều chỗ ([1, 2]), rải đều trong bài; in danh sách lid:khung cho sheet.py. Chạy: focus_frames.py L05 [số khung=8]"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

lid, k = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 8
plan = yaml.safe_load((ROOT / "audit" / "cs115" / "focus_plan" / f"{lid}.yaml").read_text(encoding="utf-8")) or {}
sp = lv.load_spec(next((ROOT / "lessons" / "cs115").glob(lid + "_*.yaml")))
risky, plain, i = [], [], 0
for sc in sp["scenes"]:
    for ki, st in enumerate(sc["steps"]):
        n = len(lv.sentences(st["say"]))
        foc = plan.get(f"{sc['id']}.{ki}")
        if foc:
            for j, it in enumerate(foc):
                (risky if isinstance(it, list) or "." in str(it) else plain).append(i + j)
        i += n
pick = risky if len(risky) >= k else risky + plain
step = max(1, len(pick) / k)
sel = sorted({pick[int(m * step)] for m in range(min(k, len(pick)))})
print(" ".join(f"{lid}:{x}" for x in sel))
