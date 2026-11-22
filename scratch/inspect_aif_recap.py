import sys
from pathlib import Path
ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv

for i in range(14):
    lid = f"L{i:02d}"
    fp = sorted((ROOT / "lessons" / "aif").glob(f"{lid}_*.yaml"))[0]
    sp = lv.load_spec(fp)
    rc0 = [sc for sc in sp["scenes"] if sc["kind"] == "recap"][0]["steps"][0]
    print(f"{lid} rc0 focus={rc0.get('focus')} say={rc0['say']!r}")
    if lid in ("L02", "L04", "L07", "L12"):
        chk0 = [sc for sc in sp["scenes"] if sc["id"] == "check"][0]["steps"][0]
        print(f"  chk0 show={chk0['show']!r}")
    if lid == "L09":
        for sc in sp["scenes"]:
            if sc["id"] in ("example", "check"):
                print(f"  L09 {sc['id']}: {[s['show'][:120] for s in sc['steps']]}")
