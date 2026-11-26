import sys
from pathlib import Path

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402

for c in ("dan", "dsc", "mlo", "evt", "den", "cld", "clc", "sar"):
    for fp in sorted((ROOT / "lessons" / c).glob("L*.yaml")):
        sp = lv.load_spec(fp)
        objs = sp.get("objectives") or []
        kinds = {sc["id"]: sc["kind"] for sc in sp["scenes"]}
        for n, obj in enumerate(objs, 1):
            t = str(obj).strip().lower()
            do_v = t.startswith(lv.AF2_DO_VERBS)
            if do_v:
                print(f"{c.upper()} {sp['id']} obj{n} (DO): {obj!r}")
