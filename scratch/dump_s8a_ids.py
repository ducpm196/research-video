import sys
from pathlib import Path
ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv
sys.stdout.reconfigure(encoding="utf-8")
for c in ("DAN", "DSC", "MLO"):
    for fp in sorted((ROOT / "lessons" / c.lower()).glob("L*.yaml")):
        sp = lv.load_spec(fp)
        sc_ids = [f"{sc['id']}({sc['kind']})" for sc in sp["scenes"]]
        print(f"{c} {sp['id']}: {sc_ids}")
