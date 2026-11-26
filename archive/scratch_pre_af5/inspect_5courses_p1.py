import sys
from pathlib import Path
ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv

targets = [
    ("agt", "L10", "sym"), ("agt", "L02", "recap"), ("agt", "L03", "recap"), ("agt", "L06", "recap"), ("agt", "L08", "recap"), ("agt", "L10", "recap"),
    ("llm", "L00", "sym"), ("llm", "L01", "sym"), ("llm", "L02", "sym"), ("llm", "L05", "sym"), ("llm", "L06", "sym"), ("llm", "L11", "sym"), ("llm", "L12", "sym"),
    ("rln", "L06", "sym"), ("rln", "L08", "sym"), ("rln", "L12", "sym"), ("rln", "L13", "sym"),
    ("cvi", "L00", "sym"), ("cvi", "L04", "sym"),
]
for c, lid, sid in targets:
    fp = sorted((ROOT / "lessons" / c).glob(f"{lid}_*.yaml"))[0]
    sp = lv.load_spec(fp)
    sc = [s for s in sp["scenes"] if s["id"] == sid][0]
    st0 = sc["steps"][0]
    print(f"=== {c.upper()}:{lid} {sid}#0 ===")
    print("  show:", repr(st0["show"]))
    if sid == "recap":
        print("  say:", repr(st0["say"]))
