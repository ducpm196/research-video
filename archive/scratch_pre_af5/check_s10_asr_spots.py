from pathlib import Path
import yaml

for c, lids in [("toc", ["L00", "L01", "L02", "L06", "L07", "L08", "L09", "L11"]),
                ("plc", ["L00", "L03", "L04", "L06", "L07", "L09", "L10", "L11", "L12"]),
                ("par", ["L12"]),
                ("hci", ["L11", "L12"])]:
    for lid in lids:
        p = next(Path("lessons", c).glob(f"{lid}_*.yaml"))
        doc = yaml.safe_load(p.read_text(encoding="utf-8"))
        ar = [x.get("sentence") for x in (doc.get("asr_reviewed") or [])]
        r0 = next(sc["steps"][0] for sc in doc["scenes"] if sc["id"] == "recap")
        r0_in_ar = [s for s in ar if s in (r0.get("say") or "")]
        print(f"{c.upper()}:{lid} asr_reviewed_in_recap0={len(r0_in_ar)}/{len(ar)}")
