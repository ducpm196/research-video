import glob
import sys
from pathlib import Path
import yaml

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]

CASES = [
    ("aif", "L02", "recap"),
    ("aif", "L04", "recap"),
    ("aif", "L05", "recap"),
    ("aif", "L08", "recap"),
    ("aif", "L09", "check"),
    ("aif", "L09", "recap"),
    ("aif", "L10", "sym"),
    ("aif", "L10", "recap"),
    ("aif", "L12", "recap"),
    ("aif", "L13", "recap"),
    ("aif", "L14", "recap"),
    ("irs", "L02", "sym"),
    ("irs", "L03", "sym"),
    ("irs", "L05", "recap"),
    ("irs", "L07", "sym"),
    ("irs", "L09", "recap"),
    ("irs", "L10", "sym"),
    ("irs", "L11", "sym"),
    ("agt", "L01", "sym"),
    ("llm", "L00", "sym"),
    ("llm", "L01", "sym"),
    ("llm", "L06", "sym"),
    ("rln", "L01", "recap"),
    ("rln", "L06", "sym"),
    ("rln", "L10", "sym"),
    ("rln", "L13", "recap"),
    ("cvi", "L12", "recap"),
]

for c, lid, scid in CASES:
    fp = sorted(glob.glob(str(ROOT / f"lessons/{c}/{lid}_*.yaml")))[0]
    d = yaml.safe_load(Path(fp).read_text(encoding="utf-8"))
    for sc in d["scenes"]:
        if sc["id"] == scid:
            print(f"=== {c.upper()} {lid} [{scid}] ===")
            for i, st in enumerate(sc["steps"]):
                sh = str(st.get("show") or "")
                sy = str(st.get("say") or "")
                if scid in ("recap",) and i != 1:
                    continue
                print(f"  [{i}] focus={st.get('focus')} show={sh!r}")
                print(f"      say={sy!r}")
