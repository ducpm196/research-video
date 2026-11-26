import json
from pathlib import Path
import yaml

STAGES = {
    "S08": ["DAN", "DSC", "MLO", "EVT", "DEN", "CLD", "CLC", "SAR"],
    "S09": ["IRS", "LLM", "RLN", "AGT", "CVI", "AIF", "CS115"],
    "S10": ["TOC", "PLC", "PAR", "HCI", "SEP", "CAS"],
    "S11": ["RBM", "ESY", "ROB", "GFX", "BCH"],
}
MED_SPW = 0.331  # observed median (dur - pause) / words across 777 builds
P5_SPW = 0.305   # fast-speech guard

for st, courses in STAGES.items():
    print(f"=== {st} ===")
    for c in courses:
        short = []
        for yp in sorted(Path("lessons", c.lower()).glob("L*.yaml")):
            lid = yp.stem.split("_")[0]
            if c == "CS115" and int(lid[1:]) < 22:
                continue
            doc = yaml.safe_load(yp.read_text(encoding="utf-8"))
            w = sum(len((s.get("say") or "").split()) for sc in doc.get("scenes", []) for s in sc.get("steps", []))
            pauses = sum(float(s.get("pause", 0) or 0) for sc in doc.get("scenes", []) for s in sc.get("steps", []))
            est_med = w * MED_SPW + pauses
            est_p5 = w * P5_SPW + pauses
            bp = Path("out", c.lower(), lid, "build_report.json")
            built = None
            if bp.exists():
                built = json.loads(bp.read_text(encoding="utf-8")).get("timeline_seconds")
            if est_p5 < 540 or (built is not None and built < 540):
                b_str = f", built={built:.1f}s" if built else ""
                short.append(f"{lid}({w}w, est_med={est_med:.0f}s, est_p5={est_p5:.0f}s{b_str})")
        print(f"  {c}: {len(short)} tight/short -> {', '.join(short)}")
