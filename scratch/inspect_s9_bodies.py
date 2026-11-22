import sys
from pathlib import Path
import re

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv

for c in ("aif", "irs", "agt", "llm", "rln", "cvi"):
    print(f"\n================ {c.upper()} BODY NUMBERS ================")
    for p in sorted((ROOT / "lessons" / c).glob("L*.yaml")):
        sp = lv.load_spec(p)
        lid = sp["id"]
        # Collect compact summary of example / formula / check / stage* steps
        snippets = []
        for sc in sp["scenes"]:
            if sc["kind"] in ("hook", "prereq", "quiz", "practice", "pitfall"):
                continue
            for idx, st in enumerate(sc["steps"]):
                sh = re.sub(r"<[^>]+>", " ", st.get("show") or "")
                sh = re.sub(r"\s+", " ", sh).strip()
                if sh:
                    snippets.append(f"[{sc['id']}#{idx}] {sh[:150]}")
        print(f"  {lid}: " + " | ".join(snippets[:4]))
