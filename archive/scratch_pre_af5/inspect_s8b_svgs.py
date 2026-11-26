"""Print full SVG lines for CLC L11, CLD L10, DEN L08 + missing Hai muc quy mo / spoken say in EVT/DEN/CLC/SAR."""
import ast, re, sys
from pathlib import Path
ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv
sys.stdout.reconfigure(encoding="utf-8")

for c, lid, ln in [("clc", "L11", 81), ("cld", "L10", 185), ("den", "L08", 77)]:
    fp = sorted((ROOT / "lessons" / c).glob(f"{lid}_*.yaml"))[0]
    line = fp.read_text(encoding="utf-8").splitlines()[ln - 1]
    print(f"\n=== {c.upper()} {lid}:{ln} SVG (len={len(line)}) ===")
    print(line)

for c in ("evt", "den", "cld", "clc", "sar"):
    print(f"\n=== {c.upper()} RECAP CHECK ===")
    for fp in sorted((ROOT / "lessons" / c).glob("L*.yaml")):
        sp = lv.load_spec(fp)
        rec = [sc for sc in sp["scenes"] if sc["kind"] == "recap"][0]
        if len(rec["steps"]) >= 2:
            sh = str(rec["steps"][1].get("show") or "")
            sa = str(rec["steps"][1].get("say") or "")
            has_2m = "Hai mức quy mô" in sh
            spoken_2m = any(k in sa.lower() for k in ("mức quy mô", "quy mô", "nhỏ", "thực tế", "từ 1", "từ 2", "từ 3", "từ 4", "từ 5", "ở hệ", "hàng"))
            if not has_2m or len(sa.split()) < 45:
                print(f"  {sp['id']}: has_2m={has_2m} say_w={len(sa.split())} sa={sa[:100]}")
