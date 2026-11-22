import glob
import sys
from pathlib import Path
import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]

for c in ["dan", "dsc", "mlo"]:
    print(f"=== {c.upper()} ===")
    for fp in sorted(glob.glob(str(ROOT / f"lessons/{c}/L*.yaml"))):
        d = yaml.safe_load(Path(fp).read_text(encoding="utf-8"))
        words = sum(len(str(st.get("say") or "").split()) for sc in d["scenes"] for st in sc.get("steps", []))
        if words < 1660:
            pit = next((sc for sc in d["scenes"] if sc["id"] == "pitfalls"), None)
            n_pit = len(pit["steps"]) if pit else 0
            last_pit_focus = pit["steps"][-1].get("focus") if pit and pit["steps"] else None
            print(f"  {d['id']} ({Path(fp).name}) w={words} need={1670-words} n_pit={n_pit} pit_focus={last_pit_focus} | title={d.get('title','')[:60]}")
