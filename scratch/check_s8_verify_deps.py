from pathlib import Path
ROOT = Path(r"D:\research-video")
for c in ("dan", "dsc", "mlo", "evt", "den", "cld", "clc", "sar"):
    p = ROOT / "audit" / c / f"verify_{c}.py"
    txt = p.read_text(encoding="utf-8")
    hits = [f"L{i}: {ln.strip()}" for i, ln in enumerate(txt.splitlines(), 1) if "lab" in ln.lower() or "loi_giai" in ln.lower() or "de.md" in ln.lower()]
    print(f"verify_{c}.py lab refs:", hits)
