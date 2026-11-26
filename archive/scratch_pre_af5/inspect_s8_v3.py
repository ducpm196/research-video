import glob
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

# 1. All " vs " across Stage 8 lessons & labs
print("=== VS HITS ===")
for c in ("dan", "dsc", "mlo", "evt", "den", "cld", "clc", "sar"):
    for p in sorted(list((ROOT / f"lessons/{c}").glob("L*.yaml")) + list((ROOT / f"labs/{c}").glob("L*/de.md"))):
        for i, l in enumerate(p.read_text("utf-8").splitlines(), 1):
            if " vs " in l and "<code>" not in l and "<div>" not in l:
                print(f"{p.relative_to(ROOT)}:{i}: {l.strip()[:110]}")

# 2. Check all flagged `covers:` lessons in Stage 8
COVERS_TARGETS = [
    ("dan", "L03"), ("dan", "L06"), ("dan", "L07"), ("dan", "L08"), ("dan", "L11"),
    ("dsc", "L03"), ("dsc", "L06"), ("dsc", "L09"), ("dsc", "L11"), ("dsc", "L12"), ("dsc", "L13"),
    ("mlo", "L01"), ("mlo", "L03"), ("mlo", "L06"), ("mlo", "L07"), ("mlo", "L08"), ("mlo", "L12"), ("mlo", "L13"), ("mlo", "L14"),
    ("evt", "L01"), ("evt", "L02"), ("evt", "L03"), ("evt", "L04"), ("evt", "L05"), ("evt", "L06"), ("evt", "L09"), ("evt", "L10"), ("evt", "L11"),
    ("den", "L08"), ("den", "L12"),
    ("cld", "L02"), ("cld", "L03"), ("cld", "L08"), ("cld", "L09"), ("cld", "L13"),
    ("clc", "L00"), ("clc", "L04"), ("clc", "L05"), ("clc", "L06"), ("clc", "L07"), ("clc", "L10"), ("clc", "L11"), ("clc", "L12"),
    ("sar", "L01"), ("sar", "L04"), ("sar", "L05"), ("sar", "L06"), ("sar", "L10"), ("sar", "L12"), ("sar", "L13"),
]
print("\n=== COVERS TARGETS ===")
for c, lid in COVERS_TARGETS:
    p = sorted((ROOT / f"lessons/{c}").glob(f"{lid}_*.yaml"))[0]
    d = yaml.safe_load(p.read_text("utf-8"))
    scs = [(s["id"], s["kind"], s["title"][:45]) for s in d["scenes"]]
    print(f"\n[{c.upper()} {lid}] {p.name}")
    for idx, o in enumerate(d["objectives"], 1):
        print(f"  obj{idx}: {o}")
    print(f"  covers: {[(x['objective'], x['scene']) for x in d.get('covers', [])]}")
    print(f"  scenes: {scs}")
