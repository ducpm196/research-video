"""Số từ lời đọc và thời lượng ước tính (≈ 135 từ/phút ở tốc độ -5%) của các bài FND: stats.py [L00 …]"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import lv
want = [a.upper() for a in sys.argv[1:]]
for f in sorted((ROOT / "lessons" / "fnd").glob("L*.yaml")):
    if want and f.stem[:3] not in want:
        continue
    sp = lv.load_spec(f)
    w = sum(len(st["say"].split()) for sc in sp["scenes"] for st in sc["steps"])
    n = sum(len(lv.sentences(st["say"])) for sc in sp["scenes"] for st in sc["steps"])
    pause = sum(st.get("pause", 0) for sc in sp["scenes"] for st in sc["steps"])
    print(f"{f.stem[:3]} {w} từ, {n} câu, {len(sp['scenes'])} cảnh, ≈ {w/135:.1f} phút (+ dừng {pause}s)")
