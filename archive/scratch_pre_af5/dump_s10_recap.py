from pathlib import Path
import yaml

tight = [
    ("toc", ["L00", "L01", "L02", "L06", "L07", "L08", "L09", "L11"]),
    ("plc", ["L00", "L03", "L04", "L06", "L07", "L09", "L10", "L11", "L12"]),
    ("par", ["L12"]),
    ("hci", ["L11", "L12"]),
]
for c, lids in tight:
    for lid in lids:
        p = next(Path("lessons", c).glob(f"{lid}_*.yaml"))
        doc = yaml.safe_load(p.read_text(encoding="utf-8"))
        w = sum(len((s.get("say") or "").split()) for sc in doc["scenes"] for s in sc["steps"])
        r0 = next(sc["steps"][0] for sc in doc["scenes"] if sc["id"] == "recap")
        print(f"=== {c.upper()} {p.name} ({w}w) ===")
        print("  FOCUS:", r0.get("focus"))
        print("  SAY0:", repr(r0.get("say")))
        if c == "toc" and lid in ("L02", "L03", "L04", "L06", "L07", "L08", "L10", "L11", "L12", "L13"):
            pf = next((sc for sc in doc["scenes"] if sc.get("kind") == "pitfall"), None)
            print("  PITFALL_LAST:", pf["id"] if pf else None, len(pf["steps"]) if pf else 0)
            if pf:
                print("    SHOW:", repr(pf["steps"][-1].get("show")[:120]))
                print("    SAY:", repr(pf["steps"][-1].get("say")))
                print("    FOCUS:", pf["steps"][-1].get("focus"))
for lid in ("L03", "L04", "L10", "L12", "L13"):
    p = next(Path("lessons/toc").glob(f"{lid}_*.yaml"))
    doc = yaml.safe_load(p.read_text(encoding="utf-8"))
    pf = next((sc for sc in doc["scenes"] if sc.get("kind") == "pitfall"), None)
    print(f"=== TOC {p.name} PITFALL_LAST ===")
    print("  FOCUS:", pf["steps"][-1].get("focus") if pf else None)
    print("  SHOW:", repr(pf["steps"][-1].get("show")[:140]) if pf else None)
    print("  SAY:", repr(pf["steps"][-1].get("say")) if pf else None)
