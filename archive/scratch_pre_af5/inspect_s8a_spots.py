import glob
import sys
from pathlib import Path
import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]

for pat, scid in [
    ("lessons/dan/L01*.yaml", "recap"),
    ("lessons/dan/L05*.yaml", "recap"),
    ("lessons/dsc/L03*.yaml", "check"),
    ("lessons/dsc/L13*.yaml", "check"),
    ("lessons/mlo/L09*.yaml", "recap"),
    ("lessons/mlo/L11*.yaml", "example"),
]:
    fp = sorted(glob.glob(str(ROOT / pat)))[0]
    d = yaml.safe_load(Path(fp).read_text(encoding="utf-8"))
    print("===", Path(fp).name, scid)
    for sc in d["scenes"]:
        if sc["id"] == scid:
            for i, st in enumerate(sc["steps"]):
                print(f"  [{i}] focus={st.get('focus')} show={st.get('show','')!r}")
                print(f"      say={st.get('say','')!r}")
