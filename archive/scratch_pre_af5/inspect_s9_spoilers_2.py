import sys
from pathlib import Path
import re

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv

checks = [
    ("cvi", ["L00", "L01", "L02", "L06", "L07"]),
    ("irs", ["L06", "L07"]),
    ("llm", ["L02", "L06", "L11", "L12"]),
    ("rln", ["L03", "L04", "L05", "L06", "L07", "L12", "L13"]),
]
for c, lids in checks:
    print(f"=== {c.upper()} ===")
    for lid in lids:
        fp = sorted((ROOT / "lessons" / c).glob(f"{lid}_*.yaml"))[0]
        sp = lv.load_spec(fp)
        print(f"  {lid}:")
        for sc in sp["scenes"]:
            if sc["id"] in ("sym", "formula", "example", "check", "pitfalls", "practice"):
                if sc["kind"] == "practice":
                    txt = sc["steps"][0]["show"]
                    print(f"    practice#0: {txt}")
                else:
                    for idx, st in enumerate(sc["steps"][:2]):
                        txt = re.sub(r"<[^>]+>", " ", st["show"])
                        txt = re.sub(r"\s+", " ", txt).strip()
                        print(f"    [{sc['id']}#{idx}]: {txt[:150]}")
