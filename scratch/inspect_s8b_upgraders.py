"""Summarize Batch 8B upgrader structures, existing labs vs curriculum examples, and COVERS."""
import sys
from pathlib import Path
ROOT = Path(r"D:\research-video")
sys.path.insert(0, str(ROOT / "tools"))
import lv
sys.stdout.reconfigure(encoding="utf-8")

for c in ("evt", "den", "cld", "clc", "sar"):
    p = ROOT / "audit" / c / "af2" / f"upgrade_{c}.py"
    lines = p.read_text(encoding="utf-8").splitlines()
    print(f"\n=== {p.name} (total={len(lines)} lines) ===")
    for i, ln in enumerate(lines, 1):
        if any(k in ln for k in ("def ", "apply_upgrade", "upgrade_lesson", "COVERS", "DATA", "sync_course_ledger", "sync_practice_run")):
            print(f"  L{i}: {ln[:120]}")
    # Check curriculum examples vs current lab de.md / loi_giai
    cur = lv.load_yaml(ROOT / "curriculum" / f"{c}.yaml")
    for les in cur["lessons"]:
        lid = les["id"]
        de = (ROOT / "labs" / c / lid / "de.md").read_text(encoding="utf-8") if (ROOT / "labs" / c / lid / "de.md").exists() else ""
        sol_p = ROOT / "labs" / c / lid / "loi_giai.py"
        sol = sol_p.read_text(encoding="utf-8").strip() if sol_p.exists() else ""
        print(f"  {c.upper()}:{lid} ex='{les.get('example','')[:90]}'")
        print(f"       de1='{de.splitlines()[2][:90] if len(de.splitlines())>2 else ''}' | sol_lines={len(sol.splitlines())}")
