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
        txt = Path(fp).read_text(encoding="utf-8")
        d = yaml.safe_load(txt)
        lid = d["id"]
        say_all = " ".join(
            str(st.get("say") or "")
            for sc in d.get("scenes", [])
            for st in sc.get("steps", [])
        )
        words = len(re.findall(r"\w+", say_all))
        cangs = [
            (sc["id"], i, st.get("say", ""))
            for sc in d.get("scenes", [])
            for i, st in enumerate(sc.get("steps", []))
            if re.search(r"\bcàng\b", str(st.get("say") or ""), re.I)
        ]
        rec = [
            st.get("say", "")
            for sc in d.get("scenes", [])
            if sc["id"] == "recap"
            for st in sc.get("steps", [])
        ]
        print(f"{lid} w={words} cang={len(cangs)}")
        for scid, idx, s in cangs:
            print(f"  CANG [{scid}#{idx}] {s}")
        for idx, s in enumerate(rec):
            print(f"  RECAP#{idx}: {s}")
