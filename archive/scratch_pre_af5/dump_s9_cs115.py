from pathlib import Path
import yaml

tight = [22, 24, 25, 26, 27, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43]
for n in tight:
    p = next(Path("lessons/cs115").glob(f"L{n:02d}_*.yaml"))
    doc = yaml.safe_load(p.read_text(encoding="utf-8"))
    w = sum(len((s.get("say") or "").split()) for sc in doc["scenes"] for s in sc["steps"])
    rec = next(sc for sc in doc["scenes"] if sc["id"] == "recap")
    hk = next((sc for sc in doc["scenes"] if sc["id"] == "hook"), None)
    print(f"L{n:02d} ({p.name}, {w}w): need=+{max(0, 1650 - w)}w | r0_focus={rec['steps'][0].get('focus')} | r1_focus={rec['steps'][1].get('focus') if len(rec['steps'])>1 else 'NA'} | hook_focus={hk['steps'][0].get('focus') if hk else 'NA'}")
    print("  R0 SAY:", repr(rec["steps"][0]["say"]))
    if len(rec["steps"]) > 1:
        print("  R1 SAY:", repr(rec["steps"][1]["say"]))
