import sys
from pathlib import Path
ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv

for c in ("aif", "irs", "agt", "llm", "rln", "cvi"):
    print(f"=== {c.upper()} ===")
    for p in sorted((ROOT / "lessons" / c).glob("L*.yaml")):
        sp = lv.load_spec(p)
        objs = sp.get("objectives") or []
        covs = {x["objective"]: x["scene"] for x in (sp.get("covers") or [])}
        scs = [(sc["id"], sc["kind"], sc["title"]) for sc in sp["scenes"]]
        print(f"  {sp['id']}: cov={covs}")
        for idx, o in enumerate(objs, 1):
            print(f"    obj{idx}: {o}")
        print(f"    scenes: {[(a,b) for a,b,_ in scs if b not in ('hook','prereq','quiz','practice','recap')]}")
