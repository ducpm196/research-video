"""Print exact sentences containing standalone word 'cang' in Stage 8 (DAN, DSC, MLO, EVT, DEN, CLD, CLC, SAR)."""
import re
import sys
from pathlib import Path

ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

for c in ("DAN", "DSC", "MLO", "EVT", "DEN", "CLD", "CLC", "SAR"):
    for fp in sorted((ROOT / "lessons" / c.lower()).glob("L*.yaml")):
        sp = lv.load_spec(fp)
        lid = sp["id"]
        for si, sc in enumerate(sp["scenes"]):
            for ti, st in enumerate(sc["steps"]):
                for fld in ("say", "show"):
                    v = st.get(fld)
                    if not isinstance(v, str):
                        continue
                    if re.search(r"\bcàng\b", v, re.I):
                        for part in re.split(r"(?<=[.!?])\s+|\n", v):
                            if re.search(r"\bcàng\b", part, re.I):
                                print(f"{c} {lid} sc{si}({sc['id']})#{ti}.{fld}: {part.strip()}")
