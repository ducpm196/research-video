import sys
from pathlib import Path

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv

for c in ("aif", "irs", "agt", "llm", "rln", "cvi"):
    print(f"=== P1 CHECK: {c.upper()} ===")
    for p in sorted((ROOT / "lessons" / c).glob("L*.yaml")):
        sp = lv.load_spec(p)
        lid = sp["id"]
        pr = [sc for sc in sp["scenes"] if sc["kind"] == "practice"]
        if not pr:
            print(f"  {lid}: NO PRACTICE")
            continue
        p0 = pr[0]["steps"][0]["show"]
        # Check if legacy read table markers appear in practice steps
        has_legacy_table = False
        for idx, st in enumerate(pr[0]["steps"]):
            sh = st["show"]
            if "<code>{k: v} / dict(...)</code>" in sh or "<code>elif / else</code>" in sh or "<code>{a, b} / set(...)</code>" in sh:
                has_legacy_table = True
        if has_legacy_table:
            print(f"  {lid}: LEGACY ast_p1 table")
