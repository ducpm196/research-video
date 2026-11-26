import sys
from pathlib import Path
import re

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "audit" / "review"))
import lv

COURSES = ["aif", "irs", "agt", "llm", "rln", "cvi"]
for c in COURSES:
    print(f"\n================ {c.upper()} ================")
    for p in sorted((ROOT / "lessons" / c).glob("L*.yaml")):
        sp = lv.load_spec(p)
        lid = sp["id"]
        words = sum(len((st.get("say") or "").split()) for sc in sp["scenes"] for st in sc["steps"])
        scenes_id = [(i, sc["id"], sc["kind"], sc["title"]) for i, sc in enumerate(sp["scenes"])]
        covs = sp.get("covers") or []
        objs = sp.get("objectives") or []
        # Check SVG text fills/strokes or small fonts in show
        svg_issues = []
        katex_scale = []
        for sc in sp["scenes"]:
            for idx, st in enumerate(sc["steps"]):
                sh = st.get("show") or ""
                if "<svg" in sh:
                    for m in re.finditer(r'(fill|stroke)=["\'](#[0-9a-fA-F]{6})["\']', sh):
                        col = m.group(2).lower()
                        if col in ("#38bdf8", "#22c55e", "#4ade80", "#93c5fd", "#a5f3fc", "#facc15", "#eab308", "#fde047"):
                            svg_issues.append(f"{sc['id']}#{idx}:{m.group(0)}")
                if "Hai mức quy mô" in sh and "$" in sh:
                    katex_scale.append(f"{sc['id']}#{idx}")
        if words < 1645 or svg_issues or katex_scale or c == "aif":
            print(f"{lid} ({p.name}) w={words} objs={len(objs)} covs={[(x['objective'], x['scene']) for x in covs]}")
            if svg_issues:
                print(f"  SVG bright colors: {svg_issues}")
            if katex_scale:
                print(f"  KaTeX in scale: {katex_scale}")
            if words < 1645:
                recap = [sc for sc in sp["scenes"] if sc["kind"] == "recap"][0]
                print(f"  TIGHT need=+{1655-words} recap0.focus={recap['steps'][0].get('focus')} recap0.say={recap['steps'][0]['say']!r}")
