import sys
from pathlib import Path

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv


def dump_svgs(course: str, lids):
    for lid in lids:
        fp = sorted((ROOT / "lessons" / course).glob(f"{lid}_*.yaml"))[0]
        sp = lv.load_spec(fp)
        for sc in sp["scenes"]:
            for idx, st in enumerate(sc["steps"]):
                sh = st.get("show") or ""
                if "<svg" in sh:
                    print(f"SVG {course.upper()}:{lid} {sc['id']}#{idx}:")
                    print(sh)


dump_svgs("agt", ["L08"])
dump_svgs("llm", ["L01", "L07"])
dump_svgs("rln", ["L11"])
dump_svgs("cvi", ["L09"])

# Also print AGT L10 & L12 full check/pitfalls/stage5 + LLM P1 & RLN P1
for c, l, ids in [
    ("agt", "L06", {"sym", "example", "check"}),
    ("agt", "L10", {"sym", "example", "check"}),
    ("agt", "L12", {"stage3", "stage5", "check"}),
    ("cvi", "L00", {"sym", "example", "check"}),
    ("cvi", "L04", {"sym", "example", "check"}),
]:
    fp = sorted((ROOT / "lessons" / c).glob(f"{l}_*.yaml"))[0]
    sp = lv.load_spec(fp)
    print(f"=== {c.upper()}:{l} ===")
    for sc in sp["scenes"]:
        if sc["id"] in ids:
            for idx, st in enumerate(sc["steps"]):
                print(f"  [{sc['id']}#{idx}] {st['show']!r}")
