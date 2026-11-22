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
    hook = [sc for sc in spec["scenes"] if sc["kind"] == "hook"][0]
    recap = [sc for sc in spec["scenes"] if sc["kind"] == "recap"][0]
    if words < 1645 or 27 <= i <= 39:
        print(f"=== {lid} ({fp.name}) words={words} ===")
        print("  hook.steps[0].focus:", hook["steps"][0].get("focus"))
        print("  hook.steps[0].say:", hook["steps"][0].get("say"))
        print("  recap.steps[0].focus:", recap["steps"][0].get("focus"))
        print("  recap.steps[0].say:", recap["steps"][0].get("say"))
        print("  recap.steps[0].show:", repr(recap["steps"][0].get("show")))
