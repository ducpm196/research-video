import sys
from pathlib import Path
ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv

for i in range(22, 44):
    lid = f"L{i:02d}"
    fp = sorted((ROOT / "lessons" / "cs115").glob(f"{lid}_*.yaml"))[0]
    spec = lv.load_spec(fp)
    words = sum(len((st.get("say") or "").split()) for sc in spec["scenes"] for st in sc["steps"])
    if words >= 1645:
        continue
    recap = [sc for sc in spec["scenes"] if sc["kind"] == "recap"][0]
    in_ai = [sc for sc in spec["scenes"] if sc["id"] == "in_ai"]
    print(f"=== {lid} ({fp.name}) words={words} need={1655-words} ===")
    print("  recap0.say:", recap["steps"][0]["say"])
    print("  recap1.say:", recap["steps"][1]["say"], "| focus:", recap["steps"][1].get("focus"))
    if in_ai:
        print("  in_ai.say:", in_ai[0]["steps"][-1]["say"], "| focus:", in_ai[0]["steps"][-1].get("focus"))
