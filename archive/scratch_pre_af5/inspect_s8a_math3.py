import glob
import sys
from pathlib import Path
import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]

for pat in ["lessons/dan/L07*.yaml", "lessons/dsc/L08*.yaml", "lessons/dsc/L15*.yaml", "lessons/mlo/L07*.yaml"]:
    fp = sorted(glob.glob(str(ROOT / pat)))[0]
    print("FILE:", Path(fp).name)
    d = yaml.safe_load(Path(fp).read_text(encoding="utf-8"))
    for sc in d["scenes"]:
        if sc["id"] in ("example", "stage5", "recap"):
            print("  SC:", sc["id"])
            for i, st in enumerate(sc["steps"]):
                print(f"    [{i}] say={st.get('say', '')}")
                if sc["id"] == "recap":
                    print(f"        show={st.get('show', '')!r}")
