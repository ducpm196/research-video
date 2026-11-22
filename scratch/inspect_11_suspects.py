from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import lv

SUS = [
    ("aif", "L13", "example", 3),
    ("aif", "L14", "stage5", 1),
    ("llm", "L01", "example", 3),
    ("llm", "L05", "sym", 0),
    ("rln", "L00", "example", 3),
    ("rln", "L11", "example", 3),
    ("cvi", "L00", "intuition", 1),
    ("cvi", "L05", "example", 1),
    ("cvi", "L06", "formula", 2),
    ("cvi", "L10", "example", 3),
    ("cld", "L09", "example", 3),
]
for c, lid, sid, ki in SUS:
    p = sorted((ROOT / f"lessons/{c}").glob(f"{lid}_*.yaml"))[0]
    d = yaml.safe_load(p.read_text("utf-8"))
    sc = next(s for s in d["scenes"] if s["id"] == sid)
    st = sc["steps"][ki]
    us = lv.html_units(st["show"])
    print(f"=== {c.upper()} {lid} {sid}[{ki}] focus={st.get('focus')} len_u={len(us)} ===")
    print("  show_tail:", st["show"][-160:].replace("\n", " "))
    print("  say_tail:", st["say"][-140:])
