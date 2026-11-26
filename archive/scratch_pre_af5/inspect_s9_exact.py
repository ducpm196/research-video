import sys
from pathlib import Path
import re

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv

for c in ("aif", "irs", "agt", "llm", "rln", "cvi"):
    print(f"\n*** {c.upper()} ***")
    for p in sorted((ROOT / "lessons" / c).glob("L*.yaml")):
        sp = lv.load_spec(p)
        lid = sp["id"]
        # 1) Print KaTeX in 'Hai mức quy mô'
        for sc in sp["scenes"]:
            for idx, st in enumerate(sc["steps"]):
                sh = st.get("show") or ""
                if "Hai mức quy mô" in sh and "$" in sh:
                    m = re.search(r"Hai mức quy mô.*", sh, re.S)
                    print(f"  {lid} {sc['id']}#{idx} KaTeX_scale: {m.group(0)[:240]!r}")
                if "<svg" in sh and any(col in sh for col in ("#93c5fd", "#22c55e", "#38bdf8")):
                    print(f"  {lid} {sc['id']}#{idx} bright_SVG")
        # 2) Print body numbers / formulas for lab comparison where needed
        if c == "agt" and lid in ("L10", "L12"):
            print(f"  {lid} scenes: {[(sc['id'], sc['title']) for sc in sp['scenes']]}")
        if c == "rln" and lid in ("L07", "L10"):
            chk = [sc for sc in sp["scenes"] if sc["id"] == "check"][0]
            print(f"  {lid} check#0: {chk['steps'][0]['show']!r}")
        if c == "cvi" and lid in ("L00", "L04"):
            for sc in sp["scenes"]:
                if sc["kind"] in ("sym", "formula", "example"):
                    print(f"  {lid} {sc['id']}: {sc['steps'][0]['show'][:220]!r}")
