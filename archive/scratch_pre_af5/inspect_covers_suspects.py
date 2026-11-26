import sys
from pathlib import Path
import re
ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv

for c, lid in [("aif","L03"),("aif","L13"),("irs","L01"),("irs","L13"),("agt","L12"),("llm","L05"),("llm","L14"),("rln","L01"),("rln","L09"),("cvi","L12")]:
    fp = sorted((ROOT / "lessons" / c).glob(f"{lid}_*.yaml"))[0]
    sp = lv.load_spec(fp)
    print(f"=== {c.upper()}:{lid} ===")
    for i, o in enumerate(sp["objectives"], 1):
        print(f"  obj{i}: {o}")
    for sc in sp["scenes"]:
        if sc["kind"] in ("hook","prereq","practice","recap"):
            continue
        txt = " ".join(re.sub(r"<[^>]+>", " ", s.get("show") or "") for s in sc["steps"])
        txt = re.sub(r"\s+", " ", txt).strip()
        print(f"  [{sc['id']} ({sc['kind']})]: {sc['title']} || {txt[:140]}")
