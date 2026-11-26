"""Resume Stage 8 non-browser gates from DSC..SAR, then sequential layout_scan.py for S9 + S8 + CAS."""
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
PY = str(ROOT / ".venv/Scripts/python.exe")

REMAINING_NONBROWSER = ["DSC", "MLO", "EVT", "DEN", "CLD", "CLC", "SAR"]
for c in REMAINING_NONBROWSER:
    cmds = [
        [PY, "-B", "audit/review/sync_tpl_from_lesson.py", c, "--write"],
        [PY, "-B", "audit/review/screen_code.py", "check", "--course", c],
        [PY, "-B", "audit/review/lab_gate.py", c],
        [PY, "-B", "tools/lv.py", "curriculum", f"curriculum/{c.lower()}.yaml"],
        [PY, "-B", "audit/review/arith_scan.py", c],
        [PY, "-B", f"audit/{c.lower()}/verify_{c.lower()}.py"],
    ]
    for cmd in cmds:
        print(">>> RUN:", c, Path(cmd[2]).name, flush=True)
        res = subprocess.run(cmd, cwd=ROOT)
        assert res.returncode == 0, f"FAILED {c}: {cmd}"

# Sequential headless Chromium layout_scan across Stage 9 (7) + Stage 8 (8) + CAS (modified L01)
ALL_LAYOUT = [
    "CS115", "AIF", "IRS", "AGT", "LLM", "RLN", "CVI",
    "DAN", "DSC", "MLO", "EVT", "DEN", "CLD", "CLC", "SAR", "CAS",
]
for c in ALL_LAYOUT:
    print(">>> LAYOUT SCAN:", c, flush=True)
    res = subprocess.run([PY, "-B", "-u", "audit/layout_scan.py", c], cwd=ROOT)
    assert res.returncode == 0, f"LAYOUT SCAN FAILED: {c}"

print("ALL S8 REMAINING GATES + S9/S8/CAS LAYOUT SCAN 100% PASS!", flush=True)
