from pathlib import Path
import re

spots = [
    ("par", "L05", ["MB"]),
    ("par", "L06", ["GB"]),
    ("par", "L07", ["ms", "Roofline"]),
    ("par", "L09", ["GB"]),
    ("par", "L10", ["GB", "MB", "ms"]),
    ("par", "L11", ["ms", "GB"]),
    ("par", "L13", ["ms", "GB"]),
    ("plc", "L05", ["1.0f"]),
    ("plc", "L06", ["bool"]),
    ("plc", "L08", ["with", "try", "finally"]),
    ("plc", "L09", ["void", "deepcopy"]),
    ("plc", "L12", ["@lru_cache"]),
]
for c, lid, terms in spots:
    p = next(Path("lessons", c).glob(f"{lid}_*.yaml"))
    lines = p.read_text(encoding="utf-8").splitlines()
    print(f"=== {c.upper()} {p.name} ===")
    for t in terms:
        hits = [f"{i}:{l}" for i, l in enumerate(lines, 1) if re.search(rf"(?<![A-Za-z0-9_]){re.escape(t)}(?![A-Za-z0-9_])", l) and "source:" not in l and "say:" not in l]
        print(f"  {t}: {hits[:2]}")
