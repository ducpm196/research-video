import sys
from pathlib import Path
ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv

# Check AIF L04 SVG completely + L13 pitfalls/check + all 14 tight AIF lessons' recap0
for lid in ["L00","L01","L02","L03","L04","L05","L06","L07","L08","L09","L10","L11","L12","L13"]:
    fp = sorted((ROOT / "lessons" / "aif").glob(f"{lid}_*.yaml"))[0]
    sp = lv.load_spec(fp)
    w = sum(len((st.get("say") or "").split()) for sc in sp["scenes"] for st in sc["steps"])
    hk = sp["scenes"][0]["steps"][0]
    recap = [sc for sc in sp["scenes"] if sc["kind"] == "recap"][0]
    print(f"{lid} w={w} need=+{1655-w} hook_focus={hk.get('focus')} hook_say={hk['say']!r}")
    if lid in ("L04", "L08", "L13"):
        intuit = [sc for sc in sp["scenes"] if sc["id"] == "intuition"][0]
        print(f"  SVG {lid}: {intuit['steps'][0]['show']!r}")
