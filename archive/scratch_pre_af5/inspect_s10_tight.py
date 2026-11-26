import json
from pathlib import Path
import yaml

MED_SPW, P5_SPW = 0.331, 0.305
for c in ("toc", "plc", "par", "hci", "sep", "cas"):
    tight = []
    for p in sorted(Path("lessons", c).glob("L*.yaml")):
        lid = p.stem.split("_")[0]
        doc = yaml.safe_load(p.read_text(encoding="utf-8"))
        w = sum(len((s.get("say") or "").split()) for sc in doc["scenes"] for s in sc["steps"])
        pauses = sum(float(s.get("pause", 0) or 0) for sc in doc["scenes"] for s in sc["steps"])
        est_med = w * MED_SPW + pauses
        est_p5 = w * P5_SPW + pauses
        bp = Path("out", c, lid, "build_report.json")
        built = json.loads(bp.read_text(encoding="utf-8")).get("timeline_seconds") if bp.exists() else None
        if w < 1620 or est_p5 < 540 or (built is not None and built < 540):
            b = f", built={built:.1f}s" if built else ""
            tight.append(f"{lid}({w}w, p={pauses:.0f}s, med={est_med:.0f}s, p5={est_p5:.0f}s{b})")
    print(f"=== {c.upper()} tight (<1620w or p5<540): {len(tight)} ===")
    for t in tight:
        print(" ", t)
