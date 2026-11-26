import glob
import re
import sys
from pathlib import Path
import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]

for c in ["dan", "dsc", "mlo"]:
    print(f"=== {c.upper()} ===")
    for fp in sorted(glob.glob(str(ROOT / f"lessons/{c}/L*.yaml"))):
        d = yaml.safe_load(Path(fp).read_text(encoding="utf-8"))
        lid = d["id"]
        for sc in d["scenes"]:
            for idx, st in enumerate(sc.get("steps", [])):
                for fld in ("show", "say"):
                    val = str(st.get(fld) or "")
                    if re.search(r"\bcàng\b", val, re.I):
                        print(f"  {lid} [{sc['id']}#{idx}.{fld}]: {val!r}")
