from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import lv

TARGETS = [
    ("dan", "L02", ["sym", "practice"]),
    ("dan", "L03", ["check", "practice"]),
    ("dan", "L04", ["sym"]),
    ("dan", "L07", ["check"]),
    ("dan", "L11", ["check"]),
    ("dan", "L12", ["sym"]),
    ("dsc", "L02", ["sym"]),
    ("dsc", "L03", ["check"]),
    ("dsc", "L06", ["sym", "example"]),
    ("dsc", "L09", ["sym"]),
    ("dsc", "L11", ["sym", "cost"]),
    ("dsc", "L12", ["example"]),
    ("mlo", "L02", ["sym"]),
    ("mlo", "L03", ["sym"]),
    ("mlo", "L06", ["example", "sym"]),
    ("mlo", "L07", ["example"]),
    ("mlo", "L08", ["check"]),
    ("mlo", "L13", ["sym"]),
    ("mlo", "L14", ["stage4"]),
    ("evt", "L00", ["sym"]),
    ("evt", "L01", ["check"]),
    ("evt", "L02", ["check"]),
    ("evt", "L03", ["example"]),
    ("evt", "L06", ["check"]),
    ("evt", "L09", ["example", "check"]),
    ("evt", "L11", ["stage5"]),
    ("den", "L08", ["check"]),
    ("den", "L10", ["practice"]),
    ("den", "L12", ["sym", "example", "check", "practice"]),
    ("cld", "L03", ["example"]),
    ("cld", "L08", ["check"]),
    ("cld", "L09", ["example"]),
    ("clc", "L01", ["sym"]),
    ("clc", "L02", ["sym", "practice"]),
    ("clc", "L03", ["sym"]),
    ("clc", "L04", ["example"]),
    ("clc", "L05", ["sym"]),
    ("clc", "L06", ["sym"]),
    ("clc", "L07", ["sym"]),
    ("clc", "L08", ["sym"]),
    ("clc", "L09", ["sym"]),
    ("clc", "L10", ["sym"]),
    ("clc", "L11", ["sym"]),
    ("clc", "L12", ["stage5"]),
    ("sar", "L00", ["sym"]),
    ("sar", "L01", ["sym"]),
    ("sar", "L02", ["sym"]),
    ("sar", "L03", ["sym"]),
    ("sar", "L04", ["sym", "check"]),
    ("sar", "L05", ["sym", "example", "practice"]),
    ("sar", "L08", ["sym"]),
    ("sar", "L09", ["sym", "practice"]),
    ("sar", "L10", ["sym", "check"]),
    ("sar", "L11", ["sym", "practice"]),
    ("sar", "L12", ["sym"]),
    ("sar", "L13", ["stage5"]),
]

for c, lid, sids in TARGETS:
    p = sorted((ROOT / f"lessons/{c}").glob(f"{lid}_*.yaml"))[0]
    d = yaml.safe_load(p.read_text("utf-8"))
    for sid in sids:
        sc = next(s for s in d["scenes"] if s["id"] == sid)
        st = sc["steps"][-1]
        blks = lv.split_blocks(st["show"]) if hasattr(lv, "split_blocks") else []
        print(f"{c.upper()} {lid} {sid} (idx={len(sc['steps'])-1}, kind={sc['kind']}, blocks={len(blks)}, focus={st.get('focus')}): say_prefix={st['say'][:55]!r}")
