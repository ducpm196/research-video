"""Run all Stage 9 + Stage 8 non-browser gates cleanly, then sequential layout_scan.py for S9 + S8."""
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
PY = str(ROOT / ".venv/Scripts/python.exe")

# 1. Verify MLO L03 passes lint cleanly after final edit
print(">>> LINT MLO L03", flush=True)
r = subprocess.run([PY, "-B", "tools/lv.py", "lint", "lessons/mlo/L03_kiem_thu_he_ml.yaml"], cwd=ROOT)
assert r.returncode == 0, "MLO L03 lint failed"

# 2. All non-browser gates for Stage 9 (7) + Stage 8 (8)
ALL_COURSES = [
    "CS115", "AIF", "IRS", "AGT", "LLM", "RLN", "CVI",
    "DAN", "DSC", "MLO", "EVT", "DEN", "CLD", "CLC", "SAR",
]
for c in ALL_COURSES:
    cmds = [
        [PY, "-B", "audit/review/sync_tpl_from_lesson.py", c, "--write"],
        [PY, "-B", "audit/review/screen_code.py", "check", "--course", c],
        [PY, "-B", "audit/review/lab_gate.py", c],
        [PY, "-B", "tools/lv.py", "curriculum", f"curriculum/{c.lower()}.yaml"],
        [PY, "-B", "audit/review/arith_scan.py", c],
    ]
    if c == "CS115":
        cmds.append([PY, "-B", "audit/verify_cs115_tex.py"])
    else:
        cmds.append([PY, "-B", f"audit/{c.lower()}/verify_{c.lower()}.py"])
    for cmd in cmds:
        print(">>> RUN:", c, Path(cmd[2]).name, flush=True)
        res = subprocess.run(cmd, cwd=ROOT)
        assert res.returncode == 0, f"FAILED {c}: {cmd}"

# 3. Sequential headless Chromium layout_scan across Stage 9 + Stage 8 (1 browser at a time)
for c in ALL_COURSES:
    print(">>> LAYOUT SCAN:", c, flush=True)
    res = subprocess.run([PY, "-B", "-u", "audit/layout_scan.py", c], cwd=ROOT)
    assert res.returncode == 0, f"LAYOUT SCAN FAILED: {c}"

print("STAGE 9 + STAGE 8 ALL 15 COURSES GATES + LAYOUT SCAN 100% PASS!", flush=True)
