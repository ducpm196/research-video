"""Dump scene kinds/titles + curriculum examples + exact math lines for Stage 8 Batch 8A (DAN, DSC, MLO)."""
import sys
from pathlib import Path

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

for c in ("DAN", "DSC", "MLO"):
    cur = lv.load_yaml(ROOT / "curriculum" / f"{c.lower()}.yaml")
    print(f"\n==================== {c} ====================", flush=True)
    for les in cur["lessons"]:
        lid = les["id"]
        fp = sorted((ROOT / "lessons" / c.lower()).glob(f"{lid}_*.yaml"))[0]
        sp = lv.load_spec(fp)
        sc_str = " | ".join(f"{i}:{sc['kind']}({sc.get('title','')[:28]})" for i, sc in enumerate(sp["scenes"]))
        print(f"{lid} objs={les['objectives']}", flush=True)
        print(f"    ex={les.get('example','')[:160]}", flush=True)
        print(f"    sc={sc_str}", flush=True)
