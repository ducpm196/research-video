import sys
from pathlib import Path
ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv

for lid in ["L00", "L03", "L04", "L05", "L07", "L08", "L11", "L12", "L13"]:
    fp = sorted((ROOT / "lessons" / "aif").glob(f"{lid}_*.yaml"))[0]
    sp = lv.load_spec(fp)
    print(f"=== AIF:{lid} ===")
    for sc in sp["scenes"]:
        if sc["kind"] in ("practice", "recap", "prereq", "hook", "quiz"):
            continue
        for idx, st in enumerate(sc["steps"]):
            sh = st.get("show") or ""
            if "<svg" in sh or lid in ("L00", "L03", "L04", "L05", "L07", "L11", "L12", "L13"):
                if len(sh) < 900 or "<svg" in sh:
                    print(f"  [{sc['id']}#{idx}] checks={sc.get('checks') if idx==0 else None}")
                    print(f"    show={sh[:600]!r}")
