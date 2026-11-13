"""In chỉ số khung PNG (out/BNK/Lxx/frames/NNNNN.png) đầu tiên của từng cảnh: .venv/Scripts/python -B audit/bnk/frame_of.py L00"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv  # noqa: E402

f = next((ROOT / "lessons" / "bnk").glob(sys.argv[1].upper() + "_*.yaml"))
spec = yaml.safe_load(f.read_text(encoding="utf-8"))
n = 0
for sc in spec["scenes"]:
    first = n
    for st in sc["steps"]:
        n += len(lv.sentences(" ".join(st["say"].split())))
    print(f"{sc['id']:12s} khung {first:4d}–{n - 1}")
