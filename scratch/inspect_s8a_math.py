"""Inspect exact math strings in DAN L07, DSC L08/L15, MLO L07 and P1 glosses across DAN/DSC/MLO."""
import re, sys
from pathlib import Path
ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv
sys.stdout.reconfigure(encoding="utf-8")

targets = [
    ("DAN", "L07", ["1,5", "1.5", "MAE", "WMAPE", "1,25", "1 phẩy 5"]),
    ("DSC", "L08", ["356", "1000", "1 000", "295", "14 751", "14751"]),
    ("DSC", "L15", ["2,6", "2.6", "0,85", "phần trăm"]),
    ("MLO", "L07", ["8 158", "8158", "14 751", "14751", "shadow"]),
]
for c, lid, pats in targets:
    fp = sorted((ROOT / "lessons" / c.lower()).glob(f"{lid}_*.yaml"))[0]
    lines = fp.read_text(encoding="utf-8").splitlines()
    print(f"=== {c} {lid} ({fp.name}) ===")
    for i, ln in enumerate(lines, 1):
        if any(p.lower() in ln.lower() for p in pats):
            print(f"  L{i}: {ln[:160]}")
