from pathlib import Path
import re

checks = {
    "par": ["s", "bit", "ms", "RAM", "GB", "MB", "LPT", "makespan", "TF/s", "TB/s", "Roofline", "GFLOP/s"],
    "plc": ["1.0f", "0x", "bool", "with", "try", "finally", "void", "deepcopy", "@lru_cache", "∘"],
}
for c, terms in checks.items():
    print(f"=== {c.upper()} ===")
    for p in sorted(Path("lessons", c).glob("L*.yaml")):
        txt = p.read_text(encoding="utf-8")
        # ignore practice scene when checking body presence
        body = txt.split("- id: practice")[0]
        hits = [t for t in terms if re.search(rf"(?<![A-Za-z0-9_]){re.escape(t)}(?![A-Za-z0-9_])", body)]
        if hits:
            print(f"  {p.name[:3]}: {hits}")

cas7 = next(Path("lessons/cas").glob("L07*.yaml")).read_text(encoding="utf-8")
print("CAS L07 backticks:", [f"{i}:{l.strip()[:100]}" for i, l in enumerate(cas7.splitlines(), 1) if "`" in l])
