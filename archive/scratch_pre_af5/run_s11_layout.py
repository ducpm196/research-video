import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
for c in ("GFX", "BCH"):
    r = subprocess.run([PY, "-B", "audit/layout_scan.py", c], cwd=ROOT)
    assert r.returncode == 0, f"layout_scan {c} failed"
    rows = [l for l in (ROOT / "audit" / f"layout_{c}.tsv").read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(rows) == 0, f"{c} has layout issues: {rows[:5]}"
print("ALL ESY ROB GFX BCH LAYOUT SCANS 0 ISSUES!", flush=True)
